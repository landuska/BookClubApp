from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, Float, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, validates

db = SQLAlchemy()