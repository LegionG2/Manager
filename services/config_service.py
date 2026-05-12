from dataclasses import dataclass
from pathlib import Path

from domain.app_config import AppConfig
from domain.app_section import AppSectionDefinition
from domain.field_definition import FieldDefinition
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
