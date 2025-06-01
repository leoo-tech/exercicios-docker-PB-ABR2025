# Exercício Docker: Terminal Interativo no Ubuntu e Instalação do `curl`

Este guia descreve os passos para iniciar um container Docker a partir da imagem `ubuntu`, obter um terminal interativo (shell Bash), navegar pelo sistema de arquivos do container e instalar o pacote `curl` utilizando o gerenciador de pacotes `apt`.

## Objetivo

O objetivo deste exercício é praticar:
* A execução de containers Docker em modo interativo.
* A exploração básica do sistema de arquivos dentro de um container.
* A instalação de pacotes de software dentro de um container Ubuntu usando `apt`.

## Pré-requisitos

* Docker instalado e em execução na sua máquina.

## Passos para Execução

### 1. Iniciar o Container Ubuntu Interativamente

Abra o seu terminal e execute o seguinte comando para iniciar um novo container a partir da imagem `ubuntu` e acessar seu shell Bash:

```bash
docker run -it ubuntu bash
```

#### Explicação do comando:

`docker run`: Comando para criar e iniciar um novo container.

`-it`: Combinação de duas flags:
`-i (--interactive)`: Mantém o STDIN (entrada padrão) aberto, permitindo interação.
`-t (--tty)`: Aloca um pseudo-TTY (terminal), o que nos dá a interface de linha de comando.

`ubuntu`: Especifica a imagem Docker a ser utilizada (a versão mais recente da imagem oficial ubuntu será baixada se você não a tiver localmente).

`bash`: O comando que será executado dentro do container assim que ele iniciar. Neste caso, iniciamos o shell Bash.

Após executar este comando, o prompt do seu terminal mudará, indicando que você agora está dentro do shell do container Ubuntu (algo como `root@<id_do_container>:/#`).

### 2. Navegando no Sistema de Arquivos (Dentro do Container)

Agora que você está dentro do container, pode usar comandos Linux padrão para explorar o sistema de arquivos:

`ls`: Listar arquivos e diretórios no diretório atual.

`pwd`: Mostrar o caminho do diretório atual.

`cd <caminho>`: Mudar de diretório. Exemplos:

`cd /`: Ir para o diretório raiz.

`cd /etc`: Ir para o diretório de configurações.

`cd /tmp`: Ir para o diretório temporário.

`cd ..`: Voltar um nível no diretório.

`ls -la /etc`	: Listar todos os arquivos (incluindo ocultos) no diretório /etc com detalhes.

Sinta-se à vontade para explorar diferentes diretórios para se familiarizar com a estrutura de um container Linux básico.

### 3. Instalando o `curl`

Ainda dentro do terminal do container, execute os seguintes comandos para instalar o curl:

- a. Atualize a lista de pacotes disponíveis:

É uma boa prática atualizar os repositórios de pacotes antes de instalar qualquer software novo.
```bash
apt update
```

- b. Instale o `curl`:

```bash
apt install curl -y
```
A flag -y confirma automaticamente quaisquer prompts durante a instalação.

O apt fará o download e a instalação do curl e suas dependências.

### 4. Verificando a Instalação do curl (Opcional, Dentro do Container)

Verificar a versão do curl:

```bash
curl --version
``` 
Verificar o caminho do executável do curl:

```bash
which curl
```

(Deverá retornar algo como /usr/bin/curl)

Tentar usar o curl para buscar uma página simples (ele imprimirá o HTML da página no terminal):
```bash
curl http://example.com
```

### 5. Saindo do Container

Quando terminar de explorar e instalar o curl, você pode sair do terminal interativo do container e retornar ao terminal do seu computador host. Para isso, simplesmente digite:

```bash
exit
``` 

Ao executar `exit`, o processo bash principal do container terminará. Como este era o processo principal e o container foi iniciado com `-it` (e não com `-d` ou `--rm` por padrão para este comando específico), o container parará após você sair.

Se você tivesse iniciado o container com `docker run -it --rm ubuntu bash`, ele seria parado E removido automaticamente ao sair. Caso contrário, o container parado ainda existirá e poderá ser iniciado novamente (`docker start <id_do_container>`) ou removido (`docker rm <id_do_container>`).

