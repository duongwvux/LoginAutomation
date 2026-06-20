import unittest

from domain.entities import AccountStatus
from domain.deactivation_case_detector import DeactivationCaseDetector


class TestDeactivationCaseDetector(unittest.TestCase):
    def setUp(self):
        self.detector = DeactivationCaseDetector()

    def test_login_issue_with_deactivated_account_is_in_scope(self):
        result = self.detector.is_deactivation_case(
            is_login_issue=True, account_status=AccountStatus.DEACTIVATED
        )
        self.assertTrue(result)

    def test_login_issue_with_active_account_is_out_of_scope(self):
        # Account vẫn Active -> nhiều khả năng do sai password, không phải
        # deactivation -> KHÔNG thuộc phạm vi automation này
        result = self.detector.is_deactivation_case(
            is_login_issue=True, account_status=AccountStatus.ACTIVE
        )
        self.assertFalse(result)

    def test_non_login_issue_is_never_in_scope(self):
        # Ticket không liên quan đăng nhập -> dù account có đang deactivated
        # cũng không được tự xử lý
        result = self.detector.is_deactivation_case(
            is_login_issue=False, account_status=AccountStatus.DEACTIVATED
        )
        self.assertFalse(result)

    def test_unknown_account_status_is_out_of_scope(self):
        # Chưa xác minh được account status -> không tự đoán, phải escalate
        result = self.detector.is_deactivation_case(
            is_login_issue=True, account_status=AccountStatus.UNKNOWN
        )
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()