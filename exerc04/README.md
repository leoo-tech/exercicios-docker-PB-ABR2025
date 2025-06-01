# Exercício Docker: Persistência de Dados no MySQL com Volumes Nomeados

Este guia detalha como configurar um container Docker para o MySQL (versão 5.7), utilizando um **volume nomeado** para garantir que os dados do banco de dados persistam mesmo após o container ser parado, removido e recriado.

## Objetivo

O objetivo principal é demonstrar e praticar:
1.  A criação e utilização de volumes nomeados no Docker.
2.  A execução de um container MySQL configurado para usar um volume nomeado para seus dados.
3.  A criação de um banco de dados dentro do container.
4.  A verificação da persistência dos dados após parar e reiniciar (ou recriar) o container.

## Pré-requisitos

* Docker Engine instalado e em execução na sua máquina.

## Passos para Execução

### 1. Crie um Volume Nomeado (Opcional, mas Recomendado)

Embora o Docker possa criar um volume nomeado automaticamente se ele não existir ao ser referenciado no comando `docker run`, é uma boa prática criá-lo explicitamente para melhor gerenciamento.

```bash
docker volume create dados_mysql_app
```

### 2. Inicie o Container MySQL
Vamos iniciar um container a partir da imagem `mysql:5.7`, montando o volume nomeado no diretório de dados padrão do MySQL (`/var/lib/mysql`) e definindo a senha do usuário root.

⚠️ Importante: Substitua `SUA_SENHA_FORTE_AQUI` por uma senha de sua escolha.

```bash
docker run -d \
  --name mysql_app \
  -e MYSQL_ROOT_PASSWORD=SUA_SENHA_FORTE_AQUI \
  -v dados_mysql_app:/var/lib/mysql \
  mysql:5.7
```
#### Explicação dos parâmetros:
* `-d`: Executa o container em segundo plano (modo "detached").
* `--name mysql_app`: Nomeia o container como `mysql_app`.
* `-e MYSQL_ROOT_PASSWORD=SUA_SENHA_FORTE_AQUI`: Define a variável de ambiente para a senha do usuário root do MySQL.
* `-v dados_mysql_app:/var/lib/mysql`: Monta o volume nomeado `dados_mysql_app` no diretório de dados do MySQL dentro do container.

Aguarde alguns instantes para o MySQL inicializar completamente. Você pode verificar os logs com `docker logs mysql_app`.

3. Conecte-se ao MySQL e Crie um Banco de Dados

Use `docker exec` para entrar no container e acessar o cliente MySQL:

```bash
docker exec -it mysql_app mysql -u root -p
```
- O comando solicitará a senha. Digite a `SUA_SENHA_FORTE_AQUI` que você definiu.

Dentro do prompt do MySQL (mysql>), crie um novo banco de dados e verifique sua existência:
```sql
CREATE DATABASE meu_banco_de_dados;
SHOW DATABASES;
```
Você deverá ver `meu_banco_de_dados` na lista de bancos de dados.

Para sair do cliente MySQL, digite:

```sql
exit;
```

### 4. Pare o Container
Para parar o container, use o seguinte comando:

```bash
docker stop mysql_app
```

### 5. Inicie o Container Novamente
Para reiniciar o container, use:

```bash
docker start mysql_app
```

### 6. Verifique a Persistência dos Dados
Para verificar se os dados persistiram, conecte-se novamente ao MySQL:

```bash
docker exec -it mysql_app mysql -u root -p
```
Digite sua senha.

Dentro do prompt do MySQL, verifique novamente os bancos de dados:
```sql
SHOW DATABASES;
```

Você deverá ver `meu_banco_de_dados` listado, confirmando que os dados persistiram mesmo após o container ser parado e reiniciado.

🎉 Você deverá ver o banco de dados `meu_banco_de_dados` ainda listado! Isso confirma que os dados foram armazenados no volume nomeado `dados_mysql_app` e persistiram mesmo após o container ser parado e reiniciado.

Saia do cliente MySQL:

```sql
EXIT;
```