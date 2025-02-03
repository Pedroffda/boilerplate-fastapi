from enum import Enum
import pytz
import uuid
from datetime import datetime
from typing import List, Optional
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import Mapped, mapped_column, relationship

tz = pytz.timezone('America/Sao_Paulo')

@as_declarative()
class Base:
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    flg_ativo: Mapped[bool] = mapped_column(default=True)
    flg_excluido: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now(tz), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now(tz), onupdate=datetime.now(tz), nullable=False)
    deleted_at: Mapped[Optional[datetime]] = None

class PolicyEffect(str, Enum):
    ALLOW = "Allow"
    DENY = "Deny"

class Usuario(Base):
    __tablename__ = "usuarios"

    id_politica: Mapped[uuid.UUID] = mapped_column(ForeignKey("access_policies.id"), nullable=True)
    nome: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True, index=True)
    senha: Mapped[str]

    policies: Mapped[List["AccessPolicy"]] = relationship("AccessPolicy", back_populates="usuario")

class AccessPolicy(Base):
    __tablename__ = "access_policies"

    nome: Mapped[str] = mapped_column(nullable=False)
    effect: Mapped[PolicyEffect] = mapped_column()
    actions: Mapped[List[str]] = mapped_column(JSONB, nullable=False)
    resources: Mapped[List[str]] = mapped_column(JSONB, nullable=False)
    conditions: Mapped[Optional[str]] = mapped_column(JSONB, nullable=True) 
    
    usuario: Mapped[Usuario] = relationship("Usuario", back_populates="policies")