from typing import Dict
from metadata.model import Schema
from config.model import Exclusions, SchemaMappings
from .schema_diff import SchemaDiff
from .model import DatabaseDiffs


def diff(left: Dict[str, Schema], right: Dict[str, Schema], exclusions: Exclusions, schema_mappings: SchemaMappings) \
        -> DatabaseDiffs:
    return SchemaDiff(left, right, exclusions, schema_mappings).diff()
