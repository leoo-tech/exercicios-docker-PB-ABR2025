# Exercício Docker - Container Alpine com Variável de Ambiente

## Objetivo
Criar um container com a imagem Alpine passando uma variável de ambiente chamada `MEU_NOME` e imprimir seu valor usando o comando `echo`.

## Resolução

### Passo 1: Criar e executar o container com variável de ambiente

```bash
docker run -e MEU_NOME="João Silva" alpine echo $MEU_NOME
```

**Explicação dos parâmetros:**
- `docker run`: comando para criar e executar um novo container
- `-e MEU_NOME="João Silva"`: define a variável de ambiente MEU_NOME com o valor "João Silva"
- `alpine`: imagem base do Alpine Linux (muito leve)
- `echo $MEU_NOME`: comando que será executado dentro do container para imprimir a variável

### Alternativa - Executar em modo interativo

Se você quiser executar o container de forma interativa para explorar mais:

```bash
# Executar container em modo interativo
docker run -it -e MEU_NOME="João Silva" alpine sh

# Dentro do container, execute:
echo $MEU_NOME
echo "Olá, $MEU_NOME!"
```

### Passo 2: Verificar o resultado

O comando deve retornar:
```
João Silva
```

## Comandos adicionais úteis

### Listar containers em execução
```bash
docker ps
```

### Listar todos os containers (incluindo parados)
```bash
docker ps -a
```

### Remover containers parados
```bash
docker container prune
```

## Variações do exercício

### Múltiplas variáveis de ambiente
```bash
docker run -e MEU_NOME="João Silva" -e IDADE="30" alpine sh -c 'echo "Nome: $MEU_NOME, Idade: $IDADE"'
```

### Usando arquivo de variáveis
Crie um arquivo `.env`:
```bash
MEU_NOME=João Silva
IDADE=30
CIDADE=São Paulo
```

Execute com:
```bash
docker run --env-file .env alpine sh -c 'echo "Nome: $MEU_NOME, Cidade: $CIDADE"'
```

## Notas importantes

- A imagem Alpine é uma distribuição Linux muito leve (cerca de 5MB)
- As variáveis de ambiente são definidas no momento da criação do container
- O container é removido automaticamente após a execução (comportamento padrão)
- Para manter o container após execução, use a flag `--name` para nomeá-lo

## Resultado esperado

Ao executar o comando principal, você verá apenas o valor da variável impressa no terminal:
```
João Silva
```

Este exercício demonstra conceitos fundamentais do Docker:
- Uso de imagens base
- Passagem de variáveis de ambiente
- Execução de comandos em containers