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