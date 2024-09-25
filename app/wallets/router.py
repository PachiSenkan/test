import uuid
from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from app.wallets.schemas import WalletBase, WalletCreate, WalletOperation
from app.wallets import service
from app.wallets.models import Wallet
from app.wallets.dependencies import get_db, valid_wallet_uuid


router = APIRouter(prefix="/wallets")


@router.get("/{wallet_uuid}", tags=["Wallet operations"], response_model=WalletBase)
def get_balance_of_wallet(
    wallet: Wallet = Depends(valid_wallet_uuid),
):
    return wallet


@router.get("/", tags=["Utils"], response_model=list[WalletBase])
def get_all_wallets(db: Session = Depends(get_db)):
    wallets = service.get_wallets(db)
    return wallets


@router.post("/", tags=["Utils"], response_model=WalletBase)
def add_wallet_with_balance(new_wallet: WalletCreate, db: Session = Depends(get_db)):
    db_wallet = service.create_wallet(new_wallet.model_dump(), db)
    return db_wallet


@router.post(
    "/{wallet_uuid}/operation", tags=["Wallet operations"], response_model=WalletBase
)
def execute_wallet_operation(
    operation: WalletOperation,
    wallet: Wallet = Depends(valid_wallet_uuid),
    db: Session = Depends(get_db),
):
    existing_wallet = service.execute_operation(wallet, operation, db)
    return existing_wallet
