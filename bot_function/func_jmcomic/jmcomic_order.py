import jmcomic
from ..message import *

async def jmcomic_order(order, group_id, user_id):
    option = jmcomic.create_option_by_file("./option.yml")
    
    try: 
        jmcomic_dic = {
            'jm': await jm(order, option, group_id, user_id),
        }
        if order[0] in jmcomic_dic:    
            text = jmcomic_dic[order[0]]
        else:
            text = [create_text_msg('指令错误')]
    except Exception as e:
        print(e)
        text = [create_text_msg('参数错误')]
    await send_msg(group_id, text)

async def jm(order, option, group_id, user_id):
    pid = order[1]
    
    jmcomic.download_album(pid, option)
    
    file = f'file:///C:/Users/Blue_sky303/Arepo/CardsBot/1/{pid}.pdf'
    await send_file(group_id, file, name=f'{pid}.pdf')
    
    text = [
        {
            'type': 'at',
            'data': {
                'qq': str(user_id),
                'name': '不见了'
            }
        },
        create_text_msg('下载完成')
    ]
    return text