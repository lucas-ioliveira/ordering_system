from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from api.endpoints.auth.services import AuthService
from api.endpoints.auth.schemas import (CreateUserSchemas, CreateUserAdminSchemas, LoginUserSchemas, 
                                        ResponseUserSchema, ResponseUser)
from api.config.security import oauth2_scheme
from api.endpoints.auth.providers import get_auth_service
from api.endpoints.auth.providers import get_current_user
from api.models.users import User


router = APIRouter(prefix='/api/v1/auth', tags=['auth'])

@router.post('/create-account', status_code=201, response_model=ResponseUserSchema[ResponseUser])
async def create_account(
    create_user_schema: CreateUserSchemas,
    service: AuthService = Depends(get_auth_service)
):
    """
    Cria um novo usuário no banco de dados.

    Recebe os dados do usuário e verifica se o e-mail do usuário a ser criado já existe no banco de dados.
    Se existir, lança um erro HTTP 400 com a mensagem "E-mail já cadastrado!".
    Caso contrário, hash a senha do usuário e cria o novo usuário no banco de dados.

    Se o usuário for criado com sucesso, retorna o usuário criado com o status HTTP 201.
    Se o usuário não for criado, retorna um erro HTTP 400 com a mensagem 'Erro ao criar o usuário.'.
    """

    user = service.create_user(create_user_schema)
    return ResponseUserSchema(message='Usuário criado com sucesso.', data=ResponseUser.from_orm(user))

@router.post('/create-account-admin', status_code=201, response_model=ResponseUserSchema[ResponseUser])
async def create_account_admin(
    create_user_admin_schema: CreateUserAdminSchemas,
    service: AuthService = Depends(get_auth_service),
    user: User = Depends(get_current_user)
):
    """
    Cria um novo usuário com admin no banco de dados.

    Recebe os dados do usuário e verifica se o e-mail do usuário a ser criado já existe no banco de dados.
    Se existir, lança um erro HTTP 400 com a mensagem "E-mail já cadastrado!".
    Caso contrário, hash a senha do usuário e cria o novo usuário no banco de dados.

    Se o usuário for criado com sucesso, retorna o usuário criado com o status HTTP 201.
    Se o usuário não for criado, retorna um erro HTTP 400 com a mensagem 'Erro ao criar o usuário.'.
    """

    user = service.create_user_admin(create_user_admin_schema, user)
    return ResponseUserSchema(message='Usuário criado com sucesso.', data=ResponseUser.from_orm(user))

@router.get('/refresh-token')
async def refresh_token(refresh_token: str = Depends(oauth2_scheme), 
                        service: AuthService = Depends(get_auth_service)):
    """
    Renova o token de acesso com o token de refresh informado.

    Utiliza o token de refresh informado para renovar o token de acesso.
    Retorna os tokens de acesso e atualiza o.

    Args:
    ----------
    refresh_token (str): O token de refresh a ser utilizado para renovar o token de acesso.

    Returns:
    ----------
    dict: Um dicion rio com os tokens de acesso e atualiza o.
    """
    refresh_token_service = service.refresh_token(refresh_token)
    return refresh_token_service

@router.post('/login')
async def login(login_user_schema: LoginUserSchemas, 
                service: AuthService = Depends(get_auth_service)):
    
    """
    Realiza o login do usuário e retorna os tokens de acesso.

    Verifica se o usuário existe e se as credenciais são válidas.
    Se o usuário não existir ou as credenciais forem inválidas,
    lança um erro HTTP 400 com a mensagem "Usuário não encontrado ou credenciais incorretas!".
    Caso contrário, cria os tokens de acesso e atualiza o e os retorna.

    Args:
    ----------
    login_user_schema (LoginUserSchemas): Os dados do usuário a ser logado.

    Returns:
    ----------
    dict: Um dicionário com os tokens de acesso e atualiza o.

    Raises:
    ----------
    HTTPException: Se o usuário não existir ou as credenciais forem inválidas.
    """
    login = service.login(login_user_schema)
    return login

@router.post('/login-form')
async def login_form(login_user_form: OAuth2PasswordRequestForm = Depends(), 
                service: AuthService = Depends(get_auth_service)):
    """
    Realiza o login do usuário para uso da documentação do FastAPI e retorna os tokens de acesso.

    Verifica se o usuário existe e se as credenciais são válidas.
    Se o usuário não existir ou as credenciais forem inválidas,
    lança um erro HTTP 400 com a mensagem "Usuário não encontrado ou credenciais incorretas!".
    Caso contrário, cria os tokens de acesso e atualiza o e os retorna.

    Args:
    ----------
    login_user_form (OAuth2PasswordRequestForm): Os dados do usuário a ser logado.

    Returns:
    ----------
    dict: Um dicionário com os tokens de acesso e atualiza o.

    Raises:
    ----------
    HTTPException: Se o usuário não existir ou as credenciais forem inválidas.
    """
    return service.login_form(login_user_form)


