#!/bin/bash

set -e  # Encerra o script caso qualquer comando falhe

echo "Aguardando o banco de dados..."
sleep 5  # opcional, mas pode ser substituído por uma verificação ativa de conexão

echo "Verificando se existem migrações..."

if [ -d "alembic/versions" ] && [ "$(ls -A alembic/versions)" ]; then
    echo "Aplicando migrações existentes..."
    alembic upgrade head
else
    echo "Nenhum arquivo de migração encontrado. Gerando migração inicial..."
    alembic revision --autogenerate -m "initial"
    alembic upgrade head
fi

echo "Criando usuário admin padrão (caso necessário)..."
python -c "from api.config.scripts.create_admin_user import create_super_user; create_super_user()"

echo "Iniciando o servidor..."
exec uvicorn main:app --host 0.0.0.0 --port 8009 --reload
