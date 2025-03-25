import uvicorn
from fastapi import FastAPI, Request

import bot_function.state as state
import bot_function.message as message

app = FastAPI() 

state_now = 'battle'

@app.post("/onebot")
async def root(request: Request):
    global state_now
    data = await request.json()
    if 'raw_message' in data and data['raw_message'][0] == '/':
        group_id = data['group_id']
        user_id = data['user_id']
        order = data['raw_message'][1:].split(' ')
        try:
            if order[0] == '切换' and user_id == 506473613:
                state_now = order[1]
                text = {
                    'text': '切换成功'
                }
            elif order[0] == '状态':
                text = {
                    'text': '当前状态为' + state_now
                }
            else:
                await state.state_dic[state_now](group_id, user_id, order)
        except Exception as e:
            print(e)
            text = {
                'text': '参数错误'
            }
        await message.send_msg(group_id, text)
if __name__ == "__main__":
    uvicorn.run(app, port=8070)
