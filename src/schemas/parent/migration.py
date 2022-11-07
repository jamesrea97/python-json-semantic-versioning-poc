from typing import Dict
import copy

class ParentMigration:

    @staticmethod
    def from_one_to_two(v_1: Dict) -> Dict:
        """
        Destructive changes 1.0->2.0:
        - deleted 'name' field
        - added 'renamed_name_parent' field with its value
        """
        v_1 = copy.deepcopy(v_1)
        v_1["__version__"] = "2.0"
        v_1["renamed_name_parent"] = v_1.pop("name", None)

        return v_1

    

PARENT_VERSIONS_DICT = {
    "1": ("src/schemas/parent/parent_1.json", None),
    "2": ("src/schemas/parent/parent_2.json", ParentMigration.from_one_to_two),
}

