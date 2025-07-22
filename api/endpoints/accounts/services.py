from fastapi import HTTPException

from api.endpoints.accounts.repository import AccountRepository
from api.models.users import User
from api.config.emuns import UserErrorMessages
from api.endpoints.accounts.schemas import UpdateAccountsSchema


class AccountService:
    def __init__(self, repository: AccountRepository):
        self.repository = repository
    
    def get_all_accounts(self, user: User, offset: int = 0, limit: int = 10):
        """
        Retorna uma lista paginada de todas as contas visíveis no sistema, acessível apenas por administradores.

        Verifica se o usuário autenticado possui permissão de administrador. 
        Caso contrário, lança uma exceção de autorização. Se autorizado, delega a 
        busca ao repositório com suporte a paginação.

        Args:
            user (User): Usuário autenticado realizando a operação.
            offset (int, optional): Número de registros a serem ignorados para paginação. Default é 0.
            limit (int, optional): Número máximo de registros a serem retornados. Default é 10.

        Returns:
            List[Account]: Lista paginada de contas encontradas.

        Raises:
            HTTPException: 403 se o usuário não for administrador.
        """
        if not user.admin:
            raise HTTPException(status_code=403, detail=UserErrorMessages.USER_NOT_AUTHORIZED)
        
        return self.repository.get_all_accounts(offset, limit)
    
    def get_all_accounts_admin(self, user: User, offset: int = 0, limit: int = 10):
        """
        Retorna uma lista paginada de todas as contas do sistema, apenas para administradores.

        Verifica se o usuário autenticado possui permissão de administrador. 
        Caso contrário, lança uma exceção de autorização. Se autorizado, delega a 
        busca ao repositório com suporte a paginação.

        Args:
            user (User): Usuário autenticado realizando a operação.
            offset (int, optional): Número de registros a serem pulados para paginação. Default é 0.
            limit (int, optional): Número máximo de registros a serem retornados. Default é 10.

        Returns:
            List[Account]: Lista de contas de usuários cadastradas no sistema.

        Raises:
            HTTPException: 403 se o usuário não for administrador.
        """
        if not user.admin:
            raise HTTPException(status_code=403, detail=UserErrorMessages.USER_NOT_AUTHORIZED)
        
        return self.repository.get_all_accounts_admin(offset, limit)
    
    def get_account(self, user: User, account_id: int):
        """
        Retorna uma conta a partir do ID, garantindo que o usuário tenha permissão para acessá-la.

        Se o usuário não for administrador e tentar acessar uma conta diferente da sua, 
        é lançada uma exceção de autorização. A função busca a conta pelo ID no repositório 
        e lança exceção caso ela não exista.

        Args:
            user (User): Usuário autenticado realizando a operação.
            account_id (int): ID da conta a ser recuperada.

        Returns:
            Account: A conta correspondente ao `account_id` se encontrada e autorizada.

        Raises:
            HTTPException:
                - 403 se o usuário não tiver permissão para acessar a conta.
                - 404 se a conta com o `account_id` não for encontrada.
        """
        if not user.admin and user.id != account_id:
            raise HTTPException(status_code=403, detail=UserErrorMessages.USER_NOT_AUTHORIZED)
        
        account = self.repository.get_account(account_id)
        if not account:
            raise HTTPException(status_code=404, detail=UserErrorMessages.USER_NOT_FOUND)
        return account
    
    def update_account(self, user: User, account_id: int, data:UpdateAccountsSchema):
        """
        Atualiza os dados de uma conta, respeitando as permissões do usuário autenticado.

        Se o usuário não for administrador e tentar atualizar outra conta que não a sua, 
        é lançada uma exceção de autenticação. Em seguida, a função busca a conta no banco e, 
        se encontrada, delega a atualização para o repositório.

        Args:
            user (User): Usuário autenticado realizando a operação.
            account_id (int): ID da conta a ser atualizada.
            data (UpdateAccountsSchema): Dados de atualização, contendo campos opcionais como `name` e `email`.

        Returns:
            Account: A conta atualizada com os novos dados.

        Raises:
            HTTPException: 
                - 4003 se o usuário não tiver permissão para alterar a conta.
                - 404 se a conta com o `account_id` fornecido não for encontrada.
        """
        if not user.admin and user.id != account_id:
            raise HTTPException(status_code=403, detail=UserErrorMessages.USER_NOT_AUTHORIZED)
        
        account = self.repository.get_account(account_id)
        if not account:
            raise HTTPException(status_code=404, detail=UserErrorMessages.USER_NOT_FOUND)
        
        updated_account = self.repository.update_account(account, data)
        return updated_account
        