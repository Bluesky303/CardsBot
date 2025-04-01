'''
处理战斗过程中的指令
'''



from .cards import *
from ..message import *

async def battle_order(order: list, group_id, user_id):
    battle_dic = { # 指令列表
        '抽牌堆': Pile.show_draw_pile,
        '手牌': Pile.show_hand_pile,
        '弃牌堆': Pile.show_discard_pile,
        '消耗': Pile.show_exhausted_pile,
        '抽牌': Pile.draw,
        '使用': Pile.using,
        '弃牌': Pile.discard,
        '搜寻': Pile.search,
        '回收': Pile.reclaim,
    }
   
    try:
        if order[0] in battle_dic:
            Piledata = battle_dic[order[0]](order[1:]) # 执行指令，返回值都是牌堆列表，表示需要展示牌堆信息
            '''
            例如：
            当前抽牌堆：
            0 打击*5
            1 防御*5
            '''
            text = [create_text_msg(f'当前{Piledata[0]}:\n' + '\n'.join([str(num) + ' ' + Piledata[1][num].name for num in range(len(Piledata[1]))]))]
        else:
            text = [create_text_msg('指令错误')]
    except Exception as e:
        print(e)
        text = [create_text_msg('参数错误')]
    
    await send_msg(group_id, text)
    
def attack(damage):
    return {'attack': damage}

def defence(shield):
    return {'defence': shield}
card1 = Card({
    'name': 'attack',
    'type': 'attack',
    'value': 1, 
    'func': attack(6)
    })
card2 = Card({
    'name': 'defence',
    'type': 'defence',
    'value': 2, 
    'func': defence(6)
    })
Pile = CardPile([card1]*5+[card2]*5)


