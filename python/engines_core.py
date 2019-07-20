'''
Example of using Marshmallow with SqlAlchemy with sqlite
'''
import pathlib
import logging
import json

SCRIPT_DIR = pathlib.Path(__file__).parent.resolve()
LOG = logging.getLogger(__name__)


def get_author_json_str():
    return """
        {
          "id": 1,
          "name": "Chuck Paluhniuk",
          "books": [
            {
              "id": 100,
              "title": "Fight Club"
            },
            {
              "id": 101,
              "title": "Survivor"
            }
          ]
        }
    """


def get_author_json_obj():
    return json.loads(get_author_json_str())
