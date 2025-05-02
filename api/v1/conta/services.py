from sqlalchemy.orm import Session
from passlib.context import CryptContext

from api.core.decorators import handle_sqlalchemy_errors
from api.core.exceptions import ExceptionBadRequest
from api.core.security import create_access_token
from api.v1._database.models import Usuario
from api.v1.conta.schema import UsuarioLogin
from api.v1.usuarios.schema import UsuarioCreate
from api.v1.usuarios.services import usuario_services

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class ContaServices:

    @handle_sqlalchemy_errors
    def register(self, db: Session, obj: UsuarioCreate) -> Usuario:
        usuario_services.validate_user_data(db, obj)
        
        hashed_password = pwd_context.hash(obj.senha)

        novo_usuario = Usuario(
            nome=obj.nome,
            email=obj.email,
            senha=hashed_password
        )
        
        db.add(novo_usuario)
        db.commit()
        db.refresh(novo_usuario)
        return novo_usuario

    @handle_sqlalchemy_errors
    def login(self, db: Session, obj: UsuarioLogin) -> Usuario:
        usuario = usuario_services.get_by_email(db, obj.username)
        if not usuario:
            raise ExceptionBadRequest("Credenciais inválidas")
        if not pwd_context.verify(obj.password, usuario.senha):
            raise ExceptionBadRequest("Credenciais inválidas")
        access_token = create_access_token(data={"sub": usuario.email})
        return {"access_token": access_token, "token_type": "Bearer" }
    
    def refresh_token(self, current_user: Usuario) -> Usuario:
        access_token = create_access_token(data={"sub": current_user.email})
        return {"access_token": access_token, "token_type": "Bearer" }
    
    @handle_sqlalchemy_errors
    def get_me(self, db: Session, id: str) -> Usuario:
        return usuario_services.get_me(db, id)

account_service = ContaServices()