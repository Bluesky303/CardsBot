import cards

def handle(Pile: cards.CardPlie, order: list):
    dic1 = {
        '抽牌堆': Pile.show_draw_pile,
        '手牌': Pile.show_hand_pile,
        '弃牌堆': Pile.show_discard_pile,
        '消耗': Pile.show_exhausted_pile,
        '抽牌': Pile.draw,
        '使用': Pile.using,
        '弃牌': Pile.discard,
        '搜寻': Pile.search,
        '回收': Pile.reclaim,
        }
    if order[0] in dic1:
        return dic1[order[0]](order[1:])
    return None


    