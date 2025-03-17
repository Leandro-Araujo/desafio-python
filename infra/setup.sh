#!/bin/bash

# Cria a tabela no DynamoDB
aws dynamodb create-table --table-name tb001_users --attribute-definitions AttributeName=user_id,AttributeType=N AttributeName=order_id,AttributeType=N --key-schema AttributeName=user_id,KeyType=HASH AttributeName=order_id,KeyType=RANGE --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5 --endpoint-url=http://localhost:4566

echo "Tabela tb001_users criada com sucesso."