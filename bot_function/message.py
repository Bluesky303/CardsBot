import aiohttp

async def send_msg(group_id, text):
    async with aiohttp.ClientSession() as session:
        await session.post(
            'http://localhost:3000/send_group_msg', 
            json = {
                'group_id': group_id,
                'message': text
            })

async def send_file(group_id, file, name):
    async with aiohttp.ClientSession() as session:
        await session.post(
            'http://localhost:3000/upload_group_file', 
            json={
                'group_id': group_id,
                'file': file,
                'name': name,
            })
        
def create_text_msg(text):
    return {
        'type': 'text',
        'data': {
            'text': text
        }
    }

def at_user(user_id):
    return {
        'type': 'at',
        'data': {
           'qq': user_id,
           'name': '不见了'
        }
    }