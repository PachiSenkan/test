from fastapi import FastAPI

from app.wallets.router import router as wallet_router
from app.wallets.on_startup import create_initial_wallet


app = FastAPI(title="Wallet operations API", lifespan=create_initial_wallet)

app.include_router(wallet_router, prefix="/api/v1")
