import unittest

from domain.entities import Ticket
from domain.ticket_classifier import TicketClassifier

class TestTicketClassifier(unittest.TestCase):
    def setUp(self):
        self.classifier = TicketClassifier()

    def test_identifies_login_issue_tickets(self):
        login_issue_contents = [
            "Em không đăng nhập được vào hệ thống, báo lỗi tài khoản bị khóa.",
            "Tài khoản của tôi bị deactivate, không vào được LMS.",
            "Please reactivate my account, I can't log in anymore.",
            "Account locked after 30 days of inactivity, need access again.",
        ]
        for content in login_issue_contents:
            with self.subTest(content=content):
                ticket = Ticket(id="T-001", content=content, requester_email="user@company.com")
                self.assertTrue(self.classifier.is_login_issue(ticket))

    def test_does_not_misclassify_unrelated_tickets(self):
        unrelated_ticket_contents = [
            "Máy in ở tầng 3 bị kẹt giấy, cần hỗ trợ.",
            "Tôi muốn xin nghỉ phép 2 ngày tuần sau.",
            "Internet ở phòng họp A rất chậm, không vào web được.",
        ]
        for content in unrelated_ticket_contents:
            with self.subTest(content=content):
                ticket = Ticket(id="T-002", content=content, requester_email="user@company.com")
                self.assertFalse(self.classifier.is_login_issue(ticket))

    def test_handles_empty_content_gracefully(self):
        ticket = Ticket(id="T-003", content="", requester_email="user@company.com")
        self.assertFalse(self.classifier.is_login_issue(ticket))

if __name__ == '__main__':
    unittest.main()