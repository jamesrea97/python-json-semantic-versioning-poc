import json
from typing import Dict

def get_major_version(version: str) -> str:
    return version[:version.find(".")]

def load_schema(path: str) -> Dict:
    with open(path) as file:
        return json.loads(file.read())