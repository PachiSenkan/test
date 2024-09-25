from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.wallets.service import create_wallet, get_wallets
from app.db import SessionLocal


@asynccontextmanager
async def create_initial_wallet(app: FastAPI):
    print("Creating initial wallet")
    db = SessionLocal()
    if not get_wallets(db):
        wallet = create_wallet({"balance": 1000}, db)
        print(
            f"Created initial wallet with UUID: {wallet.id} and balance: {wallet.balance}"
        )
    else:
        print("Wallets exist: no initial wallet created")
    db.close()
    yield
