#Business logic or helper functions related to each module.
from database.models import UserModel
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

DATABASE_URL = "mysql://root:password123@localhost/temporary_user_db"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

class UserService:
    @staticmethod
    def get_user_by_id(user_id):
        session = Session()
        user = session.query(UserModel).filter_by(id=user_id).first()
        session.close()
        return user

    @staticmethod
    def create_user(username, password, email):
        session = Session()
        new_user = UserModel(username=username, password=password, email=email)
        session.add(new_user)
        session.commit()
        session.close()
