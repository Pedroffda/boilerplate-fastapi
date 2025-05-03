import uuid
from api.models.base import Base
from datetime import datetime, timedelta
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, ForeignKey, DateTime

class PasswordResetToken(Base):
    __tablename__ = "password_reset_tokens"

    token: Mapped[str] = mapped_column(String(255), primary_key=True)
    usuario_id: Mapped[str] = mapped_column(ForeignKey("usuarios.id"), nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    @classmethod
    def create_token(cls, user_id: str, expires_in: int = 3600) -> "PasswordResetToken":
        return cls(
            token=str(uuid.uuid4()), 
            usuario_id=user_id,
            expires_at=datetime.now() + timedelta(seconds=expires_in)
        )