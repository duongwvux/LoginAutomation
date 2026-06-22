import unittest

from adapters.mock_ticket_system_adapter import MockTicketSystemAdapter
from domain.entities import AccountStatus, Ticket


class TestMockTicketSystemAdapter(unittest.TestCase):
    def test_returns_configured_status_for_known_email(self):
        adapter = MockTicketSystemAdapter({"a@mindx.edu.vn": AccountStatus.DEACTIVATED})
        ticket = Ticket(id="T-400", content="...", requester_email="a@mindx.edu.vn")

        self.assertEqual(adapter.get_account_status(ticket), AccountStatus.DEACTIVATED)

    def test_returns_unknown_for_unrecognized_email(self):
        adapter = MockTicketSystemAdapter({"a@mindx.edu.vn": AccountStatus.DEACTIVATED})
        ticket = Ticket(id="T-401", content="...", requester_email="unknown@mindx.edu.vn")

        self.assertEqual(adapter.get_account_status(ticket), AccountStatus.UNKNOWN)

    def test_works_with_no_config_at_all(self):
        adapter = MockTicketSystemAdapter()
        ticket = Ticket(id="T-402", content="...", requester_email="b@mindx.edu.vn")

        self.assertEqual(adapter.get_account_status(ticket), AccountStatus.UNKNOWN)

    def test_add_note_records_the_note(self):
        adapter = MockTicketSystemAdapter()
        ticket = Ticket(id="T-403", content="...", requester_email="c@mindx.edu.vn")

        adapter.add_note(ticket, "test note")

        self.assertEqual(adapter.notes, [(ticket, "test note")])

    def test_add_note_does_not_raise(self):
        adapter = MockTicketSystemAdapter()
        ticket = Ticket(id="T-404", content="...", requester_email="d@mindx.edu.vn")

        adapter.add_note(ticket, "test note")  # không raise = pass


if __name__ == "__main__":
    unittest.main()