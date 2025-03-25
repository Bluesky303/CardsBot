import uvicorn
from fastapi import FastAPI, Request

import bot_function.state as state
import bot_function.message as message
from bot_function.state_switch import switch_state, get_state

app = FastAPI() 


@app.post("/onebot")
async def root(request: Request):
    global state_now
    iftext = True
    data = await request.json()
    if 'raw_message' in data and data['raw_message'][0] == '/':
        group_id = data['group_id']
        user_id = data['user_id']
        order = data['raw_message'][1:].split(' ')
        try:
            if order[0] == '切换' and user_id == 506473613:

                switch_state(tuple(order[1:]))
                text = [message.create_text_msg('状态切换为: ' + ' '.join(order[1:]))]
                
            elif order[0] == '状态':
                text = [message.create_text_msg('当前状态为: ' + ' '.join(get_state()))]
                
            else:
                await state.state_dic[get_state()](order, group_id, user_id)
                iftext = False
                
        except Exception as e:
            print(e)
            text = [message.create_text_msg('指令错误')]
            
        if iftext:
            await message.send_msg(group_id, text)

if __name__ == "__main__":
    uvicorn.run(app, port=8070)
