import battle_order, character_order, jmcomic_order

async def character(order, group_id, user_id):
    await character_order.character_order(order, group_id, user_id)

async def battle(Pile, order, group_id, user_id):
    await battle_order.battle_order(Pile, order, group_id, user_id)

async def jmcomic(order, group_id, user_id):
    await jmcomic_order.jmcomic_order(order, group_id, user_id)
    