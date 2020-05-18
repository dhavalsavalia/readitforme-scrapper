import argparse
import json
import os
import time

import requests

import generator


parser = argparse.ArgumentParser(
    description='Scrape readitfor.me and generate pretty output'
)
parser.add_argument(
    'email', help='The email to log into your premium readitfor.me account'
)
parser.add_argument(
    'password',
    help='The password to log into your premium readitfor.me account'
)
parser.add_argument(
    '--create-html',
    action='store_true',
    default=True,
    help='Generate a formatted html document for the book'
)
parser.add_argument(
    '--create-epub',
    action='store_true',
    default=False,
    help='Generate a formatted epub document for the book'
)
parser.add_argument(
    '--create-pdf',
    action='store_true',
    default=False,
    help='Generate a formatted pdf document for the book. Requires wkhtmltopdf'
)
args = parser.parse_args()


def process_book_json(book_json, processed_books=0):
    if (args.create_html):
        generator.generate_book_html(book_json)
    if (args.create_epub):
        generator.generate_book_epub(book_json)
    if (args.create_pdf):
        generator.generate_book_pdf(book_json)
    return processed_books + 1


def get_auth(email, password):
    """Get auth_code."""
    data = {
        "client_id": "Readitfor.me App",
        "password": password,
        "response_type": "code",
        "state": "iphwnaojrezc6s2p",
        "username": email,
        "ver": "2.0.0"
    }

    url = 'https://pro.readitfor.me/authorize.php'
    auth_response = requests.post(url, data=data)
    if auth_response.json():
        print('[.] Authentication begin')
        data = auth_response.json()
        auth_code = data["auth_code"]
        return auth_code
    else:
        return 'Returned None'


def get_token(auth_code):
    """Get access_token and refresh_token."""
    data = {
        "client_id": "Readitfor.me App",
        "code": auth_code,
        "grant_type": "authorization_code",
        "ver": "1.0.0"
    }
    url = 'https://pro.readitfor.me/token.php'
    token_response = requests.post(url, data=data)
    if token_response.json():
        print('[.] Authentication Complete')
        data = token_response.json()
        access_token = data["access_token"]
        refresh_token = data["refresh_token"]
        return (access_token, refresh_token)
    else:
        return 'None'


def get_books(access_token):
    """Get books in json."""
    data = {
        "access_token": access_token,
        "request": "force sync",
        "source": "app"
    }

    url = 'https://pro.readitfor.me/resource.php'
    print('[.] Getting books from readitfor.me')
    books_data = requests.post(url, data=data)
    if books_data.json():
        print('[.] Getting books completed')
        data = books_data.json()
        total_books = len(data)
        return total_books, data
    else:
        return 'None'


def finish(start_time, processed_books):
    elapsed_time = time.time() - start_time
    formatted_time = '{:02d}:{:02d}:{:02d}'.format(
        int(elapsed_time // 3600),
        int(elapsed_time % 3600 // 60),
        int(elapsed_time % 60)
    )
    print(f"[#] Processed {processed_books} books in {formatted_time}")


if __name__ == '__main__':
    processed_books = 0
    start_time = time.time()
    try:
        DUMP_FILE = './dump/dump.json'
        if os.path.isfile(DUMP_FILE) and os.access(DUMP_FILE, os.R_OK):
            print(
                '[!] Dump file already exist. Do you still want to continue?',
            )
            with open(DUMP_FILE) as data_file:
                book_json = json.load(data_file)
                process_book_json(book_json)
        else:
            if not os.path.exists('./dump/'):
                print('[.] Creating dump directory')
                os.mkdir('./dump/')
            auth_code = get_auth(args.email, args.password)
            access_token, refresh_token = get_token(auth_code)
            total_books, data = get_books(access_token)
            if data:
                print(f'[.] {total_books} books captured')
                with open(DUMP_FILE, 'w+') as data_file:
                    json.dump(data, data_file)
                process_book_json(data)
    except KeyboardInterrupt:
        print('[#] Interrupted by user')
