from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class FieldType(str, Enum):
    TEXT = "text"
    NUMBER = "number"
    DATE = "date"
    BOOLEAN = "boolean"
    SELECT = "select"


@dataclass(frozen=True)
class FieldOption:
    value: str
    label: str


@dataclass(frozen=True)
class FieldDefinition:
    name: str
    label: str
    field_type: FieldType = FieldType.TEXT
    required: bool = False
    default: Any = None
    options: list[FieldOption] = field(default_factory=list)
