from pydantic import UUID4, BaseModel

class UsuarioRegister(BaseModel):
    nome: str
    email: str
    senha: str

class UsuarioResponse(BaseModel):
    id: UUID4
    nome: str
    email: str
    role: str

class UsuarioLogin(BaseModel):
    username: str
    password: str
    
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"