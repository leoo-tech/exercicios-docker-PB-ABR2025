# **Solução do Exercício: Docker com Usuário Não-Root**

Este documento apresenta a solução para o exercício de criar uma imagem Docker que executa uma aplicação simples como um usuário não-root, visando aumentar a segurança.

## **Objetivo do Exercício**

Configurar um Dockerfile para:

1. Criar um usuário não-privilegiado.  
2. Definir este usuário como o padrão para a execução da aplicação.  
3. Construir a imagem.  
4. Iniciar um container.  
5. Verificar que a aplicação no container está rodando com o usuário não-root.

## **1\. Script da Aplicação (app.py)**

Primeiro, crie um script Python simples que nos ajudará a verificar o usuário em execução.

**app.py:**

import os  
import time  
import pwd \# Módulo para obter informações do usuário no Linux/Unix

def get\_username\_from\_euid():  
    \# Obtém o nome de usuário a partir do UID efetivo do processo  
    try:  
        return pwd.getpwuid(os.geteuid()).pw\_name  
    except KeyError:  
        \# Caso o UID não tenha uma entrada correspondente em /etc/passwd  
        return f"UID\_{os.geteuid()}\_sem\_nome\_associado"

print(f"Aplicação iniciada. Rodando como usuário: {get\_username\_from\_euid()} (UID: {os.geteuid()})")  
print("Container permanecerá ativo por 60 segundos para verificação...")

\# Mantém o container ativo para permitir a execução do 'docker exec'  
try:  
    time.sleep(60)  
except KeyboardInterrupt:  
    print("Aplicação interrompida.")  
print("Aplicação finalizada.")

*Este script imprime o nome de usuário e UID do processo e aguarda para permitir a verificação.*

## **2\. Dockerfile com Usuário Não-Root**

Crie o Dockerfile no mesmo diretório do app.py:

\# Usar uma imagem base Python enxuta  
FROM python:3.11-slim-bullseye

\# Definir variáveis para o nome do usuário, grupo e diretório da aplicação  
\# Esta prática melhora a legibilidade e a manutenibilidade do Dockerfile.  
\# Ao centralizar esses valores, facilita-se a alteração futura sem ter que  
\# procurar e substituir em múltiplos locais no script.  
ENV APP\_USER="appuser"  
ENV APP\_GROUP="appgroup"  
\# A variável APP\_HOME define um caminho padronizado para a aplicação,  
\# o que é útil para comandos como WORKDIR, COPY e para definir permissões.  
\# Isso também ajuda a evitar caminhos "mágicos" espalhados pelo Dockerfile.  
ENV APP\_HOME="/home/appuser/app"

\# Passo 1: Criar um grupo e um usuário não-root  
\# \- groupadd: Cria um novo grupo. '--system' geralmente atribui um GID de um range reservado.  
\# \- useradd: Cria um novo usuário.  
\#   \--system: Cria um usuário de sistema.  
\#   \--gid: Define o grupo primário do usuário.  
\#   \--home-dir: Especifica o diretório home para o usuário.  
\#   \--create-home: Cria o diretório home especificado.  
\#   \--shell /sbin/nologin: Define um shell que não permite login interativo (boa prática para usuários de serviço).  
RUN groupadd \--system ${APP\_GROUP} && \\  
    useradd \--system \--gid ${APP\_GROUP} \--home-dir /home/${APP\_USER} \--create-home \--shell /sbin/nologin ${APP\_USER}

\# Definir o diretório de trabalho para a aplicação  
\# Utilizar a variável APP\_HOME garante consistência.  
WORKDIR ${APP\_HOME}

\# Copiar o script da aplicação para o diretório de trabalho  
COPY app.py .

\# Mudar a propriedade dos arquivos da aplicação para o usuário e grupo criados  
\# Isso garante que o usuário da aplicação tenha as permissões necessárias  
\# para ler e executar os arquivos dentro do seu diretório de trabalho.  
RUN chown \-R ${APP\_USER}:${APP\_GROUP} ${APP\_HOME}

\# Passo 2: Definir o usuário não-root como o padrão para os comandos subsequentes e para a execução do container  
USER ${APP\_USER}

\# Comando para executar a aplicação quando o container iniciar  
CMD \["python", "app.py"\]

**Destaques da Solução no Dockerfile:**

* **Criação** do **Usuário:** As instruções groupadd e useradd criam o grupo appgroup e o usuário appuser.  
* **Permissões:** chown ajusta a propriedade dos arquivos da aplicação.  
* **Definição do Usuário Padrão:** A instrução USER ${APP\_USER} garante que o CMD (e qualquer RUN ou ENTRYPOINT subsequente) seja executado como appuser.

## **3\. Construir a Imagem Docker**

No terminal, navegue até o diretório contendo app.py e Dockerfile, e execute:

docker build \-t app-nao-root .

* \-t app-nao-root: Atribui a tag app-nao-root à imagem construída.

## **4\. Iniciar o Container**

Execute o container a partir da imagem construída, em modo detached (-d) para que possamos inspecioná-lo:

docker run \-d \--name meu\_container\_seguro  
