import json
from pathlib import Path

from domain.app_section import AppSectionDefinition


class SectionConfigService:
    def load_sections(self, path: str | Path) -> list[AppSectionDefinition]:
        with open(path, "r", encoding="utf-8") as f:
            raw_sections = json.load(f)
        if not isinstance(raw_sections, list):
            raise ValueError("Section configuration must be a list.")
        return [self._section_from_dict(raw_section) for raw_section in raw_sections]

    def _section_from_dict(self, raw_section) -> AppSectionDefinition:
        if not isinstance(raw_section, dict):
            raise ValueError("Each section definition must be an object.")
        record_type_id = raw_section.get("record_type_id")
        return AppSectionDefinition(
            id=str(raw_section["id"]),
            name=str(raw_section["name"]),
            type=str(raw_section["type"]),
            record_type_id=None if record_type_id is None else str(record_type_id),
            visible=bool(raw_section.get("visible", True)),
            order=int(raw_section.get("order", 0)),
        )
