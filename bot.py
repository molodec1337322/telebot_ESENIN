import telebot as tb
import deserialize
from telebot import types
from random import randint

bot_token = "808248861:AAGOwZ8zaxh6qOO0t9h-N8JRF3yMilh2ioA"

def get_tags(tag_list, number_of_tags, database):
    """ вбивает теги """

    for i in range(number_of_tags):
        if database['quotes'][i]['tag'] not in tag_list:
            tag_list.append(database['quotes'][i]['tag']);


def tag_data(dict_to_tag, number_of_tags, database):
    """ распределяет текст по тегам в словаре """

    data = database['quotes']
    for i in range(len(data)):
        if data[i]['tag'] not in dict_to_tag:
            temp_dict = {data[i]['tag'] : [data[i]['text']]}
            dict_to_tag.update(temp_dict)

        else:
            print(data[i]['tag'])
            temp_text_list = dict_to_tag[data[i]['tag']]['text']
            temp_text_list.append(data[i]['text'])
            dict_to_tag[data[i]['tag']][temp_text_list]

    print(dict_to_tag)


# цитаты
quotes_database_filename = 'quotes_database.json'
quotes_database = deserialize.read_data(quotes_database_filename)
number_of_quotes = len(quotes_database['quotes'])
avaliable_quotes_tags = []
tagged_quotes = {}
get_tags(avaliable_quotes_tags, number_of_quotes, quotes_database)
#tag_data(tagged_quotes, number_of_quotes, quotes_database)


# стихи
poems_database_filename = 'poems_database.json'
poems_database = deserialize.read_data(poems_database_filename)
number_of_poems = len(poems_database['poems'])


# биография
boigraphy_database_filename = 'biography_database.json'
biography_database = deserialize.read_data(boigraphy_database_filename)
length_of_boigraphy = len(biography_database['facts'])

bot = tb.TeleBot(bot_token)

# основная панель кнопок
keyboard_commands_root = tb.types.ReplyKeyboardMarkup(True)
keyboard_commands_root.row("Цитата", "Стих", "Биография")


def choose_tag(message, avaliable_tags, selecteg_theme):
    """ создает панель кнопок с тегами """

    tags_keyboard_panel = tb.types.InlineKeyboardMarkup(row_width=2)
    for tag in avaliable_tags:
        button = tb.types.InlineKeyboardButton(text=tag, callback_data=tag)
        tags_keyboard_panel.add(button)
    bot.send_message(message.chat.id, "Выбери, о чем бы ты хотел услышать {0}".format(selecteg_theme),
                     reply_markup=tags_keyboard_panel)


@bot.callback_query_handler(func=lambda call:True)
def click_on_tag(call):
    """ Обработка нажатия inline кнопок """

    bot.send_message(call.message.chat.id, quotes_database['quotes'][randint(0, number_of_quotes)]['text'])


@bot.message_handler(commands=['start'])
def send_greetings(message):
    """ Приветствует пользователя, если тот написал /start """

    bot.send_message(message.chat.id, "Приветствую тебя, мой друг", reply_markup=keyboard_commands_root)


def send_poem(message):
    """ пытается отослать стих пользователю """

    try:
        bot.send_message(message.chat.id, poems_database['poems'][randint(0, number_of_poems)]['text'])
    except:
        send_poem(message)


def send_biography(message):
    """ Отсылает пользователю факты из биографии """

    try:
        bot.send_message(message.chat.id, biography_database['facts'][randint(0, length_of_boigraphy)]['text'])
    except:
        send_biography(message)


@bot.message_handler(content_types=['text'])
def send_message(message):
    """ Обрабатывает нажатие кнопок """

    if message.text.lower() == "цитата":
        try:
            choose_tag(message, avaliable_quotes_tags, "цитату")
        except:
            bot.send_message(message.chat.id, "Попробуйте еще раз")

    elif message.text.lower() == "стих":
        send_poem(message)

    elif message.text.lower() == "биография":
        send_biography(message)


@bot.message_handler(commands = ['switch'])
def switch(message):
    markup = tb.types.InlineKeyboardMarkup()
    switch_button = tb.types.InlineKeyboardButton(text='Try', switch_inline_query="Telegram")
    markup.add(switch_button)
    bot.send_message(message.chat.id, "Выбрать чат", reply_markup = markup)


print("Start")

bot.polling()
