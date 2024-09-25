from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.wallets.models import Wallet
from app.wallets.schemas import WalletOperation


def get_wallets(db: Session):
    wallets = db.scalars(select(Wallet)).all()
    return wallets


def create_wallet(wallet_data: dict, db: Session) -> Wallet:
    db_wallet = Wallet(**wallet_data)
    db.add(db_wallet)
    db.commit()
    db.refresh(db_wallet)
    return db_wallet


operation_dict = {"DEPOSIT": 1, "WITHDRAW": -1}


def execute_operation(
    wallet: Wallet, operation: WalletOperation, db: Session
) -> Wallet:
    resulting_balance = (
        wallet.balance + operation_dict[operation.operation] * operation.amount
    )
    if resulting_balance < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Max withdraw amount is {wallet.balance}",
        )
    wallet.balance += operation_dict[operation.operation] * operation.amount
    db.commit()
    db.refresh(wallet)
    return wallet
