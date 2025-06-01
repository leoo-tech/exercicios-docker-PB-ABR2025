# **Guia: Hospedando uma Landing Page Estática (Creative Tim) com Nginx e Docker**

Este guia detalha como criar uma imagem Docker utilizando Nginx para servir um site HTML/CSS estático, especificamente uma landing page moderna obtida da Creative Tim.

## **Objetivo**

O objetivo é demonstrar como:

1. Obter e preparar os arquivos de um site estático.  
2. Criar um Dockerfile para configurar o Nginx como servidor web para este site.  
3. Construir uma imagem Docker contendo o site e o Nginx.  
4. Executar um container a partir desta imagem para hospedar o site.

## **Pré-requisitos**

* **Docker Engine** instalado e em execução.  
* Uma **Landing Page da Creative Tim** (ou qualquer site HTML/CSS estático) baixada e os arquivos extraídos para uma pasta no seu computador.

## **Passos para Configuração e Execução**

### **1\. Obtenha e Prepare sua Landing Page**

1. **Escolha e Baixe um Template:**  
   * Visite [Creative Tim](https://www.creative-tim.com/) e procure por templates HTML/CSS gratuitos (seção "Freebies" ou templates com versões "HTML").  
   * Faça o download do arquivo ZIP do template escolhido.  
2. **Extraia os Arquivos:**  
   * Extraia o conteúdo do arquivo ZIP para uma pasta no seu computador. Por exemplo, nomeie esta pasta como meu-template-site.  
   * Dentro desta pasta (meu-template-site), você deverá ter o arquivo index.html principal e subpastas como assets/ (contendo CSS, JS, imagens, etc.).

### **2\. Estruture seu Projeto**

Crie uma pasta principal para este projeto Docker. Dentro dela, coloque a pasta com os arquivos do seu site e o Dockerfile que criaremos a seguir.

Estrutura de diretórios sugerida:

/seu-projeto-docker/  
├── Dockerfile                \<-- Nosso arquivo Docker  
└── meu-template-site/        \<-- Pasta com os arquivos da landing page  
    ├── index.html  
    ├── assets/  
    │   ├── css/  
    │   ├── js/  
    │   └── img/  
    └── ... (outros arquivos e pastas do template)

### **3\. Crie o Dockerfile**

Na raiz do seu diretório de projeto (ex: /seu-projeto-docker/), crie um arquivo chamado Dockerfile (sem extensão) com o seguinte conteúdo:

\# Usar uma imagem base oficial do Nginx (Alpine é leve e recomendada)  
FROM nginx:1.27-alpine  
\# Você pode usar nginx:latest, mas especificar uma versão Alpine é bom para o tamanho.

\# Definir o diretório de trabalho (opcional, mas bom para organização se houver mais passos)  
\# WORKDIR /usr/share/nginx/html

\# Remover o conteúdo padrão do Nginx para garantir uma cópia limpa (opcional)  
\# RUN rm \-rf /usr/share/nginx/html/\*

\# Copiar os arquivos do seu site estático para o diretório raiz do Nginx  
\# ATENÇÃO: Substitua 'meu-template-site/' pelo nome exato da pasta  
\#          onde você extraiu os arquivos da sua landing page.  
\# O './' no início refere-se ao contexto de build (o diretório onde o Dockerfile está).  
COPY ./meu-template-site/ /usr/share/nginx/html/

\# Expor a porta 80 (Nginx escuta na porta 80 por padrão)  
EXPOSE 80

\# O comando padrão da imagem base do Nginx (nginx \-g 'daemon off;')  
\# já cuidará de iniciar o servidor. Não é necessário um CMD ou ENTRYPOINT aqui,  
\# a menos que você queira sobrescrever o comportamento padrão.

**Explicação do Dockerfile:**

* FROM nginx:1.27-alpine: Define a imagem base. nginx:1.27-alpine é uma versão específica e leve.  
* COPY ./meu-template-site/ /usr/share/nginx/html/:  
  * Esta é a instrução principal. Ela copia o **conteúdo** da sua pasta local meu-template-site/ (que deve estar no mesmo nível do Dockerfile ou em um subcaminho relativo a ele) para o diretório /usr/share/nginx/html/ dentro do container. Este é o diretório padrão de onde o Nginx serve arquivos.  
  * **Certifique-se de que o caminho de origem (./meu-template-site/) corresponda exatamente ao nome da pasta que contém seu index.html e a pasta assets/.** O / no final do caminho de origem é importante para copiar o conteúdo da pasta, e não a pasta em si com esse nome para dentro de /usr/share/nginx/html/.  
* EXPOSE 80: Documenta que o container expõe a porta 80, onde o Nginx escuta.

### **4\. Construa a Imagem Docker**

Abra seu terminal, navegue até o diretório raiz do seu projeto (ex: /seu-projeto-docker/) e execute o comando:

docker build \-t meu-site-estatico-nginx .

* \-t meu-site-estatico-nginx: Atribui uma tag (nome) meu-site-estatico-nginx à sua imagem.  
* .: Indica que o contexto do build (onde o Dockerfile e os arquivos a serem copiados estão) é o diretório atual.

### **5\. Execute o Container**

Após a construção da imagem ser concluída com sucesso, execute um container a partir dela:

docker run \-d \-p 8080:80 \--name container-site-estatico meu-site-estatico-nginx

* \-d: Executa o container em modo detached (em segundo plano).  
* \-p 8080:80: Mapeia a porta 8080 da sua máquina host para a porta 80 do container (onde o Nginx está escutando). Você pode escolher outra porta no host se a 8080 estiver ocupada (ex: \-p 81:80).  
* \--name container-site-estatico: Dá um nome ao seu container para facilitar o gerenciamento.  
* meu-site-estatico-nginx: O nome da imagem que você acabou de construir.

### **6\. Acesse seu Site**

Abra seu navegador e acesse: http://localhost:8080 (ou a porta do host que você escolheu no passo anterior).

Você deverá ver a sua landing page da Creative Tim sendo servida pelo Nginx rodando no container Docker\!

### **7\. Parando e Removendo o Container (Quando Necessário)**

Para parar o container:

docker stop container-site-estatico

Para remover o container (após pará-lo):

docker rm container-site-estatico

## **Conclusão**

Containerizar um site estático com Nginx e Docker é um processo direto que oferece grandes benefícios em termos de portabilidade, consist