from typing import List, Dict


class InvalidConfigurationException(Exception):
    def __init__(self, message):
        self.message = message


class DbConnectionParameters:
    def __init__(self, name: str, host: str, port: int, username: str, password: str):
        self.__check_param("name", name)
        self.__check_param("host", host)
        self.__check_port("port", port)
        self.__check_param("username", username)
        self.__check_param("password", password)
        self.name = name
        self.host = host
        self.port = port
        self.username = username
        self.password = password

    def __check_param(self, name: str, value: str):
        if not value or value.isspace():
            raise InvalidConfigurationException(
                "Required connection parameter {} is missing".format(name))

    def __check_port(self, name: str, value: int):
        if value <= 0:
            raise InvalidConfigurationException(
                "Required connection parameter port is not valid or missing".format(name))


class FieldExclusion:
    def __init__(self, field: str, left_value, right_value):
        self.field = field
        self.left_value = left_value
        self.right_value = right_value

    def is_exclude_always(self) -> bool:
        return self.left_value is None


class Exclusions:
    def __init__(self, schema_fields: List[FieldExclusion], table_fields: List[FieldExclusion],
                 column_fields: List[FieldExclusion], key_column_usage_fields: List[FieldExclusion],
                 referential_constraint_fields: List[FieldExclusion], index_fields: List[FieldExclusion],
                 routine_fields: List[FieldExclusion], routine_parameter_fields: List[FieldExclusion],
                 view_fields: List[FieldExclusion]):
        self.schema_fields = schema_fields
        self.table_fields = table_fields
        self.column_fields = column_fields
        self.key_column_usage_fields = key_column_usage_fields
        self.referential_constraint_fields = referential_constraint_fields
        self.index_fields = index_fields
        self.routine_fields = routine_fields
        self.routine_parameter_fields = routine_parameter_fields
        self.view_fields = view_fields


class SchemaMappings:
    def __init__(self, left_to_right_mappings: Dict[str, str]):
        self.left_to_right_mappings = left_to_right_mappings
        self.right_to_left_mappings = {left_to_right_mappings[k]: k for k in left_to_right_mappings}


class Configuration:
    def __init__(self, left: DbConnectionParameters, right: DbConnectionParameters, exclusions: Exclusions,
                 schema_mappings: SchemaMappings):
        self.left = left
        self.right = right
        self.exclusions = exclusions
        self.schema_mappings = schema_mappings
