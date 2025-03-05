import re
from pydantic import BaseModel, Field, field_validator, SecretStr
from pydantic_core import PydanticCustomError
from icecream import ic
from .books import ReturnedBook, SellerBook

__all__ = ["IncomingSeller", "ReturnedSeller", "ReturnedAllSellers", "NewSeller", "UpdateSeller"]

class BaseSeller(BaseModel):
    first_name: str
    last_name: str    


class IncomingSeller(BaseSeller):
    email: str
    password: SecretStr

    def get_password(self) -> str:
        return self.password.get_secret_value()
    
    @field_validator("password")
    @staticmethod
    def validate_password(val: str) -> str:
        password = val.get_secret_value()
        if len(val) < 8:
            raise PydanticCustomError(
                "Valdation error", "Password is too short"
                )
        if not re.search("[!?@#$%^&*()]", password):
            raise PydanticCustomError(
                "Valdation error", "Password has no special characters"
        )
        return val

    @field_validator("email")
    @staticmethod
    def validate_email(val: str) -> str:
        if "@" not in val:
            raise PydanticCustomError(
                "Valdation error", "Email is not valid"
                )
        return val

class ReturnedSeller(BaseSeller):
    id: int
    email: str
    # books: list[ReturnedBook] = []
    books: list[SellerBook] = []

class NewSeller(BaseSeller):
    id: int
    email: str
    password: SecretStr

class UpdateSeller(BaseSeller):
    id: int
    email: str
    # password: SecretStr

    # @field_validator("password")
    # @staticmethod
    # def validate_password(val: str) -> str:
    #     password = val.get_secret_value()
    #     if len(val) < 8:
    #         raise PydanticCustomError(
    #             "Valdation error", "Password is too short"
    #             )
    #     if not re.search("[!?@#$%^&*()]", password):
    #         raise PydanticCustomError(
    #             "Valdation error", "Password has no special characters"
    #     )
    #     return val


class ReturnedAllSellers(BaseModel):
    sellers: list[ReturnedSeller]