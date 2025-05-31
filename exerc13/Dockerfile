# Usar a imagem base oficial do Python 3.11 slim
FROM python:3.11-slim

# Definir o diretório de trabalho dentro do container
WORKDIR /app

# Copiar o script app.py para o diretório de trabalho no container
COPY app.py .

# Definir o comando que será executado quando o container iniciar
CMD ["python", "app.py"]