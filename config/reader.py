from .model import *
import yaml


def __get_exclusion(exclusions, field: str) -> List[str]:
    if field in exclusions:
        return exclusions[field]
    return []


def __parse_schema_mappings(d) -> SchemaMappings:
    if 'schema_mappings' in d:
        return SchemaMappings(d["schema_mappings"])
    return SchemaMappings({})


def __parse_exclusions(d) -> Exclusions:
    if 'exclusions' in d:
        exclusions = d['exclusions']
        schema_fields = __get_exclusion(exclusions, 'schema_fields')
        table_fields = __get_exclusion(exclusions, 'table_fields')
        column_fields = __get_exclusion(exclusions, 'column_fields')
        key_column_usage_fields = __get_exclusion(exclusions, 'key_column_usage_fields')
        referential_constraint_fields = __get_exclusion(exclusions, 'referential_constraint_fields')
        index_fields = __get_exclusion(exclusions, 'index_fields')
        routine_fields = __get_exclusion(exclusions, 'routine_fields')
        routine_parameter_fields = __get_exclusion(exclusions, 'routine_parameter_fields')
        view_fields = __get_exclusion(exclusions, 'view_fields')
        return Exclusions(schema_fields, table_fields, column_fields, key_column_usage_fields,
                          referential_constraint_fields, index_fields, routine_fields, routine_parameter_fields,
                          view_fields)
    return Exclusions([], [], [], [], [], [], [], [], [])


def read_configuration(filepath: str) -> Configuration:
    with open(filepath, 'r') as stream:
        d = yaml.safe_load(stream)
        databases = d['databases']
        left = databases['left']
        right = databases['right']
        left_param = DbConnectionParameters(left["name"], left["hostname"], left["port"], left["username"],
                                            left["password"])
        right_param = DbConnectionParameters(right["name"], right["hostname"], right["port"], right["username"],
                                             right["password"])

        exclusions = __parse_exclusions(d)
        schema_mappings = __parse_schema_mappings(d)

        return Configuration(left_param, right_param, exclusions, schema_mappings)
