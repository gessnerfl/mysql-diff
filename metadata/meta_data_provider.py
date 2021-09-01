from mysql.connector import connect, connection
from config.model import DbConnectionParameters
from .model import *
from typing import List

schema_filter = "NOT IN ('information_schema', 'mysql', 'performance_schema', 'sys')"


class MetaDataProvider:
    def __init__(self, con: connection.MySQLConnection):
        self.__connection = con

    def provide(self) -> List[Schema]:
        schemas = self.__get_schemas()
        return [self.__map_schema(s) for s in schemas]

    def __get_schemas(self) -> List[SchemaMetaData]:
        with self.__connection.cursor() as cursor:
            query = """
            SELECT SCHEMA_NAME, DEFAULT_CHARACTER_SET_NAME, DEFAULT_COLLATION_NAME 
            FROM information_schema.SCHEMATA 
            WHERE SCHEMA_NAME {}
            """
            cursor.execute(query.format(schema_filter))
            result = cursor.fetchall()
            return [SchemaMetaData(i[0], i[1], i[2]) for i in result]

    def __map_schema(self, meta_data: SchemaMetaData) -> Schema:
        tables = self.__get_tables_of_schema(meta_data.name)
        views = self.__get_views_of_schema(meta_data.name)
        routines = self.__get_routines_of_schema(meta_data.name)
        return Schema(meta_data, tables, views, routines)

    def __get_tables_of_schema(self, schema: str) -> List[Table]:
        tables = self.__get_table_meta_data(schema)
        return [self.__map_table(t) for t in tables]

    def __map_table(self, meta: TableMetaData) -> Table:
        columns = self.__get_columns_of_table(meta.schema, meta.name)
        key_column_usages = self.__get_key_column_usage_of_table(meta.schema, meta.name)
        referential_constraints = self.__get_referential_constraints_of_table(meta.schema, meta.name)
        indices = self.__get_indices_of_table(meta.schema, meta.name)
        return Table(meta, columns, key_column_usages, referential_constraints, indices)

    def __get_table_meta_data(self, schema: str) -> List[TableMetaData]:
        with self.__connection.cursor() as cursor:
            query = """
            SELECT TABLE_SCHEMA,
                   TABLE_NAME, 
                   ENGINE, 
                   VERSION, 
                   ROW_FORMAT, 
                   AUTO_INCREMENT, 
                   TABLE_COLLATION, 
                   CREATE_OPTIONS, 
                   TABLE_COMMENT 
            FROM information_schema.TABLES t 
            WHERE TABLE_SCHEMA = '{}' AND TABLE_TYPE = 'BASE TABLE';
            """
            cursor.execute(query.format(schema))
            result = cursor.fetchall()
            return [TableMetaData(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8]) for i in result]

    def __get_columns_of_table(self, schema: str, table: str) -> List[ColumnMetaData]:
        with self.__connection.cursor() as cursor:
            query = """
            SELECT COLUMN_NAME, 
                   ORDINAL_POSITION, 
                   COLUMN_DEFAULT, 
                   IS_NULLABLE, 
                   DATA_TYPE, 
                   CHARACTER_MAXIMUM_LENGTH, 
                   CHARACTER_OCTET_LENGTH, 
                   NUMERIC_PRECISION, 
                   NUMERIC_SCALE, 
                   DATETIME_PRECISION, 
                   CHARACTER_SET_NAME,
                   COLLATION_NAME, 
                   COLUMN_TYPE, 
                   COLUMN_KEY, 
                   EXTRA, 
                   `PRIVILEGES`, 
                   COLUMN_COMMENT, 
                   GENERATION_EXPRESSION 
            FROM information_schema.COLUMNS 
            WHERE TABLE_SCHEMA = '{}' AND TABLE_NAME = '{}';
            """
            cursor.execute(query.format(schema, table))
            result = cursor.fetchall()
            return [ColumnMetaData(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9], i[10], i[11], i[12],
                                   i[13], i[14], i[15], i[16], i[17]) for i in result]

    def __get_key_column_usage_of_table(self, schema: str, table: str) -> List[KeyColumnUsage]:
        with self.__connection.cursor() as cursor:
            query = """
            SELECT COLUMN_NAME, 
                   ORDINAL_POSITION, 
                   POSITION_IN_UNIQUE_CONSTRAINT, 
                   REFERENCED_TABLE_SCHEMA, 
                   REFERENCED_TABLE_NAME, 
                   REFERENCED_COLUMN_NAME 
            FROM information_schema.KEY_COLUMN_USAGE 
            WHERE TABLE_SCHEMA = '{}' AND TABLE_NAME = '{}';
            """
            cursor.execute(query.format(schema, table))
            result = cursor.fetchall()
            return [KeyColumnUsage(i[0], i[1], i[2], i[3], i[4], i[5]) for i in result]

    def __get_referential_constraints_of_table(self, schema: str, table: str) -> List[ReferentialConstraint]:
        with self.__connection.cursor() as cursor:
            query = """
            SELECT CONSTRAINT_NAME, 
                   UNIQUE_CONSTRAINT_NAME, 
                   MATCH_OPTION, 
                   UPDATE_RULE, 
                   DELETE_RULE, 
                   REFERENCED_TABLE_NAME  
            FROM information_schema.REFERENTIAL_CONSTRAINTS
            WHERE CONSTRAINT_SCHEMA = '{}' AND TABLE_NAME = '{}';
            """
            cursor.execute(query.format(schema, table))
            result = cursor.fetchall()
            return [ReferentialConstraint(i[0], i[1], i[2], i[3], i[4], i[5]) for i in result]

    def __get_indices_of_table(self, schema: str, table: str) -> List[Index]:
        with self.__connection.cursor() as cursor:
            query = """
            SELECT INDEX_NAME, 
                   NON_UNIQUE, 
                   SEQ_IN_INDEX, 
                   COLUMN_NAME, 
                   `COLLATION`, 
                   `CARDINALITY`, 
                   SUB_PART, 
                   PACKED, 
                   NULLABLE, 
                   INDEX_TYPE, 
                   COMMENT, 
                   INDEX_COMMENT 
            FROM information_schema.STATISTICS
            WHERE TABLE_SCHEMA = '{}' AND TABLE_NAME = '{}';
            """
            cursor.execute(query.format(schema, table))
            result = cursor.fetchall()
            return [Index(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9], i[10], i[11]) for i in result]

    def __get_views_of_schema(self, schema: str) -> List[View]:
        with self.__connection.cursor() as cursor:
            query = """
            SELECT TABLE_SCHEMA,
                   TABLE_NAME, 
                   VIEW_DEFINITION, 
                   CHECK_OPTION, 
                   IS_UPDATABLE, 
                   `DEFINER`, 
                   SECURITY_TYPE, 
                   CHARACTER_SET_CLIENT, 
                   COLLATION_CONNECTION 
            FROM information_schema.VIEWS
            WHERE TABLE_SCHEMA = '{}';
            """
            cursor.execute(query.format(schema))
            result = cursor.fetchall()
            return [View(ViewMetaData(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8])) for i in result]

    def __get_routines_of_schema(self, schema: str) -> List[Routine]:
        routines = self.__get_meta_data_of_routines(schema)
        return [self.__map_routine(r) for r in routines]

    def __map_routine(self, meta_data: RoutineMetaData) -> Routine:
        parameters = self.__get_parameters_of_routines(meta_data.schema, meta_data.name)
        return Routine(meta_data, parameters)

    def __get_meta_data_of_routines(self, schema: str) -> List[RoutineMetaData]:
        with self.__connection.cursor() as cursor:
            query = """
            SELECT ROUTINE_SCHEMA,
                   ROUTINE_NAME, 
                   ROUTINE_TYPE, 
                   DATA_TYPE, 
                   CHARACTER_MAXIMUM_LENGTH, 
                   CHARACTER_OCTET_LENGTH, 
                   NUMERIC_PRECISION, 
                   NUMERIC_SCALE, 
                   DATETIME_PRECISION, 
                   CHARACTER_SET_NAME, 
                   COLLATION_NAME, 
                   DTD_IDENTIFIER, 
                   ROUTINE_BODY, 
                   ROUTINE_DEFINITION, 
                   EXTERNAL_NAME, 
                   EXTERNAL_LANGUAGE, 
                   PARAMETER_STYLE, 
                   IS_DETERMINISTIC, 
                   SQL_DATA_ACCESS, 
                   SQL_PATH,
                   SECURITY_TYPE,
                   SQL_MODE,
                   ROUTINE_COMMENT,
                   `DEFINER`,
                   CHARACTER_SET_CLIENT,
                   COLLATION_CONNECTION,
                   DATABASE_COLLATION
            FROM information_schema.ROUTINES
            WHERE ROUTINE_SCHEMA = '{}';
            """
            cursor.execute(query.format(schema))
            result = cursor.fetchall()
            return [RoutineMetaData(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9], i[10], i[11], i[12],
                                    i[13], i[14], i[15], i[16], i[17], i[18], i[19], i[20], i[21], i[22], i[23], i[24],
                                    i[25], i[26]) for i in result]

    def __get_parameters_of_routines(self, schema: str, routine: str) -> List[RoutineParameter]:
        with self.__connection.cursor() as cursor:
            query = """
            SELECT PARAMETER_NAME, 
                   ORDINAL_POSITION, 
                   PARAMETER_MODE, 
                   DATA_TYPE, 
                   CHARACTER_MAXIMUM_LENGTH, 
                   CHARACTER_OCTET_LENGTH, 
                   NUMERIC_PRECISION, 
                   NUMERIC_SCALE, 
                   DATETIME_PRECISION, 
                   CHARACTER_SET_NAME, 
                   COLLATION_NAME, 
                   DTD_IDENTIFIER 
            FROM information_schema.PARAMETERS
            WHERE SPECIFIC_SCHEMA = '{}' AND SPECIFIC_NAME = '{}';
            """
            cursor.execute(query.format(schema, routine))
            result = cursor.fetchall()
            return [RoutineParameter(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9], i[10], i[11])
                    for i in result]


class MetaDataProviderFactory:
    def __init__(self, params: DbConnectionParameters):
        self.params = params

    def __enter__(self) -> MetaDataProvider:
        self.__connection = connect(host=self.params.host, port=self.params.port, user=self.params.username,
                                    password=self.params.password)
        return MetaDataProvider(self.__connection)

    def __exit__(self, t, value, tb):
        self.__connection.close()


def collect_meta_data(params: DbConnectionParameters) -> MetaDataProviderFactory:
    return MetaDataProviderFactory(params)
