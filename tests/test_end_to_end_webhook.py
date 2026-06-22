import unittest
from unittest.mock import MagicMock, Mock, patch

from adapters.email_adapter import EmailAdapter
from adapters.mock_hr_system_adapter import MockHRSystemAdapter
from adapters.mock_lms_adapter import MockLMSAdapter
from adapters.odoo_api_adapter import OdooAPIAdapter
from adapters.python_logging_adapter import PythonLoggingAdapter
from adapters.webhook_app import create_app
from domain.deactivation_case_detector import DeactivationCaseDetector
from domain.decision_engine import DecisionEngine
from domain.entities import EmployeeStatus
from domain.process_login_ticket_use_case import ProcessLoginTicketUseCase
from domain.ticket_classifier import TicketClassifier


def _build_test_use_case(employee_status_by_email):
    odoo = OdooAPIAdapter(base_url="https://odoo.mindx.edu.vn", api_key="fake-key")
    email = EmailAdapter(
        smtp_host="smtp.mindx.edu.vn",
        smtp_port=465,
        smtp_username="support@mindx.edu.vn",
        smtp_password="fake-password",
    )
    return ProcessLoginTicketUseCase(
        classifier=TicketClassifier(),
        detector=DeactivationCaseDetector(),
        decision_engine=DecisionEngine(),
        ticket_system=odoo,
        hr_system=MockHRSystemAdapter(employee_status_by_email),
        account_system=MockLMSAdapter(),
        notifier=email,
        logger=PythonLoggingAdapter(),
    )


class TestEndToEndWebhook(unittest.TestCase):
    @patch("adapters.email_adapter.smtplib.SMTP_SSL")
    @patch("adapters.odoo_api_adapter.requests.post")
    @patch("adapters.odoo_api_adapter.requests.get")
    def test_deactivated_active_employee_reactivates_via_webhook(
            self, mock_get, mock_post, mock_smtp_ssl
    ):
        mock_get.return_value = Mock(status_code=200, json=lambda: {"status": "deactivated"})
        mock_post.return_value = Mock(status_code=201)
        mock_server = MagicMock()
        mock_smtp_ssl.return_value.__enter__.return_value = mock_server

        use_case = _build_test_use_case({"teacher@mindx.edu.vn": EmployeeStatus.ACTIVE})
        client = create_app(use_case).test_client()

        response = client.post(
            "/webhooks/odoo/ticket-created",
            json={
                "ticket_id": "T-9001",
                "subject": "Không thể đăng nhập vào LMS",
                "description": "Tài khoản bị deactivate, không đăng nhập được.",
                "partner_email": "teacher@mindx.edu.vn",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["action"], "reactivate")
        mock_server.send_message.assert_called_once()  # email xác nhận đã gửi
        mock_post.assert_called_once()  # note đã ghi vào Odoo

    @patch("adapters.odoo_api_adapter.requests.get")
    def test_non_login_ticket_ignored_via_webhook(self, mock_get):
        use_case = _build_test_use_case({})
        client = create_app(use_case).test_client()

        response = client.post(
            "/webhooks/odoo/ticket-created",
            json={
                "ticket_id": "T-9002",
                "subject": "Máy in lỗi",
                "description": "Máy in tầng 3 kẹt giấy.",
                "partner_email": "staff@mindx.edu.vn",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["action"], "ignore")
        mock_get.assert_not_called()  # IGNORE sớm, không tốn lần gọi Odoo nào

    @patch("adapters.odoo_api_adapter.requests.post")
    @patch("adapters.odoo_api_adapter.requests.get")
    def test_active_account_login_issue_escalates_via_webhook(self, mock_get, mock_post):
        # Account còn Active -> nhiều khả năng sai password, ngoài phạm vi automation
        mock_get.return_value = Mock(status_code=200, json=lambda: {"status": "active"})
        mock_post.return_value = Mock(status_code=201)  # add_note() khi escalate

        use_case = _build_test_use_case({})
        client = create_app(use_case).test_client()

        response = client.post(
            "/webhooks/odoo/ticket-created",
            json={
                "ticket_id": "T-9003",
                "subject": "Invalid username or password",
                "description": "Không đăng nhập được vào LMS.",
                "partner_email": "teacher2@mindx.edu.vn",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["action"], "escalate")
        mock_post.assert_called_once()  # note giải thích lý do escalate đã ghi vào Odoo

    def test_invalid_payload_returns_400(self):
        use_case = _build_test_use_case({})
        client = create_app(use_case).test_client()

        response = client.post(
            "/webhooks/odoo/ticket-created",
            json={"subject": "thiếu ticket_id và partner_email"},
        )

        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()
