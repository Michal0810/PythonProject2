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


def test_connection():
    client = MongoClient(MONGO_URI)
    dbs = client.list_database_names()
    assert isinstance(dbs, list)


def test_mongo_insert_and_find():
    client = MongoClient(MONGO_URI)
    db = client.test_db
    col = db.test_collection
    doc = {"name": "Roman", "age": 30}

    inserted_id = col.insert_one(doc).inserted_id
    found_doc = col.find_one({"_id": inserted_id})

    assert found_doc["name"] == "Roman"
    assert found_doc["age"] == 30

    col.delete_many({})  # cleanup
