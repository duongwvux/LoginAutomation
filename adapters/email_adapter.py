import smtplib
from email.message import EmailMessage

from domain.entities import Ticket


class EmailAdapterError(Exception):
    """Lỗi khi gửi email - kết nối SMTP, auth, hoặc gửi thất bại."""


class EmailAdapter:
    def __init__(
            self,
            smtp_host: str,
            smtp_port: int,
            smtp_username: str,
            smtp_password: str,
    ) -> None:
        self._smtp_host = smtp_host
        self._smtp_port = smtp_port
        self._smtp_username = smtp_username
        self._smtp_password = smtp_password

    def send_email(self, ticket: Ticket, message: str) -> None:
        email_msg = EmailMessage()
        email_msg["Subject"] = f"RE: Vấn đề đăng nhập - Ticket #{ticket.id}"
        email_msg["From"] = self._smtp_username
        email_msg["To"] = ticket.requester_email
        email_msg.set_content(message)

        try:
            with smtplib.SMTP_SSL(self._smtp_host, self._smtp_port) as server:
                server.login(self._smtp_username, self._smtp_password)
                server.send_message(email_msg)
        except smtplib.SMTPException as exc:
            raise EmailAdapterError(f"Không gửi được email: {exc}") from exc