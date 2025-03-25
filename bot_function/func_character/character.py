import cards
import json
import os

if not os.path.exists("./character"):
    os.mkdir("./character")

class Character:
    def __init__(self, qnum, name):
        with open(f"./character/{qnum}/{name}.json", "r", encoding="utf-8") as f:
            self.dic = json.load(f)

    def new(self):
        pass

    
    
    def save(self):
        pass