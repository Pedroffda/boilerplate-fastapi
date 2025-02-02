from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from api.utils.security import get_current_user
from api.v1._database.models import Usuario
from .schema import UsuarioCreate, UsuarioUpdate, UsuarioView, UsuarioResponseList, UsuarioResponse
from .services import usuario_services
from api.utils.db_conection import get_db
from typing import Annotated

router = APIRouter(prefix="/api/v1/usuarios", tags=["Usuarios"], dependencies=[Depends(get_current_user)])

T_Session = Annotated[Session, Depends(get_db)]
T_CurrentUser = Annotated[Usuario, Depends(get_current_user)]

@router.get("/", response_model=UsuarioResponseList)
async def get_all(db: T_Session, skip: int = 0, limit: int = 100):
    items, total = usuario_services.get_all(db, skip, limit)
    return {"total": total, "data": items}

@router.get("/{id}", response_model=UsuarioResponse)
async def get_by_id(id: str, db: T_Session, current_user: T_CurrentUser):
    item = usuario_services.get_by_id(db, id, current_user)
    if not item:
        raise HTTPException(status_code=404, detail="Usuario não encontrado")
    return {"data": [item]}

@router.post("/", response_model=UsuarioView, status_code=status.HTTP_201_CREATED)
async def create(data: UsuarioCreate,db: T_Session):
    return usuario_services.add(db, data)

@router.patch("/{id}", response_model=UsuarioView)
async def update(id: str, data: UsuarioUpdate, db: T_Session, current_user: T_CurrentUser):
    return usuario_services.update(db, id, data, current_user)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(id: str, db: T_Session, current_user: T_CurrentUser):
    usuario_services.delete(db, id, current_user)