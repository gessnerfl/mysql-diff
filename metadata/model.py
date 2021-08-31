from typing import List
import json


class RoutineParameter:
    def __init__(self, parameter_name: str, ordinal_position: str, parameter_mode: str, data_type: str,
                 character_maximum_length: str, character_octet_length: str, numeric_precision: str, numeric_scale: str,
                 datetime_precision: str, character_set_name: str, collation_name: str, dtd_identifier: str):
        self.parameter_name = parameter_name
        self.ordinal_position = ordinal_position
        self.parameter_mode = parameter_mode
        self.data_type = data_type
        self.character_maximum_length = character_maximum_length
        self.character_octet_length = character_octet_length
        self.numeric_precision = numeric_precision
        self.numeric_scale = numeric_scale
        self.datetime_precision = datetime_precision
        self.character_set_name = character_set_name
        self.collation_name = collation_name
        self.dtd_identifier = dtd_identifier

    def to_dict(self):
        return self.__dict__


class RoutineMetaData:
    def __init__(self, schema: str, name: str, routine_type: str, data_type: str, character_max_length: str,
                 character_octet_length: str, numeric_precision: str, numeric_scale: str, datetime_precision: str,
                 character_set_name: str, collation_name: str, dtd_identifier: str, routine_body: str,
                 routine_definition: str, external_name: str, external_language: str, parameter_style: str,
                 is_deterministic: str, sql_data_access: str, sql_path: str, security_type: str, sql_mode: str,
                 routine_comment: str, definer: str, character_set_client: str, collation_connection: str,
                 database_collation: str):
        self.schema = schema
        self.name = name
        self.routine_type = routine_type
        self.data_type = data_type
        self.character_max_length = character_max_length
        self.character_octet_length = character_octet_length
        self.numeric_precision = numeric_precision
        self.numeric_scale = numeric_scale
        self.datetime_precision = datetime_precision
        self.character_set_name = character_set_name
        self.collation_name = collation_name
        self.dtd_identifier = dtd_identifier
        self.routine_body = routine_body
        self.routine_definition = routine_definition
        self.external_name = external_name
        self.external_language = external_language
        self.parameter_style = parameter_style
        self.is_deterministic = is_deterministic
        self.sql_data_access = sql_data_access
        self.sql_path = sql_path
        self.security_type = security_type
        self.sql_mode = sql_mode
        self.routine_comment = routine_comment
        self.definer = definer
        self.character_set_client = character_set_client
        self.collation_connection = collation_connection
        self.database_collation = database_collation
        self.parameters = []

    def to_dict(self):
        return self.__dict__


class ViewMetaData:
    def __init__(self, schema: str, name: str, definition: str, check_option: str, is_updatable: str, definer: str,
                 security_type: str, character_set_client: str, collation_connection: str):
        self.schema = schema
        self.name = name
        self.definition = definition
        self.check_option = check_option
        self.is_updatable = is_updatable
        self.definer = definer
        self.security_type = security_type
        self.character_set_client = character_set_client
        self.collation_connection = collation_connection

    def to_dict(self):
        return self.__dict__


class KeyColumnUsage:
    def __init__(self, column_name: str, ordinal_position: str, position_in_unique_constraint: str,
                 referenced_table_schema: str, referenced_table_name: str, referenced_column_name: str):
        self.column_name = column_name
        self.ordinal_position = ordinal_position
        self.position_in_unique_constraint = position_in_unique_constraint
        self.referenced_table_schema = referenced_table_schema
        self.referenced_table_name = referenced_table_name
        self.referenced_column_name = referenced_column_name

    def to_dict(self):
        return self.__dict__


class ReferentialConstraint:
    def __init__(self, constraint_name: str, unique_constraint_name: str, match_option: str,
                 update_rule: str, delete_rule: str, referenced_table_name: str):
        self.constraint_name = constraint_name
        self.unique_constraint_name = unique_constraint_name
        self.match_option = match_option
        self.update_rule = update_rule
        self.delete_rule = delete_rule
        self.referenced_table_name = referenced_table_name

    def to_dict(self):
        return self.__dict__


class Index:
    def __init__(self, index_name: str, non_unique: str, seq_in_index: str, column_name: str, collation: str,
                 cardinality: str, sub_part: str, packed: str, nullable: str, index_type: str, comment: str,
                 index_comment: str):
        self.index_name = index_name
        self.non_unique = non_unique
        self.seq_in_index = seq_in_index
        self.column_name = column_name
        self.collation = collation
        self.cardinality = cardinality
        self.sub_part = sub_part
        self.packed = packed
        self.nullable = nullable
        self.index_type = index_type
        self.comment = comment
        self.index_comment = index_comment

    def to_dict(self):
        return self.__dict__


class ColumnMetaData:
    def __init__(self, column_name: str, ordinal_position: str, column_default: str, is_nullable: str, data_type: str,
                 character_maximum_length: str, character_octet_length: str, numeric_precision: str, numeric_scale: str,
                 datetime_precision: str, character_set_name: str, collation_name: str, column_type: str,
                 column_key: str, extra: str, privileges: str, column_comment: str, generation_expression: str):
        self.column_name = column_name
        self.ordinal_position = ordinal_position
        self.column_default = column_default
        self.is_nullable = is_nullable
        self.data_type = data_type
        self.character_maximum_length = character_maximum_length
        self.character_octet_length = character_octet_length
        self.numeric_precision = numeric_precision
        self.numeric_scale = numeric_scale
        self.datetime_precision = datetime_precision
        self.character_set_name = character_set_name
        self.collation_name = collation_name
        self.column_type = column_type
        self.column_key = column_key
        self.extra = extra
        self.privileges = privileges
        self.column_comment = column_comment
        self.generation_expression = generation_expression

    def to_dict(self):
        return self.__dict__


class TableMetaData:
    def __init__(self, schema: str, name: str, engine: str, version: str, row_format: str, auto_increment: str,
                 table_collation: str, create_option: str, table_comment: str):
        self.schema = schema
        self.name = name
        self.engine = engine
        self.version = version
        self.row_format = row_format
        self.auto_increment = auto_increment
        self.table_collation = table_collation
        self.create_option = create_option
        self.table_comment = table_comment
        self.columns = []
        self.key_column_usages = []
        self.referential_constraints = []
        self.indices = []

    def to_dict(self):
        return self.__dict__


class SchemaMetaData:
    def __init__(self, name: str, default_character_set: str, default_collation: str):
        self.name = name
        self.default_character_set = default_character_set
        self.default_collation = default_collation

    def to_dict(self):
        return self.__dict__


def to_json(o):
    return o.to_dict()


class MetaDataCatalog:
    def __init__(self, schemas: List[SchemaMetaData], tables: List[TableMetaData], views: List[ViewMetaData],
                 routines: List[RoutineMetaData]):
        self.schemas = schemas
        self.tables = tables
        self.views = views
        self.routines = routines

    def __str__(self) -> str:
        return json.dumps(self.__dict__, indent=3, default=to_json)

    def to_dict(self):
        return self.__dict__
