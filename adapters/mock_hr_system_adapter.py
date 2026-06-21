import logging

from domain.entities import EmployeeStatus, Ticket

logger = logging.getLogger(__name__)


class MockHRSystemAdapter:
    def __init__(self, employee_status_by_email: dict[str, EmployeeStatus] | None = None) -> None:
        self._employee_status_by_email = employee_status_by_email or {}

    def get_employee_status(self, ticket: Ticket) -> EmployeeStatus:
        status = self._employee_status_by_email.get(
            ticket.requester_email, EmployeeStatus.UNKNOWN
        )
        logger.warning(
            "MOCK HR adapter - không gọi HR system thật (email=%s -> %s)",
            ticket.requester_email,
            status.value,
        )
        return status