from fastapi import (
    APIRouter,
    Depends,
)
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status
from api.utils.db_conection import get_db
from api.utils.security import get_current_user
from api.v1._database.models import Usuario
from .schema import UsuarioRegister, UsuarioResponse
from .services import account_service
from sqlalchemy.orm import Session
from typing import Annotated

router = APIRouter(
    prefix="/api/v1/contas",
    tags=["Contas"],
)

T_Session = Annotated[Session, Depends(get_db)]
T_OAuth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]
T_CurrentUser = Annotated[Usuario, Depends(get_current_user)]

@router.post('/registrar', status_code=status.HTTP_201_CREATED)
def create_user(user: UsuarioRegister, db: T_Session):
    return account_service.register(db, user)

@router.post("/entrar", status_code=status.HTTP_200_OK)
async def user_login(db: T_Session,form_data: T_OAuth2Form):
    return account_service.login(db, form_data)

@router.post("/refresh", status_code=status.HTTP_200_OK)
async def refresh_token(current_user: Usuario = Depends(get_current_user)):
    return account_service.refresh_token(current_user)

@router.get("/me", status_code=status.HTTP_200_OK, response_model=UsuarioResponse)
async def get_me(db: T_Session, current_user: T_CurrentUser):
    return account_service.get_me(db, current_user.id)