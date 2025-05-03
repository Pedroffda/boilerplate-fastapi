from starlette import status
from fastapi import APIRouter

from api.core.security import T_OAuth2Form
from api.core.dependencies import T_ContaDeps, T_CurrentUser, T_PasswordResetDeps

from api.schemas.usuario import UsuarioCreate

router = APIRouter(
    prefix="/contas",
    tags=["Contas"],
)

@router.post('/registrar', status_code=status.HTTP_201_CREATED)
async def create_user(user: UsuarioCreate, deps: T_ContaDeps):
    return deps.conta_service.register(user)

@router.post("/entrar", status_code=status.HTTP_200_OK)
async def user_login(form_data: T_OAuth2Form, deps: T_ContaDeps):
    return deps.conta_service.login(form_data)

@router.post("/refresh", status_code=status.HTTP_200_OK)
async def refresh_token(current_user: T_CurrentUser, deps: T_ContaDeps):
    return deps.conta_service.refresh_token(current_user)

@router.get("/me", status_code=status.HTTP_200_OK)
async def get_me(current_user: T_CurrentUser, deps: T_ContaDeps):
    print(current_user.id)
    return deps.conta_service.get_me(current_user.id)

@router.post("/password-reset", status_code=status.HTTP_200_OK)
async def request_password_reset(email: str, deps: T_PasswordResetDeps):
    return deps.password_reset_service.request_password_reset(email)

@router.post("/password-reset/confirm", status_code=status.HTTP_200_OK)
async def confirm_password_reset(token: str, new_password: str, deps: T_PasswordResetDeps):
    return deps.password_reset_service.reset_password(token, new_password)