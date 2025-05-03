from api.repositories.password_reset_repository import PasswordResetRepository
from api.repositories.usuario_repository import UsuarioRepository
from api.core.email_service import EmailService

class PasswordResetService:
    def __init__(
        self,
        password_reset_repo: PasswordResetRepository,
        user_repo: UsuarioRepository,
        email_service: EmailService
    ):
        self.reset_repo = password_reset_repo
        self.user_repo = user_repo
        self.email_service = email_service

    def request_password_reset(self, email: str) -> bool:
        user = self.user_repo.get_user_by_email(email)
        if not user:
            return False  # Não revela se o e-mail existe por segurança
        
        token = self.reset_repo.create_token(user.id)
        return self.email_service.send_password_reset_email(user.email, token.token)

    def reset_password(self, token: str, new_password: str) -> bool:
        token_obj = self.reset_repo.get_valid_token(token)
        if not token_obj:
            return False
        
        self.user_repo.update_password(token_obj.usuario_id, new_password)
        self.reset_repo.delete_token(token)
        return True