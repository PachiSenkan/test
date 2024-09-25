import uuid
from sqlalchemy.orm import mapped_column, Mapped

from app.db import Base


class Wallet(Base):
    __tablename__ = "wallets"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    balance: Mapped[float]
