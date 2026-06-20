import unittest

from domain.entities import Action, EmployeeStatus
from domain.decision_engine import DecisionEngine

class TestDecisionEngine(unittest.TestCase):
    def setUp(self):
        self.engine = DecisionEngine()

    def test_active_employee_gets_reactived(self):
        self.assertEqual(self.engine.decide(EmployeeStatus.ACTIVE), Action.REACTIVATE)

    def test_terminated_employee_gets_note_for_manual_review(self):
        self.assertEqual(self.engine.decide(EmployeeStatus.TERMINATED), Action.ADD_NOTE)

    def test_unknown_status_escalates_instead_of_guessing(self):
        self.assertEqual(self.engine.decide(EmployeeStatus.UNKNOWN), Action.ESCALATE)


if __name__ == "__main__":
    unittest.main()