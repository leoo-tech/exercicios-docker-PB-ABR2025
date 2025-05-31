# Configurando PostgreSQL e pgAdmin com Docker Compose

Este guia descreve como configurar e executar um ambiente com um banco de dados **PostgreSQL** e a ferramenta de administração **pgAdmin**, utilizando Docker Compose. O exemplo é baseado no projeto `postgresql-pgadmin` do repositório `docker/awesome-compose`.

## Objetivo

O objetivo é demonstrar como usar o Docker Compose para orquestrar múltiplos containers (PostgreSQL e pgAdmin), configurar variáveis de ambiente, gerenciar a persistência de dados com volumes e conectar as ferramentas.

---
## Pré-requisitos

* **Docker Engine** instalado e em execução.
* **Docker Compose** instalado (geralmente incluído no Docker Desktop).
* **Git** para clonar o repositório.

---
## Passos para Configuração e Execução

### 1. Obter os Arquivos do Projeto

Clone o repositório `docker/awesome-compose` e navegue até o diretório do projeto:

```bash
git clone [https://github.com/docker/awesome-compose.git](https://github.com/docker/awesome-compose.git)
cd awesome-compose/postgresql-pgadmin
```

Neste diretório, você encontrará o arquivo `compose.yaml` e um arquivo `.env`.

## 2. Arquivo de Variáveis de Ambiente (.env)
O arquivo .env neste diretório é usado para definir variáveis de ambiente que serão injetadas nos seus containers. Ele se parecerá com:

```env
# PostgreSQL
POSTGRES_USER=example
POSTGRES_PASSWORD=example
POSTGRES_DB=example

# pgAdmin
PGADMIN_DEFAULT_EMAIL=example@example.com
PGADMIN_DEFAULT_PASSWORD=example
PGADMIN_PORT=5050
```
- Credenciais do PostgreSQL: POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB são usados para inicializar o banco de dados.
- Credenciais do pgAdmin: PGADMIN_DEFAULT_EMAIL, PGADMIN_DEFAULT_PASSWORD são para o login no pgAdmin.
- Porta do pgAdmin: PGADMIN_PORT define a porta do host para acessar a interface web do pgAdmin.


## 3. Entendendo o compose.yaml
O arquivo compose.yaml define os serviços, redes e volumes:

```yaml
version: '3.8'

services:
  db: # Serviço PostgreSQL
    image: postgres:15
    container_name: db_container
    restart: always
    environment:
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: ${POSTGRES_DB}
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  pgadmin: # Serviço pgAdmin
    image: dpage/pgadmin4:latest
    container_name: pgadmin_container
    restart: always
    environment:
      PGADMIN_DEFAULT_EMAIL: ${PGADMIN_DEFAULT_EMAIL}
      PGADMIN_DEFAULT_PASSWORD: <span class="math-inline">\{PGADMIN\_DEFAULT\_PASSWORD\}
ports\:
\- "</span>{PGADMIN_PORT}:80"
    volumes:
      - pgadmin_data:/var/lib/pgadmin
    depends_on:
      - db

volumes:
  postgres_data:
  pgadmin_data:
```

### Destaques:

- Serviço db (PostgreSQL):
  - Usa a imagem postgres:15.
  - Configurado com variáveis do .env.
  - Mapeia a porta 5432 do container para a porta 5432 do host.
  - Usa o volume nomeado postgres_data para persistir os dados do banco.

- Serviço pgadmin:
  - Usa a imagem dpage/pgadmin4:latest.
  - Configurado com variáveis do .env para login e porta.
  - A porta interna 80 do pgAdmin é mapeada para a porta definida em PGADMIN_PORT (padrão 5050) no host.
  - Usa o volume nomeado pgadmin_data para persistir as configurações do pgAdmin.
  - depends_on: - db garante que o PostgreSQL inicie antes do pgAdmin.
  - volumes: Declara os volumes nomeados postgres_data e pgadmin_data.

## 4. Iniciando os Serviços

  No terminal, dentro do diretório awesome-compose/postgresql-pgadmin, execute:

```bash
docker compose up -d
```

Este comando fará o download das imagens (se não existirem localmente) e iniciará os containers do PostgreSQL e pgAdmin em segundo plano (-d).

## 5. Acessando o pgAdmin e Conectando ao PostgreSQL

1. Acesse o pgAdmin: Abra seu navegador e vá para http://localhost:${PGADMIN_PORT} (por padrão, http://localhost:5050).

2. Login no pgAdmin: Use o email e senha definidos no arquivo .env (padrão: example@example.com / example).

3. Adicionar um Novo Servidor (Conectar ao PostgreSQL):
- Dentro do pgAdmin, clique com o botão direito em "Servers" -> "Create" -> "Server...".
- Aba "General": Dê um nome à conexão (ex: Docker-PostgreSQL).
- Aba "Connection":
  - Host name/address: db (Este é o nome do serviço PostgreSQL no compose.yaml).
  - Port: 5432.
  - Maintenance database: O valor de POSTGRES_DB do seu .env (padrão: example).
  - Username: O valor de POSTGRES_USER do seu .env (padrão: example).
  - Password: O valor de POSTGRES_PASSWORD do seu .env (padrão: example).
- Clique em "Save".
Agora você deve estar conectado ao seu banco de dados PostgreSQL e pode gerenciá-lo através do pgAdmin.


## 6. Parando os Serviços
```bash
docker compose down
```

Se desejar remover também os volumes de dados (onde os dados do PostgreSQL e as configurações do pgAdmin são armazenados), use:

```bash
docker compose down -v
```

