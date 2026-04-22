from models import User, Book, UserBooks, Author, Community, UserCommunities, db
from sqlalchemy.exc import IntegrityError


class DataManager():
    def add_user(self, name: str, password: str) -> None:
        existing_user = db.session.query(User).filter_by(name=name).first()
        if existing_user:
            raise ValueError(f"User with name '{name}' already exists.")
        try:
            new_user = User(name=name, password=password)
            db.session.add(new_user)
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise


    def add_book(self, book: Book) -> None:
        try:
            db.session.add(book)
            db.session.commit()
        except IntegrityError:
            raise ValueError(f"Book {book} was already added to the user's library.")
        except Exception:
            db.session.rollback()
            raise

    def create_community(self, name: str) -> None:
        existing_community = db.session.query(Community).filter_by(community_name=name).first()
        if existing_community:
            raise ValueError(f"Community with name '{name}' already exists.")
        try:
            new_community = Community(name=name)
            db.session.add(new_community)
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise

