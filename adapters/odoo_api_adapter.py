import requests

from domain.entities import AccountStatus, Ticket


class OdooAdapterError(Exception):
    """Lỗi khi gọi Odoo API - HTTP fail, timeout, response không hợp lệ."""


class OdooAPIAdapter:
    def __init__(self, base_url: str, api_key: str, timeout: float = 10.0) -> None:
        self._base_url = base_url.rstrip("/")
        self._headers = {"Authorization": f"Bearer {api_key}"}
        self._timeout = timeout

    def get_account_status(self, ticket: Ticket) -> AccountStatus:
        url = f"{self._base_url}/api/v1/accounts/status"
        try:
            response = requests.get(
                url,
                params={"email": ticket.requester_email},
                headers=self._headers,
                timeout=self._timeout,
            )
        except requests.RequestException as exc:
            raise OdooAdapterError(f"Không gọi được Odoo API: {exc}") from exc

        if response.status_code == 404:
            return AccountStatus.UNKNOWN

        if response.status_code != 200:
            raise OdooAdapterError(
                f"Odoo API trả về status {response.status_code} khi check account status"
            )

        status_value = response.json().get("status")
        return {
            "active": AccountStatus.ACTIVE,
            "deactivated": AccountStatus.DEACTIVATED,
        }.get(status_value, AccountStatus.UNKNOWN)

    def add_note(self, ticket: Ticket, note: str) -> None:
        url = f"{self._base_url}/api/v1/tickets/{ticket.id}/notes"
        try:
            response = requests.post(
                url,
                json={"note": note},
                headers=self._headers,
                timeout=self._timeout,
            )
        except requests.RequestException as exc:
            raise OdooAdapterError(f"Không gọi được Odoo API: {exc}") from exc

        if response.status_code not in (200, 201):
            raise OdooAdapterError(
                f"Odoo API trả về status {response.status_code} khi add note"
            )