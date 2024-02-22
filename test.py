import json
import hashlib
import base64
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

class CryptoJsAes:
    @staticmethod
    def encrypt(value, passphrase):
        salt = get_random_bytes(8)
        salted = b''
        dx = b''
        while len(salted) < 48:
            dx = hashlib.md5(dx + passphrase.encode() + salt).digest()
            salted += dx
        key = salted[:32]
        iv = salted[32:48]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        encrypted_data = cipher.encrypt(json.dumps(value).encode())
        data = {"ct": base64.b64encode(encrypted_data).decode(), "iv": iv.hex(), "s": salt.hex()}
        return json.dumps(data)

    @staticmethod
    def decrypt(jsonStr, passphrase):
        json_data = json.loads(jsonStr)
        salt = bytes.fromhex(json_data["s"])
        iv = bytes.fromhex(json_data["iv"])
        ct = base64.b64decode(json_data["ct"])
        concatedPassphrase = passphrase + salt.decode()
        md5 = [hashlib.md5(concatedPassphrase.encode()).digest()]
        result = md5[0]
        i = 1
        while len(result) < 32:
            md5.append(hashlib.md5(md5[i - 1] + concatedPassphrase.encode()).digest())
            result += md5[i]
            i += 1
        key = result[:32]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted_data = cipher.decrypt(ct).rstrip(b'\0')
        return json.loads(decrypted_data.decode())

# Contoh penggunaan:
plaintext = {"message": "Hello, World!"}
password = "my_secret_password"

# Enkripsi
encrypted = CryptoJsAes.encrypt(plaintext, password)
print("Encrypted:", encrypted)

# Dekripsi
decrypted = CryptoJsAes.decrypt(encrypted, password)
print("Decrypted:", decrypted)
