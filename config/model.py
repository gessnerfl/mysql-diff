from typing import List


class InvalidConfigurationException(Exception):
    def __init__(self, message):
        self.message = message


class DbConnectionParameters:
    def __init__(self, host: str, port: int, username: str, password: str):
        self.__check_param("host", host)
        self.__check_port("port", port)
        self.__check_param("username", username)
        self.__check_param("password", password)
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


class Exclusions:
    def __init__(self, schema_fields: List[str], table_fields: List[str], column_fields: List[str],
                 key_column_usage_fields: List[str], referential_constraint_fields: List[str],
                 index_fields: List[str], routine_fields: List[str], routine_parameter_fields: List[str],
                 view_fields: List[str]):
        self.schema_fields = schema_fields
        self.table_fields = table_fields
        self.column_fields = column_fields
        self.key_column_usage_fields = key_column_usage_fields
        self.referential_constraint_fields = referential_constraint_fields
        self.index_fields = index_fields
        self.routine_fields = routine_fields
        self.routine_parameter_fields = routine_parameter_fields
        self.view_fields = view_fields


class Configuration:
    def __init__(self, left: DbConnectionParameters, right: DbConnectionParameters, exclusions: Exclusions):
        self.left = left
        self.right = right
        self.exclusions = exclusions
