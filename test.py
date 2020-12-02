import jwt
import datetime
# from Crypto.Cipher import AES
# obj = AES.new('This is a key123', AES.MODE_CBC, 'This is an IV456')
# message = "The answer is no"
# ciphertext = obj.encrypt(message)
# print(ciphertext)
# obj2 = AES.new('This is a key123', AES.MODE_CBC, 'This is an IV456')
# print(obj2.decrypt(ciphertext))
# app = {"config":''}
import json
from base64 import b64decode
from nacl.secret import SecretBox

secret_key = '_THIS_IS_MY_32_CHARS_SECRET_KEY_'
encrypted = '6mNohLkeVCPgv6r4Jfx2cRhFHtnIa04K:rWTEbQ0GdzpXdxXZ9JRk+drr3JtEmt1I70DGNpXvPO9lKgOZbflf'
encrypted = encrypted.split(':')
# We decode the two bits independently
nonce = b64decode(encrypted[0])
encrypted = b64decode(encrypted[1])
# We create a SecretBox, making sure that out secret_key is in bytes
box = SecretBox(bytes(secret_key, encoding='utf8'))
decrypted = box.decrypt(encrypted, nonce).decode('utf-8')
print(decrypted)

# token = jwt.encode({'user_id' : 5, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, "sexy")
# print(str(token))
