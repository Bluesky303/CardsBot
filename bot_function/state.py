import bot_function.func_cards, bot_function.func_jmcomic
import os

state_dic = {
    'cards': bot_function.func_cards.character_order,
    'jmcomic': bot_function.func_jmcomic.jmcomic_order
}

def switch_state(state):
    with open('./state.txt', 'w') as f:
        f.write(state)

def get_state():
    with open('./state.txt', 'r') as f:
        return f.read()

if not os.path.exists('./state.txt'):
    with open('./state.txt', 'w') as f:
        f.write('cards')