import unittest
from unittest.mock import Mock, patch

import requests

from adapters.lms_api_adapter import LMSAdapterError, LMSAPIAdapter
from domain.entities import Ticket


class TestLMSAPIAdapter(unittest.TestCase):
    def setUp(self):
        self.adapter = LMSAPIAdapter(base_url="https://lms.mindx.edu.vn", api_key="fake-key")
        self.ticket = Ticket(id="T-202", content="...", requester_email="user@mindx.edu.vn")

    @patch("adapters.lms_api_adapter.requests.post")
    def test_reactivate_success(self, mock_post):
        mock_post.return_value = Mock(status_code=200)

        self.adapter.reactivate(self.ticket)  # không raise = pass

        self.assertEqual(mock_post.call_args.kwargs["json"], {"email": "user@mindx.edu.vn"})

    @patch("adapters.lms_api_adapter.requests.post")
    def test_reactivate_account_not_found_raises(self, mock_post):
        mock_post.return_value = Mock(status_code=404)

        with self.assertRaises(LMSAdapterError):
            self.adapter.reactivate(self.ticket)

    @patch("adapters.lms_api_adapter.requests.post")
    def test_reactivate_server_error_raises(self, mock_post):
        mock_post.return_value = Mock(status_code=500)

        with self.assertRaises(LMSAdapterError):
            self.adapter.reactivate(self.ticket)

    @patch("adapters.lms_api_adapter.requests.post")
    def test_reactivate_network_error_raises(self, mock_post):
        mock_post.side_effect = requests.Timeout("timed out")

        with self.assertRaises(LMSAdapterError):
            self.adapter.reactivate(self.ticket)


if __name__ == "__main__":
    unittest.main()