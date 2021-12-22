import telebot
import config
from telebot import types 

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start'])
def hello(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = types.InlineKeyboardButton('Добавить', callback_data='1')
    markup.add(item1)

    bot.send_message(message.chat.id, 'Привет, {0.first_name}!\n Я бот-напоминалка о днях рождениях твоих родных и друзей. \n Я напомню в нужное время о необходимости поздравить друга, которого добавишь в список, а к концу ДР этого человека переспрошу поздравили ли вы его. Для начала нужно составить список людей о чьих днях рождениях напоминать, для этого нажми \"Добавить\"'.format(message.from_user, bot.get_me()), parse_mode='html', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.message:
        if call.data == '1':
            bot.send_message(call.message.chat.id, 'Введите имя:')

@bot.message_handler(content_types=['text'])
def next(message):
    bot.send_message(message.chat.id, 'Когда день рождения у ' + message.text + '? (в формате ДД.ММ)')


bot.polling(none_stop=True)