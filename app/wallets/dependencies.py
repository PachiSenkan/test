import uuid
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.wallets.models import Wallet
from app.config import settings


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def valid_wallet_uuid(
    wallet_uuid: uuid.UUID, session: Session = Depends(get_db)
) -> Wallet:
    wallet = session.get(Wallet, wallet_uuid)
    if not wallet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Wallet with UUID: {wallet_uuid} not found",
        )
    return wallet
