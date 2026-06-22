import unittest

from adapters.odoo_webhook_adapter import InvalidWebhookPayloadError, parse_webhook_payload


class TestParseWebhookPayload(unittest.TestCase):
    def test_parses_valid_payload(self):
        ticket = parse_webhook_payload(
            {
                "ticket_id": "T-100",
                "subject": "Không đăng nhập được",
                "description": "Chi tiết vấn đề ở đây.",
                "partner_email": "a@mindx.edu.vn",
            }
        )

        self.assertEqual(ticket.id, "T-100")
        self.assertIn("Không đăng nhập được", ticket.content)
        self.assertIn("Chi tiết vấn đề", ticket.content)
        self.assertEqual(ticket.requester_email, "a@mindx.edu.vn")

    def test_missing_ticket_id_raises(self):
        with self.assertRaises(InvalidWebhookPayloadError):
            parse_webhook_payload({"partner_email": "a@mindx.edu.vn"})

    def test_missing_partner_email_raises(self):
        with self.assertRaises(InvalidWebhookPayloadError):
            parse_webhook_payload({"ticket_id": "T-100"})

    def test_missing_subject_and_description_still_works_with_empty_content(self):
        ticket = parse_webhook_payload({"ticket_id": "T-101", "partner_email": "b@mindx.edu.vn"})

        self.assertEqual(ticket.content, "")


if __name__ == "__main__":
    unittest.main()