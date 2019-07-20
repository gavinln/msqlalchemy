'''
Marshmallow objects and schemas
'''
import pathlib
import logging

from typing import List

from dataclasses import dataclass

from marshmallow import Schema, fields
from marshmallow import pre_load, post_load

SCRIPT_DIR = pathlib.Path(__file__).parent.resolve()
LOG = logging.getLogger(__name__)


@dataclass
class Author:
    id: int
    name: str
    books: List


@dataclass
class Book:
    id: int
    title: str
    _author: Author


class BookSchema(Schema):
    id = fields.Int()
    title = fields.Str()

    @post_load
    def make_book(self, data, **kwargs):
        assert 'author' in self.context, 'No author in context'
        data['_author'] = self.context['author']
        return Book(**data)


class AuthorSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    books = fields.Nested(BookSchema, many=True)

    @pre_load
    def set_author_context(self, data, **kwargs):
        self.context['author'] = data

    @post_load
    def make_author(self, data, **kwargs):
        return Author(**data)
