from typing import Optional
from pydantic import BaseModel, UUID4

from api.schemas.politica import AccessPolicyRead

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

class UsuarioRead(BaseModel):
    id: UUID4
    nome: str
    email: str
    policies: Optional[AccessPolicyRead] = None
