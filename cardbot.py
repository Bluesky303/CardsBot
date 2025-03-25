import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
import aiohttp, asyncio
import time
import cards

app = FastAPI() 

def attack(damage):
    return {'attack': damage}

def defence(shield):
    return {'defence': shield}
card1 = cards.Card('attack', 'attack', 1, attack(6))
card2 = cards.Card('defence', 'defence', 2, defence(5))
Pile = cards.CardPlie([card1]*5+[card2]*5)

def handle(Pile: cards.CardPlie, order: list):
    dic1 = {
        '抽牌堆': Pile.show_draw_pile,
        '手牌': Pile.show_hand_pile,
        '弃牌堆': Pile.show_discard_pile,
        '消耗': Pile.show_exhausted_pile,
    }
    dic2 = {
        '抽牌': Pile.draw,
        '使用': Pile.using,
        '弃牌': Pile.discard,
        '搜寻': Pile.search,
        '回收': Pile.reclaim,
        }
    if order[0] in dic1:
        return dic1[order[0]]()
    if order[0] in dic2:
        return dic2[order[0]](int(order[1]))
    return None

async def printPile(Piledata: tuple, group_id):
    async with aiohttp.ClientSession() as session:
        reply = {
            'group_id': group_id,
            'message': [{
                'type': 'text',
                'data': {
                    'text': f'当前{Piledata[0]}:' + ' '.join([card.name for card in Piledata[1]])
                }
            }]
        }
        await session.post('http://localhost:3000/send_group_msg', json=reply)
    

@app.post("/onebot")
async def root(request: Request):
    data = await request.json()
    if 'raw_message' in data and data['raw_message'][0] == '/':
        group_id = data['group_id']
        order = data['raw_message'][1:].split(' ')
        re = handle(Pile, order)
        if re != None:
            await printPile(re, group_id)
        
if __name__ == "__main__":
    uvicorn.run(app, port=8070)
    
# import cards
# import random
# import copy
# def attack(damage):
#     return {'attack': damage}

# def defence(shield):
#     return {'defence': shield}

# def print1(Pile):
#     for card in Pile:
#         print(card.name, end=' ')
#     print()

# if __name__ == "__main__":
#     card1 = cards.Card('attack', 'attack', 1, attack(6))
#     card2 = cards.Card('defence', 'defence', 2, defence(5))
#     Pile = cards.CardPlie([card1]*5+[card2]*5)
#     print1(Pile.show_draw_pile())
#     Pile.draw(5)
#     print1(Pile.show_hand_pile())
#     Pile.using(2)
#     print1(Pile.show_hand_pile())
#     Pile.discard(2)
#     print1(Pile.show_hand_pile())
#     print1(Pile.show_discard_pile())
        