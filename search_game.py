from site_request import get_results


def search_game(game_id) -> list:
    result_list = get_results(game_id)
    return result_list


def make_str(games: list, with_cat=False) -> str:
    result = ''
    for game in games:
        category = '[' + game['category'] + ']' if with_cat else ''
        result += f"{game['title']} {category} \n " \
                  f"Покупка: {game['sell_price']} / Обмен: {game['trade_price']}\n"
    return result
