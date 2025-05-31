import os
import time
import pwd

def get_username():
    try:
        return pwd.getpwuid(os.geteuid()).pw_name
    except KeyError:
        return "N/A (UID not in passwd)"

print("🚀 Aplicação Python iniciada!")
uid = os.geteuid()
username = get_username()
print(f" UID do processo: {uid}")
print(f" Nome de usuário: {username}")

print(f" Olá, {os.getenv('NAME', 'Mundo Anônimo')}!")

# Mantém o container rodando por um tempo para permitir o 'docker exec'
print(" Aplicação rodando por 30 segundos...")
time.sleep(30)
print("✅ Aplicação finalizada.")