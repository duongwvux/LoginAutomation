import enum
from dataclasses import dataclass
from enum import Enum

@dataclass(frozen=True)
class Ticket:
    id: int
    content: str
    requester_email: str

class AccountStatus(Enum):
    ACTIVE = 'active'
    DEACTIVATED = 'deactivated'
    UNKNOWN = 'unknown'

class EmployeeStatus(Enum):
    ACTIVE = 'active'
    TERMINATED = 'inactive'
    UNKNOWN = 'unknown'

class Action(Enum):
    IGNORE = 'ignore'
    REACTIVATE = 'reactivate'
    ADD_NOTE = 'add_note'
    ESCALATE = 'escalate'