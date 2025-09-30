from cryptography.fernet import Fernet

with open("encryption.key", "rb") as key_file:
    key = key_file.read()

fernet = Fernet(key)

with open("key_log.txt", "rb") as f:
    for line in f:
        try:
            print(fernet.decrypt(line.strip()).decode())
        except Exception as e:
            print(f"[Error decrypting line] {e}")
