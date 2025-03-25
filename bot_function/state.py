import bot_function.func_cards, bot_function.func_jmcomic
import os

state_dic = {
    ('cards', 'character'): bot_function.func_cards.character_order,
    ('cards', 'battle'):  bot_function.func_cards.battle_order,
    ('jmcomic'): bot_function.func_jmcomic.jmcomic_order
}

def switch_state(state: tuple):
    with open('./state.txt', 'w') as f:
        f.write(' '.join(state))

def get_state():
    with open('./state.txt', 'r') as f:
        return tuple(f.read().split(' '))

if not os.path.exists('./state.txt'):
    with open('./state.txt', 'w') as f:
        f.write('cards character')