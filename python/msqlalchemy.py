'''
Example of using Marshmallow with SqlAlchemy with sqlite
'''
import pathlib
import logging


import sqlalchemy as sa
from sqlalchemy.orm import scoped_session, sessionmaker

from engines_core import get_author_json_obj

from engines_obj import AuthorSchema

from engines_sql import Base
from engines_sql import AuthorDB, BookDB
from engines_sql import AuthorSchemaDB
from engines_sql import BookSchemaDB

SCRIPT_DIR = pathlib.Path(__file__).parent.resolve()
LOG = logging.getLogger(__name__)

engine = sa.create_engine("sqlite:///:memory:")
session = scoped_session(sessionmaker(bind=engine))

Base.metadata.create_all(engine)


def load_data_into_db(author_obj):
    print('-----Loading data into db')
    author = AuthorDB.create(author_obj)
    session.add(author)

    for book_obj in author_obj.books:
        book = BookDB.create(book_obj, author)
        session.add(book)
    session.commit()

    author_schema = AuthorSchema()

    print('-----Dumping objects from db using schema')
    print(author_schema.dump(author).data)

    author_schema = AuthorSchemaDB()
    book_schema = BookSchemaDB()
    print('-----Dumping objects from db using db schema')
    authors = session.query(AuthorDB).all()
    print(author_schema.dump(authors[0]).data)
    books = session.query(BookDB).all()
    for book in books:
        print('\t', book_schema.dump(book).data)

    print('-----convert db objects to schema objs')
    print(authors[0].to_obj())


def main():
    logging.basicConfig(level=logging.DEBUG)
    author_json_obj = get_author_json_obj()

    print("-----Author json obj")
    print(author_json_obj)

    author_schema = AuthorSchema()
    print("-----Author json schema obj")
    # author_schema.context = {'author': author_json_obj}
    author_obj = author_schema.load(author_json_obj).data
    print("-----Recursive structure not handled using print")
    print(author_obj)
    print("-----Recursive structure handled using dump")
    print(author_schema.dump(author_obj).data)

    load_data_into_db(author_obj)

    print('-----Retrieving all authors from the db')
    print(session.query(AuthorDB).all())
    print('-----Retrieving all books from the db')
    print(session.query(BookDB).all())


if __name__ == '__main__':
    logging.basicConfig(level=logging.WARNING)
    main()
