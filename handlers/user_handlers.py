import io
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.types.input_file import BufferedInputFile
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from lexicon.lexicon import LEXICON_RU
from data import Data
from keyboards.keyboards import mode_keyboard, padding_keyboard
from services.services import generate_key_iv, run_encrypt

router = Router()
data = Data()

class FSMFillForm(StatesGroup):
    wait_for_password = State()
    wait_for_encrypt = State()
    wait_for_decrypt = State()

@router.message(Command(commands='start'))
async def process_start_command(message: Message):
    await message.answer(text=LEXICON_RU['/start'])
    if message.from_user.id not in data.users.keys():
        data.users[message.from_user.id] = {}


@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON_RU['/help'])


@router.message(Command(commands='password'))
async def process_password_command(message: Message, state: FSMContext):
    await message.answer(text='Пожалуйста, введите пароль (ключ шифрования)')
    await state.set_state(FSMFillForm.wait_for_password)

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
async def process_encrypt_command(message: Message, state: FSMContext):
    await message.answer(text='Пожалуйста, введите текст, который необходимо зашифровать')
    await state.set_state(FSMFillForm.wait_for_encrypt)

@router.message(Command(commands='decrypt'))
async def process_decrypt_command(message: Message, state: FSMContext):
    await message.answer(text='Пожалуйста, пришлите бинарный файл, который необходимо расшифровать')
    await state.set_state(FSMFillForm.wait_for_decrypt)


@router.callback_query(F.data.in_(['mode ECB', 'mode CBC', 'mode CFB', 'mode OFB', 'mode CTR']))
async def process_mode_inline_button_pressed(callback: CallbackQuery):
    mode: str = str(callback.data)[5:]
    await callback.message.edit_text(
        text=f'{LEXICON_RU['mode_chosen']} {mode}',
        reply_markup=callback.message.reply_markup
    )
    data.users[callback.from_user.id]['mode'] = mode
    await callback.answer()


@router.callback_query(F.data.in_(['padding ANSI X.923', 'adding ISO 10126', 'padding PKCS7', 'padding ISO/IEC 7816-4']))
async def process_padding_inline_button_pressed(callback: CallbackQuery):
    padding: str = str(callback.data)[8:]
    await callback.message.edit_text(
        text=f'{LEXICON_RU['padding_chosen']} {padding}',
        reply_markup=callback.message.reply_markup
    )
    data.users[callback.from_user.id]['padding'] = padding
    await callback.answer()


@router.message(StateFilter(FSMFillForm.wait_for_password))
async def process_password_sent(message: Message, state: FSMContext):
    await message.answer(text='Спасибо!\nКлюч шифрования введен')
    pw = message.text
    key, iv = generate_key_iv(pw)
    data.users[message.from_user.id]['key'] = key
    data.users[message.from_user.id]['iv'] = iv
    await state.clear()

@router.message(StateFilter(FSMFillForm.wait_for_encrypt))
async def process_data_to_encrypt_sent(message: Message, state: FSMContext):
    str_to_encrypt = message.text
    key = data.users[message.from_user.id]['key']
    iv = data.users[message.from_user.id]['iv']
    mode = data.users[message.from_user.id]['mode']
    padding = data.users[message.from_user.id]['padding']
    encrypted_bytes: bytes = run_encrypt(str_to_encrypt, key, iv, 'encrypt', mode, padding)

    # Создаем объект BytesIO для передачи данных в память
    file_in_memory = io.BytesIO(encrypted_bytes)
    file_in_memory.name = 'result.bin'  # Указываем имя файла (не обязательно, но полезно)

    # Отправляем файл как документ
    document = BufferedInputFile(file_in_memory.getvalue(), "example.bin")
    await message.answer_document(document)
    await state.clear()

@router.message(StateFilter(FSMFillForm.wait_for_decrypt))
async def process_data_to_decrypt_sent(message: Message, state: FSMContext, bot):
    key = data.users[message.from_user.id]['key']
    iv = data.users[message.from_user.id]['iv']
    mode = data.users[message.from_user.id]['mode']
    padding = data.users[message.from_user.id]['padding']

    file_id = message.document.file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path

    # Загружаем содержимое файла в байты
    file_bytes = await bot.download_file(file_path) # _io.BytesIO
    bytes_to_decrypt = file_bytes.getvalue()

    decrypted_str: str = run_encrypt(bytes_to_decrypt, key, iv, 'decrypt', mode, padding)

    await state.clear()
    await message.answer(text=decrypted_str)
