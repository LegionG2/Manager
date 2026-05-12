import json
from pathlib import Path

from domain.record_type import RecordTypeDefinition


class RecordTypeConfigService:
    def load_record_type(self, path: str | Path) -> RecordTypeDefinition:
        with open(path, "r", encoding="utf-8") as f:
            raw_record_type = json.load(f)
        return self._record_type_from_dict(raw_record_type)

    def _record_type_from_dict(self, raw_record_type) -> RecordTypeDefinition:
        if not isinstance(raw_record_type, dict):
            raise ValueError("Record type configuration must be an object.")
        fields = raw_record_type.get("fields", [])
        if not isinstance(fields, list):
            raise ValueError("Record type fields must be a list.")
        return RecordTypeDefinition(
            id=str(raw_record_type["id"]),
            name=str(raw_record_type["name"]),
            description=str(raw_record_type.get("description", "")),
            fields=[str(field_name) for field_name in fields],
        )
