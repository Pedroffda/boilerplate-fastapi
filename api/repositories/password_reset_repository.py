from datetime import datetime
from sqlalchemy.orm import Session
from api.models.password_reset import PasswordResetToken

class PasswordResetRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create_token(self, user_id: str) -> PasswordResetToken:
        token = PasswordResetToken.create_token(user_id)
        self.db_session.add(token)
        self.db_session.commit()
        self.db_session.refresh(token)
        return token

    def get_valid_token(self, token: str) -> PasswordResetToken | None:
        return self.db_session.query(PasswordResetToken).filter(
            PasswordResetToken.token == token,
            PasswordResetToken.expires_at > datetime.now()
        ).first()

    def delete_token(self, token: str) -> None:
        self.db_session.query(PasswordResetToken).filter(
            PasswordResetToken.token == token
        ).delete()
        self.db_session.commit()