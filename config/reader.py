from .model import *
import yaml


def __map_exclusion(exclusion) -> FieldExclusion:
    field = exclusion['field']
    left_value = exclusion['left_value'] if 'left_value' in exclusion else None
    right_value = exclusion['right_value'] if 'right_value' in exclusion else None
    return FieldExclusion(field, left_value, right_value)


def __get_exclusions_for_asset_type(all_exclusions, asset_type: str) -> List[FieldExclusion]:
    if asset_type in all_exclusions:
        asset_exclusions = all_exclusions[asset_type]
        return [__map_exclusion(e) for e in asset_exclusions]
    return []


def __parse_schema_mappings(d) -> SchemaMappings:
    if 'schema_mappings' in d:
        return SchemaMappings(d["schema_mappings"])
    return SchemaMappings({})


def __parse_exclusions(d) -> Exclusions:
    if 'exclusions' in d:
        exclusions = d['exclusions']
        schema_fields = __get_exclusions_for_asset_type(exclusions, 'schema_fields')
        table_fields = __get_exclusions_for_asset_type(exclusions, 'table_fields')
        column_fields = __get_exclusions_for_asset_type(exclusions, 'column_fields')
        key_column_usage_fields = __get_exclusions_for_asset_type(exclusions, 'key_column_usage_fields')
        referential_constraint_fields = __get_exclusions_for_asset_type(exclusions, 'referential_constraint_fields')
        index_fields = __get_exclusions_for_asset_type(exclusions, 'index_fields')
        routine_fields = __get_exclusions_for_asset_type(exclusions, 'routine_fields')
        routine_parameter_fields = __get_exclusions_for_asset_type(exclusions, 'routine_parameter_fields')
        view_fields = __get_exclusions_for_asset_type(exclusions, 'view_fields')
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
