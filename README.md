# MySQL Diff Tool

This is a simple python 3 application to identify database schema diffs between two MySQL database servers. The diffs
are identified using the MySQL `information_schema`. The following assets are analyzed by the tool:

* DB **Schemas**:
    * Based on  `information_schema.SCHEMATA`
    * The schemas `information_schema`, `mysql`, `performance_schema`, `sys` are excluded
* **Tables** defined in resolved schemas:
    * Based on  `information_schema.TABLES`
    * Restricted to `TABLE_TYPE` `BASE TABLE`
* **Columns** of resolved tables:
    * Based on `information_schema.COLUMNS`
* **Key column usage** of resolved tables:
    * Based on `information_schema.KEY_COLUMN_USAGE`
* **Referential constraints** of resolved tables:
    * Based on `information_schema.KEY_COLUMN_USAGE`
* **Indices** of resolved tables:
    * Based on `information_schema.STATISTICS`
* **Views** defined in resolved schemas:
    * Based on `information_schema.VIEWS`
* **Routines** defined in resolved schemas:
    * Based on `information_schema.ROUTINES`
* **Routine Parameters** defined for resolved routines:
    * Based on `information_schema.PARAMETERS`

The tool compares the two database in both direction. It checks that each asset exists on each side and compares the
metadata of the matching assets with each other.

## Usage

```bash
python mysql-diff.py -c my-config.yaml
```

**CLI Usage:**

```bash
mysql-diff [-h] -c CONFIG [-o OUT] [--left-out-path LEFT_OUT_PATH] [--right-out-path RIGHT_OUT_PATH]
```

Determine structural differences between two MySQL database

**Arguments:**

```text
-h, --help                       Show the help message and exit
-c CONFIG, --config CONFIG       The yaml configuration file required for the execution
-o OUT, --out OUT                The file path of the output file
--left-out-path LEFT_OUT_PATH    The file path to store the meta data of the left side
--right-out-path RIGHT_OUT_PATH  The file path to store the meta data of the right side
```

## Configuration file

The following yaml snippet shows a sample configuration file. It requires both databases systems to be configured.
Optionally exclusion rules and mappings of schema names can be configured.

```yaml
databases:
  left:
    name: test
    hostname: test.example.com
    port: 3306
    username: my-user
    password: my-secure-password
  right:
    name: prod
    hostname: prod.example.com
    port: 3306
    username: my-user
    password: my-secure-password
exclusions:
  view_fields:
    - field: definer
  table_fields:
    - field: row_format
      left_value: Compact
      right_value: Dynamic
schema_mappings:
  app1-schema: app_schema
  app2_schema: app2
```

### Configuration reference:

* databases - required: root element for configuring the database servers
    * left / right - required: the root elements for each database server
        * name - required: a short name identifying the DB
        * hostname - required: the database host name
        * port - optional: the database port number - defaults to 3306
        * username - required: the username to login to the database
        * password - required: the password to login to the database
* exclusions - optional: root element for all kind of field exclusions
    * schema_fields / table_fields / column_fields / key_column_usage_fields / referential_constraint_fields /
      index_fields / routine_fields / routine_parameter_fields / view_fields - optional: root element to for exclusion
      rules for the given type:
        * field - required: the name to which the exclusion rule should be applied. If no values are provided the whole
          filed will be excluded
        * left_value / right_value - optional: restrict filter to specific values only. If filtering based on field
          values should be applied both left and right need to be provided
* schema_mappings - optional: The root element to map schema names. It contains a list of key value pairs where the key
  is the name of the schema on the left side and the value the name of the schema on the right side