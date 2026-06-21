import logging

from domain.entities import Ticket

logger = logging.getLogger(__name__)


class MockLMSAdapter:
    def __init__(self) -> None:
        self.reactivated_tickets: list[Ticket] = []

    def reactivate(self, ticket: Ticket) -> None:
        self.reactivated_tickets.append(ticket)
        logger.warning(
            "MOCK LMS adapter - KHÔNG reactivate account thật (ticket=%s email=%s)",
            ticket.id,
            ticket.requester_email,
        )