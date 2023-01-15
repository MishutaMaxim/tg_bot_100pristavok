import telebot
import wikipedia

from config import API_KEY
from search_game import search_game, make_str
from telebot import types

bot = telebot.TeleBot(API_KEY)

SEARCH_RESULT = []
CATEGORIES = set()


# Функция, обрабатывающая команду /start
@bot.message_handler(commands=["start"])
def start(m, res=False):
    bot.send_message(m.chat.id, 'Отправьте мне название игры')


# Получение сообщений от юзера
@bot.message_handler(content_types=["text"])
def handle_text(message):
    global SEARCH_RESULT
    global CATEGORIES
    SEARCH_RESULT = search_game(message.text)
    CATEGORIES = set([i['category'] for i in SEARCH_RESULT or []])
    if not SEARCH_RESULT:
        bot.send_message(message.chat.id, 'Ничего не найдено')
    elif len(CATEGORIES) < 2:
        search_result_str = make_str(SEARCH_RESULT, with_cat=True)
        bot.send_message(message.chat.id, search_result_str)
    else:
        keyboard = types.InlineKeyboardMarkup()
        for cat in CATEGORIES:
            key = types.InlineKeyboardButton(text=cat, callback_data=cat)
            keyboard.add(key)
        all_key = types.InlineKeyboardButton(text='Показать все', callback_data='show_all')
        keyboard.add(all_key)
        bot.send_message(message.chat.id, 'Игра найдена в нескольких категориях, выберите нужную', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "show_all":
        search_result_str = make_str(SEARCH_RESULT, with_cat=True)
        bot.send_message(call.message.chat.id, search_result_str)
    elif call.data in CATEGORIES:
        filtered_result = [item for item in SEARCH_RESULT if item['category'] == call.data]
        search_result_str = make_str(filtered_result)
        bot.send_message(call.message.chat.id, search_result_str)


# Запускаем бота
bot.polling(none_stop=True, interval=0)
