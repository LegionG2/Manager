from dataclasses import dataclass, field


@dataclass(frozen=True)
class RecordTypeDefinition:
    id: str
    name: str
    fields: list[str] = field(default_factory=list)
    description: str = ""
