#!/usr/bin/env python3
"""
Combined single-file implementation for the Library Inventory Manager
(Contains Book, LibraryInventory classes, JSON persistence, CLI, and logging)

Save this file as `library_inventory_manager_combined.py` and run:
    python library_inventory_manager_combined.py

This file is meant for educational/demo purposes — for the assignment you may
split it into modules under /library_manager/ and /cli/ as requested.
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List, Optional

# ---------------------- Configuration & Logging ----------------------
DATA_FILE = Path("books_catalog.json")
LOG_FILE = Path("library.log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)


# ---------------------- Book Class ----------------------
@dataclass
class Book:
    title: str
    author: str
    isbn: str
    status: str = "available"  # either 'available' or 'issued'

    def __post_init__(self):
        self.title = self.title.strip()
        self.author = self.author.strip()
        self.isbn = self.isbn.strip()
        if self.status not in {"available", "issued"}:
            logger.debug("Invalid status provided for ISBN %s: %s", self.isbn, self.status)
            self.status = "available"

    def __str__(self) -> str:
        return f"{self.title} by {self.author} (ISBN: {self.isbn}) - {self.status}"

    def to_dict(self) -> dict:
        """Return a JSON-serializable representation."""
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "Book":
        return cls(
            title=d.get("title", ""),
            author=d.get("author", ""),
            isbn=d.get("isbn", ""),
            status=d.get("status", "available"),
        )

    def issue(self) -> bool:
        """Issue the book if available. Returns True if successful."""
        if self.status == "available":
            self.status = "issued"
            logger.info("Book issued: %s", self)
            return True
        logger.warning("Attempted to issue an already issued book: %s", self)
        return False

    def return_book(self) -> bool:
        """Return the book if issued. Returns True if successful."""
        if self.status == "issued":
            self.status = "available"
            logger.info("Book returned: %s", self)
            return True
        logger.warning("Attempted to return a book that wasn't issued: %s", self)
        return False

    def is_available(self) -> bool:
        return self.status == "available"


# ---------------------- Library Inventory ----------------------
class LibraryInventory:
    def __init__(self, data_file: Path = DATA_FILE):
        self.data_file = Path(data_file)
        self.books: List[Book] = []
        self.load()

    # ---------- Persistence ----------
    def save(self) -> None:
        """Save the books list to JSON. Robustly handles IO errors."""
        try:
            payload = [b.to_dict() for b in self.books]
            with self.data_file.open("w", encoding="utf-8") as f:
                json.dump(payload, f, indent=2, ensure_ascii=False)
            logger.info("Saved %d books to %s", len(self.books), self.data_file)
        except Exception as e:
            logger.exception("Failed to save books to %s: %s", self.data_file, e)

    def load(self) -> None:
        """Load books from JSON file, handle missing/corrupt files gracefully."""
        if not self.data_file.exists():
            logger.info("Data file %s not found — starting with empty catalog.", self.data_file)
            self.books = []
            return

        try:
            with self.data_file.open("r", encoding="utf-8") as f:
                payload = json.load(f)

            if not isinstance(payload, list):
                raise ValueError("Data file root must be a list")

            self.books = [Book.from_dict(item) for item in payload]
            logger.info("Loaded %d books from %s", len(self.books), self.data_file)
        except Exception as e:
            logger.exception("Failed to load books from %s: %s", self.data_file, e)
            logger.error("Starting with an empty catalog due to load error.")
            self.books = []

    # ---------- CRUD-like operations ----------
    def add_book(self, book: Book) -> bool:
        """Add a book if ISBN not already present. Returns True on success."""
        if self.search_by_isbn(book.isbn) is not None:
            logger.warning("Book with ISBN %s already exists. Skipping add.", book.isbn)
            return False
        self.books.append(book)
        logger.info("Added book: %s", book)
        self.save()
        return True

    def search_by_title(self, title_query: str) -> List[Book]:
        q = title_query.strip().lower()
        return [b for b in self.books if q in b.title.lower()]

    def search_by_isbn(self, isbn: str) -> Optional[Book]:
        isbn = isbn.strip()
        for b in self.books:
            if b.isbn == isbn:
                return b
        return None

    def display_all(self) -> None:
        if not self.books:
            print("No books in the catalog.")
            return
        for idx, book in enumerate(self.books, start=1):
            print(f"{idx}. {book}")

    def issue_book(self, isbn: str) -> bool:
        book = self.search_by_isbn(isbn)
        if not book:
            logger.info("Issue failed — ISBN not found: %s", isbn)
            return False
        success = book.issue()
        if success:
            self.save()
        return success

    def return_book(self, isbn: str) -> bool:
        book = self.search_by_isbn(isbn)
        if not book:
            logger.info("Return failed — ISBN not found: %s", isbn)
            return False
        success = book.return_book()
        if success:
            self.save()
        return success


# ---------------------- Command-Line Interface ----------------------
def input_non_empty(prompt: str) -> str:
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Input cannot be empty. Please try again.")


def menu() -> None:
    inv = LibraryInventory()

    MENU = """
Library Inventory Manager
-------------------------
1) Add Book
2) Issue Book
3) Return Book
4) View All Books
5) Search by Title
6) Search by ISBN
7) Exit
"""

    while True:
        print(MENU)
        choice = input("Enter choice (1-7): ").strip()
        try:
            if not choice:
                print("Please enter a choice.")
                continue
            c = int(choice)
        except ValueError:
            print("Invalid choice — enter a number between 1 and 7.")
            continue

        if c == 1:
            title = input_non_empty("Title: ")
            author = input_non_empty("Author: ")
            isbn = input_non_empty("ISBN: ")
            book = Book(title=title, author=author, isbn=isbn)
            added = inv.add_book(book)
            print("Book added." if added else "Book with that ISBN already exists.")

        elif c == 2:
            isbn = input_non_empty("ISBN to issue: ")
            if inv.issue_book(isbn):
                print("Book issued successfully.")
            else:
                print("Could not issue book — check ISBN or status.")

        elif c == 3:
            isbn = input_non_empty("ISBN to return: ")
            if inv.return_book(isbn):
                print("Book returned successfully.")
            else:
                print("Could not return book — check ISBN or status.")

        elif c == 4:
            inv.display_all()

        elif c == 5:
            q = input_non_empty("Title search query: ")
            results = inv.search_by_title(q)
            if results:
                print(f"Found {len(results)} result(s):")
                for r in results:
                    print(r)
            else:
                print("No books matched your title query.")

        elif c == 6:
            isbn = input_non_empty("ISBN to search: ")
            book = inv.search_by_isbn(isbn)
            if book:
                print(book)
            else:
                print("No book found with that ISBN.")

        elif c == 7:
            print("Goodbye — saving catalog and exiting.")
            inv.save()
            break

        else:
            print("Choice must be between 1 and 7.")


# ---------------------- Main ----------------------
if __name__ == "__main__":
    try:
        menu()
    except KeyboardInterrupt:
        print("\nInterrupted by user. Exiting.")
        logger.info("Program interrupted by user via KeyboardInterrupt.")
    except Exception as e:
        logger.exception("Unexpected error in main: %s", e)
        print("An unexpected error occurred. Check the log file for details.")
