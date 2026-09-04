from datetime import datetime

from sqlalchemy import Integer, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column


from app.db.base import Base


class MerchantMapping(Base):
    __tablename__ = 'merchant_mappings'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    match_text: Mapped[str] = mapped_column(
        String,
        unique=True,
        index=True,
        nullable= False,
    )

    merchant: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    category: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default= datetime.now,
    )