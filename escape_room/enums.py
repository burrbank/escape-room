from enum import Enum

class Status(Enum):
    SUCCESS = "success"
    FAIL = "failure"


class ItemStatus(Enum):
    NO_ITEM_GIVEN = "no item given"
    NO_ITEM_FOUND = "item not found"

