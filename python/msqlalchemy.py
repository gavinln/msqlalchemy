'''
Example of using Marshmallow with SqlAlchemy with sqlite
'''
import pathlib
import logging

from dataclasses import dataclass

from marshmallow import Schema, fields

import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker, relationship, backref

# for marshmallow schemas
from marshmallow_sqlalchemy import ModelSchema


SCRIPT_DIR = pathlib.Path(__file__).parent.resolve()
LOG = logging.getLogger(__name__)

engine = sa.create_engine("sqlite:///:memory:")
session = scoped_session(sessionmaker(bind=engine))
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


Base.metadata.create_all(engine)


class AuthorSchemaDB(ModelSchema):
    class Meta:
        model = AuthorDB


class BookSchemaDB(ModelSchema):
    class Meta:
        model = BookDB
        # optionally attach a Session
        # to use for deserialization
        sqla_session = session


author_schema = AuthorSchemaDB()


@dataclass
class Author:
    id: int
    name: str


@dataclass
class Book:
    id: int
    title: str
    author_id: int


class AuthorSchema(Schema):
    id = fields.Int()
    name = fields.Str()


class BookSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    author_id = fields.Int()


def dump_load_data_DB():
    author = AuthorDB(name="Chuck Paluhniuk")
    book = BookDB(title="Fight Club", author=author)
    session.add(author)
    session.add(book)
    session.commit()

    author_schema = AuthorSchemaDB()
    dump_data = author_schema.dump(author).data
    LOG.debug('dump data %s', dump_data)
    # {'books': [1], 'id': 1, 'name': 'Chuck Paluhniuk'}

    load_data = author_schema.load(dump_data, session=session).data
    LOG.debug('load data %s', load_data)
    # <Author(name='Chuck Paluhniuk')>

    author_schema = AuthorSchema()
    book_schema = BookSchema()

    LOG.debug('author: %s', author_schema.dump(author).data)
    LOG.debug('book: %s', book_schema.dump(book).data)


def dump_load_data():
    author = Author(name="Chuck Paluhniuk", id=1)
    book = Book(title="Fight Club", author_id=author.id, id=1)
    LOG.debug('author: %s', author)
    LOG.debug('book: %s', book)

    author_schema = AuthorSchema()
    book_schema = BookSchema()

    LOG.debug('author: %s', author_schema.dump(author).data)
    LOG.debug('book: %s', book_schema.dump(book).data)


def main():
    logging.basicConfig(level=logging.DEBUG)
    dump_load_data_DB()
    print('-------------------------')
    dump_load_data()


if __name__ == '__main__':
    main()
