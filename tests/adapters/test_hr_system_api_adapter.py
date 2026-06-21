import unittest
from unittest.mock import Mock, patch

import requests

from adapters.hr_system_api_adapter import HRAdapterError, HRSystemAPIAdapter
from domain.entities import EmployeeStatus, Ticket


class TestHRSystemAPIAdapter(unittest.TestCase):
    def setUp(self):
        self.adapter = HRSystemAPIAdapter(base_url="https://hr.mindx.edu.vn", api_key="fake-key")
        self.ticket = Ticket(id="T-201", content="...", requester_email="user@mindx.edu.vn")

    @patch("adapters.hr_system_api_adapter.requests.get")
    def test_employee_active(self, mock_get):
        mock_get.return_value = Mock(status_code=200, json=lambda: {"employment_status": "active"})

        result = self.adapter.get_employee_status(self.ticket)

        self.assertEqual(result, EmployeeStatus.ACTIVE)
        self.assertEqual(mock_get.call_args.kwargs["params"], {"email": "user@mindx.edu.vn"})

    @patch("adapters.hr_system_api_adapter.requests.get")
    def test_employee_terminated(self, mock_get):
        mock_get.return_value = Mock(status_code=200, json=lambda: {"employment_status": "terminated"})

        result = self.adapter.get_employee_status(self.ticket)

        self.assertEqual(result, EmployeeStatus.TERMINATED)

    @patch("adapters.hr_system_api_adapter.requests.get")
    def test_employee_not_found_returns_unknown_not_error(self, mock_get):
        # Không tìm thấy nhân sự là kết quả hợp lệ (escalate), không phải lỗi hệ thống
        mock_get.return_value = Mock(status_code=404)

        result = self.adapter.get_employee_status(self.ticket)

        self.assertEqual(result, EmployeeStatus.UNKNOWN)

    @patch("adapters.hr_system_api_adapter.requests.get")
    def test_server_error_raises(self, mock_get):
        mock_get.return_value = Mock(status_code=500)

        with self.assertRaises(HRAdapterError):
            self.adapter.get_employee_status(self.ticket)

    @patch("adapters.hr_system_api_adapter.requests.get")
    def test_network_error_raises(self, mock_get):
        mock_get.side_effect = requests.ConnectionError("unreachable")

        with self.assertRaises(HRAdapterError):
            self.adapter.get_employee_status(self.ticket)


if __name__ == "__main__":
    unittest.main()