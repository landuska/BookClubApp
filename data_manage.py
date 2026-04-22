from models import User, Book, Author, Community, db
from sqlalchemy.exc import IntegrityError
from datetime import date
from typing import Type


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

    def add_author(self, name: str, birth_date: date, death_date=None) -> None:
        existing_author = db.session.query(Author).filter_by(author_name=name).first()
        if existing_author:
            raise ValueError(f"Author with name '{name}' already exists.")
        try:
            new_author = Author(author_name=name, birth_date=birth_date, death_date=death_date)
            db.session.add(new_author)
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise

    def create_community(self, name: str) -> None:
        existing_community = db.session.query(Community).filter_by(community_name=name).first()
        if existing_community:
            raise ValueError(f"Community with name '{name}' already exists.")
        try:
            new_community = Community(community_name=name)
            db.session.add(new_community)
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise

    def get_users(self) -> list[User]:
        return db.session.query(User).all()

    def get_books_by_user(self, user_id: int):
        user = db.session.get(User, user_id)
        if user:
            return user.list_of_reading_books
        return []

    def get_authors(self) -> list[Author]:
        return db.session.query(Author).all()

    def get_communities_by_user(self, user_id: int):
        user = db.session.get(User, user_id)
        if user:
            return user.list_of_communities_of_user
        return []

    def update_book(self, book_id: int, new_title: str) -> None:
        book = db.session.get(Book, book_id)
        if book:
            try:
                book.title = new_title
                db.session.commit()
            except Exception:
                db.session.rollback()
                raise
        else:
            raise ValueError(f"Book with id {book_id} not found")

    def delete(self, entity_id: int, model: Type[db.Model]) -> None:
        entity = db.session.get(model, entity_id)
        if entity:
            try:
                db.session.delete(entity)
                db.session.commit()
            except Exception:
                db.session.rollback()
                raise
        else:
            raise ValueError(f"{model.__name__} with id {entity_id} not found")

