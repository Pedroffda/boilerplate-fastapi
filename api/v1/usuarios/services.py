from datetime import datetime
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from api.utils.decorators import handle_sqlalchemy_errors
from api.utils.exceptions import ExceptionBadRequest
from typing import Optional
import uuid

from api.v1._database.models import Usuario
from api.v1.usuarios.schema import UsuarioCreate, UsuarioUpdate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UsuarioServices:
    
    not_found_message = "Usuário não encontrado"
    
    def _not_excluido(self, db: Session):
        return db.query(Usuario).filter(Usuario.flg_excluido == False)

    def validate_user_data(self, db: Session, obj: UsuarioCreate):
        if self.get_by_email(db, obj.email):
            raise ExceptionBadRequest("Email já cadastrado")
        
    def get_me(self, db: Session, id: str) -> Optional[Usuario]:
        return self._not_excluido(db).filter(Usuario.id == id).first()

    def get_by_email(self, db: Session, email: str) -> Optional[Usuario]:
        return self._not_excluido(db).filter(Usuario.email.ilike(email)).first()
    
    def check_exists_email(self, db: Session, email: str) -> bool:
        usuario = self._not_excluido(db).filter(Usuario.email.ilike(email)).first()
        if usuario:
            return True
        return False

    def get_by_id(self, db: Session, id: uuid.UUID, current_user: Usuario) -> Optional[Usuario]:
        usuario = self._not_excluido(db).filter(Usuario.id == id).first()
        if not usuario:
            raise ExceptionBadRequest(self.not_found_message)
        if usuario.id != current_user.id:
            raise ExceptionBadRequest(self.not_found_message)
        return usuario

    def get_all(self, db: Session, skip: int = 0, limit: int = 100):
        query = self._not_excluido(db)
        objs = query.order_by(Usuario.created_at.desc()).offset(skip).limit(limit).all()
        total = query.count()
        return objs, total

    @handle_sqlalchemy_errors
    def add(self, db: Session, obj: UsuarioCreate) -> Usuario:
        self.validate_user_data(db, obj)

        hashed_password = pwd_context.hash(obj.senha)

        novo_usuario = Usuario(
            nome=obj.nome,
            email=obj.email,
            senha=hashed_password,
            role = "user"
        )
        
        db.add(novo_usuario)
        db.commit()
        db.refresh(novo_usuario)
        return novo_usuario

    @handle_sqlalchemy_errors
    def update(self, db: Session, id: str, data: UsuarioUpdate, current_user: Usuario) -> Usuario:
        obj_to_update = self.get_by_id(db, id, current_user)
        
        if obj_to_update.id != current_user.id:
            raise ExceptionBadRequest(self.not_found_message)
        
        updated_data = data.model_dump(exclude_unset=True)
        
        if "senha" in updated_data:
            updated_data["senha"] = pwd_context.hash(updated_data["senha"])
            
        if "email" in updated_data:
            if self.check_exists_email(db, updated_data["email"]):
                raise ExceptionBadRequest("Email já cadastrado")
        
        for key, value in updated_data.items():
            setattr(obj_to_update, key, value)

        db.commit()
        db.refresh(obj_to_update)
        return obj_to_update

    def delete(self, db: Session, id: uuid.UUID, current_user: Usuario) -> Optional[str]:
        usuario = self.get_by_id(db, id, current_user)
        
        if usuario.id != current_user.id:
            raise ExceptionBadRequest(self.not_found_message)
        
        usuario.flg_excluido = True
        usuario.flg_ativo = False
        usuario.deleted_at = datetime.now()
        db.commit()
        db.refresh(usuario)

usuario_services = UsuarioServices()