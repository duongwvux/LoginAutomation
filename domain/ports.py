from typing import Protocol

from .entities import AccountStatus, EmployeeStatus, Ticket

class TicketSystemPort(Protocol):
    def get_account_status(self, ticket: Ticket) -> AccountStatus: ...

    def add_notes(self, ticket: Ticket, note: str) -> None: ...

class HRSystemPort(Protocol):
    def get_employee_status(self, ticket: Ticket) -> EmployeeStatus: ...

class AccountSystemPort(Protocol):
    def reactivate(self, ticket: Ticket) -> None: ...

class NotificationPort(Protocol):
    def send_email(self, ticket: Ticket, message: str) -> None: ...

class LoggingPort(Protocol):
    def log(self, event: str) -> None: ...