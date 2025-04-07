'''
角色相关指令
'''
import traceback

from .character import *
from ..message import *
from .character import *

def help(arg):
    return '''
可用指令：
/help：查看帮助
1.非战斗状态
    /创建角色 <角色名> （没有角色请先创建一个以初始化）
    /角色状态 （目前作用是查看卡组） 
    /角色列表
    /切换角色 <角色名>
    /删除角色 <角色名>
    /新建卡牌 <卡牌名> <属性参数>（新建后才能添加进卡组，属性参数暂时仅支持“佚亡”，“回响”）
    /卡牌库 （查看拥有的卡牌）
    /卡牌 <卡牌名> <{符号}{数目}> （修改卡组，只能填入卡牌库中卡牌，数量为0即为去除，符号可选+, -, =）
    例如：/卡牌 打击 =1
    /删除卡牌 <卡牌名> （删除卡组中的卡牌）
    /开始（初始化牌堆）
2.战斗状态
    /结束
    /抽牌堆
    /手牌
    /弃牌堆
    /消耗（佚亡牌使用后）
    /抽牌 <数目> 
    /使用 <卡牌编号> 
    /弃牌 <卡牌编号1> <卡牌编号2> ..
    /搜寻 <卡牌名> （从抽牌堆中获取一张对应名字的牌）
    /回收 <卡牌名> （从弃牌堆中获取一张对应名字的牌）
'''



async def character_order(order, group_id, user_id):
    character_dic_list = ['角色状态', '角色列表', '创建角色', '切换角色', '修改角色属性', '删除角色', '添加效果', '删除效果', '卡牌', '新建卡牌', '卡牌库', '删除卡牌', '开始', 'help']
    battle_dic_list = ['抽牌堆', '手牌', '弃牌堆', '消耗', '抽牌', '使用', '弃牌', '搜寻', '回收', '结束', 'help']
    if order[0] in character_dic_list + battle_dic_list:
        P = Character(group_id, user_id) # 从文件创建角色并及时保存保证可中断
    else:
        return [create_text_msg('指令错误')]
    
    def start(arg):
        P.start_battle()
        return '战斗开始'
    
    def end(arg):
        P.end_battle()
        return '战斗结束'

    character_dic = {
        '角色状态': P.show_now_character, 
        '角色列表': P.show_character_list,
        '创建角色': P.create_character,
        '切换角色': P.switch_character,
        '修改角色属性': P.modify_character_attr,
        '删除角色': P.delete_character,
        '添加效果': P.add_effect,
        '删除效果': P.delete_effect,
        '卡牌': P.add_card,
        '新建卡牌': P.create_card,
        '卡牌库': P.show_card_list,
        '删除卡牌': P.delete_card,
        '开始': start,
        'help': help,
    }
    if not P.character == None:
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
            '结束': end,
            'help': help,
        }
    try:
        if P.onbattle:
            if not order[0] in battle_dic_list: return [at_user(user_id), create_text_msg(' ' + '战斗中无法进行此操作')]
            Piledata = battle_dic[order[0]](order[1:]) # 执行指令，返回值都是牌堆列表，表示需要展示牌堆信息
            '''
            例如：
            当前抽牌堆：
            0 打击*5
            1 防御*5
            '''
            if order[0] == '结束': 
                return [at_user(user_id), create_text_msg(' ' + Piledata)]
            else:
                P.save_battle()
                return [at_user(user_id), create_text_msg(f' 当前{Piledata[0]}:\n' + '\n'.join([str(num) + ' ' + Piledata[1][num]['name'] for num in range(len(Piledata[1]))]))]
        else:
            if not order[0] in character_dic_list: return [at_user(user_id), create_text_msg(' ' + '非战斗状态无法进行此操作')]
            CharacterData = character_dic[order[0]](order[1:])
            return [at_user(user_id), create_text_msg(' ' + CharacterData)]
    except Exception as e:
        print(traceback.format_exc())
        return [at_user(user_id), create_text_msg(' ' + '参数错误')]
    