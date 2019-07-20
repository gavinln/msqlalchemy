'''
Sqlalchemy objects and schemas
'''
import pathlib
import logging

import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

# for marshmallow schemas
from marshmallow_sqlalchemy import ModelSchema


SCRIPT_DIR = pathlib.Path(__file__).parent.resolve()
LOG = logging.getLogger(__name__)

Base = declarative_base()


class AuthorDB(Base):
    __tablename__ = "authors"
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String)

    def __repr__(self):
        return "<Author(name={self.name!r})>".format(self=self)


class BookDB(Base):
    __tablename__ = "books"
    id = sa.Column(sa.Integer, primary_key=True)
    title = sa.Column(sa.String)
    author_id = sa.Column(sa.Integer, sa.ForeignKey("authors.id"))
    author = relationship("AuthorDB", backref=backref("books"))


class AuthorSchemaDB(ModelSchema):
    class Meta:
        model = AuthorDB


class BookSchemaDB(ModelSchema):
    class Meta:
        model = BookDB
