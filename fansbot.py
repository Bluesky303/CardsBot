import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
import aiohttp, asyncio
import time

async def readfile():
    with open('num.txt', 'r', encoding='utf-8') as f:
        return f.readlines()

async def writefile(l, num):
    with open('num.txt', 'w', encoding='utf-8') as f:
        f.writelines(l)
        f.write('\n')
        f.write(f'{num},{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}') 

async def GetFansNum():
    """
    获取粉丝数
    40462777
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 Edg/133.0.0.0'
    }
    url = 'https://api.bilibili.com/x/web-interface/card'
    params = {
        'mid': 40462777,
    }
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, headers=headers, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    num = data['data']['follower']
                    return num
                else:
                    print(f"Error: {response.status}")
                    return None
        except Exception as e:
            print(f"Exception: {e}")
            return None

async def reply():
    """
    粉丝数达到一定量时推送
    """
    l = await readfile()
    async with aiohttp.ClientSession() as session:
        num = await GetFansNum()
        if l[-1].split(',')[0] != str(num) and num != None and num%10 == 0:
            try:
                reply = {
                    'group_id': 1034706563,
                    'message': [{
                        'type': 'text',
                        'data': {
                            'text': '粉丝数达到了：' + str(num) + '!!!'
                        }
                    }]
                }
                async with session.post('http://127.0.0.1:3000/send_group_msg', json = reply) as response:
                    if response.status == 200:
                        print(f"Success: {response.status}") 
                await writefile(l, num)
            except Exception as e:
                print(f"Exception: {e}")
                return None

async def get_fans_num_loop():
    """
    循环调用
    """
    while True:
        await reply()
        await asyncio.sleep(1)  # 每1秒调用一次

@asynccontextmanager
async def get_fans_num(app: FastAPI):
    # 在应用启动时启动异步循环
    app.state.fans_num_loop = asyncio.create_task(get_fans_num_loop())
    
    yield
    app.state.fans_num_loop.cancel()
    try:
        await app.state.fans_num_loop
    except asyncio.CancelledError:
        pass
    
app = FastAPI(lifespan=get_fans_num) 

@app.post("/onebot")
async def root(request: Request):
    data = await request.json()  # 获取事件数据
    if 'raw_message' in data and data['raw_message']=='粉丝数':
        num = await GetFansNum()
        if num == -1:
            return {'reply': '获取失败'}
        else:
            return {'reply': '当前粉丝数：' + str(num)}
    return {}

if __name__ == "__main__":
    uvicorn.run(app, port=8070)

