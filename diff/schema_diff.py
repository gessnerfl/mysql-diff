from deepdiff import DeepDiff
from .model import *
from typing import Dict, Any, TypeVar, Callable, NoReturn, List
from metadata.model import Schema, Table, View, Routine, RoutineParameter, ColumnMetaData, KeyColumnUsage, \
    ReferentialConstraint, Index
from .model import Diff
from config.model import Exclusions

ASSET_TYPE_SCHEMA = "Schema"
ASSET_TYPE_TABLE = "Table"
ASSET_TYPE_COLUMN = "Column"
ASSET_TYPE_KEY_COLUMN_USAGE = "Key Column Usage"
ASSET_TYPE_REFERENTIAL_CONSTRAINT = "Referential Constraint"
ASSET_TYPE_INDEX = "Index"
ASSET_TYPE_ROUTINE = "Routine"
ASSET_TYPE_ROUTINE_PARAMETER = "Routine-Parameter"
ASSET_TYPE_VIEW = "View"

T = TypeVar('T')


def schema_name(schema: Schema) -> str: return schema.meta_data.name


def table_name(table: Table) -> str:
    return "{} - {}".format(table.meta_data.schema, table.meta_data.name)


def column_name(column: ColumnMetaData) -> str:
    return "{} - {} - {}".format(column.table_schema, column.table_name, column.column_name)


def key_column_usage_name(k: KeyColumnUsage) -> str:
    return "{} - {} - {}".format(k.table_schema, k.table_name, k.column_name)


def referential_constraint_name(c: ReferentialConstraint) -> str:
    return "{} - {} - {}".format(c.constraint_schema, c.table_name, c.constraint_name)


def index_name(c: Index) -> str:
    return "{} - {} - {}".format(c.table_schema, c.table_name, c.index_name)


def view_name(view: View) -> str:
    return "{} - {}".format(view.meta_data.schema, view.meta_data.name)


def routine_name(routine: Routine) -> str:
    return "{} - {}".format(routine.meta_data.schema, routine.meta_data.name)


def routine_param_name(param: RoutineParameter) -> str:
    return "{} - {} - {}".format(param.routine_schema, param.routine_name, param.parameter_name)


def map_excluded_fields(excluded_fields: List[str]) -> List[str]:
    if excluded_fields is None:
        return []
    return ["root['{}']".format(e) for e in excluded_fields]


class SchemaDiff:
    def __init__(self, left: Dict[str, Schema], right: Dict[str, Schema], exclusions: Exclusions):
        self.left = left
        self.right = right
        self.database_diff = DatabaseDiffs()
        self.exclusions = exclusions

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
                                    right: Dict[str, T], excluded_fields: List[str]):
        self.__check_diff_of_assets(asset_type, asset_name_fn, left, right,
                                    lambda l, r: self.__check_meta_data_diff(asset_type,
                                                                             asset_name_fn(l),
                                                                             l.to_dict(),
                                                                             r.to_dict(),
                                                                             excluded_fields))

    def __check_diff_of_assets(self, asset_type: str, asset_name_fn: Callable[[T], str], left: Dict[str, T],
                               right: Dict[str, T], comparator: Callable[[T, T], NoReturn]):
        for k in left:
            if k in right:
                comparator(left[k], right[k])
            else:
                asset_name = asset_name_fn(left[k])
                diff = Diff(asset_name, asset_type, "{} is not present on right side".format(k))
                self.database_diff.append_diff(diff)

        for k in right:
            if k not in left:
                asset_name = asset_name_fn(right[k])
                diff = Diff(asset_name, asset_type, "{} is not present on left side".format(k))
                self.database_diff.append_diff(diff)

    def __check_meta_data_diff(self, asset_type: str, asset_name: str, left: Dict[str, Any], right: Dict[str, Any],
                               excluded_fields: List[str]):
        if left != right:
            exclusions = map_excluded_fields(excluded_fields)
            pretty = DeepDiff(left, right, exclude_paths=exclusions).pretty()
            if pretty != "":
                diff_message = "Meta data differs:\n{}".format(pretty)
                diff = Diff(asset_name, asset_type, diff_message)
                self.database_diff.append_diff(diff)
