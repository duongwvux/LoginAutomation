from .entities import Ticket

_LOGIN_KEYWORDS = (
    "đăng nhập",
    "log in",
    "log-in",
    "login",
    "tài khoản",
    "account",
    "reactivate",
    "deactivate",
    "mật khẩu",
    "password",
    "invalid username",
)

class TicketClassifier:
    def is_login_issue(self, ticket: Ticket) -> bool:
        content = ticket.content.lower()
        return any(keyword in content for keyword in _LOGIN_KEYWORDS)