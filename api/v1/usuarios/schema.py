from pydantic import BaseModel, UUID4
from typing import Optional, List

from api.v1.politicas.schema import AccessPolicyView


class UsuarioCreate(BaseModel):
    nome: str
    email: str
    senha: str
    id_politica: Optional[UUID4] = None
    
    class Config:
        from_attributes = True

class UsuarioUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[str] = None
    senha: Optional[str] = None
    id_politica: Optional[UUID4] = None
    
    class Config:
        from_attributes = True

class UsuarioView(BaseModel):
    id: UUID4
    nome: str
    email: str
    policies: Optional[AccessPolicyView] = None

class UsuarioResponseList(BaseModel):
    total: int
    data: List[UsuarioView]

    class Config:
        from_attributes = True

class UsuarioResponse(BaseModel):
    data: List[UsuarioView]

    class Config:
        from_attributes = True