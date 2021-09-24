from deepdiff import DeepDiff
from .model import *
from typing import Dict, Any, TypeVar, Callable, NoReturn, List
from metadata.model import Schema, Table, View, Routine, RoutineParameter, ColumnMetaData, KeyColumnUsage, \
    ReferentialConstraint, Index
from .model import Diff
from config.model import Exclusions, SchemaMappings, FieldExclusion

ASSET_TYPE_SCHEMA = "Schema"
ASSET_TYPE_TABLE = "Table"
ASSET_TYPE_COLUMN = "Column"
ASSET_TYPE_KEY_COLUMN_USAGE = "Key Column Usage"
ASSET_TYPE_REFERENTIAL_CONSTRAINT = "Referential Constraint"
ASSET_TYPE_INDEX = "Index"
ASSET_TYPE_ROUTINE = "Routine"
ASSET_TYPE_ROUTINE_PARAMETER = "Routine-Parameter"
ASSET_TYPE_VIEW = "View"

ASSET_TYPE_VIEW = "View"

CHANGE_VALUE_FIELD = "values_changed"

T = TypeVar('T')


def schema_name(schema: Schema) -> str: return schema.meta_data.name


def table_name(table: Table) -> str:
    return "{} - {}".format(table.meta_data.schema, table.meta_data.name)


def column_name(column: ColumnMetaData) -> str:
    return "{} - {} - {}".format(column.schema, column.table_name, column.column_name)


def key_column_usage_name(k: KeyColumnUsage) -> str:
    return "{} - {} - {}".format(k.schema, k.table_name, k.column_name)


def referential_constraint_name(c: ReferentialConstraint) -> str:
    return "{} - {} - {}".format(c.schema, c.table_name, c.constraint_name)


def index_name(c: Index) -> str:
    return "{} - {} - {}".format(c.schema, c.table_name, c.index_name)


def view_name(view: View) -> str:
    return "{} - {}".format(view.meta_data.schema, view.meta_data.name)


def routine_name(routine: Routine) -> str:
    return "{} - {}".format(routine.meta_data.schema, routine.meta_data.name)


def routine_param_name(param: RoutineParameter) -> str:
    return "{} - {} - {}".format(param.schema, param.routine_name, param.parameter_name)


def map_excluded_fields(excluded_fields: List[FieldExclusion]) -> List[str]:
    if excluded_fields is None:
        return []
    return [format_excluded_field(e.field) for e in filter(lambda e: e.is_exclude_always(), excluded_fields)]


def format_excluded_field(name):
    return "root['{}']".format(name)


def filter_value_exclusions_from_diff(diff_dict, field_exclusions: List[FieldExclusion]):
    result = diff_dict
    for f in filter(lambda e: not e.is_exclude_always(), field_exclusions):
        key = format_excluded_field(f.field)
        if CHANGE_VALUE_FIELD in result and key in result[CHANGE_VALUE_FIELD] and \
                "old_value" in result[CHANGE_VALUE_FIELD][key] and "new_value" in result[CHANGE_VALUE_FIELD][key] and \
                result[CHANGE_VALUE_FIELD][key]["old_value"] == f.left_value and \
                result[CHANGE_VALUE_FIELD][key]["new_value"] == f.right_value:
            del result[CHANGE_VALUE_FIELD][key]

    if CHANGE_VALUE_FIELD in result and len(result[CHANGE_VALUE_FIELD]) == 0:
        del result[CHANGE_VALUE_FIELD]

    return result


class SchemaDiff:
    def __init__(self, left: Dict[str, Schema], right: Dict[str, Schema], exclusions: Exclusions,
                 schema_mappings: SchemaMappings):
        self.left = left
        self.right = right
        self.database_diff = DatabaseDiffs()
        self.exclusions = exclusions
        self.schema_mappings = schema_mappings

    def diff(self) -> DatabaseDiffs:
        self.__check_diff_of_assets(ASSET_TYPE_SCHEMA, schema_name, self.left, self.right, self.__process_schema)
        return self.database_diff

    def __process_schema(self, left: Schema, right: Schema):
        asset_name = schema_name(left)
        self.__check_meta_data_diff(ASSET_TYPE_SCHEMA, asset_name, left.meta_data.to_dict(), right.meta_data.to_dict(),
                                    self.exclusions.schema_fields)

        self.__check_diff_of_assets(ASSET_TYPE_TABLE, table_name, left.tables, right.tables, self.__process_table)
        self.__check_diff_of_assets(ASSET_TYPE_VIEW, view_name, left.views, right.views, self.__process_view)
        self.__check_diff_of_assets(ASSET_TYPE_ROUTINE, routine_name, left.routines, right.routines,
                                    self.__process_routine)

    def __process_table(self, left: Table, right: Table):
        asset_name = table_name(left)
        self.__check_meta_data_diff(ASSET_TYPE_TABLE, asset_name, left.meta_data.to_dict(), right.meta_data.to_dict(),
                                    self.exclusions.table_fields)

        self.__check_diff_of_leaf_assets(ASSET_TYPE_COLUMN, column_name, left.columns, right.columns,
                                         self.exclusions.column_fields)
        self.__check_diff_of_leaf_assets(ASSET_TYPE_KEY_COLUMN_USAGE, key_column_usage_name, left.key_column_usages,
                                         right.key_column_usages, self.exclusions.key_column_usage_fields)
        self.__check_diff_of_leaf_assets(ASSET_TYPE_REFERENTIAL_CONSTRAINT, referential_constraint_name,
                                         left.referential_constraints, right.referential_constraints,
                                         self.exclusions.referential_constraint_fields)
        self.__check_diff_of_leaf_assets(ASSET_TYPE_INDEX, index_name, left.indices, right.indices,
                                         self.exclusions.index_fields)

    def __process_view(self, left: View, right: View):
        asset_name = view_name(left)
        self.__check_meta_data_diff(ASSET_TYPE_VIEW, asset_name, left.meta_data.to_dict(), right.meta_data.to_dict(),
                                    self.exclusions.view_fields)

    def __process_routine(self, left: Routine, right: Routine):
        asset_name = routine_name(left)
        self.__check_meta_data_diff(ASSET_TYPE_ROUTINE, asset_name, left.meta_data.to_dict(), right.meta_data.to_dict(),
                                    self.exclusions.routine_fields)

        self.__check_diff_of_leaf_assets(ASSET_TYPE_ROUTINE_PARAMETER, routine_param_name,
                                         left.parameters, right.parameters, self.exclusions.routine_parameter_fields)

    def __check_diff_of_leaf_assets(self, asset_type: str, asset_name_fn: Callable[[T], str], left: Dict[str, T],
                                    right: Dict[str, T], field_exclusions: List[FieldExclusion]):
        self.__check_diff_of_assets(asset_type, asset_name_fn, left, right,
                                    lambda l, r: self.__check_meta_data_diff(asset_type,
                                                                             asset_name_fn(l),
                                                                             l.to_dict(),
                                                                             r.to_dict(),
                                                                             field_exclusions))

    def __check_diff_of_assets(self, asset_type: str, asset_name_fn: Callable[[T], str], left: Dict[str, T],
                               right: Dict[str, T], comparator: Callable[[T, T], NoReturn]):
        for k in left:
            right_key = self.__get_right_asset_name(asset_type, k)
            if right_key in right:
                comparator(left[k], right[right_key])
            else:
                asset_name = asset_name_fn(left[k])
                diff = Diff(asset_name, asset_type, "{} is not present on right side".format(k))
                self.database_diff.append_diff(diff)

        for k in right:
            left_key = self.__get_left_asset_name(asset_type, k)
            if left_key not in left:
                asset_name = asset_name_fn(right[k])
                diff = Diff(asset_name, asset_type, "{} is not present on left side".format(k))
                self.database_diff.append_diff(diff)

    def __get_right_asset_name(self, asset_type: str, left_key: str):
        if asset_type == ASSET_TYPE_SCHEMA:
            if left_key in self.schema_mappings.left_to_right_mappings:
                return self.schema_mappings.left_to_right_mappings[left_key]
        return left_key

    def __get_left_asset_name(self, asset_type: str, right_key: str):
        if asset_type == ASSET_TYPE_SCHEMA:
            if right_key in self.schema_mappings.right_to_left_mappings:
                return self.schema_mappings.right_to_left_mappings[right_key]
        return right_key

    def __check_meta_data_diff(self, asset_type: str, asset_name: str, left: Dict[str, Any], right: Dict[str, Any],
                               field_exclusions: List[FieldExclusion]):
        if left != right:
            exclusions = map_excluded_fields(field_exclusions)
            # to properly handle schema mappings, the field schema must be excluded
            exclusions.append(format_excluded_field("schema"))
            deep_diff = DeepDiff(left, right, exclude_paths=exclusions)
            diff_dict = filter_value_exclusions_from_diff(deep_diff, field_exclusions)
            if len(diff_dict) > 0:
                diff_message = "Meta data differs:\n{}".format(diff_dict.pretty())
                diff = Diff(asset_name, asset_type, diff_message)
                self.database_diff.append_diff(diff)

