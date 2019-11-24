import telebot as tb
import deserialize
from telebot import types
from random import randint

bot_token = "808248861:AAGOwZ8zaxh6qOO0t9h-N8JRF3yMilh2ioA"

def get_tags(tag_list, number_of_tags, database):
    """ вбивает теги """

    for i in range(number_of_statements):
        if database['quotes'][i]['tag'] not in tag_list:
            tag_list.append(statement_database['quotes'][i]['tag']);


# цитаты
statements_database_filename = 'statements_database.json'
statement_database = deserialize.read_data(statements_database_filename)
number_of_statements = len(statement_database['quotes'])
avaliable_statement_tags = []
get_tags(avaliable_statement_tags, number_of_statements, statement_database)


# стихи
poems_database_filename = 'poems_database.json'
poems_database = deserialize.read_data(poems_database_filename)
number_of_poems = len(poems_database['quotes'])
avaliable_poem_tags = []
get_tags(avaliable_poem_tags, number_of_poems, poems_database)


# биография
boigraphy_database_filename = 'biography_database.json'
biography_database = deserialize.read_data(boigraphy_database_filename)
length_of_boigraphy = len(poems_database['quotes'])

bot = tb.TeleBot(bot_token)

# основная панель кнопок
keyboard_commands_root = tb.types.ReplyKeyboardMarkup(True)
keyboard_commands_root.row("Цитата", "Стих", "Биография")

# кейборд для всплывающих тегов
tags_keyboard_panel = tb.types.ReplyKeyboardMarkup(True, True)


def choose_tag(message, avaliable_tags):
    """ создает панель кнопок с тегами """

    tags_keyboard_panel = tb.types.ReplyKeyboardMarkup(True, True)
    for tag in avaliable_tags:
        tags_keyboard_panel.row(tag)
    bot.send_message(message.chat.id, "По какой теме вы хотите услышать цитату?", reply_markup=tags_keyboard_panel)


@bot.message_handler(commands=['start'])
def send_greetings(message):
    """ Приветствует пользователя, если тот написал /start """

    bot.send_message(message.chat.id, "Приветствую тебя, мой друг", reply_markup=keyboard_commands_root)


@bot.message_handler(content_types=['text'])
def send_message(message):
    """ Обрабатывает нажатие кнопок """

    if message.text.lower() == "цитата":
        choose_tag(message, avaliable_statement_tags)

    elif message.text.lower() == "стих":
        choose_tag(message, avaliable_poem_tags)

    elif message.text.lower() == "биография":
        bot.send_message(message.chat.id, biography_database['quotes'][randint(0, length_of_boigraphy)]['text'])

    else:
        bot.send_message(message.chat.id, "что тебе еще надо, друг мой?", reply_markup=keyboard_commands_root)


@bot.message_handler(commands = ['switch'])
def switch(message):
    markup = tb.types.InlineKeyboardMarkup()
    switch_button = tb.types.InlineKeyboardButton(text='Try', switch_inline_query="Telegram")
    markup.add(switch_button)
    bot.send_message(message.chat.id, "Выбрать чат", reply_markup = markup)


print("Start")
bot.polling()