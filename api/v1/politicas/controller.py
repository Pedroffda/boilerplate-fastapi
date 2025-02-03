from typing import Annotated
from sqlalchemy.orm import Session
from api.utils.db_conection import get_db
from api.v1._database.models import Usuario
from api.utils.security import check_access, get_current_user
from fastapi import APIRouter, Depends, status
from api.v1.politicas.services import politicas_services
from api.v1.politicas.schema import AccessPolicyCreate, AccessPolicyResponse, AccessPolicyResponseList, AccessPolicyUpdate, AccessPolicyView


router = APIRouter(prefix="/api/v1/politicas", tags=["Politicas"], dependencies=[Depends(get_current_user)])

T_Session = Annotated[Session, Depends(get_db)]
T_CurrentUser = Annotated[Usuario, Depends(get_current_user)]

@router.get("/", response_model=AccessPolicyResponseList)
async def get_all(db: T_Session,  current_user: T_CurrentUser, skip: int = 0, limit: int = 100):
    check_access(db, current_user, action="Politica:List")
    items, total = politicas_services.get_all(db, skip, limit)
    return {"total": total, "data": items}

@router.get("/{id}", response_model=AccessPolicyResponse)
async def get_by_id(id: str, db: T_Session, current_user: T_CurrentUser):
    check_access(db, current_user, action="Politica:Get", resource_id=id)
    item = politicas_services.get_by_id(db, id)
    return {"data": [item]}

@router.post("/", response_model=AccessPolicyView, status_code=status.HTTP_201_CREATED)
async def create(data: AccessPolicyCreate,db: T_Session, current_user: T_CurrentUser):
    check_access(db, current_user, action="Politica:Create")
    return politicas_services.add(db, data)

@router.patch("/{id}", response_model=AccessPolicyView)
async def update(id: str, data: AccessPolicyUpdate, db: T_Session, current_user: T_CurrentUser):
    check_access(db, current_user, action="Politica:Update", resource_id=id)
    return politicas_services.update(db, id, data)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(id: str, db: T_Session, current_user: T_CurrentUser):
    check_access(db, current_user, action="Politica:Delete", resource_id=id)
    return politicas_services.delete(db, id)