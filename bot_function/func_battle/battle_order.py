from .cards import *
from ..message import *

battle_dic = ['抽牌堆', '手牌', '弃牌堆', '消耗', '抽牌', '使用', '弃牌', '搜寻', '回收']
character_dic = ['角色列表', '使用角色', '新建角色', '删除角色', '角色信息', '修改角色属性']

async def battle_order(order: list, group_id):
    battle_dic = {
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
            Piledata = battle_dic[order[0]](order[1:])
            text = {
                'text': f'当前{Piledata[0]}:\n' + '\n'.join([str(num) + Piledata[1][num].name for num in range(len(Piledata[1]))])
            }
        else:
            text = {
                'text': '指令错误'
            }
    except Exception as e:
        print(e)
        text = {
            'text': '参数错误'
        }
    
    await send_msg(group_id, text)
    
def attack(damage):
    return {'attack': damage}

def defence(shield):
    return {'defence': shield}
card1 = Card('attack', 'attack', 1, attack(6))
card2 = Card('defence', 'defence', 2, defence(5))
Pile = CardPlie([card1]*5+[card2]*5)


