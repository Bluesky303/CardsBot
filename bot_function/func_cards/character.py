from .cards import *
from ..message import *

import json
import os

# 创建文件夹
if not os.path.exists("./character"):
    os.mkdir("./character")

class Character:
    def __init__(self, group_id, user_id):
        # 基础变量
        self.group_id = group_id
        self.user_id = user_id
        self.path = f"./character/{user_id}/"
        if not os.path.exists(self.path): 
            # 如果不存在路径说明没有保存过id，新建文件夹
            # 文件夹结构：
            # qq号/
            # - character_list.json
            # - 角色名/
            #   - 角色名.json
            #   - 卡牌x.json
            #   - 战斗信息.json
            os.mkdir(self.path)
            json.dump({'list': [], 'now': None}, open(self.path + 'character_list.json', 'w', encoding='utf-8'))
        self.dic = json.load(open(self.path + 'character_list.json', 'r', encoding='utf-8')) # 获取角色列表
        self.character = {} # 执行switch后保存当前角色信息
        # 准备显示的属性列表
        # 可选项['状态', '效果', '详细效果', '属性', '能力', '详细能力', '固有技能', '详细固有', '卡组', '详细卡组']
        self.show = ['状态', '效果', '属性', '能力', '固有技能', '卡组']
        if self.dic['now'] == None:
            self.character = None
            self.cardpile = None
        else:
            self.switch_character([self.dic['now']])

    def save(self): # 保存
        json.dump(self.character, open(self.path + self.dic['now'] + '/' + self.dic['now'] + '.json', 'w', encoding='utf-8'))
        json.dump(self.dic, open(self.path + 'character_list.json', 'w', encoding='utf-8'))

    def switch_character(self, arg): # 切换角色
        # 参数限制
        if len(arg) == 0: return '请输入参数'
        if len(arg) > 1: return '参数错误'
        if arg[0] not in self.dic['list']: return '角色不存在'
        
        self.dic['now'] = arg[0]
        self.character = json.load(open(self.path + self.dic['now'] + '/' + self.dic['now'] + '.json', 'r', encoding='utf-8'))
        #p = []
        #for card in self.character['cards']:
        #    p += [json.load(open(self.path + self.dic['now'] + '/' + card + '.json'))] * self.character['cards'][card]
        #self.cardpile = CardPile(p)
        return '当前角色为' + self.dic['now']
    
    def show_character_list(self, arg): # 显示角色列表
        return '\n' + ' '.join(self.dic['list']) + f'\n当前角色：{self.dic["now"]}' 
    
    def show_now_character(self, arg=[]):
        if self.character == None: return '当前没有角色'
        
        show_list = ['状态', '效果', '详细效果', '属性', '能力', '详细能力', '固有技能', '详细固有', '卡组', '详细卡组']
        # 处理参数
        # 参数:
        #   -显示 ..    表示显示选项内容并更新self.show列表
        #   -仅显示 ..  表示仅显示选项内容，不更新self.show
        if len(arg) == 0: show = self.show
        if len(arg) == 1: return '参数错误'
        if len(arg) > 1:
            for i in arg[1:]: 
                if i not in show_list: return '参数错误'
            if arg[0] == '-显示': self.show = arg[1:]
            show = arg[1:]
        
        def effect_text(dic, arg = [], filter = [], format = '\n    $0: $1'):
            # arg 返回每一项的什么内容， 项数必须和格式中 $个数-1 相同
            # 不输入arg则认为$1替换为value本身
            # filter 过滤部分项
            # e.g. dic = character['ability'], arg = ['text']
            # 返回：
            #     能力1：文本1
            #     能力2：文本2
            text = ''
            for key, value in dic.items():
                if key in filter: continue
                format_text = format
                format_text = format_text.replace('$0', key)
                if arg == []:
                    format_text = format_text.replace('$1', str(value))
                for a in range(len(arg)):
                    format_text = format_text.replace(f'${a+1}', str(value[arg[a]]))
                text += format_text + '\n'
            return text

        dic = {
            '状态':     f'\n状态: ' + effect_text(self.character['state'], filter=['effect']),
            '详细效果': f'\n效果: ' + effect_text(self.character['state']['effect'], ['value', 'text'], format='\n    $0: $1 ($2)'),
            '效果':     f'\n效果: ' + effect_text(self.character['state']['effect'], ['value']),
            '属性':     f'\n属性: ' + effect_text(self.character['attr']),
            '详细能力': f'\n能力: ' + effect_text(self.character['ability'], ['text']),
            '能力':     f'\n能力: ' + effect_text(self.character['ability'], format='\n    $0'),
            '详细固有': f'\n固有技能: ' + effect_text(self.character['innate'], ['text']),
            '固有技能': f'\n固有技能: ' + effect_text(self.character['innate'], format='\n    $0'),
            '卡组':     f'\n卡组: ' + effect_text(self.character['cards'], format='\n    $0: $1 张'),
        }
        
        text = f'姓名: {self.character["name"]}'
        for i in show:
            text += dic[i]
        return text
     
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
        def operation(a, b, c):
            dic = {'+': a + b, '-': a - b, '=': b}
            return dic[c]
        for i in range(0, len(arg), 2):
            if arg[i] == 'effect' or not arg[i+1][1:].isdigit() or not arg[i+1][0] in ['+', '-', '=']: return '参数值错误'
            else:
                if arg[i] in self.character['state']:
                    self.character['state'][arg[i]] = operation(self.character['state'][arg[i]], int(arg[i+1]), arg[i+1][0])
                if arg[i] in self.character['attr']:
                    self.character['attr'][arg[i]] = operation(self.character['attr'][arg[i]], int(arg[i+1]), arg[i+1][0])
        self.save()
        return self.show_now_character()
    
    def add_effect(self, arg):
        if self.character == None: return '当前没有角色'
        if len(arg) == 0: return '请输入参数'
        if len(arg) % 2 != 0: return '参数数目错误'
        for i in range(0, len(arg), 2):
            pass