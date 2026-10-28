from sqlalchemy.orm import Session
from app.models.user_model import User
from app.repository.user_repository import UserRepository

class UserServiceImpl:

    def __init__(self):
        self.user_repo = UserRepository()

    def create_user(self, db: Session, user_data):
        user = User(
            name=user_data.name,
            email=user_data.email
        )
        return self.user_repo.save(db, user)

    def get_all_users(self, db: Session):
        return self.user_repo.find_all(db)