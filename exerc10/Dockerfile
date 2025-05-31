# 1. Escolha uma imagem base
FROM python:3.10-slim

# 2. Defina o diretório de trabalho dentro do container
WORKDIR /usr/src/app

# 3. Crie um grupo e um usuário não-root
#    'appgroup' será o grupo e 'appuser' será o usuário.
#    -r ou --system cria um usuário/grupo de sistema.
#    -g ou --gid especifica o GID primário do usuário.
#    -s /sbin/nologin ou /bin/false impede logins interativos para este usuário.
#    --no-create-home não cria um diretório home, o que é comum para usuários de serviço.
RUN groupadd --system appgroup && \
  useradd --system --gid appgroup --no-create-home --shell /bin/false appuser

# 4. Copie o script da aplicação para o diretório de trabalho no container
COPY ./app.py .

# 5. (Opcional, mas boa prática) Mude a propriedade dos arquivos da aplicação para o novo usuário
#    Isso garante que o usuário 'appuser' tenha as permissões corretas nos arquivos.
RUN chown appuser:appgroup ./app.py

# 6. Mude para o usuário não-root
USER appuser

# 7. (Opcional) Defina uma variável de ambiente
ENV NAME="Usuário App"

# 8. Defina o comando para executar a aplicação quando o container iniciar
CMD ["python", "./app.py"]