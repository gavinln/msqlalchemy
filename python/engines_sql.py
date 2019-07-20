'''
Sqlalchemy objects and schemas
'''
import pathlib
import logging

from typing import Any

import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

# for marshmallow schemas
from marshmallow_sqlalchemy import ModelSchema

import engines_obj as eobj

SCRIPT_DIR = pathlib.Path(__file__).parent.resolve()
LOG = logging.getLogger(__name__)

Base: Any = declarative_base()


class AuthorDB(Base):
    __tablename__ = "authors"
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column('name_special', sa.String)

    def __repr__(self):
        return f"<Author(id={self.id},name={self.name!r})>"

    @classmethod
    def create(cls, author: eobj.Author) -> 'AuthorDB':
        return cls(name=author.name)

    def to_obj(self) -> eobj.Author:
        books = [book.to_obj() for book in self.books]
        return eobj.Author(id=self.id, name=self.name, books=books)


class BookDB(Base):
    __tablename__ = "books"
    id = sa.Column(sa.Integer, primary_key=True)
    title = sa.Column(sa.String)
    author_id = sa.Column(sa.Integer, sa.ForeignKey("authors.id"))
    author = relationship("AuthorDB", backref=backref("books"))

    def __repr__(self):
        return f"<Book(id={self.id},name={self.title!r})>"

    @classmethod
    def create(cls, book: eobj.Book, author: AuthorDB) -> 'BookDB':
        return cls(title=book.title, author=author)

    def to_obj(self) -> eobj.Book:
        return eobj.Book(id=self.id, title=self.title, author=None)


class AuthorSchemaDB(ModelSchema):
    class Meta:
        model = AuthorDB


class BookSchemaDB(ModelSchema):
    class Meta:
        model = BookDB
