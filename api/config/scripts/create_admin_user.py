import secrets
import string

from sqlalchemy.orm import Session

from api.database.session import get_session
from api.endpoints.accounts.repository import AccountRepository
from api.endpoints.auth.repository import AuthRepository
from api.endpoints.auth.services import AuthService
from api.models.users import User


def generate_password(size=12):
    characters = string.ascii_letters + string.digits + "!@#$%&*?"
    return ''.join(secrets.choice(characters) for _ in range(size))

def create_super_user():
    session: Session = next(get_session())
    auth_repository = AuthRepository(session)
    auth_service = AuthService(auth_repository)
    account_repository = AccountRepository(session)
    
    existing_admins = account_repository.get_all_accounts_admin()
    if existing_admins:
        print('Já existe pelo menos um usuário admin. Reutilize-o se necessário.', flush=True)
        return

    name = 'Admin'
    email = 'admin@email.com'
    password = generate_password()

    encrypted = auth_service.encrypt_password(password)
    user = User(
        name=name,
        email=email,
        password=encrypted,
        active=True,
        admin=True
    )
    user_created = auth_repository.create_user(user)
    if not user_created:
        print('Erro ao criar usuário administrador', flush=True)
        return

    print(f'Usuário admin criado com sucesso!', flush=True)
    print(f'Email: {email}', flush=True)
    print(f'Senha: {password}', flush=True)

