from typing import Callable, List
from pynamodb.exceptions import DoesNotExist
from src.model.account_model import AccountModel, AccountPynamoModel, get_account_model_from_account_pynamo_model


class AccountRepository:
    def __init__(self, model_get_func: Callable) -> None:
        self.__model: AccountPynamoModel = model_get_func()

    def get_all_accounts(self) -> List[AccountModel]:
        try:
            pynamodb_accounts = list(self.__model.scan())
        except DoesNotExist:
            return []

        accounts = []
        for pynamodb_account in pynamodb_accounts:
            res = get_account_model_from_account_pynamo_model(pynamodb_account)
            accounts.append(res)

        return accounts

    def get_account(self, id: str) -> AccountModel:
        try:
            account = self.__model.get(hash_key=id)
            res = get_account_model_from_account_pynamo_model(account)
            return res
        except DoesNotExist:
            raise ValueError(f"Account with id '{id}' not found")

    def register_account(self, account: AccountModel) -> AccountModel:
        new_account = AccountPynamoModel(
            id=account.id,
            info=account.info,
            account_id=account.account_id
        )
        new_account.save()
        return account

    def update_account(self, account: AccountModel) -> AccountModel:
        try:
            account_item = self.__model.get(hash_key=str(account.id))
            account_item.update(actions=[
                self.__model.info.set(account.info),
                self.__model.account_id.set(str(account.account_id))
            ])
            return get_account_model_from_account_pynamo_model(account_item)
        except DoesNotExist:
            raise ValueError(f"Account with id {account.id} does not exist")

    def delete_account(self, id: str) -> bool:
        try:
            account = self.__model.get(hash_key=id)
            account.delete()
            return True
        except DoesNotExist:
            raise ValueError(f"Account with id {id} does not exist")
