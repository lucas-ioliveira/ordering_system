from fastapi import APIRouter, Depends, status
from typing import List

from api.endpoints.auth.providers import get_current_user
from api.endpoints.accounts.providers import get_account_service
from api.endpoints.accounts.services import AccountService
from api.endpoints.accounts.schemas import (ResponseAccountsSchema, ResponseAccountsPublicSchema, 
                                            ResponseAccountsAdminSchema)
from api.models.users import User

router = APIRouter(
    prefix='/api/v1/accounts', 
    tags=['accounts'], 
    dependencies=[Depends(get_current_user)]
)

@router.get('/', status_code=status.HTTP_200_OK, response_model=ResponseAccountsSchema[List[ResponseAccountsPublicSchema]])
async def get_all_accounts(offset: int = 0, limit: int = 10,
                           service: AccountService = Depends(get_account_service),
                           user: User = Depends(get_current_user)):
    
    """
    Recupera todos os usuários do banco de dados com paginação.

    Parâmetros
    ----------
    offset : int, opcional
        O número de usuários a serem pulados antes de iniciar a coleta do conjunto de resultados. Padrão é 0.
    limit : int, opcional
        O número m ximo de usuários a serem retornados. Padrão é 10.
    service : AccountService
        A inst ncia do serviço de usuários usada para recuperar usuários.
    user : User
        O usuário autenticado atual.

    Retornos
    -------
    ResponseAccountsSchema[List[ResponseAccountsPublicSchema]]
        Um esquema de resposta contendo uma mensagem e a lista de usuários.
    """
    account = service.get_all_accounts(user, offset, limit)
    return ResponseAccountsSchema(message='Accounts found', data=account)

@router.get('/admin', status_code=status.HTTP_200_OK, response_model=ResponseAccountsSchema[List[ResponseAccountsAdminSchema]])
async def get_all_accounts_admin(offset: int = 0, limit: int = 10,
                           service: AccountService = Depends(get_account_service),
                           user: User = Depends(get_current_user)):
    
    """
    Recupera todos os usuários administradores do banco de dados com paginação.

    Parâmetros
    ----------
    offset : int, opcional
        O número de usuários a serem pulados antes de iniciar a coleta do conjunto de resultados. Padrão é 0.
    limit : int, opcional
        O número m ximo de usuários a serem retornados. Padrão é 10.
    service : AccountService
        A inst ncia do serviço de usuários usada para recuperar usuários.
    user : User
        O usuário autenticado atual.

    Retornos
    -------
    ResponseAccountsSchema[List[ResponseAccountsAdminSchema]]
        Um esquema de resposta contendo uma mensagem e a lista de usuários administradores.
    """
    account = service.get_all_accounts_admin(user, offset, limit)
    return ResponseAccountsSchema(message='Accounts found', data=account)

@router.get('/{account_id}', status_code=status.HTTP_200_OK, response_model=ResponseAccountsSchema[ResponseAccountsPublicSchema])
async def get_account(account_id: int, service: AccountService = Depends(get_account_service),
                      user: User = Depends(get_current_user)):
    
    account = service.get_account(user, account_id)
    return ResponseAccountsSchema(message='Account found', data=account)