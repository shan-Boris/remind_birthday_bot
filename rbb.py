import telebot
import config
from telebot import types 

bot = telebot.TeleBot(config.TOKEN)

all_dr={}

markup2 = types.InlineKeyboardMarkup(row_width=2)
item1 = types.InlineKeyboardButton('Добавить ещё', callback_data='add')
item2 = types.InlineKeyboardButton('Весь список людей', callback_data='all')
item3 = types.InlineKeyboardButton('Удалить из списка', callback_data='del')
markup2.add(item1, item3, item2)
    
def get_ddmm(x):
    try:
        d, m = [int(s) for s in x.split('.')]
        if 0 <= d <= 31 and 0 <= m <= 12:
            return d, m
        else:
            return False
    except:
        return False


@bot.message_handler(commands=['start'])
def hello(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    item0 = types.InlineKeyboardButton('Добавить', callback_data='add')
    markup.add(item0)

    bot.send_message(message.chat.id, 'Привет, {0.first_name}!\n Я бот-напоминалка о днях рождениях твоих родных и друзей. \n Я напомню в нужное время о необходимости поздравить друга, которого добавишь в список, а к концу ДР этого человека переспрошу поздравили ли вы его. Для начала нужно составить список людей о чьих днях рождениях напоминать, для этого нажми \"Добавить\"'.format(message.from_user, bot.get_me()), parse_mode='html', reply_markup=markup)

run = False
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.message:
        if call.data == 'add':
            global run
            global name
            run = True
            name = False
            bot.send_message(call.message.chat.id, 'Введите имя:')
        if call.data == 'all':      # выводим весь список ДР, к последнему сообщению прикрепляем клавиатуру
            v=0
            n = len(all_dr.keys())
            for i in all_dr:
                v +=1
                if v != n:
                    bot.send_message(call.message.chat.id, f'{i} {all_dr[i]}')
                else:
                    bot.send_message(call.message.chat.id, f'{i} {all_dr[i]}', reply_markup=markup2)
    
        if call.data == 'del':      # удаляем чье-то др
            bot.send_message(call.message.chat.id, 'Вот кто в списке:')
            for i in all_dr:
                bot.send_message(call.message.chat.id, i)
            bot.send_message(call.message.chat.id, 'Кого удалить?')
            bot.message_handler(content_types=['text'])
            def del_dr(message):
                print('запуск')
                if message.text in all_dr.keys():
                    del all_dr[message.text]

@bot.message_handler(content_types=['text'])
def get_name(message):
    if run:
      
        global name
        if name == False:
            name = message.text
        bot.send_message(message.chat.id, f'Когда день рождения у {name}? (в формате ДД.ММ)',)
        bot.register_next_step_handler(message, get_dr)

def get_dr(message): #получаем дату др
    global dr
    dr = message.text
    if get_ddmm(dr) != False:
        
        run = False
        all_dr[name]=dr
        bot.send_message(message.from_user.id, f'Запомнил: ДР у {name} {dr} \n Я напомню в 9.00 {dr}, что у {name} день рождения, \n а в 23.00 спрошу: поздравили ли {name}', reply_markup=markup2)
   

    else:
        bot.send_message(message.from_user.id, 'Неверная дата')
        get_name(message)
    # bot.register_next_step_handler(message, get_surnme);
                



bot.polling(none_stop=True)


