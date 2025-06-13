import pytest 
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from characters import Player, Enemy, Fight, Npc

@pytest.fixture
def player():
    return Player(hp=100, xp=0, level=1, name="Hero", dmg=20, dfs=5, kills=0)

@pytest.fixture
def enemy():
    return Enemy(hp=30, xp=50, name="Goblin", dmg=10, dfs=2)

@pytest.fixture
def npc():
    return Npc("Gargula")


def test_player_get_xp_and_level_up(player, mocker):
    mocker.patch("characters.charactersModel.update_character")  # Evita chamada ao DB

    player.get_xp(120)
    assert player.level == 2
    assert player.xp == 0
    assert player.kills == 0


def test_player_die(player, mocker):
    player.hp = 0
    mocker.patch("characters.charactersModel.delete_player")
    mock_exit = mocker.patch("characters.exit")

    player.die()
    mock_exit.assert_called_once()


def test_npc_message(mocker):
    npc = Npc("Velho Sábio")
    mocked_print = mocker.patch("builtins.print")
    npc.message("Siga em frente.")
    mocked_print.assert_any_call("Velho Sábio", ": ", "Siga em frente.")


def test_enemy_spawn(enemy, mocker):
    mocked_print = mocker.patch("builtins.print")
    enemy.spawn()
    mocked_print.assert_called_with("Um ", "Goblin", " apareceu!")


def test_fight_attack_and_win(player, enemy, mocker):
    # Simula entrada de comandos do usuário
    mocker.patch("builtins.input", side_effect=["Atacar", "Atacar"])
    mocker.patch("characters.charactersModel.update_character")
    mocked_print = mocker.patch("builtins.print")

    fight = Fight(enemy, player)

    assert enemy.hp == 0
    assert player.kills == 1
    mocked_print.assert_any_call("Voce derrotou ", "Goblin", " e recebeu ", 50, " XP!")

