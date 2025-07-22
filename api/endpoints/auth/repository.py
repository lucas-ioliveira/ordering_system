from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional
from api.models.users import User

class AuthRepository:
    def __init__(self, session: Session):
        """
        Inicializa o repositório de usuários.

        Par metros
        ----------
        session : Session
            A sessão do do banco de dados.
        """
        self.session = session

    def get_user_by_id(self, id: int) -> Optional[User]:
        """
        Recupera um usuário pelo seu ID do banco de dados.

        Par metros
        id : int O ID do usuário a ser recuperado.

        Retornos
        Optional[User] O objeto do usuário se encontrado, caso contrário None.
        """
        
        try:
            return self.session.query(User).filter(User.id == id).first()
        except SQLAlchemyError:
            return None

    def get_user_by_email(self, email: str) -> Optional[User]:
        """
        Recupera um usuário pelo seu email do banco de dados.

        Parâmetros
        email : str O email do usuário a ser recuperado.

        Retornos
        Optional[User] O objeto do usuário se encontrado, caso contrário None.
        """
        try:
            return self.session.query(User).filter(User.email == email).first()
        except SQLAlchemyError:
            return None

    def create_user(self, user: User) -> User:
        """
        Cria um novo usuário no banco de dados.

        Args:
            user (User): O usuário a ser criado.

        Returns:
            User: O usuário criado com o ID atualizado.
        """
        try:
            self.session.add(user)
            self.session.commit()
            self.session.refresh(user)
            return user
        except SQLAlchemyError:
            return None
