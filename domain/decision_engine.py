from .entities import Action, EmployeeStatus

_DECISION_BY_STATUS = {
    EmployeeStatus.ACTIVE: Action.REACTIVATE,
    EmployeeStatus.TERMINATED: Action.ADD_NOTE,
    EmployeeStatus.UNKNOWN: Action.ESCALATE,
}

class DecisionEngine:
    def decide(self, status: EmployeeStatus) -> Action:
        return _DECISION_BY_STATUS.get(status, Action.ESCALATE)