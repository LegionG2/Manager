import json
from pathlib import Path

from domain.field_definition import FieldDefinition, FieldOption, FieldType


class FieldConfigService:
    def load_fields(self, path: str | Path) -> list[FieldDefinition]:
        with open(path, "r", encoding="utf-8") as f:
            raw_fields = json.load(f)
        if not isinstance(raw_fields, list):
            raise ValueError("Field configuration must be a list.")
        return [self._field_from_dict(raw_field) for raw_field in raw_fields]

    def _field_from_dict(self, raw_field) -> FieldDefinition:
        if not isinstance(raw_field, dict):
            raise ValueError("Each field definition must be an object.")
        options = [
            FieldOption(value=str(raw_option["value"]), label=str(raw_option["label"]))
            for raw_option in raw_field.get("options", [])
        ]
        return FieldDefinition(
            name=str(raw_field["name"]),
            label=str(raw_field["label"]),
            field_type=FieldType(raw_field.get("field_type", FieldType.TEXT.value)),
            required=bool(raw_field.get("required", False)),
            visible=bool(raw_field.get("visible", True)),
            default=raw_field.get("default"),
            options=options,
        )
