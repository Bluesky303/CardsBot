import aiohttp
import jmcomic
import message

async def jmcomic_order(order, group_id, user_id):
    option = jmcomic.create_option_by_file("./option.yml")
    
    try: 
        if order[0] in jmcomic_dic:
            jmcomic_dic = {
                'jm': await jm(order, option),
            }
            text = await jmcomic_dic[order[0]]
        else:
            text = {
                'text': '指令错误'
            }
    except:
        text = {
            'text': '参数错误'
        }
    await message.send_msg(group_id, text)

async def jm(order, option, group_id):
    pid = order[1]
    
    jmcomic.download_album(pid, option)
    
    file = f'file:///C:/Users/Blue_sky303/Arepo/CardsBot/1/{pid}.pdf'
    await message.send_file(group_id, file, name=f'{pid}.pdf')
    
    text = {
        'text': '下载完成'
    }
    return text