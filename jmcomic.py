import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
import aiohttp, asyncio
import time

import jmcomic

option = jmcomic.create_option_by_file("./option.yml")

app = FastAPI() 

async def file_upload(group_id, pid):
    async with aiohttp.ClientSession() as session:
        await session.post('http://localhost:3000/upload_group_file', 
                           json={
                              'group_id': group_id,
                              'file': f'file:///C:/Users/Blue_sky303/Arepo/FansNum/1/{pid}.pdf',
                              'name': f'{pid}.pdf',
                           })

@app.post("/onebot")
async def root(request: Request):
    data = await request.json()  # 获取事件数据
    print(data)
    if 'raw_message' in data and data['raw_message'][:4]=='/jm ':
        pid = data['raw_message'][4:]
        group_id = data['group_id']
        jmcomic.download_album(pid, option)
        await file_upload(group_id, pid)
    return {}

if __name__ == "__main__":
    uvicorn.run(app, port=8070)
