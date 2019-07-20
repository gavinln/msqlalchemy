'''
Marshmallow objects and schemas
'''
import pathlib
import logging

from dataclasses import dataclass

from marshmallow import Schema, fields


SCRIPT_DIR = pathlib.Path(__file__).parent.resolve()
LOG = logging.getLogger(__name__)


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
