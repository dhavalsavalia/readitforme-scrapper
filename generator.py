import os

from ebooklib import epub

from utils import (
    get_or_read_json,
    get_book_pretty_filepath,
    get_book_pretty_filename
)


def generate_book_html(book_json_or_file):
    # TODO Make a way to download audio as well
    book_json = get_or_read_json(book_json_or_file)
    for book in book_json:
        if '/' in book["title"]:
            clean_title = book["title"].replace("/", "-")
        else:
            clean_title = book["title"]
        html_file = os.path.join('books', book["category"], clean_title, f'{clean_title}.html')
        if (os.path.exists(html_file)):
            print(f"[.] Html file for {book['title']} already exists, not generating...")
        print(f"[.] Generating .html for {book['title']}")


        book_template_file = open(os.path.join("templates", "book.html"), "r")
        book_template = book_template_file.read()
        book_html = book_template
        for key in book:
            book_html = book_html.replace(f'{{{key}}}', str(book[key]))

        book_path = f'books/{book["category"]}/{clean_title}'
        if not os.path.exists(book_path):
            os.makedirs(book_path)
        with open(html_file, 'w',  encoding='utf-8') as outfile:
            outfile.write(book_html)


def generate_book_epub(book_json_or_file):
    book_json = get_or_read_json(book_json_or_file)
    for book in book_json:
        filepath = get_book_pretty_filepath(book)
        filename = get_book_pretty_filename(book, ".epub")
        epub_file = os.path.join(filepath, filename)
        if (os.path.exists(epub_file)):
            print(f"[.] Epub file for {book['title']} already exists, not generating...")
        print(f"[.] Generating .epub for {book['title']}")
        book = epub.EpubBook()
        book.set_identifier(book_json['book_id'])
        book.set_title(book_json['title'])
        book.set_language('en')
        book.add_author(book_json['author'])

        # TODO Impliment the rest
        pass


def generate_book_pdf(book_json_or_file):
    # TODO Impliment this
    pass
