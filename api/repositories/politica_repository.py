from sqlalchemy import select, func
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from api.models.access_policy import AccessPolicy
from api.schemas.politica import AccessPolicyRead

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class PoliticaRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session
        
    def _not_excluido(self):
        """Query base filtrada por não excluídos"""
        return select(AccessPolicy).where(AccessPolicy.flg_excluido == False)

    def list_politicas(self, skip: int = 0, limit: int = 100) -> tuple[list[AccessPolicy], int]:
        """Lista políticas com paginação"""
        stmt = (
            self._not_excluido()
            .order_by(AccessPolicy.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        politicas = self.db_session.execute(stmt).scalars().all()
        
        total = self.db_session.execute(
            select(func.count()).select_from(self._not_excluido())
        ).scalar_one()
        
        return politicas, total

    def get_politica_by_id(self, id: str) -> AccessPolicy | None:
        """Obtém política por ID"""
        stmt = self._not_excluido().where(AccessPolicy.id == id)
        return self.db_session.execute(stmt).scalars().first()
    
    def get_politica_by_nome(self, nome: str) -> AccessPolicy | None:
        """Busca política por nome (case insensitive)"""
        stmt = self._not_excluido().where(AccessPolicy.nome.ilike(nome))
        return self.db_session.execute(stmt).scalars().first()
    
    def add_politica(self, politica_data: AccessPolicyRead) -> int:
        """Adiciona nova política"""
        new_politica = AccessPolicy(**politica_data.model_dump(exclude_unset=True))
        
        self.db_session.add(new_politica)
        self.db_session.commit()
        self.db_session.refresh(new_politica)
        return new_politica.id
    
    def update_politica(self, politica_id: str, politica_data: AccessPolicyRead) -> AccessPolicy:
        """Atualiza política existente"""
        politica = self.get_politica_by_id(politica_id)
        if not politica:
            raise ValueError("Política não encontrada")
        
        for key, value in politica_data.model_dump(exclude_unset=True).items():
            setattr(politica, key, value)
        
        self.db_session.commit()
        self.db_session.refresh(politica)
        return politica
    
    def delete_politica(self, politica_id: str) -> None:
        """Exclusão lógica de política"""
        politica = self.get_politica_by_id(politica_id)
        if not politica:
            raise ValueError("Política não encontrada")
            
        politica.flg_excluido = True
        self.db_session.commit()
        self.db_session.refresh(politica)