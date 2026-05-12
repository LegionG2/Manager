from dataclasses import dataclass, field


@dataclass(frozen=True)
class AppSection:
    id: str
    label: str
    enabled: bool = True


@dataclass(frozen=True)
class AppConfig:
    app_name: str
    active_record_type_id: str
    sections: list[AppSection] = field(default_factory=list)
