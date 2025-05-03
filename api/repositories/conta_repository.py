from sqlalchemy import select
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from api.core.security import T_OAuth2Form, create_access_token
from api.models.usuario import Usuario
from api.repositories.usuario_repository import UsuarioRepository
from api.schemas.usuario import UsuarioRead

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class ContaRepository:
    def __init__(self, db_session: Session):
        self.usuario_repository = UsuarioRepository(db_session)
        self.db_session = db_session
        
    def _not_excluido(self):
        """Query base para usuários não excluídos"""
        return select(Usuario).where(Usuario.flg_excluido == False)

    def login(self, current_user: T_OAuth2Form) -> dict:
        """Gera token JWT para login"""
        access_token = create_access_token(data={"sub": current_user.username})
        return {
            "access_token": access_token, 
            "token_type": "Bearer"
        }
        
    def refresh_token(self, current_user: Usuario) -> dict:
        """Gera novo token JWT"""
        access_token = create_access_token(data={"sub": current_user.email})
        return {
            "access_token": access_token, 
            "token_type": "Bearer"
        }
        
    def register(self, user_data: Usuario) -> UsuarioRead:
        """Registra novo usuário"""
        return self.usuario_repository.add_user(user_data)
        
    def get_me(self, user_id: int) -> UsuarioRead:
        """Obtém dados do usuário logado"""
        return self.usuario_repository.get_user_by_id(user_id)