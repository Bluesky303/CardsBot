import uvicorn
from fastapi import FastAPI, Request

import bot_function.state as state
import bot_function.message as message

app = FastAPI() 

Characters = {}

@app.post("/onebot")
async def root(request: Request):
    global Characters
    iftext = True
    data = await request.json()
    if 'raw_message' in data and data['raw_message'][0] == '/':
        group_id = data['group_id']
        user_id = data['user_id']
        order = data['raw_message'][1:].split(' ')
        try:
            if order[0] == '切换' and user_id == 506473613:

                state.switch_state(tuple(order[1:]))
                text = [message.create_text_msg('状态切换为: ' + ' '.join(order[1:]))]
                
            elif order[0] == '状态':
                text = [message.create_text_msg('当前状态为: ' + ' '.join(state.get_state()))]
                
            else:
                text = await state.state_dic[state.get_state()](order, group_id, user_id)
                
        except Exception as e:
            print(e)
            text = [message.create_text_msg('指令错误')]
            
        await message.send_msg(group_id, text)

if __name__ == "__main__":
    uvicorn.run(app, port=8070)
