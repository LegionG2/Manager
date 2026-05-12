from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class RecordField:
    name: str
    label: str
    field_type: str = "text"
    required: bool = False
    default: Any = None


@dataclass(frozen=True)
class RecordStatus:
    name: str
    label: str
    is_final: bool = False


@dataclass
class RecordType:
    name: str
    label: str
    fields: list[RecordField] = field(default_factory=list)
    statuses: list[RecordStatus] = field(default_factory=list)


@dataclass
class Record:
    record_type: str
    values: dict[str, Any] = field(default_factory=dict)
    status: str | None = None
    record_id: int | None = None
