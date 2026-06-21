import requests

from domain.entities import Ticket


class LMSAdapterError(Exception):
    """Lỗi khi gọi LMS API - HTTP fail, timeout, account không tồn tại."""


class LMSAPIAdapter:
    def __init__(self, base_url: str, api_key: str, timeout: float = 10.0) -> None:
        self._base_url = base_url.rstrip("/")
        self._headers = {"Authorization": f"Bearer {api_key}"}
        self._timeout = timeout

    def reactivate(self, ticket: Ticket) -> None:
        url = f"{self._base_url}/api/v1/accounts/reactivate"
        try:
            response = requests.post(
                url,
                json={"email": ticket.requester_email},
                headers=self._headers,
                timeout=self._timeout,
            )
        except requests.RequestException as exc:
            raise LMSAdapterError(f"Không gọi được LMS API: {exc}") from exc

        if response.status_code != 200:
            raise LMSAdapterError(
                f"LMS API trả về status {response.status_code} khi reactivate account"
            )