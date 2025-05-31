# Exercício Docker: Servindo Página HTML Customizada com Nginx e Volume Local

Este documento descreve a solução para o exercício de criar um container Docker com Nginx que sirva uma página HTML (`index.html`) customizada. A página é disponibilizada para o Nginx através de um volume local montado no container, permitindo que alterações no arquivo local sejam refletidas em tempo real.

## Objetivo

O objetivo principal é demonstrar como:
1.  Criar um arquivo HTML simples.
2.  Executar um container Nginx.
3.  Mapear uma porta do host para a porta do container Nginx.
4.  Montar um diretório local (contendo o `index.html`) como um volume dentro do container Nginx, no diretório raiz do servidor web.
5.  Acessar a página customizada através do navegador.

## Pré-requisitos

* Docker instalado e em execução na sua máquina.

## Passos para a Solução

### 1. Crie sua Página HTML (`index.html`)

Primeiro, crie um diretório no seu computador para armazenar os arquivos do seu site. Por exemplo, `meu_site_nginx`. Dentro deste diretório, crie um arquivo chamado `index.html`.

**Estrutura de diretórios sugerida:**

/caminho/no/seu/computador/
└── meu_site_nginx/
└── index.html

### 2. Conteúdo do `index.html`

**Exemplo de conteúdo para `index.html`:**
```html
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Minha Página Customizada com Nginx</title>
    <style>
        body { font-family: Arial, sans-serif; display: flex; flex-direction: column; justify-content: center; align-items: center; height: 100vh; margin: 0; background-color: #f4f4f4; text-align: center; }
        h1 { color: #0077cc; }
        p { color: #333; }
    </style>
</head>
<body>
    <h1>Olá, Nginx com Docker!</h1>
    <p>Esta página está sendo servida a partir de um volume local montado.</p>
</body>
</html>
```
Substitua `/caminho/no/seu/computador/` pelo caminho real onde você criou a pasta `meu_site_nginx`.

### 3. Execute o Container Nginx com Volume Montado
Abra seu terminal ou prompt de comando e execute o comando Docker abaixo.

> _Observação Importante sobre Portas:_ A porta padrão para HTTP é a 80. No entanto, esta porta pode já estar em uso por outro serviço no seu computador. Para evitar conflitos, neste exemplo, mapearemos a porta 8080 do seu computador (host) para a porta 80 do container Nginx.

Comando:
```bash
docker run -d -p 8080:80 -v /caminho/no/seu/computador/meu_site_nginx:/usr/share/nginx/html:ro --name meu-nginx-customizado nginx
```
Lembre-se de substituir `/caminho/no/seu/computador/meu_site_nginx` pelo caminho absoluto para a pasta `meu_site_nginx`  que você criou.

#### 3.1 Explicação do comando:

`docker run:` Comando para criar e iniciar um novo container.

`-d:` Executa o container em modo "detached" (em segundo plano), liberando o terminal.

`-p 8080:80:` Mapeia a porta.

`8080:` Porta no seu computador (host) pela qual você acessará o Nginx.

`80:` Porta padrão em que o Nginx escuta dentro do container.

`-v`: Monta um volume.

`/caminho/no/seu/computador/meu_site_nginx:` Caminho absoluto para o diretório no seu computador que contém o index.html.

`/usr/share/nginx/html:` Diretório raiz padrão onde o Nginx serve arquivos dentro do container.

`:ro:` (Read-Only) Monta o volume como somente leitura dentro do container. Isso é uma boa prática quando o container não precisa escrever no volume.

`--name meu-nginx-customizado:` Atribui um nome amigável (meu-nginx-customizado) ao container para facilitar o gerenciamento.

`nginx:` Especifica a imagem Docker oficial do nginx a ser utilizada (será baixada automaticamente se não existir localmente).

### 4. Acesse sua Página HTML

