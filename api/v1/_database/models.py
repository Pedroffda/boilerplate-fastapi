from enum import Enum
import pytz
import uuid
from datetime import datetime
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import Mapped, mapped_column

tz = pytz.timezone('America/Sao_Paulo')

@as_declarative()
class Base:

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    flg_ativo: Mapped[bool] = True
    flg_excluido: Mapped[bool] = False
    created_at: Mapped[datetime] = mapped_column(default=datetime.now(tz), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now(tz), onupdate=datetime.now(tz), nullable=False)
    deleted_at: Mapped[datetime] = None

class Role(str, Enum):
    user = "user"
    admin = "admin"    

class Usuario(Base):
    __tablename__ = "usuarios"

    nome: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True, index=True)
    senha: Mapped[str]
    role: Mapped[Role] = Role.user
