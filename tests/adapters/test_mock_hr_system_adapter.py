import unittest

from adapters.mock_hr_system_adapter import MockHRSystemAdapter
from domain.entities import EmployeeStatus, Ticket


class TestMockHRSystemAdapter(unittest.TestCase):
    def test_returns_configured_status_for_known_email(self):
        adapter = MockHRSystemAdapter({"a@mindx.edu.vn": EmployeeStatus.ACTIVE})
        ticket = Ticket(id="T-300", content="...", requester_email="a@mindx.edu.vn")

        self.assertEqual(adapter.get_employee_status(ticket), EmployeeStatus.ACTIVE)

    def test_returns_unknown_for_unrecognized_email(self):
        adapter = MockHRSystemAdapter({"a@mindx.edu.vn": EmployeeStatus.ACTIVE})
        ticket = Ticket(id="T-301", content="...", requester_email="unknown@mindx.edu.vn")

        self.assertEqual(adapter.get_employee_status(ticket), EmployeeStatus.UNKNOWN)

    def test_works_with_no_config_at_all(self):
        adapter = MockHRSystemAdapter()
        ticket = Ticket(id="T-302", content="...", requester_email="b@mindx.edu.vn")

        self.assertEqual(adapter.get_employee_status(ticket), EmployeeStatus.UNKNOWN)


if __name__ == "__main__":
    unittest.main()