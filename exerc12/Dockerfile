# Dockerfile Melhorado para a Aplicação Flask

# 1. Usar uma imagem base Python mais enxuta e específica
FROM python:3.9-slim-bullseye
# 'slim' é menor que a padrão. 'bullseye' especifica a release do Debian.
# Considere versões mais recentes do Python (ex: 3.11 ou 3.12) e do OS (ex: bookworm) para novas aplicações.

LABEL maintainer="seu_email@example.com"
LABEL description="Aplicação Flask segura rodando como usuário não-root."

# 2. Definir variáveis de ambiente úteis
ENV PYTHONUNBUFFERED=1 \
  PYTHONDONTWRITEBYTECODE=1 \
  FLASK_APP=app.py \
  FLASK_RUN_HOST=0.0.0.0 \
  FLASK_RUN_PORT=5000 \
  APP_USER="appuser" \
  APP_GROUP="appgroup" \
  APP_HOME="/app"

# 3. Criar grupo, usuário e diretório da aplicação
#    - Criar um grupo de sistema 'appgroup'.
#    - Criar um usuário de sistema 'appuser' sem home directory tradicional e sem shell de login.
#    - Criar o diretório APP_HOME e dar propriedade ao novo usuário/grupo.
RUN groupadd --system ${APP_GROUP} && \
  useradd --system --gid ${APP_GROUP} --shell /sbin/nologin --no-create-home ${APP_USER} && \
  mkdir -p ${APP_HOME} && \
  chown -R ${APP_USER}:${APP_GROUP} ${APP_HOME}

# 4. Definir o diretório de trabalho
WORKDIR ${APP_HOME}

# 5. Copiar o arquivo de dependências
#    Este arquivo será inicialmente propriedade de root.
COPY requirements.txt .

# 6. Instalar dependências usando pip
#    --no-cache-dir reduz o tamanho da imagem ao não armazenar o cache do pip.
#    Instalamos como root antes de mudar de usuário, mas os arquivos da app pertencerão ao appuser.
RUN pip install --no-cache-dir -r requirements.txt

# 7. Copiar o código da aplicação (app.py)
#    Este arquivo também será inicialmente propriedade de root.
COPY app.py .

# 8. Mudar a propriedade de todos os arquivos no APP_HOME para o appuser.
#    Isso é feito DEPOIS que todos os arquivos são copiados e as dependências instaladas.
RUN chown -R ${APP_USER}:${APP_GROUP} ${APP_HOME}

# 9. Mudar para o usuário não-root.
#    Todos os comandos subsequentes e a aplicação rodarão como este usuário.
USER ${APP_USER}

# 10. Expor a porta em que o Flask rodará (definida por FLASK_RUN_PORT)
EXPOSE ${FLASK_RUN_PORT}

# 11. Comando para executar a aplicação
#     O Flask CLI usará as variáveis de ambiente FLASK_APP, FLASK_RUN_HOST e FLASK_RUN_PORT.
CMD ["flask", "run"]