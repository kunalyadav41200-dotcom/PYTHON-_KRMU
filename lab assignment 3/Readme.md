Here is a complete `README.md` file for your Python Library Inventory Manager application.

-----

# `README.md`

## 📚 Library Inventory Manager

This is a combined, single-file implementation of a command-line utility for managing a small library's book inventory. It uses **Python's dataclasses** for book objects, provides **JSON persistence** for saving the catalog, and includes basic **logging** for tracking operations.

***Note:** This single-file structure (`library_inventory_manager_combined.py`) is primarily for educational and demonstration purposes. For a production-ready application or the final assignment, the code should be split into logical modules (e.g., `Book`, `LibraryInventory`, and `CLI` components).*

## ✨ Features

  * **Book Management:** Add, search, issue, and return books.
  * **Persistent Storage:** Automatically saves the catalog to a JSON file (`books_catalog.json`).
  * **Data Integrity:** Uses ISBN as a unique identifier to prevent duplicate entries.
  * **Status Tracking:** Books track their own status (`available` or `issued`).
  * **Logging:** Records all major operations, warnings, and errors to a log file (`library.log`).
  * **Command-Line Interface (CLI):** Simple, interactive menu for inventory operations.

## 🚀 Getting Started

### Prerequisites

You need **Python 3.6+** installed on your system.

### Installation and Setup

1.  **Save the Code:** Save the provided Python script as `library_inventory_manager_combined.py`.

2.  **Run the Application:** Open your terminal or command prompt, navigate to the directory where you saved the file, and run:

    ```bash
    python library_inventory_manager_combined.py
    ```

## 📖 Usage

The application will start with an interactive menu:

```
Library Inventory Manager
-------------------------
1) Add Book
2) Issue Book
3) Return Book
4) View All Books
5) Search by Title
6) Search by ISBN
7) Exit
```

1.  **Add Book (1):** Enter the title, author, and ISBN. The book is added with the status **available**.
2.  **Issue Book (2):** Enter the ISBN of an available book to change its status to **issued**.
3.  **Return Book (3):** Enter the ISBN of an issued book to change its status back to **available**.
4.  **View All Books (4):** Prints a list of all books in the catalog with their current status.
5.  **Search by Title (5):** Find books whose title contains the entered query (case-insensitive search).
6.  **Search by ISBN (6):** Find a specific book by its unique ISBN.
7.  **Exit (7):** Saves the current state of the catalog to `books_catalog.json` and closes the application.

## 🗃️ File Structure

Running the application will generate the following files in the same directory:

  * `library_inventory_manager_combined.py`: The main source code file.
  * `books_catalog.json`: **The persistent data file** where the book catalog is stored.
  * `library.log`: **The log file** containing a record of application events.

## 🛠️ Code Overview

The script is structured into the following key components:

### 1\. `Book` Class (via `@dataclass`)

The core data structure representing a book with attributes:

  * `title`
  * `author`
  * `isbn` (unique identifier)
  * `status` (`available` or `issued`)

It includes methods like `issue()`, `return_book()`, and `to_dict()`/`from_dict()` for JSON serialization.

### 2\. `LibraryInventory` Class

The central management component:

  * **Persistence (`save`/`load`):** Handles reading and writing the book list to `books_catalog.json`. Includes robust error handling for file operations.
  * **CRUD Operations:** Implements `add_book`, `search_by_title`, `search_by_isbn`, `issue_book`, and `return_book`.

### 3\. CLI (`menu` function)

The user interface:

  * Presents a text-based menu for interacting with the `LibraryInventory`.
  * Uses a utility function (`input_non_empty`) to ensure user input is valid.

## 🐞 Logging

The application uses Python's built-in `logging` module. All significant actions (add, issue, return, save, load) are recorded in **`library.log`** with timestamps and log levels (`INFO`, `WARNING`, `EXCEPTION`). This is useful for auditing and debugging.
