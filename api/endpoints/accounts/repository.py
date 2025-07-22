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
    
    def update_account(self, account, data):
        """
        Atualiza os dados de uma conta existente no banco de dados.

        Essa função atualiza os campos `name` e `email` de uma conta, se esses forem fornecidos.
        Caso ocorra um erro durante a transação com o banco, a operação é revertida e `None` é retornado.

        Args:
            account (Account): Instância do modelo de conta a ser atualizada.
            data (UpdateAccountsSchema): Dados de entrada contendo os campos opcionais `name` e `email`.

        Returns:
            Account | None: A conta atualizada com os novos dados ou `None` caso ocorra uma falha no banco.
        """
        try:
            if data.name is not None:
                account.name = data.name
            if data.email is not None:
                account.email = data.email

            self.session.add(account)
            self.session.commit()
            self.session.refresh(account)
            return account
        except SQLAlchemyError:
            self.session.rollback()
            return None