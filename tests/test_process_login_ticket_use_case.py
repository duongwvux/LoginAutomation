import unittest

from domain.decision_engine import DecisionEngine
from domain.deactivation_case_detector import DeactivationCaseDetector
from domain.entities import AccountStatus, Action, EmployeeStatus, Ticket
from domain.process_login_ticket_use_case import ProcessLoginTicketUseCase
from domain.ticket_classifier import TicketClassifier

from .fakes import (
    FakeAccountSystem,
    FakeHRSystem,
    FakeLogger,
    FakeNotifier,
    FakeTicketSystem,
)


class TestProcessLoginTicketUseCase(unittest.TestCase):
    def _build_use_case(self, ticket_system, hr_system, account_system, notifier, logger):
        return ProcessLoginTicketUseCase(
            classifier=TicketClassifier(),
            detector=DeactivationCaseDetector(),
            decision_engine=DecisionEngine(),
            ticket_system=ticket_system,
            hr_system=hr_system,
            account_system=account_system,
            notifier=notifier,
            logger=logger,
        )

    def test_non_login_ticket_is_ignored_without_touching_any_port(self):
        ticket = Ticket(id="T-100", content="Máy in bị kẹt giấy.", requester_email="a@mindx.edu.vn")
        ticket_system = FakeTicketSystem()
        hr_system = FakeHRSystem()
        account_system = FakeAccountSystem()
        notifier = FakeNotifier()
        logger = FakeLogger()
        use_case = self._build_use_case(ticket_system, hr_system, account_system, notifier, logger)

        action = use_case.handle(ticket)

        self.assertEqual(action, Action.IGNORE)
        self.assertEqual(ticket_system.get_account_status_calls, 0)
        self.assertEqual(hr_system.get_employee_status_calls, 0)
        self.assertEqual(account_system.reactivated_tickets, [])
        self.assertEqual(notifier.sent_emails, [])

    def test_active_account_login_issue_is_escalated_without_hr_check(self):
        # Account vẫn Active -> nhiều khả năng sai password, không phải
        # deactivation -> escalate, KHÔNG cần tốn 1 lần gọi HR system
        ticket = Ticket(
            id="T-101",
            content="Không đăng nhập được, Invalid username or password.",
            requester_email="teacher@mindx.edu.vn",
        )
        ticket_system = FakeTicketSystem(account_status=AccountStatus.ACTIVE)
        hr_system = FakeHRSystem()
        account_system = FakeAccountSystem()
        notifier = FakeNotifier()
        logger = FakeLogger()
        use_case = self._build_use_case(ticket_system, hr_system, account_system, notifier, logger)

        action = use_case.handle(ticket)

        self.assertEqual(action, Action.ESCALATE)
        self.assertEqual(hr_system.get_employee_status_calls, 0)
        self.assertEqual(len(ticket_system.notes), 1)
        self.assertEqual(account_system.reactivated_tickets, [])
        self.assertEqual(notifier.sent_emails, [])

    def test_unknown_account_status_escalates_without_hr_check(self):
        ticket = Ticket(
            id="T-102", content="Em không đăng nhập được vào LMS.", requester_email="b@mindx.edu.vn"
        )
        ticket_system = FakeTicketSystem(account_status=AccountStatus.UNKNOWN)
        hr_system = FakeHRSystem()
        account_system = FakeAccountSystem()
        notifier = FakeNotifier()
        logger = FakeLogger()
        use_case = self._build_use_case(ticket_system, hr_system, account_system, notifier, logger)

        action = use_case.handle(ticket)

        self.assertEqual(action, Action.ESCALATE)
        self.assertEqual(hr_system.get_employee_status_calls, 0)
        self.assertEqual(len(ticket_system.notes), 1)

    def test_deactivated_account_active_employee_reactivates_and_emails(self):
        ticket = Ticket(
            id="T-103",
            content="Tài khoản bị deactivate, không đăng nhập được.",
            requester_email="c@mindx.edu.vn",
        )
        ticket_system = FakeTicketSystem(account_status=AccountStatus.DEACTIVATED)
        hr_system = FakeHRSystem(employee_status=EmployeeStatus.ACTIVE)
        account_system = FakeAccountSystem()
        notifier = FakeNotifier()
        logger = FakeLogger()
        use_case = self._build_use_case(ticket_system, hr_system, account_system, notifier, logger)

        action = use_case.handle(ticket)

        self.assertEqual(action, Action.REACTIVATE)
        self.assertEqual(account_system.reactivated_tickets, [ticket])
        self.assertEqual(len(notifier.sent_emails), 1)
        self.assertEqual(len(ticket_system.notes), 1)
        self.assertTrue(logger.events)

    def test_deactivated_account_terminated_employee_adds_note_without_reactivating(self):
        # Nhân sự đã nghỉ -> KHÔNG tự reactivate, KHÔNG tự gửi email cho
        # user - cần người review trước khi liên hệ lại
        ticket = Ticket(
            id="T-104",
            content="Tài khoản bị deactivate, không đăng nhập được.",
            requester_email="d@mindx.edu.vn",
        )
        ticket_system = FakeTicketSystem(account_status=AccountStatus.DEACTIVATED)
        hr_system = FakeHRSystem(employee_status=EmployeeStatus.TERMINATED)
        account_system = FakeAccountSystem()
        notifier = FakeNotifier()
        logger = FakeLogger()
        use_case = self._build_use_case(ticket_system, hr_system, account_system, notifier, logger)

        action = use_case.handle(ticket)

        self.assertEqual(action, Action.ADD_NOTE)
        self.assertEqual(account_system.reactivated_tickets, [])
        self.assertEqual(notifier.sent_emails, [])
        self.assertEqual(len(ticket_system.notes), 1)

    def test_deactivated_account_unknown_employee_status_escalates(self):
        ticket = Ticket(
            id="T-105",
            content="Tài khoản bị deactivate, không đăng nhập được.",
            requester_email="e@mindx.edu.vn",
        )
        ticket_system = FakeTicketSystem(account_status=AccountStatus.DEACTIVATED)
        hr_system = FakeHRSystem(employee_status=EmployeeStatus.UNKNOWN)
        account_system = FakeAccountSystem()
        notifier = FakeNotifier()
        logger = FakeLogger()
        use_case = self._build_use_case(ticket_system, hr_system, account_system, notifier, logger)

        action = use_case.handle(ticket)

        self.assertEqual(action, Action.ESCALATE)
        self.assertEqual(account_system.reactivated_tickets, [])
        self.assertEqual(notifier.sent_emails, [])
        self.assertEqual(len(ticket_system.notes), 1)


if __name__ == "__main__":
    unittest.main()