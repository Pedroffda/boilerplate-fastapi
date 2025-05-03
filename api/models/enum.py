from enum import Enum

class PolicyEffect(str, Enum):
    ALLOW = "Allow"
    DENY = "Deny"