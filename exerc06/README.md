# Exercício Docker - Multi-stage Build para Aplicação Go (GS PING)

## Objetivo
Utilizar um **multi-stage build** para otimizar uma aplicação **Go** (projeto GS PING), reduzindo drasticamente o tamanho da imagem final Docker.

## O que é Multi-stage Build?

Multi-stage build permite usar múltiplas imagens base em um único Dockerfile, copiando apenas os artefatos necessários entre os estágios. Isso é especialmente útil para linguagens compiladas como Go, onde precisamos das ferramentas de build apenas durante a compilação.

## Estrutura do Projeto GS PING

Primeiro, vamos criar a estrutura básica do projeto:

```
gs-ping/
├── main.go
├── go.mod
├── Dockerfile
└── README.md
```

## Código da Aplicação GS PING

### main.go
```go
package main

import (
    "encoding/json"
    "fmt"
    "log"
    "net/http"
    "os"
    "time"
)

type PingResponse struct {
    Status    string    `json:"status"`
    Message   string    `json:"message"`
    Timestamp time.Time `json:"timestamp"`
    Version   string    `json:"version"`
}

type HealthResponse struct {
    Status  string `json:"status"`
    Uptime  string `json:"uptime"`
    Service string `json:"service"`
}

var startTime = time.Now()

func pingHandler(w http.ResponseWriter, r *http.Request) {
    response := PingResponse{
        Status:    "success",
        Message:   "pong",
        Timestamp: time.Now(),
        Version:   "1.0.0",
    }
    
    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(response)
}

func healthHandler(w http.ResponseWriter, r *http.Request) {
    uptime := time.Since(startTime)
    
    response := HealthResponse{
        Status:  "healthy",
        Uptime:  uptime.String(),
        Service: "GS PING",
    }
    
    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(response)
}

func main() {
    port := os.Getenv("PORT")
    if port == "" {
        port = "8080"
    }

    http.HandleFunc("/ping", pingHandler)
    http.HandleFunc("/health", healthHandler)
    http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
        fmt.Fprintf(w, "GS PING Service is running! Try /ping or /health")
    })

    fmt.Printf("GS PING server starting on port %s...\n", port)
    log.Fatal(http.ListenAndServe(":"+port, nil))
}
```

### go.mod
```go
module gs-ping

go 1.21
```

## Dockerfile com Multi-stage Build

### Versão Otimizada (Multi-stage)
```dockerfile
# ==============================================================================
# ESTÁGIO 1: BUILD (Imagem pesada com ferramentas de desenvolvimento)
# ==============================================================================
FROM golang:1.21-alpine AS builder

# Instalar dependências necessárias para build
RUN apk add --no-cache git ca-certificates tzdata

# Definir diretório de trabalho
WORKDIR /app

# Copiar arquivos de dependência
COPY go.mod go.sum ./

# Baixar dependências
RUN go mod download

# Copiar código fonte
COPY . .

# Compilar aplicação
# CGO_ENABLED=0: desabilita CGO para criar binário estático
# GOOS=linux: compilar para Linux
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o gs-ping .

# ==============================================================================
# ESTÁGIO 2: RUNTIME (Imagem mínima apenas com o binário)
# ==============================================================================
FROM alpine:latest

# Instalar certificados CA (necessário para HTTPS)
RUN apk --no-cache add ca-certificates

# Criar usuário não-root para segurança
RUN adduser -D -s /bin/sh appuser

# Definir diretório de trabalho
WORKDIR /app

# Copiar binário do estágio anterior
COPY --from=builder /app/gs-ping .

# Copiar certificados de timezone
COPY --from=builder /usr/share/zoneinfo /usr/share/zoneinfo

# Alterar proprietário dos arquivos
RUN chown -R appuser:appuser /app

# Usar usuário não-root
USER appuser

# Expor porta
EXPOSE 8080

# Definir variáveis de ambiente
ENV PORT=8080
ENV GIN_MODE=release

# Comando para executar a aplicação
CMD ["./gs-ping"]
```

## Comparação: Dockerfile Tradicional vs Multi-stage

### Dockerfile Tradicional (NÃO otimizado)
```dockerfile
FROM golang:1.21-alpine

WORKDIR /app

COPY go.mod go.sum ./
RUN go mod download

COPY . .

RUN go build -o gs-ping .

EXPOSE 8080

CMD ["./gs-ping"]
```

## Scripts de Build e Execução

### build.sh
```bash
#!/bin/bash

echo "🏗️  Building GS PING with multi-stage Docker..."

# Build da imagem multi-stage
docker build -t gs-ping:multistage .

# Build da imagem tradicional para comparação
docker build -f Dockerfile.traditional -t gs-ping:traditional .

echo "📊 Comparando tamanhos das imagens:"
echo "Multi-stage:"
docker images gs-ping:multistage --format "table {{.Repository}}:{{.Tag}}\t{{.Size}}"

echo "Tradicional:"
docker images gs-ping:traditional --format "table {{.Repository}}:{{.Tag}}\t{{.Size}}"

echo "✅ Build concluído!"
```

### run.sh
```bash
#!/bin/bash

echo "🚀 Executando GS PING..."

# Parar container se estiver rodando
docker stop gs-ping 2>/dev/null || true
docker rm gs-ping 2>/dev/null || true

# Executar novo container
docker run -d \
  --name gs-ping \
  -p 8080:8080 \
  -e PORT=8080 \
  gs-ping:multistage

echo "✅ GS PING está rodando em http://localhost:8080"
echo "🔍 Endpoints disponíveis:"
echo "  - http://localhost:8080/"
echo "  - http://localhost:8080/ping"
echo "  - http://localhost:8080/health"

# Mostrar logs
echo "📋 Logs do container:"
docker logs -f gs-ping
```

## Comandos para Executar

### 1. Criar e executar o projeto
```bash
# Criar diretório do projeto
mkdir gs-ping && cd gs-ping

# Criar arquivos (copie o conteúdo acima)
# main.go, go.mod, Dockerfile

# Tornar scripts executáveis
chmod +x build.sh run.sh

# Build da aplicação
./build.sh
```

### 2. Executar a aplicação
```bash
# Executar container
./run.sh
```

### 3. Testar a aplicação
```bash
# Testar endpoint principal
curl http://localhost:8080/

# Testar ping
curl http://localhost:8080/ping

# Testar health check
curl http://localhost:8080/health
```

## Análise de Resultados

### Comparação de Tamanhos Típicos

| Tipo de Build | Tamanho da Imagem | Redução |
|---------------|-------------------|---------|
| Tradicional   | ~300-400 MB       | -       |
| Multi-stage   | ~15-25 MB         | ~94%    |

### Verificar tamanhos reais
```bash
# Listar todas as imagens gs-ping
docker images gs-ping

# Análise detalhada da imagem
docker inspect gs-ping:multistage | grep -i size
```

## Vantagens do Multi-stage Build

1. **Tamanho Reduzido**: Imagem final 90%+ menor
2. **Segurança**: Menos superficie de ataque (sem ferramentas de build)
3. **Performance**: Download e deploy mais rápidos
4. **Limpeza**: Apenas binário e dependências essenciais
5. **Eficiência**: Menor uso de armazenamento e banda

## Comandos Úteis para Monitoramento

### Verificar container em execução
```bash
# Status do container
docker ps | grep gs-ping

# Logs em tempo real
docker logs -f gs-ping

# Estatísticas de recursos
docker stats gs-ping

# Entrar no container (debug)
docker exec -it gs-ping sh
```

### Limpeza
```bash
# Parar e remover container
docker stop gs-ping && docker rm gs-ping

# Remover imagens
docker rmi gs-ping:multistage gs-ping:traditional

# Limpeza geral
docker system prune -f
```

## Resultado Esperado

Após executar o build e run, você deve ter:

1. **Container rodando** em http://localhost:8080
2. **Imagem otimizada** com tamanho ~15-25 MB vs ~300-400 MB
3. **Aplicação funcional** respondendo nos endpoints
4. **Redução de ~94%** no tamanho da imagem

Este exercício demonstra o poder do multi-stage build para otimização de imagens Docker em aplicações Go.