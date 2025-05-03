from abc import ABC, abstractmethod

from api.models.usuario import Usuario
from api.schemas.usuario import UsuarioCreate

class IContaRepository(ABC):
    @abstractmethod
    async def login(self, email: str, senha: str) -> Usuario:
        """Método para autenticar um usuário com email e senha."""
        pass
    @abstractmethod
    async def refresh_token(self, user_id: int) -> Usuario:
        """Método para atualizar o token de acesso do usuário."""
        pass
    @abstractmethod
    async def get_me(self, user_id: int) -> Usuario:
        """Método para obter os dados do usuário autenticado."""
        pass
    @abstractmethod
    async def register(self, user_data: UsuarioCreate) -> Usuario:
        """Método para registrar um novo usuário."""
        pass