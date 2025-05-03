
from api.core.exceptions import ExceptionNotFound
from api.models.access_policy import AccessPolicy
from api.repositories.politica_repository import PoliticaRepository


class PoliticaService:
    def __init__(self, politica_repository: PoliticaRepository):
        self.politica_repository = politica_repository
        
    NOT_FOUND_MESSAGE = "Política não encontrada."
        
    def list_politicas(self, skip: int = 0, limit: int = 100) -> tuple[list[AccessPolicy], int]:
        politicas, total = self.politica_repository.list_politicas(skip, limit)
        return politicas, total
    
    def get_politica_by_id(self, id: str) -> AccessPolicy:
        politica = self.politica_repository.get_politica_by_id(id)
        if not politica:
            raise ExceptionNotFound(self.NOT_FOUND_MESSAGE)
        return politica
        
    def get_politica_by_nome(self, nome: str) -> AccessPolicy:
        politica = self.politica_repository.get_politica_by_nome(nome)
        if not politica:
            raise ExceptionNotFound(self.NOT_FOUND_MESSAGE)
        return politica
    
    def add_politica(self, politica_data: AccessPolicy) -> AccessPolicy:
        new_politica = self.politica_repository.add_politica(politica_data)
        return new_politica
    
    def update_politica(self, politica_id: str, politica_data: AccessPolicy) -> AccessPolicy:
        self.get_politica_by_id(politica_id)
        updated_politica = self.politica_repository.update_politica(politica_id, politica_data)
        return updated_politica
    
    def delete_politica(self, politica_id: str) -> None:
        self.get_politica_by_id(politica_id)
        self.politica_repository.delete_politica(politica_id)
        return None