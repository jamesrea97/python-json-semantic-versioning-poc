from typing import Dict
import copy

class ChildrenMigration:

    @staticmethod
    def from_one_to_two(v_1: Dict) -> Dict:
        """
        Destructive changes 1.0->2.0:
        - deleted 'name' field
        - added 'rename_name' field with its value
        """
        v_1 = copy.deepcopy(v_1)
        v_1["__version__"] = "2.0"
        v_1["rename_name"] = v_1.pop("name", None)

        return v_1

    @staticmethod
    def from_two_to_three(v_2: Dict) -> Dict:
        """
        Destructive changes 2.0->3.0:
        - deleted 'rename_name' field
        """
        v_2 = copy.deepcopy(v_2)
        v_2["__version__"] = "3.0"
        v_2.pop("rename_name", None)

        return v_2



CHILD_VERSIONS_DICT = {
    "1": ("src/schemas/child/children_1.json", None),
    "2": ("src/schemas/child/children_2.json", ChildrenMigration.from_one_to_two),
    "3": ("src/schemas/child/children_3.json", ChildrenMigration.from_two_to_three),
}

