import requests

from domain.entities import EmployeeStatus, Ticket


class HRAdapterError(Exception):
    """Lỗi khi gọi HR system API - HTTP fail, timeout, server error."""


class HRSystemAPIAdapter:
    def __init__(self, base_url: str, api_key: str, timeout: float = 10.0) -> None:
        self._base_url = base_url.rstrip("/")
        self._headers = {"X-API-Key": api_key}
        self._timeout = timeout

    def get_employee_status(self, ticket: Ticket) -> EmployeeStatus:
        url = f"{self._base_url}/api/v1/employees/status"
        try:
            response = requests.get(
                url,
                params={"email": ticket.requester_email},
                headers=self._headers,
                timeout=self._timeout,
            )
        except requests.RequestException as exc:
            raise HRAdapterError(f"Không gọi được HR system API: {exc}") from exc

        if response.status_code == 404:
            return EmployeeStatus.UNKNOWN

        if response.status_code != 200:
            raise HRAdapterError(
                f"HR system API trả về status {response.status_code} khi check employee status"
            )

        status_value = response.json().get("employment_status")
        return {
            "active": EmployeeStatus.ACTIVE,
            "terminated": EmployeeStatus.TERMINATED,
        }.get(status_value, EmployeeStatus.UNKNOWN)