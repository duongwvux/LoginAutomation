import smtplib
import unittest
from unittest.mock import MagicMock, patch

from adapters.email_adapter import EmailAdapter, EmailAdapterError
from domain.entities import Ticket


class TestEmailAdapter(unittest.TestCase):
    def setUp(self):
        self.adapter = EmailAdapter(
            smtp_host="smtp.mindx.edu.vn",
            smtp_port=465,
            smtp_username="support@mindx.edu.vn",
            smtp_password="fake-password",
        )
        self.ticket = Ticket(id="T-203", content="...", requester_email="teacher@mindx.edu.vn")

    @patch("adapters.email_adapter.smtplib.SMTP_SSL")
    def test_send_email_success(self, mock_smtp_ssl):
        mock_server = MagicMock()
        mock_smtp_ssl.return_value.__enter__.return_value = mock_server

        self.adapter.send_email(self.ticket, "Tài khoản đã được kích hoạt lại.")

        mock_server.login.assert_called_once_with("support@mindx.edu.vn", "fake-password")
        mock_server.send_message.assert_called_once()
        sent_message = mock_server.send_message.call_args.args[0]
        self.assertEqual(sent_message["To"], "teacher@mindx.edu.vn")
        self.assertIn("T-203", sent_message["Subject"])

    @patch("adapters.email_adapter.smtplib.SMTP_SSL")
    def test_send_email_auth_failure_raises(self, mock_smtp_ssl):
        mock_server = MagicMock()
        mock_server.login.side_effect = smtplib.SMTPAuthenticationError(535, "bad credentials")
        mock_smtp_ssl.return_value.__enter__.return_value = mock_server

        with self.assertRaises(EmailAdapterError):
            self.adapter.send_email(self.ticket, "Tài khoản đã được kích hoạt lại.")


if __name__ == "__main__":
    unittest.main()