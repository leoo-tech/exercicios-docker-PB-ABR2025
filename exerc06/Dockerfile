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
## Run the tests in the container
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