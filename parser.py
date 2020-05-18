import json
import os


def parse_dump(json_file):
    book_dump = json.load(json_file)
    for book in book_dump:

