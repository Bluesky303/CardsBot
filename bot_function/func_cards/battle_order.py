'''
处理战斗过程中的指令
'''

import traceback

from .cards import *
from ..message import *
from .character import *
async def battle_order(order: list, group_id, user_id):
    battle_dic_list = ['抽牌堆', '手牌', '弃牌堆', '消耗', '抽牌', '使用', '弃牌', '搜寻', '回收']
    if order[0] in battle_dic_list:
        P = Character(group_id, user_id) # 从文件创建角色并及时保存保证可中断
    battle_dic = { # 指令列表
        '抽牌堆': P.Pile.show_draw_pile,
        '手牌': P.Pile.show_hand_pile,
        '弃牌堆': P.Pile.show_discard_pile,
        '消耗': P.Pile.show_exhausted_pile,
        '抽牌': P.Pile.draw,
        '使用': P.Pile.using,
        '弃牌': P.Pile.discard,
        '搜寻': P.Pile.search,
        '回收': P.Pile.reclaim,
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
            text = [create_text_msg(f'当前{Piledata[0]}:\n' + '\n'.join([str(num) + ' ' + Piledata[1][num]['name'] for num in range(len(Piledata[1]))]))]
        else:
            text = [create_text_msg('指令错误')]
    except Exception as e:
        print(e)
        text = [create_text_msg('参数错误')]
        print(traceback.format_exc())
    
    await send_msg(group_id, text)
    

