from fastapi import HTTPException

from api.endpoints.accounts.repository import AccountRepository
from api.models.users import User
from api.config.emuns import UserErrorMessages


class AccountService:
    def __init__(self, repository: AccountRepository):
        self.repository = repository
    
    def get_all_accounts(self, user: User, offset: int = 0, limit: int = 10):
        if not user.admin:
            raise HTTPException(status_code=403, detail=UserErrorMessages.USER_NOT_AUTHORIZED)
        
        return self.repository.get_all_accounts(offset, limit)
    
    def get_all_accounts_admin(self, user: User, offset: int = 0, limit: int = 10):
        if not user.admin:
            raise HTTPException(status_code=403, detail=UserErrorMessages.USER_NOT_AUTHORIZED)
        
        return self.repository.get_all_accounts_admin(offset, limit)
    
    def get_account(self, user: User, account_id: int):
        if not user.admin and user.id != account_id:
            raise HTTPException(status_code=403, detail=UserErrorMessages.USER_NOT_AUTHORIZED)
        
        account = self.repository.get_account(account_id)
        if not account:
            raise HTTPException(status_code=404, detail=UserErrorMessages.USER_NOT_FOUND)
        return account
        