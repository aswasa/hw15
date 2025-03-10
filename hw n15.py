import telebot
import buttons15
import db

bot=telebot.TeleBot('')


@bot.message_handler(commands=['start'])
def start(message):
    user_id=message.from_user.id
    if db.check_user(user_id):
        name=db.check_name(user_id)
        bot.send_message(user_id, f'Добро пожаловать {name}')
    else:
        bot.send_message(user_id, 'Привет!Давай пройдем регистрацию\nНапиши свое имя.')
        bot.register_next_step_handler(message, get_name)

@bot.message_handler(commands = ['help'])
def helper(message):
    user_id = message.from_user.id
    bot.send_message(user_id, 'Вот справочная информация;')


@bot.message_handler(content_types=['text'])
def get_name(message):
    user_id=message.from_user.id
    user_name=message.text
    bot.send_message(user_id, 'Теперь введи свой номер телефона!',  reply_markup=buttons15.num_button())
    bot.register_next_step_handler(message, get_num, user_name)

def get_num(message, user_name):
    user_id = message.from_user.id
    if message.contact:
        user_num = message.contact.phone_number
        bot.send_message(user_id, 'Теперь отправь свою локацию!', reply_markup=buttons15.loc_button())
        bot.register_next_step_handler(message, get_loc, user_name, user_num)
    else:
        bot.send_message(user_id, 'Оставьте номер через кнопку!')
        bot.register_next_step_handler(message, get_num, user_name)

def get_loc(message, user_name, user_num):
    user_id=message.from_user.id
    if message.location:
        user_loc1 = message.location.latitude
        user_loc2 = message.location.longitude
        db.register(user_id, user_name, user_num, user_loc1, user_loc2)
        bot.send_message(user_id, 'Регистрация прошла успешно!')
    else:
        bot.send_message(user_id, 'Отправьте локацию через кнопку!')
        bot.register_next_step_handler(message, get_loc, user_name, user_num)

bot.polling(none_stop=True)




