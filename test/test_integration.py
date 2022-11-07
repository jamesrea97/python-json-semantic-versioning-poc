import pytest
from src.schemas.migrator import Migrator


@pytest.fixture
def test_old_config_parent():
    return {
        "__type__": "ParentModel",
        "__version__": "1.0",
        "name": "John",
        "children": [
            {
                "__type__": "ChildModel",
                "__version__": "2.0",
                "rename_name": "Benjamin"
            }
        ]
    }

@pytest.fixture
def test_old_config_child():
    return {
        "__type__": "ChildModel",
        "__version__": "2.0",
        "rename_name": "Benjamin"
    }

@pytest.fixture
def test_very_old_config_child():
    return {
        "__type__": "ChildModel",
        "__version__": "1.0",
        "name": "Benjamin"
    }

def test_can_migrate_one_version(test_old_config_child):
    res = Migrator.migrate(test_old_config_child)

    assert res == {
        "__type__": "ChildModel",
        "__version__": "3.0",
    }

def test_can_migrate_multiple_version(test_very_old_config_child):
    res = Migrator.migrate(test_very_old_config_child)

    assert res == {
        "__type__": "ChildModel",
        "__version__": "3.0",
    }

def test_can_migrate_nested(test_old_config_parent):
    res = Migrator.migrate(test_old_config_parent)


    assert res == {
        "__type__": "ParentModel",
        "__version__": "2.0",
        "renamed_name_parent": "John",
        "children": [
            {
                "__type__": "ChildModel",
                "__version__": "3.0",
            }
        ]
    }
    


