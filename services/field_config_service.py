import json
from pathlib import Path

from domain.field_definition import FieldDefinition, FieldOption, FieldType


class FieldConfigService:
    def load_fields(self, path: str | Path) -> list[FieldDefinition]:
        with open(path, "r", encoding="utf-8") as f:
            raw_fields = json.load(f)
        if not isinstance(raw_fields, list):
            raise ValueError("Field configuration must be a list.")
        return [self._field_from_dict(raw_field, index) for index, raw_field in enumerate(raw_fields)]

    def _field_from_dict(self, raw_field, index: int = 0) -> FieldDefinition:
        if not isinstance(raw_field, dict):
            raise ValueError("Each field definition must be an object.")
        legacy_visible = bool(raw_field.get("visible", True))
        try:
            order = int(raw_field.get("order", index))
        except (TypeError, ValueError):
            order = index
        options = [
            FieldOption(value=str(raw_option["value"]), label=str(raw_option["label"]))
            for raw_option in raw_field.get("options", [])
        ]
        return FieldDefinition(
            name=str(raw_field["name"]),
            label=str(raw_field["label"]),
            group_name=str(raw_field.get("group_name") or raw_field.get("group_id") or "Dane podstawowe"),
            field_type=FieldType(raw_field.get("field_type", FieldType.TEXT.value)),
            required=bool(raw_field.get("required", False)),
            visible=legacy_visible,
            visible_in_form=bool(raw_field.get("visible_in_form", legacy_visible)),
            visible_in_table=bool(raw_field.get("visible_in_table", legacy_visible)),
            summarize=bool(raw_field.get("summarize", False)),
            formula=str(raw_field.get("formula", "")),
            module_type=str(raw_field.get("module_type", "")),
            module_label=str(raw_field.get("module_label", "")),
            order=order,
            default=raw_field.get("default"),
            options=options,
        )
