# **Exercício Docker: Otimizando um Dockerfile para Segurança e Tamanho**

Após identificar vulnerabilidades, o próximo passo lógico é refatorar nossos Dockerfiles para mitigar riscos e reduzir o tamanho das imagens. Imagens grandes e genéricas, além de rodarem como root, são alvos fáceis. Este exercício foca em transformar um Dockerfile com más práticas em uma versão mais segura e enxuta.

## **Objetivo**

1. Analisar um Dockerfile de exemplo com práticas não recomendadas.  
2. Identificar os problemas relacionados à segurança e ao tamanho da imagem.  
3. Aplicar melhorias para criar uma nova versão do Dockerfile que seja:  
   * Mais segura (ex: rodando com usuário não-root).  
   * Menor em tamanho (ex: usando imagens base enxutas, otimizando camadas).

## **Exemplo de Aplicação Simples (Python Flask)**

Para este exercício, vamos considerar uma aplicação web Python simples usando Flask.

**1\. requirements.txt:**

Flask==2.0.1

*(Usamos uma versão específica para o exemplo. Em projetos reais, mantenha suas dependências atualizadas).*

**2\. app.py:**

from flask import Flask  
import os

app \= Flask(\_\_name\_\_)

@app.route('/')  
def hello\_world():  
    user \= os.getenv("APP\_USER", "usuário desconhecido")  
    return f"\<p\>Olá, Mundo\! Aplicação rodando como: {user}\</p\>"

if \_\_name\_\_ \== '\_\_main\_\_':  
    \# Escuta em todas as interfaces na porta 5000  
    app.run(host='0.0.0.0', port=5000)

## **Dockerfile Original (Com Más Práticas)**

Aqui está um exemplo de Dockerfile que, embora possa funcionar, contém várias práticas não ideais:

\# Dockerfile Original \- Com Más Práticas  
FROM ubuntu:22.04

\# Instala dependências do sistema e Python como root  
RUN apt-get update && \\  
    apt-get install \-y python3 python3-pip git vim curl wget && \\  
    rm \-rf /var/lib/apt/lists/\*

\# Define o diretório de trabalho  
WORKDIR /usr/src/app

\# Copia TUDO do contexto de build para o diretório de trabalho  
\# Isso pode incluir arquivos desnecessários ou sensíveis (.git, .env local, etc.)  
COPY . .

\# Instala dependências Python como root  
RUN pip3 install \--no-cache-dir \-r requirements.txt

\# Expõe a porta da aplicação  
EXPOSE 5000

\# Executa a aplicação como root  
CMD \["python3", "app.py"\]

## **Identificando as Más Práticas e Pontos de Melhoria**

1. **Imagem Base Genérica e Grande (FROM ubuntu:22.04):**  
   * **Problema:** ubuntu é uma imagem de sistema operacional completa, trazendo muitos pacotes e bibliotecas que não são necessários para rodar uma simples aplicação Python. Isso aumenta o tamanho da imagem final e a superfície de ataque (mais pacotes \= mais potenciais vulnerabilidades).  
   * **Melhoria:** Utilizar uma imagem base oficial específica para a linguagem e mais enxuta, como python:3.x-slim ou python:3.x-alpine.  
2. **Instalação Excessiva de Ferramentas (git vim curl wget):**  
   * **Problema:** Ferramentas como git, vim, curl, wget são úteis para desenvolvimento ou depuração, mas não deveriam estar presentes na imagem de produção final. Elas aumentam o tamanho e a superfície de ataque.  
   * **Melhoria:** Instalar apenas as dependências estritamente necessárias para a aplicação rodar. Se ferramentas de build são necessárias, usar um *multi-stage build*.  
3. **Execução de Comandos como root:**  
   * **Problema:** Todas as instruções RUN e o CMD final são executados como o usuário root por padrão. Se a aplicação ou um de seus componentes for comprometido, o invasor terá privilégios de root dentro do container, o que é um risco de segurança significativo.  
   * **Melhoria:** Criar um usuário não-privilegiado dedicado e usar a instrução USER para rodar a aplicação com esse usuário.  
4. **COPY . . Amplo e Prematuro:**  
   * **Problema:** A instrução COPY . . copia indiscriminadamente todo o conteúdo do contexto de build (o diretório onde o Dockerfile está localizado e seus subdiretórios) para dentro da imagem. Isso frequentemente inclui arquivos e pastas que são completamente desnecessários para a execução da aplicação em produção, ou pior, que podem conter informações sensíveis. Exemplos comuns incluem:  
     * Diretórios de controle de versão como .git/.  
     * Arquivos de configuração de ambiente de desenvolvimento local, como .env contendo segredos, ou pastas específicas de IDEs como .vscode/ ou .idea/.  
     * Dependências de desenvolvimento já instaladas localmente (ex: node\_modules/ em projetos Node.js, embora para Python isso seja menos comum de ser copiado diretamente se um virtualenv não estiver no contexto).  
     * Arquivos de log, arquivos temporários (\*.tmp, \*.bak), ou artefatos de build de execuções anteriores (build/, dist/).  
       A inclusão desses itens não apenas infla o tamanho da imagem desnecessariamente, tornando os uploads e downloads mais lentos e consumindo mais espaço em disco, mas também pode introduzir riscos de segurança se segredos ou informações de configuração interna forem inadvertidamente empacotados.  
       Além disso, a posição dessa instrução COPY . . no Dockerfile tem um impacto direto na eficiência do cache de build do Docker. Se você copia todo o código fonte antes de instalar dependências (como RUN pip3 install \-r requirements.txt), qualquer pequena alteração em qualquer arquivo do código fonte (mesmo um comentário em app.py) fará com que a camada do COPY . . seja invalidada. Consequentemente, todas as camadas subsequentes, incluindo a de instalação de dependências (que pode ser demorada), serão reconstruídas do zero, mesmo que o arquivo requirements.txt não tenha sofrido nenhuma alteração. Isso leva a tempos de build significativamente mais longos e a uma perda de produtividade, especialmente em pipelines de CI/CD.  
   * **Melhoria:** A abordagem correta envolve duas estratégias principais:  
     1. **Utilizar um arquivo .dockerignore:** Similar ao .gitignore, este arquivo instrui o daemon do Docker sobre quais arquivos e pastas no contexto de build devem ser ignorados e não enviados para o processo de construção da imagem. Isso reduz o tamanho do contexto de build, acelera o envio para o daemon e impede que arquivos indesejados ou sensíveis sejam incluídos na imagem. Um .dockerignore típico para um projeto Python poderia incluir:  
        \_\_pycache\_\_/  
        \*.pyc  
        \*.pyo  
        \*.pyd  
        .Python  
        env/  
        venv/  
        .git  
        .vscode/  
        .idea/  
        \*.log  
        .env

     2. **Otimizar a Ordem das Instruções para Cache:** Copie apenas os arquivos necessários e na ordem correta para maximizar o aproveitamento do cache do Docker. A regra geral é copiar primeiro os arquivos que mudam com menos frequência. Para uma aplicação Python, isso significa:  
        * Copiar o arquivo requirements.txt (que define as dependências).  
        * Executar pip install \-r requirements.txt para instalar essas dependências. Esta camada será armazenada em cache e reutilizada se requirements.txt não mudar.  
        * Depois disso, copiar o restante do código da aplicação (ex: COPY . . já filtrado pelo .dockerignore, ou cópias mais específicas como COPY app.py . e COPY ./meu\_modulo ./meu\_modulo).  
          Dessa forma, se apenas o código da aplicação (ex: app.py) for alterado, as camadas anteriores, incluindo a instalação de dependências (que é mais custosa), serão carregadas do cache, resultando em builds muito mais rápidos.  
5. **Falta de Multi-Stage Build (para cenários mais complexos):**  
   * **Problema:** Embora este exemplo seja simples, se houvesse um passo de compilação (ex: compilar assets de frontend, compilar código Go/Java), todas as ferramentas de build (compiladores, SDKs) ficariam na imagem final.  
   * **Melhoria:** Utilizar multi-stage builds para separar o ambiente de compilação do ambiente de execução final. O estágio final copiaria apenas os artefatos necessários (ex: o binário compilado, os assets construídos) para uma imagem base mínima.

## **Nova Versão do Dockerfile (Otimizada e Mais Segura)**

Aplicando as melhorias identificadas, podemos criar uma nova versão do Dockerfile:

\# Dockerfile Otimizado e Mais Seguro

\# \---- Estágio 1: Builder (Opcional para este exemplo simples, mas demonstrativo) \----  
\# Se precisássemos de ferramentas de build específicas ou compilar algo, faríamos aqui.  
\# Para este caso Python simples, o foco é mais na imagem final enxuta.  
\# Poderíamos usar este estágio para instalar dependências em um ambiente separado.

\# \---- Estágio Final: Imagem de Produção \----  
\# 1\. Usar uma imagem base oficial Python, enxuta e específica  
FROM python:3.11-slim-bullseye  
\# 'slim' é menor que a padrão. 'bullseye' especifica a release do Debian.

LABEL maintainer="seu\_email@example.com"  
LABEL description="Aplicação Flask otimizada rodando como usuário não-root."

\# 2\. Definir variáveis de ambiente úteis  
ENV PYTHONUNBUFFERED=1 \\  
    PYTHONDONTWRITEBYTECODE=1 \\  
    \# Variáveis para o usuário e diretório da aplicação  
    APP\_USER="appuser" \\  
    APP\_GROUP="appgroup" \\  
    APP\_HOME="/home/appuser/app"

\# 3\. Criar grupo, usuário e diretório da aplicação  
\#    \- Criar um grupo de sistema 'appgroup'.  
\#    \- Criar um usuário de sistema 'appuser', definir seu home e shell.  
RUN groupadd \--system ${APP\_GROUP} && \\  
    useradd \--system \--gid ${APP\_GROUP} \--home-dir /home/${APP\_USER} \--create-home \--shell /sbin/nologin ${APP\_USER}

\# 4\. Definir o diretório de trabalho. WORKDIR cria o diretório se não existir.  
WORKDIR ${APP\_HOME}

\# 5\. Copiar apenas o arquivo de dependências primeiro para otimizar o cache  
COPY requirements.txt .

\# 6\. Instalar dependências Python.  
\#    \--no-cache-dir: Não armazena o cache do pip, reduzindo o tamanho da imagem.  
\#    É comum instalar dependências como root ou em um ambiente virtual antes de mudar para o usuário da app.  
RUN pip install \--no-cache-dir \-r requirements.txt

\# 7\. Copiar o restante do código da aplicação  
\#    Assumindo que .dockerignore está configurado para excluir arquivos desnecessários.  
COPY . .

\# 8\. Mudar a propriedade de todos os arquivos no APP\_HOME para o appuser.  
\#    Isso garante que o usuário da aplicação tenha as permissões corretas.  
RUN chown \-R ${APP\_USER}:${APP\_GROUP} ${APP\_HOME}

\# 9\. Mudar para o usuário não-root.  
\#    Todos os comandos subsequentes e a aplicação rodarão como este usuário.  
USER ${APP\_USER}

\# Passar o nome do usuário como variável de ambiente para a aplicação (opcional, para demonstração)  
ENV APP\_USER=${APP\_USER}

\# 10\. Expor a porta em que a aplicação Flask rodará  
EXPOSE 5000

\# 11\. Comando para executar a aplicação  
\#     Usar 'flask run' é uma forma comum e configurável para rodar apps Flask.  
\#     As variáveis FLASK\_APP, FLASK\_RUN\_HOST e FLASK\_RUN\_PORT podem ser usadas  
\#     (FLASK\_APP=app.py, FLASK\_RUN\_HOST=0.0.0.0, FLASK\_RUN\_PORT=5000).  
\#     Alternativamente, o comando direto python app.py também funciona se app.py estiver configurado.  
CMD \["python", "app.py"\]

**Para usar com flask run, você poderia ajustar o CMD e adicionar ENVs:**

\# ... (partes anteriores do Dockerfile) ...  
\# USER ${APP\_USER}

ENV FLASK\_APP=app.py  
ENV FLASK\_RUN\_HOST=0.0.0.0  
ENV FLASK\_RUN\_PORT=5000  
ENV APP\_USER=${APP\_USER} \# Para o script app.py

EXPOSE 5000  
CMD \["flask", "run"\]

## **Verificando as Melhorias**

1. **Construa a Nova Imagem:**  
   docker build \-t minha-flask-app-otimizada .

2. Verifique o Tamanho:  
   Compare o tamanho da imagem minha-flask-app-otimizada com uma imagem que seria gerada pelo Dockerfile original (se você o construísse). A nova imagem será significativamente menor.  
   docker images minha-flask-app-otimizada

3. **Execute o Container:**  
   docker run \-d \-p 5001:5000 \--name container-flask-otimizado minha-flask-app-otimizada

   Acesse http://localhost:5001 no seu navegador.  
4. **Verifique o Usuário em Execução:**  
   docker exec container-flask-otimizado whoami

   A saída esperada é appuser.

## **Conclusão**

Ao aplicar estas melhorias, transformamos um Dockerfile problemático em um que produz imagens menores, mais seguras e mais eficientes. Práticas como usar imagens base enxutas, rodar como usuário não-root, otimizar camadas de cache e evitar ferramentas desnecessárias são fundamentais para um bom "Docker hygiene". A utilização de multi-stage builds, embora não totalmente explorada neste exemplo simples, seria o próximo passo para aplicações com processos de compilação mais complexos.