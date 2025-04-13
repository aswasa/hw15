from telebot import types

def lang_button():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    ru = types.KeyboardButton('Русский')
    uz = types.KeyboardButton('Узбекча')

    kb.add(ru, uz)
    return kb


def num_button():
    kb=types.ReplyKeyboardMarkup(resize_keyboard=True)
    num=types.KeyboardButton('Отправить номер📞', request_contact=True)

    kb.add(num)
    return kb

def loc_button():
    kb=types.ReplyKeyboardMarkup(resize_keyboard=True)
    loc=types.KeyboardButton('Отправить локацию📍', request_location=True)
    kb.add(loc)

    return kb


def to_do():
    kb=types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1=types.KeyboardButton('Зарезервировать столик')
    btn2=types.KeyboardButton('Отменить бронь')

    kb.row(btn1, btn2)

    return kb

def inline_type():
    kb=types.InlineKeyboardMarkup(row_width=2)
    type1=types.InlineKeyboardButton('Приватный', callback_data='private')
    type2=types.InlineKeyboardButton('Общий', callback_data='non-private')

    kb.add(type1, type2)

    return kb

def inline_chairs():
    kb=types.InlineKeyboardMarkup(row_width=3)
    c1= types.InlineKeyboardButton('2', callback_data='2')
    c2= types.InlineKeyboardButton('4', callback_data='4')
    c3= types.InlineKeyboardButton('6', callback_data='6')
    c4= types.InlineKeyboardButton('10', callback_data='10')
    c5= types.InlineKeyboardButton('12', callback_data='12')

    kb.add(c1, c2, c3)
    kb.row(c4, c5)

    return kb

def admin_buttons():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    k1 = btn1=types.KeyboardButton('Добавить стол')
    k2 = btn1=types.KeyboardButton('Удалить стол')

    kb.row(k1, k2)

    return kb


def inline_type_admin():
    kb=types.InlineKeyboardMarkup(row_width=2)
    type1=types.InlineKeyboardButton('Приватный', callback_data='private_admin')
    type2=types.InlineKeyboardButton('Общий', callback_data='non-private_admin')

    kb.add(type1, type2)

    return kb

def inline_chairs_admin():
    kb=types.InlineKeyboardMarkup(row_width=3)
    c1= types.InlineKeyboardButton('2', callback_data='2_ad')
    c2= types.InlineKeyboardButton('4', callback_data='4_ad')
    c3= types.InlineKeyboardButton('6', callback_data='6_ad')
    c4= types.InlineKeyboardButton('10', callback_data='10_ad')
    c5= types.InlineKeyboardButton('12', callback_data='12_ad')

    kb.add(c1, c2, c3)
    kb.row(c4, c5)

    return kb