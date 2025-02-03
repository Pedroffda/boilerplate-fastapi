from typing import Optional
from pydantic import UUID4, BaseModel

class UsuarioRegister(BaseModel):
    nome: str
    email: str
    senha: str
    id_politica: Optional[str] = None

class UsuarioResponse(BaseModel):
    id: UUID4
    nome: str
    email: str

class UsuarioLogin(BaseModel):
    username: str
    password: str
    
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"