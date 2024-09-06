# E-Z Reads

## Overview

This is a command-line-based CRUD (Create, Read, Update, Delete) application for managing an eBookstore. The application allows users to perform various operations on a SQLite database, including adding new books, updating existing book records, deleting books, and searching for books by various criteria.


## Setup

1. **Clone the repository (or download the code files).**

`git clone https://github.com/JudeKing/e_bookstore.git`

2. **Navigate to the project directory.**

`cd e_bookstore_app.py`

3. **Run the application.**

`python e_bookstore_app.py`


## How to Use

1. **Starting the Application:**

* When you run `e_bookstore_app.py`, you'll be greeted with a menu that offers several options: entering a new book, updating an existing book, deleting a book, searching for a book, or exiting the application.

2. **Menu Options:**

* **Enter Book:** Allows you to add a new book to the database. You will be prompted to enter the book's ID, title, author, and quantity.
* **Update Book:** Modify an existing book's details by providing its ID and the field you'd like to update.
* **Delete Book:** Remove a book from the database by its ID.
* **Search Books:** Search for books in the database by ID, author, or view the book with the highest or lowest quantity.
* **Exit:** Close the application.

![Screenshot of the main navigation](https://i.ibb.co/Ws2BXvk/main-navigation.png)
![Screenshot of option 1: enter book](https://i.ibb.co/BLCtctg/enter-book-option.png)

3. **CRUD Operations:**
* The program checks if the books already exist in the database to avoid duplication.
* After each operation, the user can choose to perform another action or return to the main menu.

