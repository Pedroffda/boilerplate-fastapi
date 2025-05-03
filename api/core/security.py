from typing import Annotated
import jwt
import pytz

from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from passlib.context import CryptContext
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from api.models.usuario import Usuario
from api.models.access_policy import AccessPolicy

from api.core.settings import Settings
from api.core.db_conection import get_db
from api.core.exceptions import ExceptionForbidden

settings = Settings()

tz = pytz.timezone('America/Sao_Paulo')

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/contas/entrar")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
T_OAuth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]    

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(tz) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def authenticate_user(
    db: Session, 
    email: str, senha: str):
    usuario = db.query(Usuario).filter(Usuario.email == email).first()
    if not usuario:
        return False
    if not verify_password(senha, usuario.senha):
        return False
    return usuario

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Credenciais inválidas",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
    
    usuario = db.query(Usuario).filter(Usuario.email == email).first()
    if usuario is None:
        raise credentials_exception
    return usuario

def check_access(
    db: Session,
    current_user: Usuario,
    action: str,
    resource_id: str = "*",
):
    politica = get_user_policy(db, current_user)
    validate_policy(politica)
    validate_action(politica, action)
    validate_resource(politica, resource_id)
    validate_conditions(politica, current_user)

def get_user_policy(db: Session, current_user: Usuario) -> AccessPolicy:
    politica = db.query(AccessPolicy).filter(AccessPolicy.id == current_user.id_politica).first()
    if not politica:
        raise ExceptionForbidden("Usuário não possui política de acesso configurada.")
    return politica

def validate_policy(politica: AccessPolicy):
    if politica.effect != "Allow":
        raise ExceptionForbidden()

def validate_action(politica: AccessPolicy, action: str):
    if "*" not in politica.actions and action not in politica.actions:
        raise ExceptionForbidden("Ação não permitida.")

def validate_resource(politica: AccessPolicy, resource_id: str):
    if "*" not in politica.resources and resource_id not in politica.resources:
        raise ExceptionForbidden("Recurso não permitido.")

def validate_conditions(politica: AccessPolicy, current_user: Usuario):
    if politica.conditions:
        for key, condition in politica.conditions.items():
            if key == "StringEquals":
                for cond_field, expected_value in condition.items():
                    user_value = getattr(current_user, cond_field, None)
                    if user_value != expected_value:
                        raise ExceptionForbidden(f"Condição de acesso não atendida para o campo {cond_field}.")