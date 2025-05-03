import uuid
from typing import List
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.models.base import Base
from api.models.access_policy import AccessPolicy

class Usuario(Base):
    __tablename__ = "usuarios"

    id_politica: Mapped[uuid.UUID] = mapped_column(ForeignKey("access_policies.id"), nullable=True)
    nome: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True, index=True)
    senha: Mapped[str]

    policies: Mapped[List["AccessPolicy"]] = relationship("AccessPolicy", back_populates="usuario")
