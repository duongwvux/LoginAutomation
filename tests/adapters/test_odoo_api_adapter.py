import unittest
from unittest.mock import Mock, patch

import requests

from adapters.odoo_api_adapter import OdooAdapterError, OdooAPIAdapter
from domain.entities import AccountStatus, Ticket


class TestOdooAPIAdapter(unittest.TestCase):
    def setUp(self):
        self.adapter = OdooAPIAdapter(base_url="https://odoo.mindx.edu.vn", api_key="fake-key")
        self.ticket = Ticket(id="T-200", content="...", requester_email="user@mindx.edu.vn")

    @patch("adapters.odoo_api_adapter.requests.get")
    def test_get_account_status_active(self, mock_get):
        mock_get.return_value = Mock(status_code=200, json=lambda: {"status": "active"})

        result = self.adapter.get_account_status(self.ticket)

        self.assertEqual(result, AccountStatus.ACTIVE)
        self.assertEqual(mock_get.call_args.kwargs["params"], {"email": "user@mindx.edu.vn"})

    @patch("adapters.odoo_api_adapter.requests.get")
    def test_get_account_status_deactivated(self, mock_get):
        mock_get.return_value = Mock(status_code=200, json=lambda: {"status": "deactivated"})

        result = self.adapter.get_account_status(self.ticket)

        self.assertEqual(result, AccountStatus.DEACTIVATED)

    @patch("adapters.odoo_api_adapter.requests.get")
    def test_get_account_status_not_found_returns_unknown(self, mock_get):
        mock_get.return_value = Mock(status_code=404)

        result = self.adapter.get_account_status(self.ticket)

        self.assertEqual(result, AccountStatus.UNKNOWN)

    @patch("adapters.odoo_api_adapter.requests.get")
    def test_get_account_status_server_error_raises(self, mock_get):
        mock_get.return_value = Mock(status_code=500)

        with self.assertRaises(OdooAdapterError):
            self.adapter.get_account_status(self.ticket)

    @patch("adapters.odoo_api_adapter.requests.get")
    def test_get_account_status_network_error_raises(self, mock_get):
        mock_get.side_effect = requests.Timeout("timed out")

        with self.assertRaises(OdooAdapterError):
            self.adapter.get_account_status(self.ticket)

    @patch("adapters.odoo_api_adapter.requests.post")
    def test_add_note_success(self, mock_post):
        mock_post.return_value = Mock(status_code=201)

        self.adapter.add_note(self.ticket, "test note")

        self.assertEqual(mock_post.call_args.kwargs["json"], {"note": "test note"})

    @patch("adapters.odoo_api_adapter.requests.post")
    def test_add_note_server_error_raises(self, mock_post):
        mock_post.return_value = Mock(status_code=500)

        with self.assertRaises(OdooAdapterError):
            self.adapter.add_note(self.ticket, "test note")


if __name__ == "__main__":
    unittest.main()