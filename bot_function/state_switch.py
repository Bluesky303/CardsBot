import os

def switch_state(state: tuple):
    with open('./state.txt', 'w') as f:
        f.write(' '.join(state))

def get_state():
    with open('./state.txt', 'r') as f:
        return tuple(f.read().split(' '))

if not os.path.exists('./state.txt'):
    with open('./state.txt', 'w') as f:
        f.write('cards character')