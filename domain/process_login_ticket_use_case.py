from .decision_engine import DecisionEngine
from .deactivation_case_detector import DeactivationCaseDetector
from .entities import Action, Ticket
from .ports import (
    AccountSystemPort,
    HRSystemPort,
    LoggingPort,
    NotificationPort,
    TicketSystemPort,
)
from .ticket_classifier import TicketClassifier

class ProcessLoginTicketUseCase:
    def __init__(
            self,
            classifier: TicketClassifier,
            detector: DeactivationCaseDetector,
            decision_engine: DecisionEngine,
            ticket_system: TicketSystemPort,
            hr_system: HRSystemPort,
            account_system: AccountSystemPort,
            notifier: NotificationPort,
            logger: LoggingPort,
    ) -> None:
        self._classifier = classifier
        self._detector = detector
        self._decision_engine = decision_engine
        self._ticket_system = ticket_system
        self._hr_system = hr_system
        self._account_system = account_system
        self._notifier = notifier
        self._logger = logger

    def handle(self, ticket: Ticket) -> Action:
        is_login_issue = self._classifier.is_login_issue(ticket)
        if not is_login_issue:
            self._logger.log(f"Ticket {ticket.id}: không phải login issue, bỏ qua")
            return Action.IGNORE
        account_status = self._ticket_system.get_account_status(ticket)
        if not self._detector.is_deactivation_case(is_login_issue, account_status):
            self._ticket_system.add_notes(
                ticket,
                f"Login issue nhưng account_status={account_status.value} - "
                "ngoài phạm vi automation, có thể là sai password. Cần xử lý thủ công.",
            )
            self._logger.log(f"Ticket {ticket.id}: ngoài phạm vi automation, escalate")
            return Action.ESCALATE

        employee_status = self._hr_system.get_employee_status(ticket)
        action = self._decision_engine.decide(employee_status)

        if action == Action.REACTIVATE:
            self._account_system.reactivate(ticket)
            self._notifier.send_email(
                ticket,
                "Tài khoản của bạn đã được kích hoạt lại. Vui lòng thử đăng nhập lại.",
            )
            self._ticket_system.add_notes(ticket, "Đã reactivate account tự động.")
            self._logger.log(f"Ticket {ticket.id}: reactivated tự động")
        elif action == Action.ADD_NOTE:
            self._ticket_system.add_notes(
                ticket,
                "Nhân sự đã nghỉ việc (terminated) - cần review thủ công trước "
                "khi phản hồi user.",
            )
            self._logger.log(f"Ticket {ticket.id}: nhân sự đã nghỉ, ghi note chờ review")
        else:  # ESCALATE - không xác định được employee status
            self._ticket_system.add_notes(
                ticket,
                "Không xác định được trạng thái nhân sự - cần escalate cho người xử lý.",
            )
            self._logger.log(f"Ticket {ticket.id}: employee status unknown, escalate")

        return action