from fastapi import APIRouter, Depends, status

from api.core.dependencies import T_CurrentUser, T_Session, T_UsuarioDeps
from api.core.response_model import PaginatedResponse, SingleResponse
from api.core.security import check_access, get_current_user

from api.schemas.usuario import UsuarioCreate, UsuarioRead, UsuarioUpdate

router = APIRouter(prefix="/usuarios", tags=["Usuarios"], dependencies=[Depends(get_current_user)])

@router.get("/", response_model=PaginatedResponse[UsuarioRead])
async def get_all(db: T_Session, current_user: T_CurrentUser, deps: T_UsuarioDeps, skip: int = 0, limit: int = 100):
    check_access(db, current_user, action="Usuario:List")
    items, total = deps.service.list_users(skip, limit)
    return {"total": total, "data": items}

@router.get("/{id}", response_model=SingleResponse[UsuarioRead])
async def get_by_id(id: str, db: T_Session, deps: T_UsuarioDeps, current_user: T_CurrentUser):
    check_access(db, current_user, action="Usuario:Get", resource_id=id)
    item = deps.service.get_user_by_id(id)
    return {"data": [item]}

@router.post("/", response_model=SingleResponse[UsuarioRead], status_code=status.HTTP_201_CREATED)
async def create(data: UsuarioCreate, db: T_Session, deps: T_UsuarioDeps, current_user: T_CurrentUser):
    check_access(db, current_user, action="Usuario:Create")
    return deps.service.create_user(data)

@router.patch("/{id}", response_model=SingleResponse[UsuarioRead])
async def update(id: str, data: UsuarioUpdate, db: T_Session, deps: T_UsuarioDeps, current_user: T_CurrentUser):
    check_access(db, current_user, action="Usuario:Update", resource_id=id)
    return deps.service.update_user(id, data)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(id: str, db: T_Session, deps: T_UsuarioDeps, current_user: T_CurrentUser):
    check_access(db, current_user, action="Usuario:Delete", resource_id=id)
    deps.service.delete_user(id)