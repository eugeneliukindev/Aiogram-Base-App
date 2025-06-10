import json
from os import PathLike
from typing import Any


def load_json(file_path: PathLike[str] | str) -> Any:
    with open(file_path) as file:
        return json.load(file)


MOCK_USERS = load_json("tests/integration_tests/mock_data/users.json")
