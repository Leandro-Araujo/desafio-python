# Projeto de API com Flask e DynamoDB

Este projeto é uma API construída com Flask que interage com o DynamoDB. Abaixo estão as instruções para configurar o ambiente, criar a tabela no DynamoDB, iniciar a aplicação e executar os testes.

## Pré-requisitos

- Docker
- Docker Compose
- Python 3.8+
- AWS CLI (opcional, para interagir com o DynamoDB localmente)

## Configuração do Ambiente

### Passo 1: Configurar o Docker e o Docker Compose

1. Navegue até o diretório `infra`:
    ```bash
    cd infra
    ```

2. Inicie o Docker Compose:
    ```bash
    docker-compose up -d
    ```

### Passo 2: Criar a Tabela no DynamoDB

1. Torne o script `setup.sh` executável e execute-o:
    ```bash
    chmod +x setup.sh
    ./setup.sh
    ```

### Passo 3: Instalar Dependências e Iniciar a Aplicação

1. Navegue até o diretório `app`:
    ```bash
    cd ../app
    ```

2. Crie um ambiente virtual e ative-o:
    ```bash
    python -m venv venv
    source venv/bin/activate  # No Windows, use `venv\Scripts\activate`
    ```

3. Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```

4. Inicie a aplicação Flask:
    ```bash
    python src/index.py
    ```

### Passo 4: Executar os Testes

Os testes estão quebrados devido a um problema com diretorios.

1. Navegue até o diretório `test`:
    ```bash
    cd test
    ```

2. Execute os testes:
    ```bash
    pytest
    ```

## Rotas da API

### POST /users-batch

- Descrição: Recebe um arquivo com dados de usuários e pedidos e salva no banco de dados.
- Exemplo de uso:
    ```bash
    curl -X POST -F 'file=@path/to/your/file' http://localhost:5000/users-batch
    ```

### GET /users

- Descrição: Retorna todos os usuários.
- Exemplo de uso:
    ```bash
    curl http://localhost:5000/users
    ```

### GET /users/<user_id>

- Descrição: Retorna um usuário específico pelo ID.
- Exemplo de uso:
    ```bash
    curl http://localhost:5000/users/1
    ```

### GET /users/<user_id>/orders/<order_id>

- Descrição: Retorna um pedido específico de um usuário pelo ID do usuário e do pedido.
- Exemplo de uso:
    ```bash
    curl http://localhost:5000/users/1/orders/123
    ```

## Conclusão

Seguindo os passos acima, você configurará o ambiente, criará a tabela no DynamoDB, iniciará a aplicação e executará os testes. Se tiver alguma dúvida ou problema, sinta-se à vontade para abrir uma issue.
