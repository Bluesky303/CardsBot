import uvicorn
from fastapi import FastAPI, Request
import aiohttp
import cards

import order as ord

app = FastAPI() 

def attack(damage):
    return {'attack': damage}

def defence(shield):
    return {'defence': shield}
card1 = cards.Card('attack', 'attack', 1, attack(6))
card2 = cards.Card('defence', 'defence', 2, defence(5))
Pile = cards.CardPlie([card1]*5+[card2]*5)

async def printPile(Piledata: tuple, group_id):
    text = {
        'text': f'当前{Piledata[0]}:\n' + '\n'.join([str(num) + Piledata[1][num].name for num in range(len(Piledata[1]))])
        }
    async with aiohttp.ClientSession() as session:
        reply = {
            'group_id': group_id,
            'message': [{
                'type': 'text',
                'data': text
            }]
        }
        await session.post('http://localhost:3000/send_group_msg', json=reply)

@app.post("/onebot")
async def root(request: Request):
    data = await request.json()
    if 'raw_message' in data and data['raw_message'][0] == '/':
        group_id = data['group_id']
        order = data['raw_message'][1:].split(' ')
        re = ord.handle(Pile, order)
        if re != None:
            await printPile(re, group_id)
        
if __name__ == "__main__":
    uvicorn.run(app, port=8070)
