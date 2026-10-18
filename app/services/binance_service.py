"""
Binance Pay & USDT verification service.
Supports Binance ID (Pay ID / UID: 538860756) internal transfers via Binance Pay API
and USDT TRC20 blockchain transfers via TronScan.
"""
import hashlib
import hmac
import logging
import time
import urllib.parse
from typing import Optional, Tuple
import httpx
from sqlalchemy import select

from app.core.config import settings
from app.core.database import AsyncSessionLocal
from app.models.order import SystemSetting

logger = logging.getLogger(__name__)

TRONSCAN_API = "https://apilist.tronscanapi.com/api"
BINANCE_PAY_API = "https://api.binance.com/sapi/v1/pay/transactions"


class BinanceVerificationError(Exception):
    pass


async def get_binance_id() -> str:
    """Retrieve dynamic Binance ID / Pay ID from DB or fallback to default 538860756."""
    try:
        async with AsyncSessionLocal() as session:
            res = await session.get(SystemSetting, "binance_id")
            if res and res.value and res.value.strip():
                return res.value.strip()
    except Exception as e:
        logger.warning("Could not read binance_id setting: %s", e)
    return getattr(settings, "BINANCE_ID", "538860756") or "538860756"


async def get_binance_keys() -> Tuple[str, str]:
    """Retrieve dynamic Binance API credentials from DB or fallback to config."""
    api_key = settings.BINANCE_API_KEY.strip()
    secret_key = settings.BINANCE_SECRET_KEY.strip()
    try:
        async with AsyncSessionLocal() as session:
            k = await session.get(SystemSetting, "binance_api_key")
            s = await session.get(SystemSetting, "binance_secret_key")
            if k and k.value and k.value.strip():
                api_key = k.value.strip()
            if s and s.value and s.value.strip():
                secret_key = s.value.strip()
    except Exception as e:
        logger.warning("Could not read binance keys from DB: %s", e)
    return api_key, secret_key


async def verify_binance_pay_txid(txid: str) -> dict:
    """
    Verify an internal Binance Pay / Binance ID transaction via Binance Pay API.
    Returns: {"valid": bool, "amount_usd": float, "confirmed": bool, "method": str, "order_id": str, "needs_manual": bool}
    """
    api_key, secret_key = await get_binance_keys()
    
    # If no Binance API key configured yet
    if not api_key or not secret_key or "your_binance" in api_key:
        return {
            "valid": False,
            "reason": "no_api_keys",
            "amount_usd": 0.0,
            "confirmed": False,
        }

    clean_txid = txid.strip().lstrip("#").strip()
    timestamp = int(time.time() * 1000)
    params = {
        "timestamp": timestamp,
        "recvWindow": 60000,
        "limit": 100,
    }
    query_string = urllib.parse.urlencode(params)
    signature = hmac.new(
        secret_key.encode("utf-8"),
        query_string.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()
    params["signature"] = signature

    headers = {
        "X-MBX-APIKEY": api_key,
        "Accept": "application/json",
    }

    async with httpx.AsyncClient(timeout=15.0) as client:
        try:
            resp = await client.get(BINANCE_PAY_API, params=params, headers=headers)
            if resp.status_code != 200:
                logger.error("Binance Pay API error %s: %s", resp.status_code, resp.text)
                return {
                    "valid": False,
                    "reason": f"http_{resp.status_code}",
                    "amount_usd": 0.0,
                    "confirmed": False,
                }
            payload = resp.json()
        except Exception as e:
            logger.error("Failed to query Binance Pay API: %s", e)
            return {
                "valid": False,
                "reason": str(e),
                "amount_usd": 0.0,
                "confirmed": False,
            }

    data_list = payload.get("data", [])
    if not isinstance(data_list, list):
        data_list = []

    for item in data_list:
        t_id = str(item.get("transactionId") or "").strip()
        o_id = str(item.get("orderId") or "").strip()

        matches = False
        if clean_txid.lower() in (t_id.lower(), o_id.lower()):
            matches = True
        elif t_id and clean_txid.lower() == t_id.lower():
            matches = True
        elif o_id and clean_txid.lower() == o_id.lower():
            matches = True

        if matches:
            amount = float(item.get("amount", 0) or 0)
            currency = str(item.get("currency", "")).upper()
            funds = item.get("fundsDetail")
            if not currency and isinstance(funds, list) and funds:
                currency = str(funds[0].get("currency", "")).upper()
            if amount <= 0 and isinstance(funds, list) and funds:
                amount = float(funds[0].get("amount", 0) or 0)

            if (currency == "USDT" or not currency) and amount > 0:
                return {
                    "valid": True,
                    "amount_usd": round(amount, 2),
                    "confirmed": True,
                    "method": "binance_pay",
                    "order_id": clean_txid,
                }

    # Not found in last 100 pay transactions
    return {
        "valid": False,
        "reason": "not_found",
        "amount_usd": 0.0,
        "confirmed": False,
    }


async def verify_trc20_txid(txid: str) -> dict:
    """
    Verify a USDT TRC20 transaction on TronScan.
    Returns: {"valid": bool, "amount_usdt": float, "to_address": str, "confirmed": bool}
    """
    clean_txid = txid.strip()
    async with httpx.AsyncClient(timeout=15.0) as client:
        try:
            resp = await client.get(
                f"{TRONSCAN_API}/transaction-info",
                params={"hash": clean_txid},
            )
            if resp.status_code != 200:
                return {"valid": False, "amount_usdt": 0.0, "to_address": "", "confirmed": False}
            data = resp.json()
        except Exception as e:
            logger.warning("TronScan API error: %s", e)
            return {"valid": False, "amount_usdt": 0.0, "to_address": "", "confirmed": False}

    if not data or data.get("contractRet") != "SUCCESS":
        return {"valid": False, "amount_usdt": 0.0, "to_address": "", "confirmed": False}

    trc20_transfers = data.get("trc20TransferInfo", [])
    if not trc20_transfers:
        return {"valid": False, "amount_usdt": 0.0, "to_address": "", "confirmed": False}

    USDT_CONTRACT = "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t"
    wallet = settings.BINANCE_WALLET_ADDRESS.strip()

    for transfer in trc20_transfers:
        contract = transfer.get("contract_address", "")
        to_addr = transfer.get("to_address", "")
        symbol = transfer.get("symbol", "")

        # If wallet address is set, verify recipient, or accept if valid USDT transfer
        if (symbol == "USDT" or contract == USDT_CONTRACT) and (not wallet or to_addr == wallet):
            amount_raw = int(transfer.get("amount_str", "0") or "0")
            amount_usdt = amount_raw / 1_000_000
            confirmed = data.get("confirmed", False)
            return {
                "valid": True,
                "amount_usdt": round(amount_usdt, 2),
                "to_address": to_addr,
                "confirmed": confirmed,
                "block_timestamp": data.get("timestamp", 0),
            }

    return {"valid": False, "amount_usdt": 0.0, "to_address": "", "confirmed": False}


async def verify_deposit_txid(txid: str) -> dict:
    """
    Smart verification for Binance deposits:
    1. If txid is a 64-char hex string, tries TronScan TRC-20 lookup.
    2. Tries Binance Pay API lookup (Order ID / Pay transaction ID).
    """
    clean_txid = txid.strip().lstrip("#").strip()

    # 1. TRC-20 on TronScan if 64 hex characters
    if len(clean_txid) == 64 and all(c in "0123456789abcdefABCDEF" for c in clean_txid):
        t_res = await verify_trc20_txid(clean_txid)
        if t_res.get("valid") and t_res.get("confirmed"):
            return {
                "valid": True,
                "amount_usd": t_res["amount_usdt"],
                "confirmed": True,
                "method": "trc20",
            }

    # 2. Check Binance Pay API
    b_res = await verify_binance_pay_txid(clean_txid)
    if b_res.get("valid") and b_res.get("confirmed"):
        return {
            "valid": True,
            "amount_usd": b_res["amount_usd"],
            "confirmed": True,
            "method": "binance_pay",
        }

    return {
        "valid": False,
        "amount_usd": 0.0,
        "confirmed": False,
        "reason": b_res.get("reason", "not_found"),
    }
