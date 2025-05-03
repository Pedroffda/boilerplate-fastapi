from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import Depends

from api.core.db_conection import get_db
from api.core.email_service import EmailService
from api.core.security import get_current_user
from api.models.usuario import Usuario
from api.repositories.conta_repository import ContaRepository
from api.repositories.password_reset_repository import PasswordResetRepository
from api.repositories.politica_repository import PoliticaRepository
from api.repositories.usuario_repository import UsuarioRepository
from api.services.conta_service import ContaService
from api.services.password_reset_service import PasswordResetService
from api.services.politica_service import PoliticaService
from api.services.usuario_service import UsuarioService

T_Session = Annotated[Session, Depends(get_db)]
T_CurrentUser = Annotated[Usuario, Depends(get_current_user)]

class UsuarioDependencies:
    def __init__(self, db: T_Session):
        self.repository = UsuarioRepository(db)
        self.service = UsuarioService(self.repository)

def get_usuario_deps(db: T_Session) -> UsuarioDependencies:
    return UsuarioDependencies(db)

T_UsuarioDeps = Annotated[UsuarioDependencies, Depends(get_usuario_deps)]

class ContaDependencies:
    def __init__(self, db: T_Session):
        self.conta_repository = ContaRepository(db)
        self.usuario_repository = UsuarioRepository(db)
        self.usuario_service = UsuarioService(self.usuario_repository)
        self.conta_service = ContaService(self.conta_repository, self.usuario_service)
        
def get_conta_deps(db: T_Session) -> ContaDependencies:
    return ContaDependencies(db)

T_ContaDeps = Annotated[ContaDependencies, Depends(get_conta_deps)]

class PoliticaDependencies:
    def __init__(self, db: T_Session):
        self.politicas_repository = PoliticaRepository(db)
        self.politicas_service = PoliticaService(self.politicas_repository)
        
def get_politica_deps(db: T_Session) -> PoliticaDependencies:
    return PoliticaDependencies(db)

T_PoliticaDeps = Annotated[PoliticaDependencies, Depends(get_politica_deps)]

class PasswordResetDependencies:
    def __init__(self, db: T_Session):
        self.password_reset_repository = PasswordResetRepository(db)
        self.usuario_repository = UsuarioRepository(db)
        self.email_service = EmailService()
        self.password_reset_service = PasswordResetService(self.password_reset_repository, self.usuario_repository, self.email_service)
        
def get_password_reset_deps(db: T_Session) -> PasswordResetDependencies:
    return PasswordResetDependencies(db)

T_PasswordResetDeps = Annotated[PasswordResetDependencies, Depends(get_password_reset_deps)]