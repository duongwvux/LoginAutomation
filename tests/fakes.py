from domain.entities import AccountStatus, EmployeeStatus, Ticket


class FakeTicketSystem:
    def __init__(self, account_status: AccountStatus = AccountStatus.UNKNOWN):
        self.account_status = account_status
        self.notes: list[str] = []
        self.get_account_status_calls = 0

    def get_account_status(self, ticket: Ticket) -> AccountStatus:
        self.get_account_status_calls += 1
        return self.account_status

    def add_note(self, ticket: Ticket, note: str) -> None:
        self.notes.append(note)


class FakeHRSystem:
    def __init__(self, employee_status: EmployeeStatus = EmployeeStatus.UNKNOWN):
        self.employee_status = employee_status
        self.get_employee_status_calls = 0

    def get_employee_status(self, ticket: Ticket) -> EmployeeStatus:
        self.get_employee_status_calls += 1
        return self.employee_status


class FakeAccountSystem:
    def __init__(self):
        self.reactivated_tickets: list[Ticket] = []

    def reactivate(self, ticket: Ticket) -> None:
        self.reactivated_tickets.append(ticket)


class FakeNotifier:
    def __init__(self):
        self.sent_emails: list[tuple[Ticket, str]] = []

    def send_email(self, ticket: Ticket, message: str) -> None:
        self.sent_emails.append((ticket, message))


class FakeLogger:
    def __init__(self):
        self.events: list[str] = []

    def log(self, event: str) -> None:
        self.events.append(event)