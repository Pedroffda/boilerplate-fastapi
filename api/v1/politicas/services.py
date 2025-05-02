import uuid
from typing import Optional
from sqlalchemy.orm import Session
from api.v1._database.models import AccessPolicy
from api.v1.politicas.schema import AccessPolicyUpdate, AccessPolicyCreate
from api.core.exceptions import ExceptionBadRequest
from api.core.decorators import handle_sqlalchemy_errors

class PoliticasServices:
    
    not_found_message = "Politica não encontrada"
    
    def _not_excluido(self, db: Session):
        return db.query(AccessPolicy).filter(AccessPolicy.flg_excluido == False)

    def get_all(self, db: Session, skip: int = 0, limit: int = 100):
        query = self._not_excluido(db)
        politica = query.offset(skip).limit(limit).all()
        total = query.count()
        return politica, total

    def get_by_id(self, db: Session, id: uuid.UUID):
        politica = self._not_excluido(db).filter(AccessPolicy.id == id).first()
        if not politica:
            raise ExceptionBadRequest(self.not_found_message)
        return politica

    @handle_sqlalchemy_errors
    def add(self, db: Session, obj: AccessPolicyCreate):

        nova_politica = AccessPolicy(**obj.model_dump(exclude_unset=True))
        
        db.add(nova_politica)
        db.commit()
        db.refresh(nova_politica)
        return nova_politica

    @handle_sqlalchemy_errors
    def update(self, db: Session, id: str, data: AccessPolicyUpdate):
        obj_to_update = self.get_by_id(db, id)
        
        updated_data = data.model_dump(exclude_unset=True)
        
        for key, value in updated_data.items():
            setattr(obj_to_update, key, value)

        db.commit()
        db.refresh(obj_to_update)
        return obj_to_update
    
    @handle_sqlalchemy_errors
    def delete(self, db: Session, id: str) -> Optional[str]:
        politica = self.get_by_id(db, id)
        politica.flg_excluido = True
        db.commit()
        db.refresh(politica)

politicas_services = PoliticasServices()