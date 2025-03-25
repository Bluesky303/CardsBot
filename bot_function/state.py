import bot_function.func_cards, bot_function.func_jmcomic

state_dic = {
    ('cards', 'character'): bot_function.func_cards.character_order,
    ('cards', 'battle'):  bot_function.func_cards.battle_order,
    ('jmcomic'): bot_function.func_jmcomic.jmcomic_order
}
