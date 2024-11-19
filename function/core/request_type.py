from enum import Enum


class RequestType(Enum):
    SCHEDULE = "schedule"
    ADD = "add"
    REVOKE = "revoke"
