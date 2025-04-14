'''
卡牌和牌堆类
'''

import random

class Card:
    def __init__(self, path):
        '''
        初始化，输入路径
        name: 名字
        type: 类型列表
        func_self: 对牌堆和回合有影响的功能，子功能列表[]
            子功能: 功能函数
        func_character: 对角色作用的功能, 子功能列表[]
            子功能: 字典 
                {
                    'character': 作用对象，列表
                    'func': 效果函数 
                }
        '''
        
    
class CardPile:
    def __init__(self, cards, new_cards=[]):
        random.shuffle(cards)
        self.draw_pile = cards
        self.discard_pile = []
        self.hand_pile = []
        self.exhausted_pile = []
        self.new_pile = new_cards
    def show_draw_pile(self, arg = []):
        dic = {}
        for i in range(len(self.draw_pile)):
            if self.draw_pile[i]['name'] in dic:
                dic[self.draw_pile[i]['name']] += 1
            else:
                dic[self.draw_pile[i]['name']] = 1
        l = [{'name': f'{key}*{value}'} for key, value in dic.items()]
        return ('抽牌堆', sorted(l, key = lambda x: x['name']))
    
    def show_discard_pile(self, arg = []):
        return ('弃牌堆', self.discard_pile)
    
    def show_hand_pile(self, arg = []):
        return ('手牌', self.hand_pile)
    
    def show_exhausted_pile(self, arg = []):
        return ('被消耗的牌', self.exhausted_pile)
    
    def draw(self, arg):
        num = int(arg[0])
        if len(self.draw_pile) < num:
            random.shuffle(self.discard_pile)
            self.draw_pile += self.discard_pile
            self.discard_pile = []
        self.hand_pile += self.draw_pile[:num]
        self.draw_pile = self.draw_pile[num:]
        return ('手牌', self.hand_pile)
    
    def using(self, arg):
        cardnum = int(arg[0])
        name = self.hand_pile[cardnum]['name']
        a = ()
        if self.hand_pile[cardnum]['attr'] == '佚亡' or self.hand_pile[cardnum]['name'] == '岩·天·使':
            self.exhausted_pile += [self.hand_pile[cardnum]]
            a = ('佚亡', )
        else:
            self.discard_pile += [self.hand_pile[cardnum]]
        if self.hand_pile[cardnum]['attr'][:2] == '创造':
            for i in self.new_pile:
                if i['name'] == self.hand_pile[cardnum]['attr'][2:]:
                    self.hand_pile += [i]
                    a = ('创造', i['name'])
                    break
        self.hand_pile = self.hand_pile[:cardnum] + self.hand_pile[cardnum+1:]
        re = ('手牌', self.hand_pile, name) + a
        return re
        
    def discard(self, arg):
        intermidiate = []
        bcardnum = 0
        for cardnum in arg:
            cardnum = int(cardnum)
            intermidiate += self.hand_pile[bcardnum:cardnum]
            self.discard_pile += [self.hand_pile[cardnum]]
            bcardnum = cardnum + 1    
        self.hand_pile = intermidiate + self.hand_pile[bcardnum:]
        return ('手牌', self.hand_pile)
        
    def search(self, arg):
        name = arg[0]
        temp_draw = []
        for i in range(len(self.draw_pile)):
            if self.draw_pile[i]['name'] == name:
                temp_draw.append((self.draw_pile[i], i))
        random.shuffle(temp_draw)
        self.draw_pile = self.draw_pile[:temp_draw[0][1]] + self.draw_pile[temp_draw[0][1]+1:]
        self.hand_pile += [temp_draw[0][0]]
        return ('手牌', self.hand_pile)
    
    def reclaim(self, arg):
        name = arg[0]
        temp_draw = []
        for i in range(len(self.discard_pile)):
            if self.discard_pile[i]['name'] == name:
                temp_draw.append((self.discard_pile[i], i))
        random.shuffle(temp_draw)
        self.discard_pile = self.discard_pile[:temp_draw[0][1]] + self.discard_pile[temp_draw[0][1]+1:]
        self.hand_pile += [temp_draw[0][0]]
        return ('手牌', self.hand_pile)
    
    def turn_end(self, arg):
        temp_exhausted = []
        for i in range(len(self.discard_pile)):
            if self.discard_pile[i]['attr'] == '回响':
                self.discard_pile[i]['attr'] = '佚亡'
                temp_exhausted.append((self.discard_pile[i], i))
        random.shuffle(temp_exhausted)
        for i in temp_exhausted:
            self.discard_pile = self.discard_pile[:i[1]] + self.discard_pile[i[1]+1:]
            self.draw_pile = [i[0]] + self.draw_pile
        return ('回合结束', [x[0] for x in temp_exhausted])
        
    

    