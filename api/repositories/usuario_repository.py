from typing import List, Tuple
from sqlalchemy import select, func, update
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from api.core.decorators import handle_sqlalchemy_errors
from api.core.exceptions import ExceptionConflict
from api.models.usuario import Usuario
from api.schemas.usuario import UsuarioCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UsuarioRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def _not_excluido(self):
        """Retorna a query base filtrada por usuários não excluídos"""
        return select(Usuario).where(Usuario.flg_excluido == False)

    def get_user_by_email(self, email: str) -> Usuario | None:
        """Busca um usuário pelo email."""
        stmt = self._not_excluido().where(Usuario.email.ilike(email))
        result = self.db_session.execute(stmt)
        return result.scalars().first()

    @handle_sqlalchemy_errors
    def add_user(self, user_data: UsuarioCreate) -> Usuario:
        """Adiciona um novo usuário ao banco de dados."""
        new_user = Usuario(
            nome=user_data.nome,
            email=user_data.email,
            senha=pwd_context.hash(user_data.senha)
        )
        
        self.db_session.add(new_user)
        self.db_session.commit()
        self.db_session.refresh(new_user)
        return new_user

    def get_user_by_id(self, user_id: int) -> Usuario | None:
        """Busca um usuário pelo ID."""
        stmt = self._not_excluido().where(Usuario.id == user_id)
        result = self.db_session.execute(stmt)
        return result.scalars().first()
    
    def list_users(self, skip: int = 0, limit: int = 100) -> Tuple[List[Usuario], int]:
        """Lista os usuários com paginação."""
        stmt = (
            self._not_excluido()
            .order_by(Usuario.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        users_result = self.db_session.execute(stmt)
        users = users_result.scalars().all()
        
        count_stmt = select(func.count()).select_from(self._not_excluido())
        total_result = self.db_session.execute(count_stmt)
        total = total_result.scalar_one()
        
        return users, total
    
    def update_password(self, user_id: int, new_password: str) -> None:
        """Atualiza apenas a senha do usuário"""
        hashed_password = pwd_context.hash(new_password)
        stmt = (
            update(Usuario)
            .where(Usuario.id == user_id)
            .values(senha=hashed_password)
        )
        self.db_session.execute(stmt)
        self.db_session.commit()
    
    def update_user(self, user_id: int, user_data: UsuarioCreate) -> Usuario:
        """Atualiza os dados de um usuário existente."""
        if "email" in user_data.model_dump(exclude_unset=True):
            existing_user = self.get_user_by_email(user_data.email)
            if existing_user and existing_user.id != user_id:
                raise ExceptionConflict("Email já cadastrado.")
        
        update_data = user_data.model_dump(exclude_unset=True)
        
        if "senha" in update_data:
            update_data["senha"] = pwd_context.hash(update_data["senha"])
        
        stmt = (
            update(Usuario)
            .where(Usuario.id == user_id)
            .values(**update_data)
            .returning(Usuario)
        )
        
        result = self.db_session.execute(stmt)
        updated_user = result.scalars().first()
        
        self.db_session.commit()
        self.db_session.refresh(updated_user)
        return updated_user
    
    def delete_user(self, user_id: int) -> None:
        """Marca um usuário como excluído (exclusão lógica)."""
        stmt = (
            update(Usuario)
            .where(Usuario.id == user_id)
            .values(flg_excluido=True)
        )
        self.db_session.execute(stmt)
        self.db_session.commit()