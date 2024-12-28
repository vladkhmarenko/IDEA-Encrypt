from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

mode_button_1 = InlineKeyboardButton(
    text='ECB',
    callback_data='mode ECB'
)

mode_button_2 = InlineKeyboardButton(
    text='CBC',
    callback_data='mode CBC'
)

mode_button_3 = InlineKeyboardButton(
    text='CFB',
    callback_data='mode CFB'
)

mode_button_4 = InlineKeyboardButton(
    text='OFB',
    callback_data='mode OFB'
)

mode_button_5 = InlineKeyboardButton(
    text='CTR',
    callback_data='mode CTR'
)

mode_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[mode_button_1],
                     [mode_button_2],
                     [mode_button_3],
                     [mode_button_4],
                     [mode_button_5]]
)


padding_button_1 = InlineKeyboardButton(
    text='ANSI X.923',
    callback_data='padding ANSI X.923'
)

padding_button_2 = InlineKeyboardButton(
    text='ISO 10126',
    callback_data='padding ISO 10126'
)

padding_button_3 = InlineKeyboardButton(
    text='PKCS7',
    callback_data='padding PKCS7'
)

padding_button_4 = InlineKeyboardButton(
    text='ISO/IEC 7816-4',
    callback_data='padding ISO/IEC 7816-4'
)

padding_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[padding_button_1],
                     [padding_button_2],
                     [padding_button_3],
                     [padding_button_4]]
)