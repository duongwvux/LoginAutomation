from .entities import AccountStatus


class DeactivationCaseDetector:
    def is_deactivation_case(
            self, is_login_issue: bool, account_status: AccountStatus
    ) -> bool:
        return is_login_issue and account_status == account_status.DEACTIVATED