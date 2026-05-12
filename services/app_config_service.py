import json
from pathlib import Path

from domain.app_config import AppConfig, AppSection


class AppConfigService:
    def load_config(self, path: str | Path) -> AppConfig:
        with open(path, "r", encoding="utf-8") as f:
            raw_config = json.load(f)
        return self._config_from_dict(raw_config)

    def _config_from_dict(self, raw_config) -> AppConfig:
        if not isinstance(raw_config, dict):
            raise ValueError("Application configuration must be an object.")
        sections = raw_config.get("sections", [])
        if not isinstance(sections, list):
            raise ValueError("Application configuration sections must be a list.")
        return AppConfig(
            app_name=str(raw_config["app_name"]),
            active_record_type_id=str(raw_config["active_record_type_id"]),
            sections=[self._section_from_dict(raw_section) for raw_section in sections],
        )

    def _section_from_dict(self, raw_section) -> AppSection:
        if not isinstance(raw_section, dict):
            raise ValueError("Application section must be an object.")
        return AppSection(
            id=str(raw_section["id"]),
            label=str(raw_section["label"]),
            enabled=bool(raw_section.get("enabled", True)),
        )
