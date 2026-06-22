from adapters.mock_hr_system_adapter import MockHRSystemAdapter
from adapters.mock_lms_adapter import MockLMSAdapter
from adapters.mock_ticket_system_adapter import MockTicketSystemAdapter
from adapters.python_logging_adapter import PythonLoggingAdapter
from adapters.webhook_app import create_app
from domain.deactivation_case_detector import DeactivationCaseDetector
from domain.decision_engine import DecisionEngine
from domain.entities import AccountStatus, EmployeeStatus
from domain.process_login_ticket_use_case import ProcessLoginTicketUseCase
from domain.ticket_classifier import TicketClassifier
from tools.console_notification_adapter import ConsoleNotificationAdapter

_ACCOUNT_STATUS_BY_EMAIL = {
    "active.account@mindx.edu.vn": AccountStatus.ACTIVE,
    "active.employee@mindx.edu.vn": AccountStatus.DEACTIVATED,
    "terminated.employee@mindx.edu.vn": AccountStatus.DEACTIVATED,
    "unknown.employee@mindx.edu.vn": AccountStatus.DEACTIVATED,
}
_EMPLOYEE_STATUS_BY_EMAIL = {
    "active.employee@mindx.edu.vn": EmployeeStatus.ACTIVE,
    "terminated.employee@mindx.edu.vn": EmployeeStatus.TERMINATED,
    # unknown.employee@mindx.edu.vn cố tình KHÔNG có trong map -> UNKNOWN
}


def build_demo_use_case() -> ProcessLoginTicketUseCase:
    return ProcessLoginTicketUseCase(
        classifier=TicketClassifier(),
        detector=DeactivationCaseDetector(),
        decision_engine=DecisionEngine(),
        ticket_system=MockTicketSystemAdapter(_ACCOUNT_STATUS_BY_EMAIL),
        hr_system=MockHRSystemAdapter(_EMPLOYEE_STATUS_BY_EMAIL),
        account_system=MockLMSAdapter(),
        notifier=ConsoleNotificationAdapter(),
        logger=PythonLoggingAdapter(),
    )


app = create_app(build_demo_use_case())

if __name__ == "__main__":
    app.run(port=5000)
