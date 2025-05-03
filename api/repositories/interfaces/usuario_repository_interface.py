from abc import ABC, abstractmethod

from api.models.usuario import Usuario
from api.schemas.usuario import UsuarioCreate

class IUserRepository(ABC):
    @abstractmethod
    async def get_user_by_email(self, email: str) -> Usuario:
        """Obtém um usuário pelo email"""
        pass

    @abstractmethod
    async def add_user(self, user_data: UsuarioCreate) -> int:
        """Adiciona um novo usuário"""
        pass

    @abstractmethod
    async def get_user_by_id(self, user_id: int) -> Usuario:
        """Obtém um usuário pelo ID"""
        pass
    
    @abstractmethod
    async def list_users(self, skip: int = 0, limit: int = 100) -> list[Usuario]:
        """Lista todos os usuários com paginação"""
        pass
    
    @abstractmethod
    async def update_user(self, user_id: int, user_data: UsuarioCreate) -> Usuario:
        """Atualiza um usuário existente"""
        pass
    
    @abstractmethod
    async def delete_user(self, user_id: int) -> None:
        """Exclui um usuário logicamente"""
        pass
    