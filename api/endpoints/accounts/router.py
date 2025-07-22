from fastapi import APIRouter, Depends, status
from typing import List

from api.endpoints.auth.providers import get_current_user
from api.endpoints.accounts.providers import get_account_service
from api.endpoints.accounts.services import AccountService
from api.endpoints.accounts.schemas import (ResponseAccountsSchema, ResponseAccountsPublicSchema, 
                                            ResponseAccountsAdminSchema, UpdateAccountsSchema)
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
    """
    Recupera os dados de uma conta pelo seu ID, garantindo que o usuário tenha permissão para acessá-la.

    Esta rota retorna os detalhes públicos da conta solicitada, desde que o usuário autenticado 
    seja administrador ou dono da conta.

    Args:
        account_id (int): ID da conta a ser recuperada.
        service (AccountService): Serviço injetado para lidar com a lógica de negócio da conta.
        user (User): Usuário autenticado que faz a requisição.

    Returns:
        ResponseAccountsSchema[ResponseAccountsPublicSchema]: 
            Objeto contendo uma mensagem de sucesso e os dados públicos da conta.

    Raises:
        HTTPException: 
            - 403 se o usuário não tiver permissão para acessar a conta.
            - 404 se a conta não for encontrada.
    """
    
    account = service.get_account(user, account_id)
    return ResponseAccountsSchema(message='Account found', data=account)

@router.post('/{account_id}/update', status_code=status.HTTP_200_OK, response_model=ResponseAccountsSchema[ResponseAccountsPublicSchema])
async def update_account(account_id: int, update_account_schema: UpdateAccountsSchema, 
                         service: AccountService = Depends(get_account_service),
                         user: User = Depends(get_current_user)):
    """
    Atualiza os dados de uma conta específica identificada pelo `account_id`.

    Recebe os dados para atualização via schema `UpdateAccountsSchema` e verifica se o usuário 
    autenticado tem permissão para realizar a alteração (deve ser administrador ou dono da conta).
    Retorna os dados atualizados da conta após a alteração.

    Args:
        account_id (int): ID da conta a ser atualizada.
        update_account_schema (UpdateAccountsSchema): Dados opcionais para atualização da conta.
        service (AccountService): Serviço responsável pela lógica de negócio da conta.
        user (User): Usuário autenticado realizando a requisição.

    Returns:
        ResponseAccountsSchema[ResponseAccountsPublicSchema]: 
            Objeto contendo mensagem de sucesso e os dados públicos da conta atualizada.

    Raises:
        HTTPException: 
            - 403 se o usuário não estiver autorizado a atualizar a conta.
            - 404 se a conta não for encontrada.
    """
    account = service.update_account(user, account_id, update_account_schema)
    return ResponseAccountsSchema(message='Update completed', data=account)