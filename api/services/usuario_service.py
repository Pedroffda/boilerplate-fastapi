from api.core.exceptions import ExceptionBadRequest, ExceptionConflict, ExceptionNotFound
from api.models.usuario import Usuario
from api.schemas.usuario import UsuarioCreate, UsuarioRead
from api.repositories.usuario_repository import UsuarioRepository

class UsuarioService:
    def __init__(self, user_repository: UsuarioRepository):
        self.user_repository = user_repository

    def validate_user_data(self, user_data: UsuarioCreate) -> None:
        if not user_data.email or not user_data.senha:
            raise ExceptionBadRequest("Email e senha são obrigatórios.")

    def check_user_exists(self, email: str) -> None:
        existing_user = self.user_repository.get_user_by_email(email)
        if existing_user:
            raise ExceptionConflict("Email já cadastrado.")

    def create_user(self, user_data: UsuarioCreate) -> Usuario:
        self.validate_user_data(user_data)
        self.check_user_exists(user_data.email)
        new_user = self.user_repository.add_user(user_data)
        return new_user
    
    def get_user_by_id(self, user_id: int) -> Usuario:
        user = self.user_repository.get_user_by_id(user_id)
        if not user:
            raise ExceptionNotFound("Usuário não encontrado.")
        return user
    
    def get_user_by_email(self, email: str) -> Usuario:
        user = self.user_repository.get_user_by_email(email)
        if not user:
            raise ExceptionNotFound("Usuário não encontrado.")
        return user
    
    def list_users(self, skip: int = 0, limit: int = 100) -> tuple[list[UsuarioRead], int]:
        users, total = self.user_repository.list_users(skip, limit)
        return users, total
    
    def update_user(self, user_id: int, user_data: UsuarioCreate) -> Usuario:
        self.get_user_by_id(user_id)
        updated_user = self.user_repository.update_user(user_id, user_data)
        return updated_user
    
    def delete_user(self, user_id: int) -> None:
        self.get_user_by_id(user_id)
        self.user_repository.delete_user(user_id)
        return None
