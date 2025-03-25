import cards
import json
import os
character_dic = ['角色列表', '使用角色', '新建角色', '删除角色', '角色信息', '修改角色属性']

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