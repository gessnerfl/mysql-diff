from typing import Dict
from metadata.model import Schema
from config.model import Exclusions
from .schema_diff import SchemaDiff
from .model import DatabaseDiffs


def diff(left: Dict[str, Schema], right: Dict[str, Schema], exclusions: Exclusions) -> DatabaseDiffs:
    return SchemaDiff(left, right, exclusions).diff()
