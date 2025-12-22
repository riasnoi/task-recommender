from uuid import uuid4

from sqlalchemy.orm import Session

from app.db_models import User
from app.schemas import TokenResponse, UserPublic


class AuthService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def _get_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email).first()

    def register(self, email: str, password: str) -> TokenResponse:
        user = self._get_by_email(email)
        if not user:
            user = User(id=str(uuid4()), email=email)
            self.db.add(user)
            self.db.commit()
        return TokenResponse(access_token="token-" + user.id)

    def login(self, email: str, password: str) -> TokenResponse:
        user = self._get_by_email(email)
        if not user:
            user = User(id=str(uuid4()), email=email)
            self.db.add(user)
            self.db.commit()
        return TokenResponse(access_token="token-" + user.id)

    def me(self) -> UserPublic:
        user = self.db.query(User).first()
        if not user:
            user = User(id=str(uuid4()), email="student@example.com")
            self.db.add(user)
            self.db.commit()
        return UserPublic(id=user.id, email=user.email)
