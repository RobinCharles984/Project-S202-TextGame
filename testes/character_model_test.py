import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import pytest
from unittest.mock import MagicMock
from bson import ObjectId
from charactersModel import CharactersModel


@pytest.fixture
def fake_db():
    return MagicMock()


@pytest.fixture
def model(fake_db):
    return CharactersModel(fake_db)


valid_id = ObjectId("507f1f77bcf86cd799439011")  # ID válido para os testes


def test_create_character(model):
    model.db.collection.insert_one.return_value.inserted_id = "123"

    inserted_id = model.create_character(100, 0, 1, "Hero", 10, 5, 0)

    model.db.collection.insert_one.assert_called_once_with({
        "hp": 100,
        "xp": 0,
        "level": 1,
        "name": "Hero",
        "dmg": 10,
        "dfs": 5,
        "kills": 0
    })
    assert inserted_id == "123"


def test_update_character(model):
    model.db.collection.update_one.return_value.modified_count = 1

    result = model.update_character(valid_id, 120, 50, 2, 15, 10, 5)

    model.db.collection.update_one.assert_called_once()
    assert result == 1


def test_show_player_data(model):
    valid_id = ObjectId()  # cria um ObjectId válido para teste
    
    model.db.collection.find_one.return_value = {
        "_id": valid_id,
        "name": "Hero",
        "hp": 100,
        "xp": 0,
        "level": 1,
        "dmg": 10,
        "dfs": 5,
        "kills": 0
    }

    player_id = model.show_player_data(str(valid_id))  # passe string, porque a função converte internamente para ObjectId

    model.db.collection.find_one.assert_called_once_with({"_id": valid_id})
    assert player_id == valid_id  # player_id é ObjectId, então compara direto


def test_delete_player(model):
    model.db.collection.delete_one.return_value.deleted_count = 1

    result = model.delete_player("Hero")

    model.db.collection.delete_one.assert_called_once_with({"name": "Hero"})
    assert result == 1


def test_find_player(model):
    model.db.collection.find_one.return_value = {"name": "Hero"}

    result = model.find_player("Hero")

    model.db.collection.find_one.assert_called_once_with({"name": "Hero"})
    assert result["name"] == "Hero"


def test_find_all_characters(model):
    fake_cursor = [{"name": "Hero"}, {"name": "Goblin"}]
    model.db.collection.find.return_value = fake_cursor

    result = model.find_all_characters()

    model.db.collection.find.assert_called_once()
    assert list(result) == fake_cursor