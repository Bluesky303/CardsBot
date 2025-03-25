import uvicorn
from fastapi import FastAPI, Request

import bot_function.state as state
import bot_function.message as message

app = FastAPI() 

state_now = 'battle'

@app.post("/onebot")
async def root(request: Request):
    data = await request.json()
    if 'raw_message' in data and data['raw_message'][0] == '/':
        group_id = data['group_id']
        user_id = data['user_id']
        order = data['raw_message'][1:].split(' ')
        try:
            if order[0] == '切换':
                state_now = order[1]
                text = {
                    'text': '切换成功'
                }
            else:
                await state.state_dic[state_now](group_id, user_id, order)
        except:
            text = {
                'text': '参数错误'
            }
        message.send_message(group_id, text)
if __name__ == "__main__":
    uvicorn.run(app, port=8070)
