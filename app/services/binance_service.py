"""
Binance USDT TRC20 deposit verification via TronScan API.
Automatically verifies TxID and returns credited amount.
"""
import hashlib
import time
from typing import Optional
import httpx
from app.core.config import settings


TRONSCAN_API = "https://apilist.tronscanapi.com/api"


class BinanceVerificationError(Exception):
    pass


async def verify_trc20_txid(txid: str) -> dict:
    """
    Verify a USDT TRC20 transaction on TronScan.
    Returns: {"valid": bool, "amount_usdt": float, "to_address": str, "confirmed": bool}
    """
    async with httpx.AsyncClient(timeout=15.0) as client:
        try:
            resp = await client.get(
                f"{TRONSCAN_API}/transaction-info",
                params={"hash": txid},
            )
            resp.raise_for_status()
            data = resp.json()
        except Exception as e:
            raise BinanceVerificationError(f"TronScan API error: {e}")

    # TronScan response validation
    if not data or data.get("contractRet") != "SUCCESS":
        return {"valid": False, "amount_usdt": 0.0, "to_address": "", "confirmed": False}

    # Check it's a TRC20 token transfer (USDT)
    trc20_transfers = data.get("trc20TransferInfo", [])
    if not trc20_transfers:
        return {"valid": False, "amount_usdt": 0.0, "to_address": "", "confirmed": False}

    # Find USDT transfer (contract: TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t)
    USDT_CONTRACT = "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t"
    wallet = settings.BINANCE_WALLET_ADDRESS.strip()

    for transfer in trc20_transfers:
        contract = transfer.get("contract_address", "")
        to_addr = transfer.get("to_address", "")
        symbol = transfer.get("symbol", "")

        if (symbol == "USDT" or contract == USDT_CONTRACT) and to_addr == wallet:
            amount_raw = int(transfer.get("amount_str", "0") or "0")
            amount_usdt = amount_raw / 1_000_000  # USDT has 6 decimals
            confirmed = data.get("confirmed", False)
            return {
                "valid": True,
                "amount_usdt": round(amount_usdt, 2),
                "to_address": to_addr,
                "confirmed": confirmed,
                "block_timestamp": data.get("timestamp", 0),
            }

    return {"valid": False, "amount_usdt": 0.0, "to_address": "", "confirmed": False}
