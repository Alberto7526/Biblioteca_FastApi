from sqlalchemy import Column, DateTime, Date, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


Base = declarative_base()


class Author(Base):
    __tablename__ = "authors"
    id = Column(Integer, primary_key=True, index=True)
    date_created = Column(DateTime(timezone=True), server_default=func.now())
    full_name = Column(String, nullable=False, unique=True)

    books = relationship("Book", back_populates="author", cascade="all, delete-orphan")


class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    date_created = Column(DateTime(timezone=True), server_default=func.now())
    title = Column(String, nullable=False)
    author_id = Column(Integer, ForeignKey("authors.id"))
    ISBN = Column(String, nullable=False, unique=True)
    date_published = Column(Date, nullable=True)

    author = relationship("Author", back_populates="books")
