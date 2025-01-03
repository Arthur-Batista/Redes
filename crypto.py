from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import base64

# Geração de chave de 16 bytes (128 bits)
def generate_key():
    return get_random_bytes(16)

# Criptografar mensagem
def encrypt_message(key, message):
    cipher = AES.new(key, AES.MODE_CBC)
    iv = cipher.iv  # Vetor de inicialização
    encrypted_message = cipher.encrypt(pad(message.encode('utf-8'), AES.block_size))
    return base64.b64encode(iv + encrypted_message).decode('utf-8')

# Descriptografar mensagem
def decrypt_message(key, encrypted_message):
    encrypted_data = base64.b64decode(encrypted_message)
    iv = encrypted_data[:AES.block_size]  # Extrair o IV
    encrypted_message = encrypted_data[AES.block_size:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(encrypted_message), AES.block_size).decode('utf-8')
