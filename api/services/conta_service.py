from passlib.context import CryptContext

from api.core.security import create_access_token
from api.core.exceptions import ExceptionBadRequest
from api.core.decorators import handle_sqlalchemy_errors

from api.models.usuario import Usuario
from api.services.usuario_service import UsuarioService
from api.repositories.conta_repository import ContaRepository

from api.schemas.conta import UsuarioLogin
from api.schemas.usuario import UsuarioCreate


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class ContaService:
    def __init__(self, conta_repository: ContaRepository, usuario_services: UsuarioService):
        self.user_repository = conta_repository
        self.usuario_services = usuario_services

    @handle_sqlalchemy_errors
    def register(self, obj: UsuarioCreate) -> Usuario:
        return self.usuario_services.create_user(obj)

    @handle_sqlalchemy_errors
    def login(self, obj: UsuarioLogin):
        usuario = self.usuario_services.get_user_by_email(obj.username)
        if not usuario:
            raise ExceptionBadRequest("Credenciais inválidas")
        if not pwd_context.verify(obj.password, usuario.senha):
            raise ExceptionBadRequest("Credenciais inválidas")
        access_token = create_access_token(data={"sub": usuario.email})
        return {"access_token": access_token, "token_type": "Bearer" }
    
    def refresh_token(self, current_user: Usuario):
        access_token = create_access_token(data={"sub": current_user.email})
        return {"access_token": access_token, "token_type": "Bearer" }
    
    @handle_sqlalchemy_errors
    def get_me(self, id: str) -> Usuario:
        return self.usuario_services.get_user_by_id(id)
