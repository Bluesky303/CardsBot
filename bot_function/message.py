import aiohttp

async def send_msg(group_id, text):
    async with aiohttp.ClientSession() as session:
        await session.post(
            'http://localhost:3000/send_group_msg', 
            json = {
                'group_id': group_id,
                'message': [{
                    'type': 'text',
                    'data': text
                }]
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