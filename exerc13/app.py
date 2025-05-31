from datetime import datetime

# Obtém a data e hora atuais
now = datetime.now()

# Formata a data e hora como string
current_time_str = now.strftime("%Y-%m-%d %H:%M:%S")

# Imprime a data e hora
print(f"Olá! A data e hora atuais são: {current_time_str}")

