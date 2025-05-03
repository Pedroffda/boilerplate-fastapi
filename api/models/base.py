import pytz
import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column, as_declarative

tz = pytz.timezone('America/Sao_Paulo')
@as_declarative()
class Base():
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    flg_ativo: Mapped[bool] = mapped_column(default=True)
    flg_excluido: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now(tz), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now(tz), onupdate=datetime.now(tz), nullable=False)
    deleted_at: Mapped[Optional[datetime]] = None