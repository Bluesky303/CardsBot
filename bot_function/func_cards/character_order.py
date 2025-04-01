'''
角色相关指令，主要用于战斗外场景
'''

from .character import *
from ..message import *
from .character import *

async def character_order(order, group_id, user_id):
    character_dic_list = ['角色状态', '角色列表', '创建角色', '切换角色', '修改角色属性', '添加效果', '删除效果', '卡牌', '新建卡牌', '卡牌库', '开始战斗']
    if order[0] in character_dic_list:
        P = Character(group_id, user_id) # 从文件创建角色并及时保存保证可中断
    else:
        return [create_text_msg('指令错误')]
    
    def start():
        P.start_battle()
        with open('../../state.txt', 'w') as f:
            f.write('cards battle')
        return [create_text_msg('战斗开始')]
    character_dic = {
        '角色状态': P.show_now_character, 
        '角色列表': P.show_character_list,
        '创建角色': P.create_character,
        '切换角色': P.switch_character,
        '修改角色属性': P.modify_character_attr,
        '添加效果': P.add_effect,
        '删除效果': P.delete_effect,
        '卡牌': P.add_card,
        '新建卡牌': P.create_card,
        '卡牌库': P.show_card_list,
        '开始战斗': start,
    }
    
    try:
        CharacterData = character_dic[order[0]](order[1:])
        return [at_user(user_id), create_text_msg(' ' + CharacterData)]
    except Exception as e:
        print(e)
        return [at_user(user_id), create_text_msg(' ' + '参数错误')]
    