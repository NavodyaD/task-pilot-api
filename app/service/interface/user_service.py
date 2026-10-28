from abc import ABC, abstractmethod

class UserService(ABC):

    @abstractmethod
    def create_user(self, db, user_data):
        pass

    @abstractmethod
    def get_all_users(self, db):
        pass
