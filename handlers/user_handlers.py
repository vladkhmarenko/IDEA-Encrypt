from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from lexicon.lexicon import LEXICON_RU
from data import Data
from keyboards.keyboards import mode_keyboard, padding_keyboard

router = Router()

data = Data()

@router.message(Command(commands='start'))
async def process_start_command(message: Message):
    await message.answer(text=LEXICON_RU['/start'])

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