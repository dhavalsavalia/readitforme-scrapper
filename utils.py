import json
import os


def get_or_read_json(book_json_or_file):
    if (type(book_json_or_file) is list):
        return book_json_or_file
    else:
        with open(book_json_or_file) as f:
            return json.load(f)


# TODO need to fix this
def get_book_pretty_filepath(book):
    path = os.path.join(
        'books',
        book['category'],
        get_book_pretty_filename(book)
    )
    if (len(path) >= 260):
        return "\\\\?\\" + path.replace("/", "\\")
    else:
        return path


def get_book_pretty_filename(book, extension=""):
    return f"{book['author']} - {book['title']}" + extension
