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

def test_player_hp_invalido():
    #Testa se a classe Player levanta um TypeError ao receber HP não numérico.
    with pytest.raises(TypeError):
        Player(hp="cem", xp=0, level=1, name="Herói", dmg=10, dfs=5, kills=0)

def test_player_hp_negativo():
    #Testa se a classe Player levanta um ValueError para HP negativo.
    with pytest.raises(ValueError):
        Player(hp=-50, xp=0, level=1, name="Herói", dmg=10, dfs=5, kills=0)

def test_enemy_dano_invalido():
    #Testa se a classe Enemy levanta um TypeError para dano não numérico.
    with pytest.raises(TypeError):
        Enemy(hp=50, xp=20, name="Orc", dmg="fraco", dfs=3)

def test_player_name_deve_ser_string(player):
    #Testa se um erro é levantado se o nome do jogador não for uma string.
    with pytest.raises(TypeError):
        # Tenta criar um jogador com um número como nome
        Player(hp=100, xp=0, level=1, name=12345, dmg=10, dfs=5, kills=0)

def test_enemy_defesa_negativa(enemy):
    #Testa se um erro é levantado se a defesa do inimigo for negativa.
    with pytest.raises(ValueError):
        # Tenta criar um inimigo com defesa negativa
        Enemy(hp=50, xp=20, name="Orc", dmg=10, dfs=-5)

def test_enemy_defesa_integer(enemy):
    #Testa se um erro é levantado se a defesa do inimigo não for um número.
    with pytest.raises(TypeError):
        # Tenta criar um inimigo com defesa negativa
        Enemy(hp=50, xp=20, name="Orc", dmg=10, dfs="Sim")

def test_fight_player_loses_and_dies(mocker):
    #Testa se o método die() do jogador é chamado quando seu HP chega a zero em uma luta.
    
    # Cria um jogador fraco e um inimigo muito forte para garantir a derrota
    weak_player = Player(hp=10, xp=0, level=1, name="Hero", dmg=5, dfs=5, kills=0)
    strong_enemy = Enemy(hp=100, xp=500, name="Dragon", dmg=50, dfs=20)

    # Simula o jogador atacando uma vez antes de ser derrotado
    mocker.patch("builtins.input", side_effect=["Atacar"])
    
    # "Espiona" o método die() do nosso jogador fraco para ver se ele é chamado
    mock_die = mocker.patch.object(weak_player, 'die')

    # Inicia a luta
    fight = Fight(strong_enemy, weak_player)

    # A asserção mais importante: o método die() foi chamado uma vez?
    mock_die.assert_called_once()