from pydantic import BaseModel, UUID4
from typing import Optional, List


class UsuarioCreate(BaseModel):
    nome: str
    email: str
    senha: str

class UsuarioUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[str] = None
    senha: Optional[str] = None

class UsuarioView(BaseModel):
    id: UUID4
    nome: str
    email: str
    role: str

class UsuarioResponseList(BaseModel):
    total: int
    data: List[UsuarioView]

    class Config:
        from_attributes = True

class UsuarioResponse(BaseModel):
    data: List[UsuarioView]

    class Config:
        from_attributes = True