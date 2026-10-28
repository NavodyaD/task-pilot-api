from sqlalchemy.orm import Session
from app.models.user_model import User
from app.repository.user_repository import UserRepository
from app.service.interface.user_service import UserService
from app.auth import hash_password

class UserServiceImpl(UserService):

    def __init__(self):
        self.user_repo = UserRepository()

    def create_user(self, db: Session, user_data):
        user = User(
            name=user_data.name,
            email=user_data.email,
            password_hash=hash_password(user_data.password),
            role=user_data.role.upper(),
        )
        return self.user_repo.save(db, user)

    def get_all_users(self, db: Session):
        return self.user_repo.find_all(db)
