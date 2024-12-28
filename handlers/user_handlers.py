from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from lexicon.lexicon import LEXICON_RU
from data import Data
from keyboards.keyboards import mode_keyboard, padding_keyboard

router = Router()

data = Data()

@router.message(Command(commands='start'))
async def process_start_command(message: Message):
    await message.answer(text=LEXICON_RU['/start'])
    if message.from_user.id not in data.users.keys():
        data.users[message.from_user.id] = {}


@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON_RU['/help'])


@router.message(Command(commands='password'))
async def process_password_command(message: Message):
    pass

@router.message(Command(commands='mode'))
async def process_mode_command(message: Message):
    await message.answer(
        text=LEXICON_RU['choose_mode'],
        reply_markup=mode_keyboard
    )

@router.message(Command(commands='padding'))
async def process_padding_command(message: Message):
    await message.answer(
        text=LEXICON_RU['choose_padding'],
        reply_markup=padding_keyboard
    )

@router.message(Command(commands='encrypt'))
async def process_encrypt_command(message: Message):
    pass

@router.message(Command(commands='decrypt'))
async def process_decrypt_command(message: Message):
    pass


@router.callback_query(F.data == 'mode ECB')
async def process_mode_inline_button1_pressed(callback: CallbackQuery):
    mode: str = str(callback.data)[5:]
    await callback.message.edit_text(
        text=f'{LEXICON_RU['mode_chosen']} {mode}',
        reply_markup=callback.message.reply_markup
    )
    data.users[callback.from_user.id]['mode'] = mode
    await callback.answer()

@router.callback_query(F.data == 'mode CBC')
async def process_mode_inline_button2_pressed(callback: CallbackQuery):
    mode: str = str(callback.data)[5:]
    await callback.message.edit_text(
        text=f'{LEXICON_RU['mode_chosen']} {mode}',
        reply_markup=callback.message.reply_markup
    )
    data.users[callback.from_user.id]['mode'] = mode
    await callback.answer()

@router.callback_query(F.data == 'mode CFB')
async def process_mode_inline_button3_pressed(callback: CallbackQuery):
    mode: str = str(callback.data)[5:]
    await callback.message.edit_text(
        text=f'{LEXICON_RU['mode_chosen']} {mode}',
        reply_markup=callback.message.reply_markup
    )
    data.users[callback.from_user.id]['mode'] = mode
    await callback.answer()

@router.callback_query(F.data == 'mode OFB')
async def process_mode_inline_button4_pressed(callback: CallbackQuery):
    mode: str = str(callback.data)[5:]
    await callback.message.edit_text(
        text=f'{LEXICON_RU['mode_chosen']} {mode}',
        reply_markup=callback.message.reply_markup
    )
    data.users[callback.from_user.id]['mode'] = mode
    await callback.answer()

@router.callback_query(F.data == 'mode CTR')
async def process_mode_inline_button5_pressed(callback: CallbackQuery):
    mode: str = str(callback.data)[5:]
    await callback.message.edit_text(
        text=f'{LEXICON_RU['mode_chosen']} {mode}',
        reply_markup=callback.message.reply_markup
    )
    data.users[callback.from_user.id]['mode'] = mode
    await callback.answer()

@router.callback_query(F.data == 'padding ANSI X.923')
async def process_padding_inline_button1_pressed(callback: CallbackQuery):
    padding: str = str(callback.data)[8:]
    await callback.message.edit_text(
        text=f'{LEXICON_RU['padding_chosen']} {padding}',
        reply_markup=callback.message.reply_markup
    )
    data.users[callback.from_user.id]['padding'] = padding
    await callback.answer()

@router.callback_query(F.data == 'padding ISO 10126')
async def process_padding_inline_button2_pressed(callback: CallbackQuery):
    padding: str = str(callback.data)[8:]
    await callback.message.edit_text(
        text=f'{LEXICON_RU['padding_chosen']} {padding}',
        reply_markup=callback.message.reply_markup
    )
    data.users[callback.from_user.id]['padding'] = padding
    await callback.answer()

@router.callback_query(F.data == 'padding PKCS7')
async def process_padding_inline_button3_pressed(callback: CallbackQuery):
    padding: str = str(callback.data)[8:]
    await callback.message.edit_text(
        text=f'{LEXICON_RU['padding_chosen']} {padding}',
        reply_markup=callback.message.reply_markup
    )
    data.users[callback.from_user.id]['padding'] = padding
    await callback.answer()

@router.callback_query(F.data == 'padding ISO/IEC 7816-4')
async def process_padding_inline_button4_pressed(callback: CallbackQuery):
    padding: str = str(callback.data)[8:]
    await callback.message.edit_text(
        text=f'{LEXICON_RU['padding_chosen']} {padding}',
        reply_markup=callback.message.reply_markup
    )
    data.users[callback.from_user.id]['padding'] = padding
    await callback.answer()
