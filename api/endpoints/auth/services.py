import os
from passlib.context import CryptContext
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone

from fastapi import HTTPException
from jose import JWTError, jwt

from api.endpoints.auth.repository import AuthRepository
from api.endpoints.auth.schemas import CreateUserSchemas, CreateUserAdminSchemas, LoginUserSchemas
from api.models.users import User
from api.config.emuns import UserErrorMessages

load_dotenv()


class AuthService:
    def __init__(self, repository: AuthRepository):
        """
        Inicializa o serviço de autenticação.

        Args:
        repository (AuthRepository): O repositório de usuários.
        """
        self.repository = repository
        self.bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
        self.secret_key = os.getenv('SECRET_KEY')
        self.algorithm = os.getenv('ALGORITHM')
        self.access_token_expire = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))

    def encrypt_password(self, password: str) -> str:
        """
        Encripta a senha informada.

        Recebe uma senha como string e a encripta com o algoritmo bcrypt.

        Args:
            password (str): A senha a ser encriptada.

        Returns:
            str: A senha encriptada.
        """
        return self.bcrypt_context.hash(password)
    
    def create_user(self, data: CreateUserSchemas) -> User:
        """
        Cria um novo usuário no banco de dados.

        Verifica se o e-mail do usuário a ser criado já existe no banco de dados.
        Se existir, lan a um erro HTTP 400 com a mensagem "E-mail j  cadastrado!".
        Caso contr rio, hash a senha do usu rio e cria o novo usu rio no banco de dados.

        Args:
            data (CreateUserSchemas): Os dados do usu rio a ser criado.

        Returns:
            User: O usu rio criado.

        Raises:
            HTTPException: Se o e-mail do usuário já existir no banco de dados.
        """
        user_exists = self.repository.get_user_by_email(data.email)
        if user_exists:
            raise HTTPException(status_code=400, detail=UserErrorMessages.EMAIL_ALREADY_REGISTERED)

        encrypted = self.encrypt_password(data.password)
        user = User(
            name=data.name,
            email=data.email,
            password=encrypted
        )

        created = self.repository.create_user(user)
        if not created:
            raise HTTPException(status_code=400, detail=UserErrorMessages.USER_NOT_CREATED)

        return created
    
    def create_user_admin(self, data: CreateUserAdminSchemas, user: User) -> User:
        if not user.admin:
            raise HTTPException(status_code=400, detail=UserErrorMessages.USER_NOT_AUTHORIZED)
        
        user_exists = self.repository.get_user_by_email(data.email)
        if user_exists:
            raise HTTPException(status_code=400, detail=UserErrorMessages.EMAIL_ALREADY_REGISTERED)
        
        encrypted = self.encrypt_password(data.password)
        user_admin = User(
            name=data.name,
            email=data.email,
            password=encrypted,
            active=data.active
        )

        created = self.repository.create_user(user_admin)
        if not created:
            raise HTTPException(status_code=400, detail=UserErrorMessages.USER_NOT_CREATED)

        return created

    def create_token(self, user_id: int, token_duration: timedelta = None) -> str:
        """
        Cria um token JWT para o usuário com o ID informado.

        Verifica se o usuário existe no banco de dados.
        Se o usuário não existir, lan a um erro HTTP 404 com a mensagem "Usuário não encontrado!".

        Pode ser informado um tempo de expira o customizado, sen o o tempo de expira o padr o ser  configurado.
        O token   gerado com o ID do usu rio e a data de expira o.

        Args:
            user_id (int): O ID do usu rio a ser gerado o token.
            token_duration (int, optional): O tempo de expira o do token em minutos. Defaults to None.

        Returns:
            str: O token JWT gerado.
        """
        user = self.repository.get_user_by_id(user_id)
        if not user:
            return UserErrorMessages.USER_NOT_FOUND

        expire_delta = token_duration or timedelta(minutes=self.access_token_expire)

        expiration_date = datetime.now(tz=timezone.utc) + expire_delta
        payload = {
            'sub': str(user.id),
            'exp': expiration_date
        }

        jwt_code = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
        return jwt_code

    def verify_token(self, token: str) -> User:
        """
        Verifica se o token é válido e retorna o usuário correspondente.

        Tenta decodificar o token e verifica se o usuário existe no banco de dados.
        Se o token for inválido, lança um erro com a mensagem "Não autorizado, token inválido!".
        Se o usuário não existir, lança um erro com a mensagem "usuário não encontrado!".

        Args:
        --------
        token (str): O token JWT a ser verificado.

        Returns:
        --------
        User: O usuário correspondente ao token, caso o token seja v lido e o usuário exista. Caso contr rio, retorna uma mensagem de erro.
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
        except JWTError:
            raise HTTPException(status_code=401, detail=UserErrorMessages.USER_INVALID_TOKEN)
        
        user = self.repository.get_user_by_id(int(payload['sub']))
        if not user:
            raise HTTPException(status_code=401, detail=UserErrorMessages.USER_NOT_FOUND)
        
        return user

    def authenticate_user(self, email: str, password: str):
        """
        Autentica um usuário no sistema.

        Verifica se o e-mail informado existe no banco de dados e se a senha está correta.
        Se o e-mail não existir, retorna False.
        Se a senha estiver incorreta, retorna False.
        Caso contrário, retorna o usuário autenticado.

        Args:
            email (str): O e-mail do usuário a ser autenticado.
            password (str): A senha do usuário a ser autenticado.

        Returns:
            User | bool: O usuário autenticado ou False se a autentica o falhar.
        """
        user = self.repository.get_user_by_email(email)
        if not user:
            return False
        elif not self.bcrypt_context.verify(password, user.password):
            return False
        return user

    def login(self, data: LoginUserSchemas) -> dict:
        """
        Realiza o login do usuário e retorna os tokens de acesso.

        Verifica se o usuário existe e se as credenciais são válidas.
        Se o usuário não existir ou as credenciais forem inválidas, 
        lança um erro HTTP 400 com a mensagem "Usuário não encontrado ou credenciais incorretas!".
        Caso contrário, cria os tokens de acesso e atualiza o e os retorna.

        Args:
            data (LoginUserSchemas): Os dados do usuário a ser logado.

        Returns:
            dict: Um dicionário com os tokens de acesso e atualiza o.

        Raises:
            HTTPException: Se o usuário não existir ou as credenciais forem inválidas.
        """
        user = self.authenticate_user(data.email, data.password)
        if not user:
            return UserErrorMessages.USER_NOT_FOUND_OR_CREDENTIALS_INVALID

        access_token = self.create_token(user.id)
        refresh_token = self.create_token(user.id, token_duration=timedelta(days=7))

        data = {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "Bearer"
                }

        return data
    
    def login_form(self, data) -> dict:
        """
        Realiza o login do usuário e retorna os tokens de acesso.

        Verifica se o usuário existe e se as credenciais s o v lidas.
        Se o usuário n o existir ou as credenciais forem inv lidas, 
        lan a um erro HTTP 400 com a mensagem "usuário n o encontrado ou credenciais incorretas!".
        Caso contr rio, cria os tokens de acesso e atualiza o e os retorna.

        Args:
            data (dict): Os dados do usuário a ser logado.

        Returns:
            dict: Um dicion rio com os tokens de acesso e atualiza o.

        Raises:
            HTTPException: Se o usuário n o existir ou as credenciais forem inv lidas.
        """
        user = self.authenticate_user(data.username, data.password)
        if not user:
            return UserErrorMessages.USER_NOT_FOUND_OR_CREDENTIALS_INVALID

        access_token = self.create_token(user.id)
        refresh_token = self.create_token(user.id, token_duration=timedelta(days=7))

        data = {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "Bearer"
                }
        return data

    def refresh_token(self, refresh_token: str):
        """
        Renova o token de acesso com o token de refresh informado.

        Utiliza o token de refresh informado para renovar o token de acesso.
        Retorna os tokens de acesso e atualiza o.

        Args:
            refresh_token (str): O token de refresh a ser utilizado para renovar o token de acesso.

        Returns:
            dict: Um dicionário com os tokens de acesso e atualiza o.
        """
        user = self.verify_token(refresh_token)
        access_token = self.create_token(user.id)
        refresh_token = self.create_token(user.id, token_duration=timedelta(days=7))

        data = {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "Bearer"
                }
        return data
        