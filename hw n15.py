import telebot
import buttons15
import db
from db import *

bot=telebot.TeleBot('8094077086:AAH53wloVRhjpXsQffLZqpI5q1kE_aH4BfI')
temp_data = {}
admin_data={}
admins = []


@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    if db.check_user(user_id):
        name = db.check_name(user_id)
        bot.send_message(user_id, f'Добро пожаловать {name}. Что вы хотите сделать?', reply_markup=buttons15.to_do())
        bot.register_next_step_handler(message, action)
    else:
        bot.send_message(user_id, 'Привет! Давай пройдем регистрацию.\nНапиши свое имя.')
        bot.register_next_step_handler(message, get_name)

@bot.message_handler(commands=['language'])
def lang(message):
    user_id=message.from_user.id
    bot.send_message(user_id, 'Выберите язык. Хотя это ничего не поменяет))', reply_markup=buttons15.lang_button())
    bot.register_next_step_handler(message, lang1)

def lang1(message):
    user_id=message.from_user.id
    if message.text== 'Русский':
        bot.send_message(user_id, 'Вы выбрали русский язык', reply_markup=telebot.types.ReplyKeyboardRemove())
    elif message.text== 'Узбекча':
        bot.send_message(user_id, 'Вы выбрали узбекский язык', reply_markup=telebot.types.ReplyKeyboardRemove())

@bot.message_handler(commands = ['help'])
def helper(message):
    user_id = message.from_user.id
    bot.send_message(user_id, 'Для резервации столика нажмите "Зарезервировать столик"'
                              '\nДля отмены уже существующей брони нажмите "Отменить бронь"'
                              '\n\nРады, если это помогло!'
                              '\nПо другим вопросам звоните по номеру +998955678776')

@bot.message_handler(commands=['admin'])
def admin_message(message):
    admin_id = 14276038
    if message.from_user.id == admin_id:
        bot.send_message(admin_id, 'Добро пожаловать в админ панель!', reply_markup=buttons15.admin_buttons())
        bot.register_next_step_handler(message, admin_choice)
    else:
        bot.send_message(message.from_user.id, 'Ты не админ, сори))')


def get_name(message):
    user_id = message.from_user.id
    user_name = message.text
    bot.send_message(user_id, 'Теперь введи свой номер телефона!', reply_markup=buttons15.num_button())
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
        bot.send_message(user_id, 'Регистрация прошла успешно! Что вы хотите сделать?',  reply_markup=buttons15.to_do())
    else:
        bot.send_message(user_id, 'Отправьте локацию через кнопку!')
        bot.register_next_step_handler(message, get_loc, user_name, user_num)

@bot.message_handler(content_types=['text'])
def action(message):
    user_id = message.from_user.id
    if message.text == 'Зарезервировать столик':
        if check_reservation(user_id):
            name = db.check_name(user_id)
            table_id=check_table1(user_id)
            chairs= check_table(table_id)[0]
            type = check_table(table_id)[1]
            bot.send_message(user_id, 'Вы уже зарезервировали столик. Вот информация:')
            bot.send_message(user_id, f'Имя: {name}\nТип стола: {type}\nКоличество стульев: {chairs}')
        else:
            bot.send_message(user_id, 'Выберите тип стола', reply_markup=buttons15.inline_type())
    elif message.text == 'Отменить бронь':
        if check_reservation(user_id):
            table_id=check_table1(user_id)
            cancel_reservation(user_id, table_id)
            bot.send_message(user_id, 'Вы успешно отменили бронь!')
        else:
            bot.send_message(user_id, 'Вы не зарезервировали столик, чтобы его удалить')
    else:
        bot.send_message(user_id, 'Напишите что-нибудь чтобы вернуться на главную', reply_markup=telebot.types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, start)

@bot.callback_query_handler(lambda call: call.data in ['private', 'non-private'])
def get_type(call):
    user_id = call.message.chat.id
    types = call.data
    temp_data[user_id] = {'types': types}
    bot.send_message(user_id, 'А теперь выберите количество стульев.', reply_markup=buttons15.inline_chairs())

@bot.callback_query_handler(lambda call: call.data in ['2', '4', '6', '10', '12'])
def get_chairs(call):
    user_id = call.message.chat.id
    chairs = int(call.data)
    type = temp_data[user_id]['types']
    if find_table(chairs, type):
        table_id = show_id(chairs, type)
        reserve_table(user_id, table_id)
        bot.send_message(user_id, 'Столик успешно зарезервирован!')
        temp_data.clear()
    else:
        bot.send_message(user_id, 'Такого столика не найдено, посмотрите еще', reply_markup=buttons15.to_do())
        temp_data.clear()


@bot.message_handler(content_types=['text'])
def admin_choice(message):
    admin_id = 14276038
    if message.text == 'Добавить стол':
        bot.send_message(admin_id, 'Выберите тип стола', reply_markup=buttons15.inline_type_admin())
        admins.insert(0, message.text)
    elif message.text == 'Удалить стол':
        bot.send_message(admin_id, 'Выберите тип стола, который хотите удалить', reply_markup=buttons15.inline_type_admin())
        admins.insert(0, message.text)
    else:
        # bot.send_message(admin_id, 'Работайте через кнопки пожалуйста')
        bot.send_message(admin_id, 'Напишите что-нибудь чтобы вернуться на главную', reply_markup=telebot.types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, start)

@bot.callback_query_handler(lambda call: call.data in ['private_admin', 'non-private_admin'])
def get_type_admin(call):
    admin_id = 14276038
    types = call.data.split('_')[0]
    admin_data[admin_id] = {'types': types}
    bot.send_message(admin_id, 'А теперь выберите количество стульев.', reply_markup=buttons15.inline_chairs_admin())
@bot.callback_query_handler(lambda call: call.data in ['2_ad', '4_ad', '6_ad', '10_ad', '12_ad'])
def get_chairs_admin(call):
    admin_id = 14276038
    chairs = int(call.data.split('_')[0])
    type = admin_data[admin_id]['types']
    if admins[0]=='Добавить стол':
        add_table(chairs, type)
        admin_data.clear()
        admins.clear()
        bot.send_message(admin_id, 'Столик добавлен!', reply_markup=telebot.types.ReplyKeyboardRemove())
    elif admins[0]=='Удалить стол':
        if find_table(chairs, type):
            table_id = show_id(chairs, type)
            delete_table(table_id)
            admin_data.clear()
            admins.clear()
            bot.send_message(admin_id, 'Столик удален!', reply_markup=telebot.types.ReplyKeyboardRemove())
        else:
            bot.send_message(admin_id, 'Такого стола нет, выберите другой', reply_markup=telebot.types.ReplyKeyboardRemove())
            admin_data.clear()

bot.polling(none_stop=True)

