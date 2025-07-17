from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional
from api.models.users import User

class AccountRepository:
    def __init__(self, session: Session):
        """
        Inicializa o repositório de usuários.

        Par metros
        ----------
        session : Session
            A sessão do do banco de dados.
        """
        self.session = session

    def get_all_accounts(self, offset: int = 0, limit: int = 10) -> list[User]:
        """
        Recupera todos os usuários do banco de dados.

        Parâmetros
        ----------
        offset : int, opcional
            O número de usuários a serem pulados antes de iniciar a coleta do conjunto de resultados.
            Padr o   0.
        limit : int, opcional
            O número m ximo de usuários a serem retornados.
            Padr o   10.

        Retornos
        -------
        list[User]
            A lista de usuários se encontrado, caso contr rio uma lista vazia.
        """
        try:
            return self.session.query(User).filter(User.admin == False, User.active == True).offset(offset).limit(limit).all()
        except SQLAlchemyError:
            return []
    
    def get_all_accounts_admin(self, offset: int = 0, limit: int = 10) -> list[User]:
        """
        Recupera todos os usuários administradores do banco de dados.

        Parâmetros
        ----------
        offset : int, opcional
            O número de usuários a serem pulados antes de iniciar a coleta do conjunto de resultados.
            Padr o   0.
        limit : int, opcional
            O número máximo de usuários a serem retornados.
            Padr o   10.

        Retornos
        -------
        list[User]
            A lista de usuários administradores se encontrado, caso contr rio uma lista vazia.
        """
        try:
            return self.session.query(User).filter(User.admin == True, User.active == True).offset(offset).limit(limit).all()
        except SQLAlchemyError:
            return []
    
    def get_account(self, account_id: int) -> Optional[User]:
        """
        Recupera uma conta de usuário pelo ID do banco de dados.

        Parâmetros
        ----------
        account_id : int
            O ID da conta de usuário a ser recuperada.

        Retornos
        -------
        Optional[User]
            O objeto do usuário se encontrado, caso contrário None.
        """

        try:
            return self.session.query(User).filter(User.id == account_id, User.active == True).first()
        except SQLAlchemyError:
            return None