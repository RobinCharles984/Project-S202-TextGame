## Creating Classes for Player, Enemies and NPC's
## Created by Tales Machado Prudente
 
#!!!!!!!!!!!!!!STUDY PYTHON OOP

#imports
from random import Random
from database import Database
from charactersModel import CharactersModel

#variable
random = Random()
db = Database("projeto_final", "personagens")
charactersModel = CharactersModel(db)

class Player:
    def __init__(self, hp: int, xp: int, level: int, name: str, dmg: int, dfs: int, kills: int, paths: int = None):
        if not isinstance(hp, (int, float)):
            raise TypeError("HP deve ser um valor numérico.")
        if hp < 0:
            raise ValueError("HP não pode ser negativo.")
        if not isinstance(name, str):
            raise TypeError("Nome deve ser uma string.")

        self.hp = hp
        self.xp = xp
        self.level = level
        self.name = name
        self.dmg = dmg
        self.dfs = dfs
        self.kills = kills
        self.paths = paths
    
    
    def get_xp(self, xp):
        hp_temp = 0 ########### definido temporariamente (não sei oq é isso)
        xp_levelup = 100
        self.xp += xp
        if self.xp >= xp_levelup: ##Level up system
            self.xp = 0
            self.level += 1
            xp_levelup *= 2
            self.hp += (hp_temp + self.level)
            self.dmg += self.level
            self.dfs += self.level
            charactersModel.update_character(self.name, self.hp, self.xp, self.level, self.dmg, self.dfs, self.kills)
            print("Subiu de nivel!!!")
            print("Nome: ", self.name)
            print("HP: ", self.hp)
            print("Level: ", self.level)
            print("Damage: ", self.dmg)
            print("Defense: ", self.dfs)
            print("Kills: ", self.kills)
    
    def show_stats(self):
        print("Nome: ", self.name)
        print("HP: ", self.hp)
        print("Level: ", self.level)
        print("Damage: ", self.dmg)
        print("Defense: ", self.dfs)
        print("Kills: ", self.kills)

    def die(self):
        if self.hp <= 0:
            self.hp = 0
            charactersModel.delete_player(self.name)
            print("-----------------------------------------")
            print("Voce morreu!")
            print("----------------GAME OVER----------------")
            exit()
        return False
        

##Enemies will attack player when they are at the same path and after every action
class Enemy:
    def __init__(self, hp: int, xp: int, name: str, dmg: int, dfs: int):
        if not isinstance(dmg, (int, float)):
            raise TypeError("Dano (dmg) deve ser um valor numérico.")
        if not isinstance(hp, (int, float)):
             raise TypeError("HP deve ser um valor numérico.")
        if not isinstance(dfs, (int, float)):
            raise TypeError("Defesa (dfs) deve ser um valor numérico.")
        if dfs < 0:
            raise ValueError("Defesa (dfs) não pode ser negativa.")

        self.hp = hp
        self.xp = xp
        self.name = name
        self.dmg = dmg
        self.dfs = dfs

    def spawn(self):
        print("Um ", self.name, " apareceu!")

#Fight system
class Fight():
    def __init__(self, e:Enemy, p: Player):
        while(e.hp != 0 and p.hp != 0):
            print("-------------------------------------------------")
            command = str(input("Comandos: Atacar, Defender, Fugir: "))

            if command == "Atacar":
                e.hp -= p.dmg
                p.hp -= e.dmg
                print(e.name, " tomou ", p.dmg, "!")
                print(e.name, " atacou e voce tomou ", e.dmg, "!")
                print("-------------------------------------------------")
                p.show_stats()
                if p.hp <= 0:
                    p.hp = 0
                    p.die()
            if command == "Defender":
                damage = (e.dmg - p.dfs)
                p.hp -= damage
                print("Voce tomou ", damage, " de dano!")
            if command == "Fugir":
                print("Voce fugiu!")
                break
            if e.hp <= 0:
                e.hp = 0
                p.kills += 1
                print("-------------------------------------------------")
                print("Voce derrotou ", e.name, " e recebeu ", e.xp, " XP!")
                print("-------------------------------------------------")
                p.get_xp(e.xp)
                break

#NPC's are interactive, can talk with player
#There's no way to defeat a NPC
class Npc:
    def __init__(self, name: str):
        self.name = name

    def message(self, message):
        print("_________________________________________________")
        print(self.name, ": ", message)
        print("_________________________________________________")
