from typing import Dict, List
import src.schemas.utils as SchemaUtils
from collections import OrderedDict
from src.schemas.parent.migration import PARENT_VERSIONS_DICT
from src.schemas.child.migration import CHILD_VERSIONS_DICT

SPECIAL_KEYS = {"__type__", "__version__"}

NESTED_TYPES = {list, dict}

# TODO move this to some COMMON JSON file with versioning built in git
# MODEL_NAME: (VERSION_DICT, LATEST_VALUE)
MIGRATORS = {
    "ParentModel": (PARENT_VERSIONS_DICT, "2.0"),
    "ChildModel": (CHILD_VERSIONS_DICT, "3.0"),
}

class Migrator:

    @staticmethod
    def migrate(schema: Dict) -> Dict:
        type_ = schema["__type__"]
        
        new_major_version = SchemaUtils.get_major_version(MIGRATORS[type_][1])
        old_major_version = SchemaUtils.get_major_version(schema["__version__"])
        
        schema_location, _ = MIGRATORS[type_][0][new_major_version]

        new_schema = SchemaUtils.load_schema(schema_location)
        
        new_schema_keys = set(new_schema.keys())
        
        nested_types = {
            k:v for k, v in schema.items()
            if type(v) in NESTED_TYPES and k in new_schema_keys
        }
        not_nested_types = {
            k:v for k, v in schema.items()
            if type(v) not in NESTED_TYPES
        }

        if not nested_types:
            return Migrator._migrate_type(
                MIGRATORS[type_][0],
                from_version=old_major_version,
                to_version=new_major_version,
                data= not_nested_types 
            )


        updated_schema = {}
        for k, v in nested_types.items():
            if isinstance(v, dict):
                updated_schema[k] = Migrator.migrate(v)
            elif isinstance(v, list):
                updated_schema_entries = []
                for e in v:
                    updated_schema_entries.append(Migrator.migrate(e))
                updated_schema[k] = updated_schema_entries
        
        unnested_schema = Migrator._migrate_type(
                MIGRATORS[type_][0],
                from_version=old_major_version,
                to_version=new_major_version,
                data= not_nested_types 
            )
        
        return dict(unnested_schema, **updated_schema)

    def _migrate_type(migrator_versions_dict: Dict, from_version: str, to_version: str, data: Dict) -> Dict:
        
        migrator_versions_dict = OrderedDict(migrator_versions_dict)

        if from_version == to_version:
            return data

        for k, v in migrator_versions_dict.items():
            if int(k) > int(from_version) and int(k) < int(to_version) + 1:
                data = v[1](data)

        return data
            
        