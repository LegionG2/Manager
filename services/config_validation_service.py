from dataclasses import dataclass, field

from domain.app_config import AppConfig
from domain.app_section import AppSectionDefinition
from domain.field_definition import FieldDefinition, FieldType
from domain.record_type import RecordTypeDefinition


@dataclass(frozen=True)
class ConfigValidationResult:
    errors: list[str] = field(default_factory=list)

    @property
    def is_valid(self) -> bool:
        return not self.errors


class ConfigValidationService:
    def validate_app_config(self, app_config: AppConfig) -> ConfigValidationResult:
        errors = []
        if not self._has_text(app_config.app_name):
            errors.append("app_config.app_name is required.")
        if not self._has_text(app_config.active_record_type_id):
            errors.append("app_config.active_record_type_id is required.")
        if not isinstance(app_config.sections, list):
            errors.append("app_config.sections must be a list.")
        else:
            for index, section in enumerate(app_config.sections):
                if not self._has_text(section.id):
                    errors.append(f"app_config.sections[{index}].id is required.")
                if not self._has_text(section.label):
                    errors.append(f"app_config.sections[{index}].label is required.")
                if not isinstance(section.enabled, bool):
                    errors.append(f"app_config.sections[{index}].enabled must be boolean.")
        return ConfigValidationResult(errors)

    def validate_field_definitions(self, field_definitions: list[FieldDefinition]) -> ConfigValidationResult:
        errors = []
        if not isinstance(field_definitions, list):
            return ConfigValidationResult(["field_definitions must be a list."])
        seen_names = set()
        allowed_types = {field_type.value for field_type in FieldType}
        for index, field_definition in enumerate(field_definitions):
            if not self._has_text(field_definition.name):
                errors.append(f"field_definitions[{index}].name is required.")
            elif field_definition.name in seen_names:
                errors.append(f"field_definitions[{index}].name is duplicated.")
            else:
                seen_names.add(field_definition.name)
            if not self._has_text(field_definition.label):
                errors.append(f"field_definitions[{index}].label is required.")
            if not self._has_text(field_definition.group_name):
                errors.append(f"field_definitions[{index}].group_name is required.")
            field_type = field_definition.field_type.value if isinstance(field_definition.field_type, FieldType) else field_definition.field_type
            if field_type not in allowed_types:
                errors.append(f"field_definitions[{index}].field_type is invalid.")
            if not isinstance(field_definition.required, bool):
                errors.append(f"field_definitions[{index}].required must be boolean.")
            if not isinstance(field_definition.visible, bool):
                errors.append(f"field_definitions[{index}].visible must be boolean.")
            if not isinstance(field_definition.options, list):
                errors.append(f"field_definitions[{index}].options must be a list.")
            else:
                for option_index, option in enumerate(field_definition.options):
                    if not self._has_text(option.value):
                        errors.append(f"field_definitions[{index}].options[{option_index}].value is required.")
                    if not self._has_text(option.label):
                        errors.append(f"field_definitions[{index}].options[{option_index}].label is required.")
        return ConfigValidationResult(errors)

    def validate_record_type(self, record_type: RecordTypeDefinition) -> ConfigValidationResult:
        errors = []
        if not self._has_text(record_type.id):
            errors.append("record_type.id is required.")
        if not self._has_text(record_type.name):
            errors.append("record_type.name is required.")
        if not isinstance(record_type.fields, list):
            errors.append("record_type.fields must be a list.")
        else:
            for index, field_name in enumerate(record_type.fields):
                if not self._has_text(field_name):
                    errors.append(f"record_type.fields[{index}] must not be empty.")
        return ConfigValidationResult(errors)

    def validate_sections(self, sections: list[AppSectionDefinition]) -> ConfigValidationResult:
        errors = []
        if not isinstance(sections, list):
            return ConfigValidationResult(["sections must be a list."])
        seen_ids = set()
        for index, section in enumerate(sections):
            if not self._has_text(section.id):
                errors.append(f"sections[{index}].id is required.")
            elif section.id in seen_ids:
                errors.append(f"sections[{index}].id is duplicated.")
            else:
                seen_ids.add(section.id)
            if not self._has_text(section.name):
                errors.append(f"sections[{index}].name is required.")
            if not self._has_text(section.type):
                errors.append(f"sections[{index}].type is required.")
            if section.record_type_id is not None and not self._has_text(section.record_type_id):
                errors.append(f"sections[{index}].record_type_id must not be empty.")
            if not isinstance(section.visible, bool):
                errors.append(f"sections[{index}].visible must be boolean.")
            if not isinstance(section.order, int):
                errors.append(f"sections[{index}].order must be integer.")
        return ConfigValidationResult(errors)

    def validate_all(
        self,
        app_config: AppConfig,
        field_definitions: list[FieldDefinition],
        record_type: RecordTypeDefinition,
        sections: list[AppSectionDefinition],
    ) -> ConfigValidationResult:
        errors = []
        errors.extend(self.validate_app_config(app_config).errors)
        errors.extend(self.validate_field_definitions(field_definitions).errors)
        errors.extend(self.validate_record_type(record_type).errors)
        errors.extend(self.validate_sections(sections).errors)
        return ConfigValidationResult(errors)

    def _has_text(self, value) -> bool:
        return isinstance(value, str) and bool(value.strip())
