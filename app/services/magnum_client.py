"""
Magnum Reseller API Client (v1.4.0)
Async HTTP client wrapping all endpoints.
"""
import uuid
import asyncio
from typing import Any, Optional
import httpx
from app.core.config import settings


class MagnumAPIError(Exception):
    def __init__(self, status_code: int, error: str, error_id: Optional[str] = None):
        self.status_code = status_code
        self.error = error
        self.error_id = error_id
        super().__init__(f"Magnum API Error [{status_code}]: {error}")


class MagnumClient:
    """
    Thread-safe async client for the Magnum Reseller API.
    Automatically handles Idempotency-Key generation and error normalization.
    """

    def __init__(self):
        self._client: Optional[httpx.AsyncClient] = None

    async def _get_client(self) -> httpx.AsyncClient:
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(
                base_url=settings.MAGNUM_BASE_URL,
                headers={
                    "X-API-Key": settings.MAGNUM_API_KEY,
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                },
                timeout=30.0,
            )
        return self._client

    @staticmethod
    def _make_idempotency_key(prefix: str = "req") -> str:
        return f"{prefix}-{uuid.uuid4()}"

    async def _request(
        self,
        method: str,
        path: str,
        *,
        idempotency_key: Optional[str] = None,
        **kwargs,
    ) -> dict:
        client = await self._get_client()
        headers = {}
        if idempotency_key:
            headers["Idempotency-Key"] = idempotency_key

        response = await client.request(method, path, headers=headers, **kwargs)

        if response.status_code in (200, 201, 202):
            return response.json()

        try:
            body = response.json()
            error = body.get("error", "unexpected_error")
            error_id = body.get("error_id")
        except Exception:
            error = "unexpected_error"
            error_id = None

        raise MagnumAPIError(response.status_code, error, error_id)

    # ─── Service ───────────────────────────────────────────
    async def health(self) -> dict:
        return await self._request("GET", "/v1/health")

    # ─── Wallet ────────────────────────────────────────────
    async def get_wallet(self) -> dict:
        return await self._request("GET", "/v1/wallet")

    # ─── Catalog ───────────────────────────────────────────
    async def get_products(self) -> dict:
        return await self._request("GET", "/v1/catalog/products")

    async def get_servers(self) -> dict:
        return await self._request("GET", "/v1/catalog/servers")

    async def get_nexus_options(self) -> dict:
        return await self._request("GET", "/v1/catalog/nexus/options")

    async def get_nexus_carriers(self, server_id: str, country: str, protocol: str, state: Optional[str] = None) -> dict:
        params = {"server_id": server_id, "country": country, "protocol": protocol}
        if state:
            params["state"] = state
        return await self._request("GET", "/v1/catalog/nexus/carriers", params=params)

    async def get_nexus_control_carriers(self, country: str, protocol: str, state: Optional[str] = None) -> dict:
        params = {"country": country, "protocol": protocol}
        if state:
            params["state"] = state
        return await self._request("GET", "/v1/catalog/nexus/control/carriers", params=params)

    async def get_titan_catalog(self) -> dict:
        return await self._request("GET", "/v1/catalog/titan")

    async def get_titan_fraud_options(self, country: str, isp_id: str) -> dict:
        return await self._request("GET", "/v1/catalog/titan/fraud-options",
                                    params={"country": country, "isp_id": isp_id})

    # ─── TITAN Preflight ───────────────────────────────────
    async def create_titan_preflight(self, country: str, isp_id: str, fraud_id: str,
                                     client_user_id: Optional[str] = None) -> dict:
        body: dict = {"country": country, "isp_id": isp_id, "fraud_id": fraud_id}
        if client_user_id:
            body["client_user_id"] = client_user_id
        return await self._request("POST", "/v1/titan/preflight",
                                    idempotency_key=self._make_idempotency_key("tpf"),
                                    json=body)

    async def get_titan_preflight(self, preflight_id: str) -> dict:
        return await self._request("GET", f"/v1/titan/preflight/{preflight_id}")

    async def wait_for_titan_preflight(self, preflight_id: str, timeout: int = 60) -> dict:
        """Poll preflight until terminal state or timeout."""
        terminal = {"available", "unavailable", "failed"}
        deadline = asyncio.get_event_loop().time() + timeout
        while asyncio.get_event_loop().time() < deadline:
            result = await self.get_titan_preflight(preflight_id)
            if result.get("status") in terminal:
                return result
            await asyncio.sleep(3)
        raise TimeoutError(f"Preflight {preflight_id} did not resolve in {timeout}s")

    # ─── Orders ────────────────────────────────────────────
    async def create_order(self, payload: dict, idempotency_key: Optional[str] = None) -> dict:
        key = idempotency_key or self._make_idempotency_key("order")
        return await self._request("POST", "/v1/requests", idempotency_key=key, json=payload)

    async def get_order_status(self, request_id: str) -> dict:
        return await self._request("GET", f"/v1/requests/{request_id}")

    async def get_order_result(self, request_id: str) -> dict:
        return await self._request("GET", f"/v1/requests/{request_id}/result")

    async def wait_for_order(self, request_id: str, timeout: int = 120) -> dict:
        """Poll order until succeeded or failed, returns result dict on success."""
        terminal = {"succeeded", "failed", "failed_refunded", "manual_review"}
        deadline = asyncio.get_event_loop().time() + timeout
        while asyncio.get_event_loop().time() < deadline:
            status = await self.get_order_status(request_id)
            if status.get("status") in terminal:
                if status["status"] == "succeeded":
                    return await self.get_order_result(request_id)
                raise MagnumAPIError(409, status.get("failure_reason") or "unexpected_error",
                                     status.get("error_id"))
            await asyncio.sleep(4)
        raise TimeoutError(f"Order {request_id} did not resolve in {timeout}s")

    async def list_proxies(self) -> dict:
        return await self._request("GET", "/v1/proxies")

    # ─── PRIME & HYPER Management ──────────────────────────
    async def proxy_action(self, request_id: str, action: str, **kwargs) -> dict:
        body = {"action": action, **kwargs}
        return await self._request(
            "POST", f"/v1/proxies/{request_id}/actions",
            idempotency_key=self._make_idempotency_key(f"act-{action}"),
            json=body,
        )

    async def get_management_status(self, management_id: str) -> dict:
        return await self._request("GET", f"/v1/management/{management_id}")

    async def wait_for_management(self, management_id: str, timeout: int = 60) -> dict:
        terminal = {"succeeded", "failed", "manual_review"}
        deadline = asyncio.get_event_loop().time() + timeout
        while asyncio.get_event_loop().time() < deadline:
            status = await self.get_management_status(management_id)
            if status.get("status") in terminal:
                return status
            await asyncio.sleep(3)
        raise TimeoutError(f"Management {management_id} did not resolve in {timeout}s")

    # ─── Conversion ────────────────────────────────────────
    async def convert_proxy(self, request_id: str, target_mode: str,
                             allowed_ip: Optional[str] = None,
                             username: Optional[str] = None,
                             password: Optional[str] = None) -> dict:
        body: dict = {"target_mode": target_mode}
        if allowed_ip:
            body["allowed_ip"] = allowed_ip
        if username:
            body["username"] = username
        if password:
            body["password"] = password
        return await self._request(
            "POST", f"/v1/proxies/{request_id}/convert",
            idempotency_key=self._make_idempotency_key("conv"),
            json=body,
        )

    async def get_conversion_status(self, conversion_id: str) -> dict:
        return await self._request("GET", f"/v1/conversions/{conversion_id}")

    # ─── NEXUS Management ──────────────────────────────────
    async def nexus_action(self, request_id: str, action: str, **kwargs) -> dict:
        body = {"action": action, **kwargs}
        return await self._request(
            "POST", f"/v1/nexus/{request_id}/actions",
            idempotency_key=self._make_idempotency_key(f"nxs-{action}"),
            json=body,
        )

    async def get_nexus_management_status(self, management_id: str) -> dict:
        return await self._request("GET", f"/v1/nexus/management/{management_id}")

    async def close(self):
        if self._client and not self._client.is_closed:
            await self._client.aclose()


# Singleton instance
magnum = MagnumClient()
