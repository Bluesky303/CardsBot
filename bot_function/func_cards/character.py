from .cards import *
from ..message import *

import json
import os

import asyncio

character_dic = ['角色列表', '使用角色', '新建角色', '删除角色', '角色信息', '修改角色属性']

if not os.path.exists("./character"):
    os.mkdir("./character")

def tabjoin(l):
    return tabjoin(l)


class Character:
    def __init__(self, group_id, user_id):
        self.group_id = group_id
        self.user_id = user_id
        self.path = f"./character/{user_id}/"
        if not os.path.exists(self.path):
            os.mkdir(self.path)
            json.dump({'list': [], 'now': None}, open(self.path + 'character_list.json', 'w', encoding='utf-8'))
        self.dic = json.load(open(self.path + 'character_list.json', 'r', encoding='utf-8'))
        self.character = self.dic['now']
        if self.character == None:
            self.character = None
            self.cardpile = None
        else:
            self.switch_character(self.character)
            
    def switch_character(self, arg):
        if len(arg) == 0: return '请输入参数'
        if arg[0] not in self.dic['list']: return '角色不存在'
        self.character = arg[0]
        self.character = json.load(open(self.path + self.character + '/' + self.character + '.json', 'r', encoding='utf-8'))
        p = []
        for card in self.character['cards']:
            p += [json.load(open(self.path + self.character + '/' + card + '.json'))] * self.character['cards'][card]
        self.cardpile = CardPile(p)
        return '当前角色为' + self.character
    
    def save(self):
        json.dump(self.character, open(self.path + self.character + '/' + self.character + '.json', 'w', encoding='utf-8'))
        json.dump(self.dic, open(self.path + 'character_list.json', 'w', encoding='utf-8'))
    
    def show_character_list(self, arg):
        if self.dic['list'] == []: return '当前没有角色'
        return ' '.join(self.dic['list'])
    
    def show_now_character(self, arg):
        if self.character == None: return '当前没有角色'
        return f'''
            角色姓名: {self.character['name']} 
            状态: 
                HP: {self.character['hp']} 
                MP: {self.character['mp']} 
                体力: {self.character['sp']}
            效果: 
                {tabjoin([key + ':' + value for key, value in self.character['state']['effect'].items()])}
            属性:
                {tabjoin([key + ':' + value for key, value in self.character['attr'].items()])}
            能力:
                {tabjoin([key + ':' + value['text'] for key, value in self.character['ability'].items()])}
            固有技能:
                {tabjoin([key + ':' + value['text'] for key, value in self.character['innate'].items()])}
            卡组:
                {tabjoin([f'{value}张{key}' for key, value in self.character['cards'].items()])}
        '''
     
    def create_character(self, arg):
        if len(arg) == 0: return '请输入参数'
        if arg[0] in self.dic['list']: return '角色已存在'
        self.dic['list'].append(arg[0])
        os.mkdir(self.path + arg[0])
        os.system(f'copy ./character/default_character.json {self.path}{arg[0]}/'.replace('/', '\\'))
        text1 = self.switch_character(arg[0])
        text2 = self.show_now_character([])
        return text1 + '\n' + text2