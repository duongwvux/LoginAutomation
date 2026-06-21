import unittest

from adapters.mock_lms_adapter import MockLMSAdapter
from domain.entities import Ticket


class TestMockLMSAdapter(unittest.TestCase):
    def test_reactivate_records_the_ticket(self):
        adapter = MockLMSAdapter()
        ticket = Ticket(id="T-303", content="...", requester_email="c@mindx.edu.vn")

        adapter.reactivate(ticket)

        self.assertEqual(adapter.reactivated_tickets, [ticket])

    def test_reactivate_does_not_raise(self):
        adapter = MockLMSAdapter()
        ticket = Ticket(id="T-304", content="...", requester_email="d@mindx.edu.vn")

        adapter.reactivate(ticket)  # không raise = pass

    def test_reactivate_multiple_tickets_recorded_in_order(self):
        adapter = MockLMSAdapter()
        t1 = Ticket(id="T-305", content="...", requester_email="e@mindx.edu.vn")
        t2 = Ticket(id="T-306", content="...", requester_email="f@mindx.edu.vn")

        adapter.reactivate(t1)
        adapter.reactivate(t2)

        self.assertEqual(adapter.reactivated_tickets, [t1, t2])


if __name__ == "__main__":
    unittest.main()