from .cards import *
from ..message import *

import json
import os

import asyncio

character_dic = ['角色列表', '使用角色', '新建角色', '删除角色', '角色信息', '修改角色属性']

if not os.path.exists("./character"):
    os.mkdir("./character")

def tabjoin(l):
    return '\n    '.join(l)


class Character:
    def __init__(self, group_id, user_id):
        self.group_id = group_id
        self.user_id = user_id
        self.path = f"./character/{user_id}/"
        if not os.path.exists(self.path):
            os.mkdir(self.path)
            json.dump({'list': [], 'now': None}, open(self.path + 'character_list.json', 'w', encoding='utf-8'))
        self.dic = json.load(open(self.path + 'character_list.json', 'r', encoding='utf-8'))
        self.character = {}
        if self.dic['now'] == None:
            self.character = None
            self.cardpile = None
        else:
            self.switch_character([self.dic['now']])
            
    def switch_character(self, arg):
        if len(arg) == 0: return '请输入参数'
        if arg[0] not in self.dic['list']: return '角色不存在'
        self.dic['now'] = arg[0]
        self.character = json.load(open(self.path + self.dic['now'] + '/' + self.dic['now'] + '.json', 'r', encoding='utf-8'))
        #p = []
        #for card in self.character['cards']:
        #    p += [json.load(open(self.path + self.dic['now'] + '/' + card + '.json'))] * self.character['cards'][card]
        #self.cardpile = CardPile(p)
        return '当前角色为' + self.dic['now']
    
    def save(self):
        json.dump(self.character, open(self.path + self.dic['now'] + '/' + self.dic['now'] + '.json', 'w', encoding='utf-8'))
        json.dump(self.dic, open(self.path + 'character_list.json', 'w', encoding='utf-8'))
    
    def show_character_list(self, arg):
        return '\n' + ' '.join(self.dic['list']) + f'\n当前角色：{self.dic["now"]}' 
    
    def show_now_character(self, arg=[]):
        print(self.character)
        if self.character == None: 
            return '当前没有角色'
        return f'''
角色姓名: {self.character['name']} 
状态: 
    HP: {self.character['state']['hp']} 
    MP: {self.character['state']['mp']} 
    体力: {self.character['state']['sp']}
效果: 
    {tabjoin([key + ':' + str(value) for key, value in self.character['state']['effect'].items()])}
属性:
    {tabjoin([key + ':' + str(value) for key, value in self.character['attr'].items()])}
能力:
    {tabjoin([key + ':' + value['text'] for key, value in self.character['ability'].items()])}
固有技能:
    {tabjoin([key + ':' + ['text'] for key, value in self.character['innate'].items()])}
卡组:
    {tabjoin([f'{value}张{key}' for key, value in self.character['cards'].items()])}
'''
     
    def create_character(self, arg):
        if len(arg) == 0: return '请输入参数'
        if arg[0] in self.dic['list']: return '角色已存在'
        self.dic['list'].append(arg[0])
        os.mkdir(self.path + arg[0])
        os.system(f'copy ./character/default_character.json {self.path}{arg[0]}/{arg[0]}.json'.replace('/', '\\'))
        text1 = self.switch_character(arg)
        self.character['name'] = arg[0]
        text2 = self.show_now_character()
        self.save()
        return text1 + '\n' + text2
    
    def modify_character_attr(self, arg):
        if self.character == None: return '当前没有角色'
        if len(arg) == 0: return '请输入参数'
        if len(arg) % 2 != 0: return '参数数目错误'
        dic = self.character['state'].update(self.character['attr'])
        for i in range(0, len(arg), 2):
            if arg[i] not in dic or arg[i] == 'effect' or not arg[i+1].isdigit(): return '参数值错误'
            if arg[i] in self.character['state']:
                self.character['state'][arg[i]] = int(arg[i+1])
            if arg[i] in self.character['attr']:
                self.character['attr'][arg[i]] = int(arg[i+1])
            