# Exercício Docker: Otimizando Aplicação Go (GS PING) com Multi-Stage Build

Este documento descreve como utilizar um **multi-stage build** no Docker para otimizar uma aplicação Go (especificamente o projeto "GS PING" de exemplo), resultando em uma imagem Docker final significativamente menor e mais segura.

---
## Objetivo

O objetivo principal é demonstrar como:
1.  Estruturar um `Dockerfile` com múltiplos estágios (build, teste opcional, e release).
2.  Compilar uma aplicação Go em um estágio de build que contém todas as ferramentas necessárias.
3.  Copiar apenas o binário compilado para um estágio final baseado em uma imagem mínima (como `distroless` ou `alpine`).
4.  Reduzir o tamanho da imagem final, excluindo ferramentas de desenvolvimento, código fonte e dependências de build desnecessárias.

---
## Pré-requisitos

1.  **Docker** instalado e em execução.
2.  **Código fonte da aplicação Go "GS PING"**:
    * `go.mod`
    * `go.sum`
    * Arquivos `*.go` da aplicação.
3.  Um arquivo **Dockerfile multi-stage** (o conteúdo de exemplo está abaixo). Salve este arquivo no mesmo diretório que o código fonte. Ele pode se chamar `Dockerfile` ou, como no nosso caso de depuração, `Dockerfile.multistage`.

---
## Conteúdo do `Dockerfile` Multi-Stage

Este é o Dockerfile multi-stage que utilizamos, baseado no exemplo do projeto `docker/docker-gs-ping`:

```dockerfile
# syntax=docker/dockerfile:1

##
## Build the application from source
##
FROM golang:1.19 AS build-stage

WORKDIR /app

COPY go.mod go.sum ./
RUN go mod download

COPY *.go ./

# Compila a aplicação, o executável é salvo em /docker-gs-ping
RUN CGO_ENABLED=0 GOOS=linux go build -o /docker-gs-ping

##
## Run the tests in the container (Opcional para a imagem final)
##
FROM build-stage AS run-test-stage
# Executa os testes. Este estágio não faz parte da imagem final de produção.
RUN go test -v ./...

##
## Deploy the application binary into a lean image
##
FROM gcr.io/distroless/base-debian11 AS build-release-stage

WORKDIR /

# Copia APENAS o binário compilado do 'build-stage'
COPY --from=build-stage /docker-gs-ping /docker-gs-ping

EXPOSE 8080

# Executa como um usuário não-root por segurança
USER nonroot:nonroot

# Define o ponto de entrada para o container
ENTRYPOINT ["/docker-gs-ping"]