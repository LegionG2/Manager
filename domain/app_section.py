from dataclasses import dataclass


@dataclass(frozen=True)
class AppSectionDefinition:
    id: str
    name: str
    type: str
    visible: bool = True
    order: int = 0
    record_type_id: str | None = None
