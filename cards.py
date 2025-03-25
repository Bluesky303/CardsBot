import random

class Card:
    def __init__(self, name, type, value, func):
        self.name = name
        self.type = type
        self.value = value
        self.func = func
    
    def played(self):
        self.func
        return self.type
    
    def draw(self):
        pass
    
class CardPlie:
    def __init__(self, cards):
        random.shuffle(cards)
        self.draw_pile = cards
        self.discard_pile = []
        self.hand_pile = []
        self.exhausted_pile = []
    
    def show_draw_pile(self):
        return ('抽牌堆', sorted(self.draw_pile, key = lambda x: x.name))
    
    def show_discard_pile(self):
        return ('弃牌堆', self.discard_pile)
    
    def show_hand_pile(self):
        return ('手牌', self.hand_pile)
    
    def show_exhausted_pile(self):
        return ('被消耗的牌', self.exhausted_pile)
    
    def draw(self, num):
        if len(self.draw_pile) < num:
            random.shuffle(self.discard_pile)
            self.draw_pile += self.discard_pile
        self.hand_pile += self.draw_pile[:num]
        self.draw_pile = self.draw_pile[num:]
        return ('手牌', self.hand_pile)
    
    def using(self, cardnum):
        self.hand_pile[cardnum].played()
        self.discard_pile += [self.hand_pile[cardnum]]
        self.hand_pile = self.hand_pile[:cardnum] + self.hand_pile[cardnum+1:]
        return ('手牌', self.hand_pile)
        
    def discard(self, cardnum):
        self.discard_pile += [self.hand_pile[cardnum]]
        self.hand_pile = self.hand_pile[:cardnum] + self.hand_pile[cardnum+1:]
        return ('手牌', self.hand_pile)
        
    def search(self, name):
        temp_draw = []
        for i in range(len(self.draw_pile)):
            if self.draw_pile[i].name == name:
                temp_draw.append(self.draw_pile[i], i)
        random.shuffle(temp_draw)
        self.draw_pile = self.draw_pile[:temp_draw[0][1]] + self.draw_pile[temp_draw[0][1]+1:]
        self.hand_pile += [temp_draw[0][0]]
        return ('手牌', self.hand_pile)
    
    def reclaim(self, name):
        for i in range(len(self.discard_pile)):
            if self.discard_pile[i].name == name:
                self.draw_pile += [self.discard_pile[i]]
                self.discard_pile = self.discard_pile[:i] + self.discard_pile[i+1:]
        return ('手牌', self.hand_pile)
    


        
    

    