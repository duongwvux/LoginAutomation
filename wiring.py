import os

from adapters.email_adapter import EmailAdapter
from adapters.mock_hr_system_adapter import MockHRSystemAdapter
from adapters.mock_lms_adapter import MockLMSAdapter
from adapters.mock_ticket_system_adapter import MockTicketSystemAdapter
from adapters.python_logging_adapter import PythonLoggingAdapter
from domain.deactivation_case_detector import DeactivationCaseDetector
from domain.decision_engine import DecisionEngine
from domain.entities import AccountStatus, EmployeeStatus
from domain.process_login_ticket_use_case import ProcessLoginTicketUseCase
from domain.ticket_classifier import TicketClassifier

# TODO: đổi sang đọc từ file JSON/CSV nội bộ, hoặc adapter thật khi đã xác
# nhận được cách kết nối Odoo / có access HR / LMS thật. Tạm cấu hình tay.
_MOCK_ACCOUNT_STATUS_BY_EMAIL: dict[str, AccountStatus] = {}
_MOCK_EMPLOYEE_STATUS_BY_EMAIL: dict[str, EmployeeStatus] = {}


def build_use_case() -> ProcessLoginTicketUseCase:
    email = EmailAdapter(
        smtp_host=os.environ["SMTP_HOST"],
        smtp_port=int(os.environ.get("SMTP_PORT", "465")),
        smtp_username=os.environ["SMTP_USERNAME"],
        smtp_password=os.environ["SMTP_PASSWORD"],
    )

    ticket_system = MockTicketSystemAdapter(_MOCK_ACCOUNT_STATUS_BY_EMAIL)
    hr_system = MockHRSystemAdapter(_MOCK_EMPLOYEE_STATUS_BY_EMAIL)
    account_system = MockLMSAdapter()

    return ProcessLoginTicketUseCase(
        classifier=TicketClassifier(),
        detector=DeactivationCaseDetector(),
        decision_engine=DecisionEngine(),
        ticket_system=ticket_system,
        hr_system=hr_system,
        account_system=account_system,
        notifier=email,
        logger=PythonLoggingAdapter(),
    )
