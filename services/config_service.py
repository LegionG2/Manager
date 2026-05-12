from dataclasses import dataclass
from enum import Enum
import json
from pathlib import Path
from typing import Any

from domain.app_config import AppConfig
from domain.app_section import AppSectionDefinition
from domain.field_definition import FieldDefinition, FieldOption
from domain.record_type import RecordTypeDefinition
from services.app_config_service import AppConfigService
from services.field_config_service import FieldConfigService
from services.record_type_config_service import RecordTypeConfigService
from services.section_config_service import SectionConfigService


@dataclass(frozen=True)
class ManagerConfig:
    app_config: AppConfig
    field_definitions: list[FieldDefinition]
    record_type: RecordTypeDefinition
    sections: list[AppSectionDefinition]


class ConfigService:
    def __init__(self, config_dir: str | Path = "config"):
        self.config_dir = Path(config_dir)
        self.app_config_service = AppConfigService()
        self.field_config_service = FieldConfigService()
        self.record_type_config_service = RecordTypeConfigService()
        self.section_config_service = SectionConfigService()

    def load_app_config(self) -> AppConfig:
        return self.app_config_service.load_config(self.config_dir / "app_config.json")

    def load_field_definitions(self) -> list[FieldDefinition]:
        return self.field_config_service.load_fields(self.config_dir / "default_record_fields.json")

    def load_record_type(self) -> RecordTypeDefinition:
        return self.record_type_config_service.load_record_type(self.config_dir / "default_record_type.json")

    def load_sections(self) -> list[AppSectionDefinition]:
        return self.section_config_service.load_sections(self.config_dir / "default_sections.json")

    def load_all(self) -> ManagerConfig:
        return ManagerConfig(
            app_config=self.load_app_config(),
            field_definitions=self.load_field_definitions(),
            record_type=self.load_record_type(),
            sections=self.load_sections(),
        )

    def save_app_config(self, app_config: AppConfig) -> None:
        self._write_json(self.config_dir / "app_config.json", app_config)

    def save_field_definitions(self, field_definitions: list[FieldDefinition]) -> None:
        self._write_json(self.config_dir / "default_record_fields.json", field_definitions)

    def save_record_type(self, record_type: RecordTypeDefinition) -> None:
        self._write_json(self.config_dir / "default_record_type.json", record_type)

    def save_sections(self, sections: list[AppSectionDefinition]) -> None:
        self._write_json(self.config_dir / "default_sections.json", sections)

    def save_all(self, config: ManagerConfig) -> None:
        self.save_app_config(config.app_config)
        self.save_field_definitions(config.field_definitions)
        self.save_record_type(config.record_type)
        self.save_sections(config.sections)

    def _write_json(self, path: Path, value) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self._to_json_value(value), f, ensure_ascii=False, indent=2)
            f.write("\n")

    def _to_json_value(self, value) -> Any:
        if isinstance(value, FieldDefinition):
            raw_field = {
                "name": value.name,
                "label": value.label,
                "field_type": self._to_json_value(value.field_type),
                "required": value.required,
                "default": self._to_json_value(value.default),
            }
            if value.options:
                raw_field["options"] = self._to_json_value(value.options)
            return raw_field
        if isinstance(value, FieldOption):
            return {
                "value": value.value,
                "label": value.label,
            }
        if isinstance(value, AppSectionDefinition):
            raw_section = {
                "id": value.id,
                "name": value.name,
                "type": value.type,
            }
            if value.record_type_id is not None:
                raw_section["record_type_id"] = value.record_type_id
            raw_section["visible"] = value.visible
            raw_section["order"] = value.order
            return raw_section
        if isinstance(value, Enum):
            return value.value
        if hasattr(value, "__dataclass_fields__"):
            return {
                field_name: self._to_json_value(getattr(value, field_name))
                for field_name in value.__dataclass_fields__
            }
        if isinstance(value, list):
            return [self._to_json_value(item) for item in value]
        if isinstance(value, dict):
            return {str(key): self._to_json_value(item) for key, item in value.items()}
        return value
