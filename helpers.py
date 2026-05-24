import requests
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="config/.env")
API_KEY = os.getenv('API_KEY')

def get_book_info(user_input: str) -> dict | None:

    params = {
        "q": user_input,
        "key": API_KEY
    }

    url = f"https://www.googleapis.com/books/v1/volumes"

    try:
        response = requests.get(
            url=url,
            params=params
        )

        response.raise_for_status()
        response_json = response.json()

        isbn = ""
        author = ""
        genre = ""

        if "items" in response_json:
            book_info = response_json["items"][0].get("volumeInfo", {})
            isbn_list = book_info.get("industryIdentifiers", [])
            description = book_info.get("description", "")
            title = book_info.get("title", "")
            authors_list = book_info.get("authors", [])
            genre_list = book_info.get("categories", [])
            images = book_info.get("imageLinks", {})
            cover_url = images.get("thumbnail", "")

            if isbn_list:
                isbn = isbn_list[0].get("identifier", "")

            if genre_list:
                genre = genre_list[0]

            if authors_list:
                author = authors_list[0]

            book_data = {"isbn": isbn,
                         "description": description,
                         "title": title,
                         "author": author,
                         "genre": genre,
                         "cover_url": cover_url
                         }

            return book_data

    except requests.exceptions.RequestException:
        return None



