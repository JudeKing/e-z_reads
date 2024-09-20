'''
Building out CRUD (create, read, update, delete) application
for bookstore.
Using SQLite, create the database with a table to store the books.
Prompt user to enter which CRUD option they desire as well as 
whether they wish to search for a book as well.
'''

import sqlite3

# Connect to database.
try:
    # Creates or opens the database file.
    db = sqlite3.connect('./database/ebookstore.db')
    cursor = db.cursor() # Get a cursor object.

    # Create a table for 'book' if it doesn't already exist.
    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS
           book(id INTEGER PRIMARY KEY, title TEXT, author TEXT,
           qty INTEGER)
        '''
        )
    
    # Prepare book ids for insertion in the database.
    book_id1 = 3001
    book_id2 = 3002
    book_id3 = 3003
    book_id4 = 3004
    book_id5 = 3005

    # Prepare book titles for insertion in the database.
    book_title1 = "A Tale of Two Cities"
    book_title2 = "Harry Potter and the Philosopher's Stone"
    book_title3 = "The Lion, the Witch and the Wardrobe"
    book_title4 = "The Lord of the Rings"
    book_title5 = "Alice in Wonderland"

    # Prepare book authors for insertion in the database.
    book_author1 = "Charles Dickens"
    book_author2 = "J.K Rowling"
    book_author3 = "C.S Lewis"
    book_author4 = "J.R.R Tolkien"
    book_author5 = "Lewis Carroll"

    # Prepare quantities of books for insertion in the database.
    book_qty1 = 30
    book_qty2 = 40
    book_qty3 = 25
    book_qty4 = 37
    book_qty5 = 12

    # Store all the book data.
    books_info = [(book_id1, book_title1, book_author1, book_qty1), 
                  (book_id2, book_title2, book_author2, book_qty2),
                  (book_id3, book_title3, book_author3, book_qty3),
                  (book_id4, book_title4, book_author4, book_qty4),
                  (book_id5, book_title5, book_author5, book_qty5)
    ]

    # Check if the data is already in the database.
    book_ids = [book_id1, book_id2, book_id3, book_id4, book_id5]
    book_exists = False
    # Check the database to see if one of the book IDs are
    # already present.
    for book_id in book_ids:
        cursor.execute('''SELECT id FROM book WHERE id=?''', (book_id,))
        book_exists = cursor.fetchone()
        # If the book ID exists then exit out.
        if book_exists:
            book_exists = True # The book exists.
            break

    # If none of the books exist in the database then insert the books.
    if not book_exists:
        # Insert book data into the database.
        cursor.executemany(
            '''
            INSERT INTO book(id, title, author, qty) VALUES(?,?,?,?)
            ''', books_info
        )

    # Commit the change.
    db.commit()

except sqlite3.Error as e:
    # Roll back any change if something went wrong.
    db.rollback()
    raise e
finally: 
    # Close the database connection.
    db.close()


def check_database(field_value=None, values=None,
                   return_title=False, check_if_values_exist=False ):
    '''Checks the database to see if provided data is already in it.'''
    # Convert whatever values get passed through to a list.
    if type(values) is not list and values is not None:
        values = list(values)
    value_exists = False
    # Connect to database.
    try:
        # Creates or opens the database file.
        db = sqlite3.connect('./database/ebookstore.db')
        cursor = db.cursor() # Get a cursor object.

        # Check if the database is empty.
        cursor.execute('''SELECT * FROM book''')

        is_not_empty = cursor.fetchone()

        if not is_not_empty:
            return False
        # If the database is not empty and that's all that was asked.
        elif is_not_empty and check_if_values_exist:
            return True

        if values is not None:
            for value in values:
                cursor.execute(f'''SELECT title FROM book 
                                   WHERE {field_value}=?''',
                                   (value,))
                value_exists = cursor.fetchone()
        
        if value_exists and return_title:
            # If the value exists in the database and the title has been
            # requested.
            return_title = value_exists
            return return_title
        elif value_exists and not return_title:
            # If the value exists in the database and the title has NOT
            # been requested.
            return True
        else:
            return None # There are no results.
        
    except sqlite3.Error as e:
        # Roll back any change if something went wrong.
        db.rollback()
        raise e
    finally:
        db.close()


def continue_option(user_option):
    '''Determine whether the user wishes to continue their operations.'''
    while True: 
        try: 
            user_option = int(user_option)
            # If user enters anything other than 1 or 2.
            if user_option not in [1, 2]:
                print("Please enter only one of the above options!")
                return False # Stop here.
            else:
                return True
                
        except ValueError:
            print("Please enter only a number!")
            return False # Stop here.


def insert_book():
    '''Return a user-selected book.'''
    while True:
        # Get the id, title, author and qty of the book from the user.
        try:
            book_id = int(input(
        '''
Enter the book id: '''
        ))

        except ValueError:
            print("Only enter a number!") 
            continue

        try:
        
            book_title = input(
        '''
Enter the book title: '''
            )

            book_author = input(
        '''
Enter the book author: '''
            )
        
        except ValueError:
            print("Enter a value!")
            continue

        try:
            book_qty = int(input(
            '''
Enter the current stock of the book: '''
            ))

        except ValueError:
            print('Enter only a number!')
            continue

        # Checking if the title or ID are already in the database.
        if check_database('id', [book_id]):
            print("\nThe book id is already present!")
            continue
        elif check_database('title', [book_title]):
            print("\nThe book title is already present!")
            continue

        try:
            # Opens the database file.
            db = sqlite3.connect('./database/ebookstore.db')
            cursor = db.cursor() # Get a cursor object.
            cursor.execute(
                '''INSERT INTO book(id,title,author,qty) 
                   VALUES(?,?,?,?) ''',
                   (book_id, book_title, book_author, book_qty)
            )

            db.commit()

        except sqlite3.Error as e:
            # Roll back any change if something went wrong.
            db.rollback()
            raise e
        finally:
            db.close()

        print('\n================\n')
        print(f'{book_title} has been inserted into the database!')
        print('================\n')

        # Let user decide whether they wish to insert another book.
        while True:
            try: 

                user_option = int(input('''
Do you want to continue entering more books?

1. Yes
2. No

: '''           ))
                # If user enters anything other than 1 or 2.
                if user_option not in [1, 2]:
                    print("Please enter only one of the above options!")
                    
                else:
                    break
                    
            except ValueError:
                print("Please enter only a number!")
                continue
        # If user wants to keep entering books.
        if user_option == 1:
            continue
        else: # Return to main menu.
            break 
       

def update_book():
    '''Gives the option to update a book request by the user.'''
    while True:

        # Prompt user to enter a book's ID.
        book_id = input(
        '''
Enter the book ID to update the book: '''
        )

        # Check if database has values.
        if check_database('id',[book_id]) is None:
            print('Book not found! Please enter a valid book ID. \n')
            continue
        # If the book is not in the database then the user needs to 
        # enter one that is in the database.
        elif check_database('id', [book_id]) is False: 
            print('''
There are no books available! Please add books!'''
            )
            break

        while True: 
            # Check if the user correctly entered one of the fields
            # to update from the given options.
            update_field = input(
                '''
Enter the field you wish to update (title, author, qty): ''')
            
            if update_field.lower() not in ('title', 'author', 'qty'):

                print('Enter only a field value from the database!')
                continue
            else:
                break
            
        new_updated_value = input('''
Enter the desired updated value: '''
                            )
        # Convert the entered value to an integer if the field to be 
        # updated is the 'qty' field.
        if update_field.lower() == 'qty':
            new_updated_value = int(new_updated_value)
        
        try:
            # Opens the database file.
            db = sqlite3.connect('./database/ebookstore.db')
            cursor = db.cursor() # Get a cursor object.
            cursor.execute(
                f'''UPDATE book SET {update_field} = ? WHERE id = ?''',
                (new_updated_value, book_id)
            )

            db.commit()

        except sqlite3.Error as e:
            # Roll back any change if something went wrong.
            db.rollback()
            raise e
        finally:
            db.close()

        # Return the updated info to the user.
        print(f'''
You edited book {book_id} and you changed the {update_field}
to '{new_updated_value}'.
''')
        # Give the user the option to continue editing or
        # return to the main menu.
        while True:
        
            user_option = input('''
Do you wish to continue updating books?
                            
1. Yes
2. No
                            
: '''           )
        
            if not continue_option(user_option):
                continue
            else:
                break

        # If user wants to keep entering books.
        if user_option == 1:
            continue
        else: 
            break


def delete_book():
    '''Deletes book from database.'''
    while True:
        book_id = input('''
Enter a book ID to delete it: ''')
        user_option = False

        # Check if database has values.
        if check_database('id',[book_id]) is None:
            print("\nBook not found!")
            continue
        elif check_database('id', [book_id]) is False:
            print('''
There are no books available! Please add books!'''
            )
            break
        else:
            try:
                # Opens the database file.
                db = sqlite3.connect('./database/ebookstore.db')
                cursor = db.cursor() # Get a cursor object.
                #
                cursor.execute(
                    '''DELETE FROM book WHERE id = ?''',
                    (book_id,)
                )

                db.commit()

                print(f"\nBook with an ID of {book_id} has been deleted!")

            except sqlite3.Error as e:
                # Roll back any change if something went wrong.
                db.rollback()
                raise e
            finally:
                db.close()
            
        while True:
            user_option = input('''
Do you want to continue deleting books?
1. Yes
2. No

: '''               )
    
            if not continue_option(user_option):
                continue
            else:
                break

        # If user wants to keep entering books.
        if user_option == 1:
            continue
        else: 
            break


def search_book():
    '''Search through database for books based on id, author or
       quantity.
    '''
    # Check if database has values.
    if check_database() is False:
        print('''
There are no books available! Please add books!'''
        )
        return

    while True:
        try:
            # Ensure that the user enters only a number
            user_option = int(input('''
Enter one of the below options
                                    
1. Search for book by ID.
2. Search for books by author.
3. Get the book with the highest quantity.
4. Get the book with the lowest quantity.

: '''
                ))
            
        except ValueError:
            print("Enter only a number!")
            continue

        if user_option not in (1, 2, 3, 4):
            print('\nOnly enter one of the above options!')
            continue
        
        # Search book by ID.
        if user_option == 1:
            # Prompt user to enter a book ID.
            book_id = input('''
Enter a book ID: '''         )

            # Check if book ID is in the database.
            if check_database('id', [book_id]):
                # Get the book title.
                book_title = check_database('id', [book_id], True)[0]
                # Return the response back to the user.
                print(f'''
The book by the ID of {book_id} is {book_title}.'''             )
            else: # The book does not exist.
                print(f'''
The ID of {book_id} does not match any book in our records.
'''             )
                continue
        # Get books by author.        
        elif user_option == 2:
            try:
                # Opens the database file.
                db = sqlite3.connect('./database/ebookstore.db')
                cursor = db.cursor() # Get a cursor object.
                # Search the database for all authors.
                cursor.execute('''SELECT author FROM book''')

                all_authors = cursor.fetchall()

                iterator = 1
                author_list = ''
                authors_added = []
                
                for author in all_authors:
                    # If the author is NOT already in the list.
                    if author not in authors_added:
                        authors_added.append(author)
                        author_list += f'{iterator}. {author[0]}\n'
                        iterator += 1

                # Let user pick from the authors.
                while True:
                    try:
                        select_author = int(input(f'''
Below is a list of all the authors:
                                                  
{author_list}
: '''                    ))
                        # If the entered number is not in on the list.
                        if select_author not in range(1, iterator):
                            print(
'''Only enter a number from the above options!'''
                            )
                            continue
                        else:
                            break
                    except ValueError:
                        print("Please only enter numbers!")
                        continue

                # Go through all authors and match the author number the
                # user selected with the current iteration.
                for count, author in enumerate(all_authors):
                    author_index = count + 1
                    if author_index == select_author:
                        selected_author = author[0]

                # Search the database by selected author.
                cursor.execute('''
                                SELECT title FROM book WHERE author=? 
                               ''', (selected_author,)
                              )

                all_books_from_author = cursor.fetchall()
                print(f'''
Here are the books by {selected_author}:
''')
                for book in all_books_from_author:
                    print(book[0], '\n')

                db.commit()

            except sqlite3.Error as e:
                # Roll back any change if something went wrong.
                db.rollback()
                raise e
            finally:
                db.close()
                break

        elif user_option == 3:
            try:
                # Opens the database file.
                db = sqlite3.connect('./database/ebookstore.db')
                cursor = db.cursor() # Get a cursor object.
                # Search the database by provided author.
                cursor.execute('''SELECT * FROM book''')

                all_books = cursor.fetchall()

                book_count_list = []

                # Keep track of the iterations.
                iterations = 1
                for book in all_books:
                    book_count_list.append(book[-1]) 
                    iterations += 1

                highest_book_count = max(book_count_list) 
                # Get the book with the highest count.
                cursor.execute(
                    '''
                    SELECT title FROM book WHERE
                    qty = ?
                    ''', (highest_book_count,)
                    )

                highest_book_stock = cursor.fetchall()

                for book in highest_book_stock:
                    print(f'''
{book[0]} has the highest quantity with a book
count of {highest_book_count}.
'''
                        )
                
                db.commit()

            except sqlite3.Error as e:
                # Roll back any change if something went wrong.
                db.rollback()
                raise e
            finally:
                db.close()
                break

        elif user_option == 4:

            try:
                # Opens the database file.
                db = sqlite3.connect('./database/ebookstore.db')
                cursor = db.cursor() # Get a cursor object.
                # Search the database by provided author.
                cursor.execute('''SELECT * FROM book''')

                all_books = cursor.fetchall()

                book_count_list = []

                # Keep track of the iterations
                iterations = 1
                for book in all_books:
                    book_count_list.append(book[-1]) 
                    iterations += 1

                lowest_book_count = min(book_count_list) 
                # Get the book with the lowest count.
                cursor.execute(
                    '''
                    SELECT title FROM book WHERE
                    qty = ?
                    ''', (lowest_book_count,)
                    )

                lowest_book_stock = cursor.fetchall()

                for book in lowest_book_stock:
                    print(f'''
{book[0]} has the lowest quantity with a book count
of {lowest_book_count}.
'''
                        )
                
                db.commit()

            except sqlite3.Error as e:
                # Roll back any change if something went wrong.
                db.rollback()
                raise e
            finally:
                db.close()
                break
        else:
            print("Book not found! Please enter another one.")

        while True:
            user_option = input('''
Do you want to continue searching books?
1. Yes
2. No

: '''               )
    
            if not continue_option(user_option):
                continue
            else:
                break

        # If user wants to keep entering books.
        if user_option == 1:
            continue
        else: 
            break


while True:
    # User Menu
    user_menu = input(
    '''
Welcome to E-Z Reads, the most comprehensive space for all your
reading pleasures!

To view, edit, delete or search the database, select an option
from below by entering the associated number.

1. Enter book
2. Update book
3. Delete book
4. Search books
5. Exit

:  '''
    )

    try: 
        user_menu = int(user_menu)
        if user_menu == 1:
            insert_book()
            continue
        elif user_menu == 2:
            update_book()
            continue
        elif user_menu == 3:
            delete_book()
            continue
        elif user_menu == 4:
            search_book()
            continue
        elif user_menu == 5:
            print('\nSee you soon!')
            break
        else:
            print('\n Please only enter a value from the above options!')
    
    except ValueError:
        print('\n Please enter only a number!')

