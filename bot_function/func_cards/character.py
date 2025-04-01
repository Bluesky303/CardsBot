from .cards import *
from ..message import *

import json
import os

def operation(a, b, c):
    dic = {'+': a + b, '-': a - b, '=': b}
    return dic[c]

# 创建文件夹
if not os.path.exists("./character"):
    os.mkdir("./character")

class Character:
    def __init__(self, group_id, user_id):
        '''
        初始化函数
        group_id: 群号
        user_id: qq号
        path: 保存路径
        characterlist: 角色列表
            {
                'list': 角色列表
                'now':  当前角色
            }
        character: 当前角色信息
        Pile: 卡组
        Pile_order: 卡组指令
        '''
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
            #   - 卡牌列表.json
            #   - 卡牌x.json      数值
            #   - 卡牌x.py        功能实现
            #   - 战斗信息.json
            os.mkdir(self.path)
            json.dump({'list': [], 'now': None}, open(self.path + 'character_list.json', 'w', encoding='utf-8'))
            
        self.chracterlist = json.load(open(self.path + 'character_list.json', 'r', encoding='utf-8')) # 获取角色列表
        self.character = {} # 执行switch后保存当前角色信息
        self.cards_list = {} # 执行switch后保存当前角色卡组
        self.Pile = None # 卡组
        self.onbattle = False # 是否在战斗中
        if self.chracterlist['now'] == None:
            self.character = None
            self.cards_list = None
        else:
            self.switch_character([self.chracterlist['now']])

        
    def save(self): # 保存
        '''
        保存
        '''
        json.dump(self.character, open(self.path + self.chracterlist['now'] + '/' + self.chracterlist['now'] + '.json', 'w', encoding='utf-8'))
        json.dump(self.chracterlist, open(self.path + 'character_list.json', 'w', encoding='utf-8'))
        json.dump(self.cards_list, open(self.path + self.chracterlist['now'] + '/' + 'cards_list.json', 'w', encoding='utf-8'))

    def switch_character(self, arg): # 切换角色
        '''
        切换角色
        arg[0] 为角色名 
        '''
        # 参数限制
        if len(arg) == 0: return '请输入参数'
        if len(arg) > 1: return '参数错误'
        if arg[0] not in self.chracterlist['list']: return '角色不存在'
        
        self.chracterlist['now'] = arg[0]
        self.character = json.load(open(self.path + self.chracterlist['now'] + '/' + self.chracterlist['now'] + '.json', 'r', encoding='utf-8'))
        self.cards_list = json.load(open(self.path +  self.chracterlist['now'] + '/' + 'cards_list.json', 'r', encoding='utf-8'))
        Pile = []
        for key, value in self.character['cards'].items():
            Pile += [json.load(open(self.path + self.chracterlist['now'] + '/' + key + '.json', 'r', encoding='utf-8'))] * value
        self.Pile = CardPile(Pile)
        if os.path.exists(self.path + self.chracterlist['now'] + '/' + 'battle.json'):
            self.onbattle = True
            battle = json.load(open(self.path + self.chracterlist['now'] + '/' + 'battle.json', 'r', encoding='utf-8'))
            for key, value in battle.items():   
                self.Pile.__dict__[key] = value
        return '当前角色为' + self.chracterlist['now']
    
    def show_character_list(self, arg): # 显示角色列表
        '''
        显示角色列表
        '''
        return '\n' + ' '.join(self.chracterlist['list']) + f'\n当前角色：{self.chracterlist["now"]}' 
    
    def show_now_character(self, arg=[]): # 显示当前角色信息
        '''
        显示当前角色信息
        默认显示 状态 效果 属性
        arg[0] 为选项，
            -显示 ... 为仅显示选项内容，不更新self.show
            
        '''
        if self.character == None: return '当前没有角色'
        
        show_list = ['状态', '效果', '详细效果', '属性', '能力', '详细能力', '固有技能', '详细固有', '卡组', '详细卡组']
        show = ['卡组']
        # 处理参数
        # 参数:
        #   -仅显示 ..  表示仅显示选项内容，不更新self.show
        if len(arg) == 1: return '参数错误'
        if len(arg) > 1:
            for i in arg[1:]: 
                if i not in show_list: return '参数错误'
            if arg[0] == '-显示': show = arg[1:]
            else: return '指令错误'
        
        def effect_text(dic, arg = [], filter = [], format = '\n    $0: $1', text_replace = {'text':{'$0': 'value'}}):
            # arg 为返回项目，格式由format决定，依次对应$0, $1, ...
            # 不输入arg则认为$1替换为value本身
            # filter 过滤部分项
            # text_replace 对返回项目进行格式化，将对应内容替换为对应值
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
                    if arg[a] in text_replace:
                        for b in text_replace[arg[a]]:
                            content = value[arg[a]].replace(b, str(value[text_replace[arg[a]][b]]))
                    else:
                        content = str(value[arg[a]])
                    format_text = format_text.replace(f'${a+1}', content)
                text += format_text
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
     
    def create_character(self, arg): # 创建角色
        '''
        创建角色
        arg[0] 为角色名
        '''
        if len(arg) == 0: return '请输入参数'
        if len(arg) > 1: return '参数错误'
        if arg[0] in self.chracterlist['list']: return '角色已存在'
        self.chracterlist['list'].append(arg[0])
        os.mkdir(self.path + arg[0])
        json.dump({'list': []}, open(self.path + arg[0] + '/cards_list.json', 'w', encoding='utf-8'))
        os.system(f'copy ./character/default_character.json {self.path}{arg[0]}/{arg[0]}.json'.replace('/', '\\'))
        os.system(f'copy ./character/基础卡.json {self.path}{arg[0]}/基础卡.json'.replace('/', '\\'))
        text1 = self.switch_character(arg)
        self.character['name'] = arg[0]
        text2 = self.show_now_character()
        self.save()
        return text1 + '\n' + text2
    
    def delete_character(self, arg): # 删除角色
        '''
        删除角色
        arg[0] 为角色名
        '''
        if len(arg) == 0: return '请输入参数'
        if arg[0] not in self.chracterlist['list']: return '角色不存在'
        if arg[0] == self.chracterlist['now']: return '当前角色不能删除'
        self.chracterlist['list'].remove(arg[0])
        os.system(f'rmdir {self.path}{arg[0]}'.replace('/', '\\'))
        return '已删除角色' + arg[0]
    
    def modify_character_attr(self, arg): # 修改角色属性
        if self.character == None: return '当前没有角色'
        if len(arg) == 0: return '请输入参数'
        if len(arg) % 2 != 0: return '参数数目错误'

        for i in range(0, len(arg), 2):
            if arg[i] == 'effect' or not arg[i+1][1:].isdigit() or not arg[i+1][0] in ['+', '-', '=']: return '参数值错误'
            else:
                # 修改属性值
                l = ['state', 'attr']
                for j in l:
                    if arg[i] in self.character[j]:
                        self.character[j][arg[i]] = operation(self.character[j][arg[i]], int(arg[i+1]), arg[i+1][0])
        self.save()
        return self.show_now_character()
    
    def add_effect(self, arg): # 添加效果
        if self.character == None: return '当前没有角色'
        if len(arg) == 0: return '请输入参数'
        new_effect = {}
        if arg[0] in self.character['state']['effect']:
            if not arg[1][1:].isdigit() or not arg[1][0] in ['+', '-', '=']: return '参数值错误'
            self.character['state']['effect'][arg[0]]['value'] = operation(self.character['state']['effect'][arg[0]]['value'], int(arg[1][1:]), arg[1][0])
            if arg[1][0] == '=' and len(arg) == 3:
                self.character['state']['effect'][arg[0]]['text'] = arg[2]
        else:
            if not arg[1][1:].isdigit() or not arg[1][0] == '=': return '参数值错误'
            new_effect['value'] = int(arg[1][1:])
            if len(arg) == 3:
                new_effect['text'] = arg[2]
            else:
                new_effect['text'] = ''
            self.character['state']['effect'][arg[0]] = new_effect
        self.save()
        return self.show_now_character()
    
    def delete_effect(self, arg): # 删除效果
        if self.character == None: return '当前没有角色'
        if len(arg) == 0: return '请输入参数'
        if arg[0] not in self.character['state']['effect']: return '效果不存在'
        del self.character['state']['effect'][arg[0]]
        self.save()
        return self.show_now_character()

    def create_card(self, arg): # 新建卡牌
        if self.character == None: return '当前没有角色'
        if len(arg) == 0: return '请输入参数'
        if arg[0] in self.character['cards']: return '卡牌已存在'
        card = {'name': arg[0]}
        if len(arg) == 2: card['attr'] = arg[1]
        else: card['attr'] = ''
        self.cards_list['list'].append(arg[0])
        json.dump(card, open(self.path + self.chracterlist['now'] + '/' + arg[0] + '.json', 'w', encoding='utf-8'))
        self.save()
        return self.show_card_list()
    
    def show_card_list(self, arg = []): # 显示卡牌列表
        if self.character == None: return '当前没有角色'
        return '\n' + ' '.join(self.cards_list['list'])
    
    def add_card(self, arg): # 添加卡牌
        if self.character == None: return '当前没有角色'
        if len(arg) == 0: return '请输入参数'
        if len(arg) % 2 != 0: return '参数数目错误'
        if not arg[0] in self.cards_list['list']: return '卡牌不存在'
        for i in range(0, len(arg), 2):
            if not arg[i+1].isdigit(): return '参数值错误'
            else:
                self.character['cards'][arg[i]] = int(arg[i+1])
        del_list = []
        for i in self.character['cards']:
            if self.character['cards'][i] == 0:
                del_list.append(i)
        for i in del_list:
            del self.character['cards'][i]
        if sum(self.character['cards'].values()) - self.character['cards']['基础卡'] < 15:
            self.character['cards']['基础卡'] = 15 - sum(self.character['cards'].values()) + self.character['cards']['基础卡']
        self.save()
        return self.show_now_character()
    
    def save_battle(self, arg = []): # 开始战斗
        if self.character == None: return '当前没有角色'
        Pile = {
            'draw_pile': self.Pile.draw_pile,
            'discard_pile': self.Pile.discard_pile,
            'exhausted_pile': self.Pile.exhausted_pile,
            'hand_pile': self.Pile.hand_pile,
        }
        json.dump(Pile, open(self.path + self.chracterlist['now'] + '/' + 'battle.json', 'w', encoding='utf-8'))
    
    def start_battle(self, arg = []): # 开始战斗
        self.save_battle()
        return '战斗开始'
    
    def end_battle(self, arg = []): # 结束战斗
        os.remove(self.path + self.chracterlist['now'] + '/' + 'battle.json')