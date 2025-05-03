from fastapi import APIRouter, Depends, status

from api.core.dependencies import T_PoliticaDeps, T_Session
from api.core.response_model import PaginatedResponse, SingleResponse
from api.core.security import check_access, get_current_user

from api.routes.conta import T_CurrentUser
from api.schemas.politica import AccessPolicyCreate, AccessPolicyRead, AccessPolicyUpdate

router = APIRouter(prefix="/politicas", tags=["Politicas"], dependencies=[Depends(get_current_user)])

@router.get("/", response_model=PaginatedResponse[AccessPolicyRead])
async def get_all(db: T_Session,  current_user: T_CurrentUser, deps: T_PoliticaDeps , skip: int = 0, limit: int = 100):
    check_access(db, current_user, action="Politica:List")
    items, total = deps.politicas_service.list_politicas(skip, limit)
    return {"total": total, "data": items}

@router.get("/{id}", response_model=SingleResponse[AccessPolicyRead])
async def get_by_id(id: str, db: T_Session, deps: T_PoliticaDeps, current_user: T_CurrentUser):
    check_access(db, current_user, action="Politica:Get", resource_id=id)
    item = deps.politicas_service.get_politica_by_id(id)
    return {"data": [item]}

@router.post("/", response_model=SingleResponse[AccessPolicyRead], status_code=status.HTTP_201_CREATED)
async def create(data: AccessPolicyCreate,db: T_Session, deps: T_PoliticaDeps, current_user: T_CurrentUser):
    check_access(db, current_user, action="Politica:Create")
    return deps.politicas_service.add_politica(data)

@router.patch("/{id}", response_model=SingleResponse[AccessPolicyRead])
async def update(id: str, data: AccessPolicyUpdate, db: T_Session, deps: T_PoliticaDeps, current_user: T_CurrentUser):
    check_access(db, current_user, action="Politica:Update", resource_id=id)
    return deps.politicas_service.update_politica(id, data)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(id: str, db: T_Session, current_user: T_CurrentUser, deps: T_PoliticaDeps):
    check_access(db, current_user, action="Politica:Delete", resource_id=id)
    return deps.politicas_service.delete_politica(id)