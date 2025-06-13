from bson import ObjectId
from pymongo import MongoClient

class CharactersModel:
    def __init__(self, database):
        self.db = database
    
    def create_character(self, hp: int, xp: int, level: int, name: str, dmg: int, dfs: int, kills: int):
        try:
            res = self.db.collection.insert_one({
                "hp": hp, 
                "xp": xp, 
                "level": level,
                "name": name,
                "dmg": dmg,
                "dfs": dfs,
                "kills": kills
                })
            print("Player criado!")
            return res.inserted_id 
        except Exception as e:
            print(f"Ocorreu um erro criando player: {e}")
            return None
        

    def update_character(self, id: str, hp: int, xp: int, level: int, dmg: int, dfs: int, kills: int):
        try:
            res = self.db.collection.update_one({
                "_id": ObjectId(id)}, 
                {"$set": {
                    "hp": hp,
                    "xp": xp, 
                    "level": level, 
                    "dmg": dmg, 
                    "dfs": dfs, 
                    "kills": kills
                    }})
            return res.modified_count
        except Exception as e:
            print(f"Ocorreu um erro atualizando player: {e}")
            return None
        
        
    
    def show_player_data(self, id: str):
        if not isinstance(id, str):
            raise TypeError("ID com formato inválido.")

        try:
            res = self.db.collection.find_one({"_id": ObjectId(id)})
            print("Player:", res["name"])
            print("HP:", res["hp"])
            print("XP:", res["xp"])
            print("Level: ", res["level"])
            print("Damage:", res["dmg"])
            print("Defense:", res["dfs"])
            print("Kills:", res["kills"])
            return res["_id"]
        except Exception as e:
            print(f"Ocorreu um erro mostrando os dados do jogador: {e}")
            
    def delete_player(self, name: str):
        try:
            res = self.db.collection.delete_one({"name": name})
            return res.deleted_count
        except Exception as e:
            print(f"Ocorreu um erro deletando o jogador: {e}")
            return None  


    def find_player(self, name:str):
        try:
            res = self.db.collection.find_one({"name": name})
            return res
        except Exception as e:
            print(f"Ocorreu um erro procurando jogador: {e}")
        
    def find_all_characters(self):
        try:
            res = self.db.collection.find()
            for r in res:
                print("Player: ", r["name"])
            return res
        except Exception as e:
            print(f"Ocorreu um erro mostrando os jogos existentes: {e}")
        
