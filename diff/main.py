from typing import Dict
from metadata.model import Schema
from .schema_diff import SchemaDiff
from .model import DatabaseDiffs


def diff(left: Dict[str, Schema], right: Dict[str, Schema]) -> DatabaseDiffs:
    return SchemaDiff(left, right).diff()
