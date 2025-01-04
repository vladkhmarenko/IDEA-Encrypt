LEXICON_RU: dict[str, str] = {
    '/start': 'Бот IDEA Encrypt\n\nДанный бот является программной реализацией блочно-итерационной криптосистемы IDEA (International Data Encryption Algorithm)\n\n'
              'Бот позволяет зашифровывать текстовые сообщения и расшифровывать бинарные файлы для заданного ключа\n\n'
              'Управление ботом происходит при помощи команд, для инструкции по использованию отправьте команду /help',
    '/help': 'Бот IDEA Encrypt\n\nДанный бот является программной реализацией блочно-итерационной криптосистемы IDEA (International Data Encryption Algorithm)\n\n'
             'Бот позволяет зашифровывать текстовые сообщения и расшифровывать бинарные файлы для заданного ключа'
             ' для следующих режимов шифрования: ECB, CBC, CFB, OFB, CTR. При этом может использоваться один из следующих режимов дополнения последнего блока: ANSI X.923, ISO 10126, PKCS7, ISO/IEC 7816-4'
             '\n\nИспользование бота:\nСначала требуется произвести настройку бота с помощью команд\n1) /mode - выбор одного из предложенных режимов шифрования\n2) /padding - '
             'выбор одного из предложенных режимов дополнения последнего блока\n\nКоманда /encrypt - на вход ожидает текстовое сообщение '
             'и возвращает зашифрованный бинарный файл\nКоманда /decrypt - на вход ожидает бинарный файл и отвечает на него расшифрованным сообщением',
    'error': 'К сожалению, не могу тебя понять, используй команды',

    'choose_password': 'Введите пароль (ключ шифрования)',
    'choose_mode': 'Выберите один из режимов шифрования:',
    'choose_padding': 'Выберите один из режимов дополнения последнего блока:',

    'mode_chosen': 'Выбран режим шифрования:', # для отображения в сообщении с инлайн-кнопками
    'padding_chosen': 'Выбран режим дополнения последнего блока:', # для отображения в сообщении с инлайн-кнопками
    'password_chosen': 'Ключ шифрования успешно введен',

    'validate_mode': 'Выберите режим шифрования с помощью команды /mode и повторите попытку',
    'validate_padding': 'Выберите режим дополнения последнего блока с помощью команды /padding и повторите попытку',

    'ask_encrypt': 'Отправьте текст, который необходимо зашифровать',
    'ask_decrypt': 'Отправьте файл, который необходимо расшифровать'
}

LEXICON_COMMANDS_RU: dict[str, str] = {
    '/start': 'Начало работы с ботом',
    '/help': 'Инструкция',
    '/mode': 'Задать режим шифрования',
    '/padding': 'Задать режим дополнения последнего блока',
    '/encrypt': 'Зашифровать сообщение',
    '/decrypt': 'Расшифровать бинарный файл',
}