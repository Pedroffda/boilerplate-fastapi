from typing import List, Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import JSONB

from api.models.base import Base
from api.models.enum import PolicyEffect

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from api.models.usuario import Usuario

class AccessPolicy(Base):
    __tablename__ = "access_policies"

    nome: Mapped[str] = mapped_column(nullable=False)
    effect: Mapped[PolicyEffect] = mapped_column()
    actions: Mapped[List[str]] = mapped_column(JSONB, nullable=False)
    resources: Mapped[List[str]] = mapped_column(JSONB, nullable=False)
    conditions: Mapped[Optional[str]] = mapped_column(JSONB, nullable=True) 
    
    usuario: Mapped["Usuario"] = relationship("Usuario", back_populates="policies")