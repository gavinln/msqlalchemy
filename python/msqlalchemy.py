'''
Example of using Marshmallow with SqlAlchemy with sqlite
'''
import pathlib
import logging

import sqlalchemy as sa
from sqlalchemy.orm import scoped_session, sessionmaker

from engines_obj import Author, Book
from engines_obj import AuthorSchema, BookSchema

from engines_sql import Base
from engines_sql import AuthorDB, BookDB
from engines_sql import AuthorSchemaDB


SCRIPT_DIR = pathlib.Path(__file__).parent.resolve()
LOG = logging.getLogger(__name__)

engine = sa.create_engine("sqlite:///:memory:")
session = scoped_session(sessionmaker(bind=engine))

Base.metadata.create_all(engine)


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
