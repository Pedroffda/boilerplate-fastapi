from abc import ABC, abstractmethod

from api.models.usuario import Usuario
from api.schemas.usuario import UsuarioCreate

class IPoliticaRepository(ABC):
    @abstractmethod
    async def list_politicas(self, skip: int = 0, limit: int = 100) -> tuple[list[Usuario], int]:
        """Lista todas as politicas com paginação"""
        pass
    @abstractmethod
    async def get_politica_by_id(self, id: str) -> Usuario:
        """Obtém uma politica pelo ID"""
        pass
    @abstractmethod
    async def add_politica(self, politica_data: UsuarioCreate) -> int:
        """Adiciona uma nova politica"""
        pass
    @abstractmethod
    async def update_politica(self, id: str, politica_data: UsuarioCreate) -> Usuario:
        """Atualiza uma politica existente"""
        pass
    @abstractmethod
    async def delete_politica(self, id: str) -> None:
        """Exclui uma politica logicamente"""
        pass
    @abstractmethod
    async def get_politica_by_nome(self, nome: str) -> Usuario:
        """Obtém uma politica pelo nome"""
        pass