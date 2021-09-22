from deepdiff import DeepDiff
from .model import *
from typing import Dict, Any, TypeVar, Callable, NoReturn
from metadata.model import Schema, Table, View, Routine, RoutineParameter, ColumnMetaData, KeyColumnUsage, \
    ReferentialConstraint, Index
from .model import Diff

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


class SchemaDiff:
    def __init__(self, left: Dict[str, Schema], right: Dict[str, Schema]):
        self.left = left
        self.right = right
        self.database_diff = DatabaseDiffs()

    def diff(self) -> DatabaseDiffs:
        self.__check_diff_of_assets(ASSET_TYPE_SCHEMA, schema_name, self.left, self.right, self.__process_schema)
        return self.database_diff

    def __process_schema(self, left: Schema, right: Schema):
        asset_name = schema_name(left)
        self.__check_meta_data_diff(ASSET_TYPE_SCHEMA, asset_name, left.meta_data.to_dict(), right.meta_data.to_dict())

        self.__check_diff_of_assets(ASSET_TYPE_TABLE, table_name, left.tables, right.tables, self.__process_table)
        self.__check_diff_of_assets(ASSET_TYPE_VIEW, view_name, left.views, right.views, self.__process_view)
        self.__check_diff_of_assets(ASSET_TYPE_ROUTINE, routine_name, left.routines, right.routines,
                                    self.__process_routine)

    def __process_table(self, left: Table, right: Table):
        asset_name = table_name(left)
        self.__check_meta_data_diff(ASSET_TYPE_TABLE, asset_name, left.meta_data.to_dict(), right.meta_data.to_dict())

        self.__check_diff_of_leaf_assets(ASSET_TYPE_COLUMN, column_name, left.columns, right.columns)
        self.__check_diff_of_leaf_assets(ASSET_TYPE_KEY_COLUMN_USAGE, key_column_usage_name, left.key_column_usages,
                                         right.key_column_usages)
        self.__check_diff_of_leaf_assets(ASSET_TYPE_REFERENTIAL_CONSTRAINT, referential_constraint_name,
                                         left.referential_constraints, right.referential_constraints,)
        self.__check_diff_of_leaf_assets(ASSET_TYPE_INDEX, index_name, left.indices, right.indices)

    def __process_view(self, left: View, right: View):
        asset_name = view_name(left)
        self.__check_meta_data_diff(ASSET_TYPE_VIEW, asset_name, left.meta_data.to_dict(), right.meta_data.to_dict())

    def __process_routine(self, left: Routine, right: Routine):
        asset_name = routine_name(left)
        self.__check_meta_data_diff(ASSET_TYPE_ROUTINE, asset_name, left.meta_data.to_dict(), right.meta_data.to_dict())

        self.__check_diff_of_leaf_assets(ASSET_TYPE_ROUTINE_PARAMETER, routine_param_name,
                                         left.parameters, right.parameters)

    def __check_diff_of_leaf_assets(self, asset_type: str, asset_name_fn: Callable[[T], str], left: Dict[str, T],
                                    right: Dict[str, T]):
        self.__check_diff_of_assets(asset_type, asset_name_fn, left, right,
                                    lambda l, r: self.__check_meta_data_diff(asset_type,
                                                                             asset_name_fn(l),
                                                                             l.to_dict(),
                                                                             r.to_dict()))

    def __check_diff_of_assets(self, asset_type: str, asset_name_fn: Callable[[T], str], left: Dict[str, T],
                               right: Dict[str, T], comparator: Callable[[T, T], NoReturn]):
        for k, v in left:
            if k in right:
                comparator(v, right[k])
            else:
                asset_name = asset_name_fn(v)
                diff = Diff(asset_name, asset_type, "{} is not present on right side".format(k))
                self.database_diff.append_diff(diff)

        for k, v in right:
            if k not in left:
                asset_name = asset_name_fn(v)
                diff = Diff(asset_name, asset_type, "{} is not present on left side".format(k))
                self.database_diff.append_diff(diff)

    def __check_meta_data_diff(self, asset_type: str, asset_name: str, left: Dict[str, Any], right: Dict[str, Any]):
        if left != right:
            diff_message = "Meta data differs:\n{}".format(DeepDiff(left, right).pretty())
            diff = Diff(asset_name, asset_type, diff_message)
            self.database_diff.append_diff(diff)
