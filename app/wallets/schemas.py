from enum import Enum
import uuid
from pydantic import BaseModel, ConfigDict, Field


class WalletBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    balance: float


class WalletCreate(BaseModel):
    balance: float = Field(
        ...,
        json_schema_extra={
            "example": 1000.5,
            "description": "Balance of the wallet",
        },
    )


class OperationEnum(str, Enum):
    DEPOSIT = "DEPOSIT"
    WITHDRAW = "WITHDRAW"


class WalletOperation(BaseModel):
    operation: OperationEnum = Field(...)
    amount: float = Field(
        ...,
        gt=0,
        json_schema_extra={
            "example": 2.5,
            "description": "Amount to be deposited/withdrawed to/from wallets balance",
        },
    )
