import struct
import random
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.concatkdf import ConcatKDFHash

BLOCK_SIZE = 8

def read_binary_file(filename):
    with open(filename, 'rb') as f:
        return f.read()

def write_binary_file(filename, data):
    with open(filename, 'wb') as f:
        f.write(data)

def pad(data, mode):
    pad_len = BLOCK_SIZE - (len(data) % BLOCK_SIZE)
    if mode == 'PKCS7':
        return data + bytes([pad_len] * pad_len)
    elif mode == 'ANSI X.923':
        return data + bytes([0] * (pad_len - 1)) + bytes([pad_len])
    elif mode == 'ISO 10126':
        return data + bytes([random.randint(0, 255) for _ in range(pad_len - 1)]) + bytes([pad_len])
    elif mode == 'ISO/IEC 7816-4':
        return data + b'\x80' + bytes([0] * (pad_len - 1))
    else:
        raise ValueError("Unsupported padding mode")

def unpad(data, mode):
    if mode == 'ISO/IEC 7816-4':
        padding_start_index = data.rfind(0x80)
        if padding_start_index == -1 or any(data[padding_start_index+1:]):
            raise ValueError("Invalid ISO/IEC 7816-4 padding.")
        return data[:padding_start_index]
    elif mode in ['ANSI X.923', 'ISO 10126', 'PKCS7']:
        pad_len = data[-1]
        return data[:-pad_len]
    else:
        raise ValueError("Unsupported unpadding mode")

def multiply(x, y):
    if x == 0x0000:
        x = 0x10000
    if y == 0x0000:
        y = 0x10000
    z = (x * y) % 0x10001
    if z == 0x10000:
        z = 0x0000
    return z

# IDEA encryption/decryption functions
def idea_encryption_block(block, subkeys, decrypt=False):
    block = struct.unpack('>4H', block)
    if (decrypt):
        subkeys = prepare_decryption_keys(subkeys)

    for round_num in range(8):
        x1, x2, x3, x4 = block
        k1, k2, k3, k4, k5, k6 = subkeys[round_num * 6:(round_num + 1) * 6]
        x1 = multiply(x1, k1)
        x2 = (x2 + k2) % 0x10000
        x3 = (x3 + k3) % 0x10000
        x4 = multiply(x4, k4)
        temp1 = x1 ^ x3
        temp2 = x2 ^ x4
        temp1 = multiply(temp1, k5)
        temp2 = (temp2 + temp1) % 0x10000
        temp2 = multiply(temp2, k6)
        temp1 = (temp1 + temp2) % 0x10000
        block = (
            x1 ^ temp2,
            x3 ^ temp2,
            x2 ^ temp1,
            x4 ^ temp1
        )
    x1, x2, x3, x4 = block
    k1, k2, k3, k4 = subkeys[-4:]
    x1_out = multiply(x1, k1)
    x2_out = (x3 + k2) % 0x10000
    x3_out = (x2 + k3) % 0x10000
    x4_out = multiply(x4, k4)
    return struct.pack('>4H', x1_out, x2_out, x3_out, x4_out)

def generate_subkeys(key):
    if len(key) != 16:
        raise ValueError("Ключ должен быть длиной 16 байт (128 бит).")

    key_int = int.from_bytes(key)

    subkeys = []
    for _ in range(52 // 8 + 1):
        for i in range(8):
            subkey = (key_int >> (112 - i * 16)) & (1 << 16) - 1
            subkeys.append(subkey)
        key_int = ((key_int << 25) | (key_int >> (128 - 25))) & ((1 << 128) - 1)

    return subkeys[:52]

def multiplicative_inverse(x):
    if x == 0:
        return 0
    return pow(x, 0xFFFF, 0x10001)

def additive_inverse(x):
    return (-x) & 0xFFFF

def prepare_decryption_keys(subkeys):
    decryption_keys = []

    decryption_keys.append(multiplicative_inverse(subkeys[-4]))
    decryption_keys.append(additive_inverse(subkeys[-3]))
    decryption_keys.append(additive_inverse(subkeys[-2]))
    decryption_keys.append(multiplicative_inverse(subkeys[-1]))
    decryption_keys.append(subkeys[-6])
    decryption_keys.append(subkeys[-5])

    for i in range(1, 8):
        idx = i * 6
        decryption_keys.append(multiplicative_inverse(subkeys[-idx - 4]))
        decryption_keys.append(additive_inverse(subkeys[-idx - 2]))
        decryption_keys.append(additive_inverse(subkeys[-idx - 3]))
        decryption_keys.append(multiplicative_inverse(subkeys[-idx - 1]))
        decryption_keys.append(subkeys[-idx - 6])
        decryption_keys.append(subkeys[-idx - 5])

    decryption_keys.append(multiplicative_inverse(subkeys[0]))
    decryption_keys.append(additive_inverse(subkeys[1]))
    decryption_keys.append(additive_inverse(subkeys[2]))
    decryption_keys.append(multiplicative_inverse(subkeys[3]))

    return decryption_keys

# Modes of operation
def ecb_mode(data, subkeys, encrypt):
    result = bytearray()
    for i in range(0, len(data), BLOCK_SIZE):
        block = data[i:i + BLOCK_SIZE]
        result.extend(idea_encryption_block(block, subkeys, not encrypt))
    return result

def cbc_mode(data, subkeys, iv, encrypt):
    result = bytearray()
    previous_block = iv
    for i in range(0, len(data), BLOCK_SIZE):
        block = data[i:i + BLOCK_SIZE]
        if encrypt:
            xor_block = bytes(a ^ b for a, b in zip(block, previous_block))
            encrypted_block = idea_encryption_block(xor_block, subkeys)
            result.extend(encrypted_block)
            previous_block = encrypted_block
        else:
            decrypted_block = idea_encryption_block(block, subkeys, decrypt=True)
            result.extend(bytes(a ^ b for a, b in zip(decrypted_block, previous_block)))
            previous_block = block
    return result

def ctr_mode(data, subkeys, iv):
    result = bytearray()
    counter = idea_encryption_block(iv, subkeys)
    for i in range(0, len(data), BLOCK_SIZE):
        block = data[i:i + BLOCK_SIZE]
        xor_block = bytes(a ^ b for a, b in zip(block, counter))
        result.extend(xor_block)
        counter = (int.from_bytes(counter, 'big') + 1) % (2 ** 128)
        counter = counter.to_bytes(BLOCK_SIZE, 'big')
    return result

def cfb_mode(data, subkeys, iv, encrypt):
    result = bytearray()
    previous_block = iv
    for i in range(0, len(data), BLOCK_SIZE):
        block = data[i:i + BLOCK_SIZE]
        encrypted_block = idea_encryption_block(previous_block, subkeys)
        xor_block = bytes(a ^ b for a, b in zip(encrypted_block, block))
        result.extend(xor_block)
        previous_block = xor_block if encrypt else block
    return result

def ofb_mode(data, subkeys, iv):
    result = bytearray()
    previous_key_stream = iv
    for i in range(0, len(data), BLOCK_SIZE):
        block = data[i:i + BLOCK_SIZE]
        key_stream = idea_encryption_block(previous_key_stream, subkeys)
        result.extend(bytes(a ^ b for a, b in zip(key_stream, block)))
        previous_key_stream = key_stream
    return result

def run_encrypt(data: str | bytes, key: bytes, iv: bytes, action: str, mode: str, pad_mode: str):
    subkeys = generate_subkeys(key)

    if action == 'encrypt':
        data = bytes(data, encoding="utf-8")
        data = pad(data, pad_mode)
        match mode:
            case 'ECB':
                result = ecb_mode(data, subkeys, encrypt=True)
            case 'CBC':
                result = cbc_mode(data, subkeys, iv, encrypt=True)
            case 'CTR':
                result = ctr_mode(data, subkeys, iv)
            case 'CFB':
                result = cfb_mode(data, subkeys, iv, encrypt=True)
            case 'OFB':
                result = ofb_mode(data, subkeys, iv)
            case _:
                raise ValueError("Unsupported mode")
    elif action == 'decrypt':
        match mode:
            case 'ECB':
                result = ecb_mode(data, subkeys, encrypt=False)
            case 'CBC':
                result = cbc_mode(data, subkeys, iv, encrypt=False)
            case 'CTR':
                result = ctr_mode(data, subkeys, iv)
            case 'CFB':
                result = cfb_mode(data, subkeys, iv, encrypt=False)
            case 'OFB':
                result = ofb_mode(data, subkeys, iv)
            case _:
                raise ValueError("Unsupported mode")
        result = unpad(result, pad_mode)
        result = result.decode()
    else:
        raise ValueError("Action must be 'encrypt' or 'decrypt'")

    return result

def generate_key_iv(password: str) -> tuple[bytes, bytes]:
    ckdf_key = ConcatKDFHash(algorithm=hashes.SHA256(), length=16, otherinfo=None)
    key = ckdf_key.derive(bytes(password, "utf-8"))
    ckdf_iv = ConcatKDFHash(algorithm=hashes.SHA256(), length=8, otherinfo=None)
    iv = ckdf_iv.derive(key)

    return key, iv