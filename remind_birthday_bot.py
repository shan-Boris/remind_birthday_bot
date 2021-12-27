import telebot
import config
from telebot import types 
import json

bot = telebot.TeleBot(config.TOKEN)

all_dr={}

markup2 = types.InlineKeyboardMarkup(row_width=2)           # клавиатура для дальнейших действий
item1 = types.InlineKeyboardButton('Добавить ещё', callback_data='add')
item2 = types.InlineKeyboardButton('Список дней рождений', callback_data='all')
item3 = types.InlineKeyboardButton('Удалить из списка', callback_data='del')
markup2.add(item1, item3, item2)
    
def get_ddmm(x):                # проверка правильности введенной даты ДР
    try:
        d, m = [int(s) for s in x.split('.')]
        if 0 <= d <= 31 and 0 <= m <= 12:
            return d, m
        else:
            return False
    except:
        return False


@bot.message_handler(commands=['start'])        # Действия при подключение нового пользователя
def hello(message):
    global all_dr
    markup = types.InlineKeyboardMarkup(row_width=1)
    item0 = types.InlineKeyboardButton('Добавить', callback_data='add')
    markup.add(item0)
    with open(f'{message.chat.id}.json', "w") as f:     # Создание словаря ДР пользователя
        f.write(json.dumps(all_dr))

    with open(f'{message.chat.id}.json', "r") as e:     
        all_dr = json.loads(str(e.read()))
    bot.send_message(message.chat.id, 'Привет, {0.first_name}!\n Я бот-запоминалка о днях рождениях твоих родных и друзей. \n Я запомню все дни рождения людей, которых ты добавишь в список и теперь ты сможешь всегда посмотреть когда точно у кого ДР. \n Для начала нужно составить список людей чьи ДР запомнить, для этого нажми \"Добавить\"'.format(message.from_user, bot.get_me()), parse_mode='html', reply_markup=markup)
    

run = False
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    global all_dr 
    if call.message:
        if call.data == 'add':      # ответ на кнопку "добавить" или "добавить ещё"
            global run
            global name
            run = True
            name = False
            bot.send_message(call.message.chat.id, 'Введите имя:')
        if call.data == 'all':      # выводим весь список ДР, к последнему сообщению прикрепляем клавиатуру для дальнейших действий
            v=0
            with open(f'{call.message.chat.id}.json', "r") as e:
                all_dr = json.loads(str(e.read()))

            n = len(all_dr.keys())
            for i in all_dr:
                v +=1
                if v != n:
                    bot.send_message(call.message.chat.id, f'{i} {all_dr[i]}')
                else:
                    bot.send_message(call.message.chat.id, f'{i} {all_dr[i]}', reply_markup=markup2)
    
        if call.data == 'del':      # удаляем чье-то др
            markup3 = types.InlineKeyboardMarkup(row_width=2)
            with open(f'{call.message.chat.id}.json', "r") as e:
                all_dr = json.loads(str(e.read()))

            for i in all_dr:
                i = types.InlineKeyboardButton(i, callback_data=i)
                markup3.add(i)
            bot.send_message(call.message.chat.id, 'Кого удалить?',reply_markup=markup3)
        if call.data in all_dr:
            del all_dr[call.data]
            with open(f'{call.message.chat.id}.json', "w") as f:
                f.write(json.dumps(all_dr))
            bot.send_message(call.message.chat.id, f'Больше дня рождения {call.data} в списке нет', reply_markup=markup2)


@bot.message_handler(content_types=['text'])
def get_name(message):
    
    if run:
      
        global name
        if name == False:
            name = message.text
        bot.send_message(message.chat.id, f'Когда день рождения у {name}? (в формате ДД.ММ)',)
        bot.register_next_step_handler(message, get_dr)

def get_dr(message):            
    global dr
    global run
    dr = message.text
    if get_ddmm(dr) != False:           # если дата введена верно, то добавляем в словарь ДР
        
        run = False
        with open(f'{message.from_user.id}.json', "r") as e:
            all_dr = json.loads(str(e.read()))
        all_dr[name] = dr
        with open(f'{message.from_user.id}.json', "w") as f:
            f.write(json.dumps(all_dr))
        bot.send_message(message.from_user.id, f'Запомнил: ДР у {name} {dr}', reply_markup=markup2)
   

    else:
        bot.send_message(message.from_user.id, 'Неверная дата')
        get_name(message)
                



bot.polling(none_stop=True)

