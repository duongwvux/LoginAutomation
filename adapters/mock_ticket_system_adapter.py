import logging

from domain.entities import AccountStatus, Ticket

logger = logging.getLogger(__name__)


class MockTicketSystemAdapter:
    def __init__(self, account_status_by_email: dict[str, AccountStatus] | None = None) -> None:
        self._account_status_by_email = account_status_by_email or {}
        self.notes: list[tuple[Ticket, str]] = []

    def get_account_status(self, ticket: Ticket) -> AccountStatus:
        status = self._account_status_by_email.get(
            ticket.requester_email, AccountStatus.UNKNOWN
        )
        logger.warning(
            "MOCK Ticket system adapter - không gọi Odoo thật (email=%s -> %s)",
            ticket.requester_email,
            status.value,
        )
        return status

    def add_note(self, ticket: Ticket, note: str) -> None:
        self.notes.append((ticket, note))
        logger.warning(
            "MOCK Ticket system adapter - KHÔNG ghi note vào Odoo thật (ticket=%s): %s",
            ticket.id,
            note,
        )