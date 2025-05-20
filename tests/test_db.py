import pytest
import os
from pymongo import MongoClient
from dotenv import load_dotenv

from app import hello, add, subtract, multiply, divide

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    MONGO_URI = "mongodb://localhost:27017/test_ci_db"

def test_hello():
    assert hello() == "Hello, world!"

@pytest.mark.parametrize(
    "a, b, expected",
    [
        (1, 2, 3),
        (0, 0, 0),
        (-1, 1, 0),
        (-5, -3, -8),
    ],
)
def test_add(a, b, expected):
    assert add(a, b) == expected

@pytest.mark.parametrize(
    "a, b, expected",
    [
        (5, 2, 3),
        (0, 0, 0),
        (-1, -1, 0),
        (10, 5, 5),
    ],
)
def test_subtract(a, b, expected):
    assert subtract(a, b) == expected

@pytest.mark.parametrize(
    "a, b, expected",
    [
        (2, 3, 6),
        (0, 10, 0),
        (-1, 5, -5),
        (-2, -4, 8),
    ],
)
def test_multiply(a, b, expected):
    assert multiply(a, b) == expected

@pytest.mark.parametrize(
    "a, b, expected",
    [
        (6, 3, 2),
        (10, 2, 5),
        (-8, 2, -4),
        (9, -3, -3),
    ],
)
def test_divide(a, b, expected):
    assert divide(a, b) == expected

def test_divide_by_zero():
    with pytest.raises(ValueError, match="Cannot divide by zero."):
        divide(10, 0)

def test_mongo_connection():
    if not MONGO_URI or "default_test_db_for_pytest" in MONGO_URI or "test_ci_db" in MONGO_URI :
        pytest.skip("MONGO_URI nie jest w pełni skonfigurowane dla testu połączenia z prawdziwą bazą; pomijam.")

    client = None
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        client.admin.command('ismaster')
        dbs = client.list_database_names()
        assert isinstance(dbs, list)
    except Exception as e:
        pytest.fail(f"Nie udało się połączyć z MongoDB ({MONGO_URI}): {e}")
    finally:
        if client:
            client.close()

def test_mongo_insert_and_find():
    if not MONGO_URI or "default_test_db_for_pytest" in MONGO_URI or "test_ci_db" in MONGO_URI:
        pytest.skip("MONGO_URI nie jest w pełni skonfigurowane; pomijam test insert/find.")

    client = None
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        db_name_from_uri = MONGO_URI.split('/')[-1].split('?')[0]
        if not db_name_from_uri or db_name_from_uri in ["admin", "local", "config"]:
            db_name = "pytest_specific_test_db"
        else:
            db_name = db_name_from_uri

        db = client[db_name]
        col = db.test_pytest_collection
        doc = {"name": "Test Pytest", "age": 99, "test_id": "insert_find_unique"}

        col.delete_many({"test_id": "insert_find_unique"})

        inserted_id = col.insert_one(doc).inserted_id
        found_doc = col.find_one({"_id": inserted_id})

        assert found_doc is not None
        assert found_doc["name"] == "Test Pytest"
        assert found_doc["age"] == 99

    except Exception as e:
        pytest.fail(f"Błąd podczas testu insert/find w MongoDB ({MONGO_URI}): {e}")
    finally:
        if client:
            if 'col' in locals() and col is not None:
                col.delete_many({"test_id": "insert_find_unique"})
            client.close()