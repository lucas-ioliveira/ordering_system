# Ordering System

Nesse repositório contém um projeto back-end realizado com python, framework FastApi e Docker.

Desenvolvi esse projeto com o intuito de aplicar e aprimorar minhas habilidades em FastApi e desenvolvimento em containers utilizando o Docker.

O Projeto consiste em uma Api para gereciamento de pedidos de um delivery. O sistema é acessível por usuários comuns (clientes) e colaboradores do delivery. Os mesmos conseguem realizar login no sistema, cadastrar-se como novo usuário e todas as operaçoes de um CRUD para pedidos, itens do pedido e gerenciamento de conta de usuário, lembrando que algumas operações o usuário precisa de privilégios administrativos. A api conta com uma autenticação jwt e criptografia de senhas.

<br>

<h2>Pré-requisitos</h2>

- [Docker](https://www.docker.com/) 

<br>

<h2>Clone</h2>

```bash
git clone https://github.com/lucas-ioliveira/ordering_system.git
```

<br>

<h2 id="started">🚀 Primeiros passos</h2>

<br>

<p>Obs: Na raiz do projeto encontrará um arquivo chamado .env_exemple, renomeie para .env e adicione os valores que são necessários. </p>

<br>

<p>Basta entrar no diretório do projeto e no terminal rodar o comando:</p> 

```bash
make build
```

- ou

```bash
docker compose -f docker-compose.yaml up --build
```

<p>Isso fará com que todas as dependências sejam instaladas, migrações do banco de dados, criação de um usuário com permissão admin (fique atento ao terminal pois o e-mail e senha será mostrado lá), e um container docker.</p>

<br>

<p>Verifique se o container está em execução com o comando:</p>

```bash
docker ps -a
```

<br>

<p>Acessando o container:</p>

```bash
make enter container
```
- ou

```bash
docker exec -it ordering_system_app bash
```

<h2 id="routes">📍 API Endpoints</h2>

<p>Após executar o projeto é possivel acessar a rota: (/http://localhost:8009/docs/) onde terá acesso ao swagger e uma documentação mais detalhada e também testar os endpoints.</p>

<br>

**Token**

<p>A validade do token está definida para 30 minutos.</p>
   
| <kbd>POST /api/v1/auth/login/</kbd> | Obtendo o token de acesso para consumo da API.


**REQUEST**
```json
{
  "username": "Seu usuário",
  "password": "Sua senha"
}
```

**RESPONSE**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxNzUzMjE1ODU2fQ.bi5SSdFJK9aFVOk6H3y3uwWnrw2HamwunxCTnbJXjHg",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxNzUzODE4ODU2fQ.eAQKnbbIg_wTsnAZPId4pww_SNtcEU3c2HQHnWq2Wv4",
  "token_type": "Bearer"
}
```

<br>

- A validade do  refresh token está definida para 7 dias.
   
| <kbd>POST /api/v1/auth/refresh-token/</kbd> | Obtendo um novo token.


**REQUEST**
```
curl -X 'GET' \
  'http://localhost:8009/api/v1/auth/refresh-token' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2t...'

```

**RESPONSE**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxNzUzMjE2NzI3fQ.abEhOeYOOf67LY0wVBx8bRvxxsGxSp1Ldb8kE9aUnWs",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxNzUzODE5NzI3fQ.u1-yji2W5ZCiPsCszapLWl8ECuejroX45Sbk30GOy78",
  "token_type": "Bearer"
}
```

<br><br>


**Clients**

<p>Exemplo criação de conta (Usuário comum, ou seja, um cliente.):</p>

| <kbd>POST /api/v1/auth/create-account/</kbd> | Endpoint para criação de cliente.


**REQUEST**
```json
{
  "name": "cliente",
  "email": "cliente01@email.com",
  "password": "123456",
  "active": true
}
```

**RESPONSE**
```json
{
  "message": "Usuário criado com sucesso.",
  "data": {
    "id": 2,
    "name": "cliente",
    "email": "cliente01@email.com",
    "active": true,
    "admin": false
  }
}
```
```json
status  201 created
```

<br><br>

**Pedidos**

<p>Exemplo criação de pedido:</p>

| <kbd>POST /api/v1/orders/</kbd> | Endpoint para criação de pedidos.


**REQUEST**
```json
{
  "user": 2
}
```

**RESPONSE**
```json
{
  "message": "Pedido criado com sucesso.",
  "data": {
    "id": 1,
    "user": 2,
    "status": "PENDENTE",
    "price": 0,
    "active": true,
    "items": []
  }
}
```
```json
status  201 created
```

<br><br>

**Itens do pedidos**

<p>Exemplo criação de itens do pedido:</p>

| <kbd>POST /api/v1/orders-items/</kbd> | Endpoint para criação de itens do pedido.


**REQUEST**
```json
{
  "amount": 1,
  "flavor": "Portuguesa",
  "size": "G",
  "unit_price": 50,
  "order": 1
}
```

**RESPONSE**
```json
{
  "message": "Item do do pedido criado com sucesso.",
  "data": {
    "id": 1,
    "amount": 1,
    "flavor": "Portuguesa",
    "size": "G",
    "unit_price": 50,
    "order": 1,
    "active": true
  }
}
```
```json
status  201 created
```
