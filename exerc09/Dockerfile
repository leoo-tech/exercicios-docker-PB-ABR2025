# Estágio 1: Usar uma imagem base do Nginx (Alpine é uma boa escolha por ser leve)
FROM nginx:1.27-alpine
# Você pode usar nginx:latest se preferir, mas especificar uma versão alpina é bom para o tamanho.

# Remover a configuração padrão do Nginx para evitar conflitos ou limpar o diretório
# RUN rm -rf /usr/share/nginx/html/*
# (Opcional: Descomente a linha acima se quiser garantir que o diretório html está vazio antes de copiar)

# Copiar os arquivos do seu site estático para o diretório padrão do Nginx
# ATENÇÃO: Substitua 'meu-template-creativetim/' pelo nome exato da pasta 
#          onde você extraiu os arquivos da sua landing page.
COPY ./ /usr/share/nginx/html/

# Expor a porta 80 (o Nginx escuta na porta 80 por padrão)
EXPOSE 80

# O comando padrão da imagem nginx (nginx -g 'daemon off;') já cuidará de iniciar o servidor.
# Não é necessário um CMD ou ENTRYPOINT aqui, a menos que você queira sobrescrever o padrão.