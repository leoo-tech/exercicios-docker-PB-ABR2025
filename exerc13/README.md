Olá\! Este documento irá guiá-lo através do exercício Docker que você solicitou. Ele inclui os passos para criar um Dockerfile, um script Python simples, e como interagir com o Docker Hub.

### **1\. Criar o script Python (app.py)**

Primeiro, crie um arquivo chamado app.py com o seguinte conteúdo. Este script simplesmente imprime a data e hora atuais.

import datetime

def main():  
    """  
    Função principal que imprime a data e hora atuais.  
    """  
    current\_time \= datetime.datetime.now()  
    print(f"A data e hora atuais são: {current\_time}")

if \_\_name\_\_ \== "\_\_main\_\_":  
    main()

### **2\. Criar o Dockerfile**

Agora, crie um arquivo chamado Dockerfile (sem extensão) no mesmo diretório que o app.py. Este Dockerfile usará a imagem python:3.11-slim, copiará seu script e o executará.

\# Usa a imagem oficial do Python 3.11 em uma versão slim para um tamanho menor  
FROM python:3.11-slim

\# Define o diretório de trabalho dentro do contêiner  
WORKDIR /app

\# Copia o script Python local para o diretório de trabalho no contêiner  
COPY app.py .

\# Instala quaisquer dependências (neste caso, não há, mas é uma boa prática incluir)  
\# RUN pip install \--no-cache-dir \<sua\_dependencia\>

\# Comando para executar o script quando o contêiner for iniciado  
CMD \["python", "app.py"\]

### **3\. Criar uma conta no Docker Hub**

Se você ainda não tem uma conta, vá para [https://hub.docker.com/](https://hub.docker.com/) e crie uma conta gratuita. Anote seu nome de usuário.

### **4\. Fazer login no Docker Hub pelo terminal**

Abra seu terminal ou prompt de comando e execute o seguinte comando. Você será solicitado a inserir seu nome de usuário e senha do Docker Hub.

docker login

### **5\. Reconstruir e renomear a imagem**

Agora, vamos construir sua imagem e renomeá-la no formato seu-usuario/meu-echo:v1. Substitua seu-usuario pelo seu nome de usuário do Docker Hub. Certifique-se de estar no diretório onde estão Dockerfile e app.py.

docker build \-t seu-usuario/meu-echo:v1 .

* \-t: Tag (nome) para sua imagem.  
* seu-usuario: Seu nome de usuário do Docker Hub.  
* meu-echo: O nome da sua imagem.  
* :v1: A tag da versão da sua imagem.  
* .: Indica que o Dockerfile está no diretório atual.

### **6\. Fazer o push da imagem para o Docker Hub**

Finalmente, faça o push da sua imagem para o Docker Hub.

docker push seu-usuario/meu-echo:v1

Após o push, você poderá ver sua imagem no seu repositório do Docker Hub online.

Espero que este guia detalhado ajude você a completar o exercício\! Se tiver mais alguma dúvida, é só perguntar.