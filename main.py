import streamlit as st # Import the Streamlit library for building the web interface 
import json  # Import the JSON module to handle data serialization and deserialization
import os  # Import the OS module to interact with the file system

# Define the path to the JSON file that will persist our library data
DATA_FILE = "library.json"  

def load_library():
    """
    Load the library from a JSON file.
    Returns a list of books. If the file does not exist or is invalid,
    returns an empty list.
    """
    # Check if the data file exists in the current directory
    if os.path.exists(DATA_FILE):  
        try:
            with open(DATA_FILE, "r") as f:  # Open the data file in read mode
                library = json.load(f)  # Load the JSON data from the file into a Python list
            return library  # Return the loaded library list
        except json.JSONDecodeError:
            # Display an error message if the JSON file cannot be decoded
            st.error("Error decoding the library file. Starting with an empty library.")
    return []  # Return an empty list if the file doesn't exist or an error occurred

def save_library(library):
    """
    Save the library data to a JSON file.
    This function writes the library list to the DATA_FILE in a human-readable format.
    """
    # Open the data file in write mode (this will create the file if it doesn't exist)
    with open(DATA_FILE, "w") as f:  
        # Dump the library list into the file in JSON format with indentation for readability
        json.dump(library, f, indent=4)  

def add_book(library, title, author, pub_year, genre, read_status):
    """
    Add a new book to the library list.
    
    Args:
        library (list): The current library list.
        title (str): The title of the book.
        author (str): The author of the book.
        pub_year (int): The publication year.
        genre (str): The genre of the book.
        read_status (bool): True if the book has been read, False otherwise.
    """
    # Create a dictionary representing the new book with its details
    book = {
        "title": title,  # Store the book title
        "author": author,  # Store the book author
        "publication_year": pub_year,  # Store the publication year
        "genre": genre,  # Store the book genre
        "read": read_status  # Store the read status as a boolean
    }
    # Append the new book dictionary to the library list
    library.append(book)  
    # Display a success message indicating the book has been added
    st.success(f"Added '{title}' to the library.")  

def remove_book(library, title):
    """
    Remove a book from the library by its title.
    
    Args:
        library (list): The current library list.
        title (str): The title of the book to remove.
    """
    # Record the original number of books in the library
    original_count = len(library)  
    # Update the library list by filtering out books that match the title (case insensitive)
    library[:] = [book for book in library if book["title"].lower() != title.lower()]  
    # Check if the library size decreased (i.e., a book was removed)
    if len(library) < original_count:  
        # Display a success message indicating the book was removed
        st.success(f"Removed '{title}' from the library.")  
    else:
        # Display a warning message if no matching book was found
        st.warning(f"No book found with the title '{title}'.")  

def search_books(library, keyword):
    """
    Search for books by title or author that match the given keyword.
    
    Args:
        library (list): The current library list.
        keyword (str): The search term (title or author).
    
    Returns:
        list: A list of matching books.
    """
    # Convert the search keyword to lowercase for case-insensitive matching
    keyword = keyword.lower()  
    # Create a list of books that match the keyword in either title or author
    results = [
        book for book in library 
        if keyword in book["title"].lower() or keyword in book["author"].lower()
    ]  
    # Return the list of matching books
    return results  

def display_statistics(library):
    """
    Compute statistics for the library.
    
    Returns:
        tuple: Total number of books and the percentage of books read.
    """
    # Count the total number of books in the library
    total_books = len(library)  
    # Check if the library is empty to avoid division by zero
    if total_books == 0:  
        return total_books, 0  
    # Count the number of books that have been read
    read_books = sum(1 for book in library if book["read"])  
    # Calculate the percentage of books that have been read
    percent_read = (read_books / total_books) * 100  
    # Return both the total count and the percentage of books read
    return total_books, percent_read  

# Initialize the library in Streamlit's session state if it hasn't been loaded yet
if "library" not in st.session_state:  
    st.session_state.library = load_library()  # Load library from file

# Set the main title of the Streamlit application
st.title("📚 Personal Library Manager 📚")  

# Define the list of menu options for navigation in the sidebar
menu_options = [
    "Add a Book",         # Option to add a new book
    "Remove a Book",      # Option to remove an existing book
    "Search for a Book",  # Option to search books by title or author
    "Display All Books",  # Option to list all books in the library
    "Display Statistics"  # Option to display library statistics
]  
# Create a radio button widget in the sidebar for menu selection
choice = st.sidebar.radio("Menu", menu_options)  

# If the user selects "Add a Book" from the menu
if choice == "Add a Book":  
    st.header("Add a New Book")  # Display a header for the section
    # Create a form to capture book details
    with st.form(key="add_book_form"):  
        title = st.text_input("Title")  # Input for the book title
        author = st.text_input("Author")  # Input for the book author
        pub_year = st.number_input("Publication Year", min_value=0, step=1)  # Input for publication year
        genre = st.text_input("Genre")  # Input for the book genre
        read_status = st.checkbox("Read")  # Checkbox to mark if the book has been read
        submit = st.form_submit_button("Add Book")  # Button to submit the form
    
    # When the form is submitted
    if submit:  
        # Check if required fields (title and author) are provided
        if title and author:  
            # Call the function to add the book to the library
            add_book(st.session_state.library, title, author, int(pub_year), genre, read_status)  
            # Save the updated library to the JSON file
            save_library(st.session_state.library)  
        else:
            # Display an error message if required fields are missing
            st.error("Title and Author are required fields.")  

# If the user selects "Remove a Book" from the menu
elif choice == "Remove a Book":  
    st.header("Remove a Book")  # Display a header for the section
    # Create an input for the user to enter the title of the book to remove
    title_to_remove = st.text_input("Enter the title of the book to remove")  
    # When the "Remove Book" button is pressed
    if st.button("Remove Book"):  
        # Check if a title was entered
        if title_to_remove:  
            # Call the function to remove the book from the library
            remove_book(st.session_state.library, title_to_remove)  
            # Save the updated library to the JSON file
            save_library(st.session_state.library)  
        else:
            # Display an error message if no title was provided
            st.error("Please enter a book title.")  

# If the user selects "Search for a Book" from the menu
elif choice == "Search for a Book":  
    st.header("Search for a Book")  # Display a header for the section
    # Create an input for the user to enter a search keyword (title or author)
    keyword = st.text_input("Enter a keyword (title or author)")  
    # When the "Search" button is pressed
    if st.button("Search"):  
        # Check if a keyword was provided
        if keyword:  
            # Get the list of matching books by calling the search function
            results = search_books(st.session_state.library, keyword)  
            # Check if any books were found
            if results:  
                st.write("### Search Results:")  # Display a subheader for results
                # Loop through the list of matching books and display their details
                for book in results:  
                    st.write(
                        f"**Title:** {book['title']}, "
                        f"**Author:** {book['author']}, "
                        f"**Year:** {book['publication_year']}, "
                        f"**Genre:** {book['genre']}, "
                        f"**Read:** {'Yes' if book['read'] else 'No'}"
                    )
            else:
                # Inform the user if no matching books are found
                st.info("No matching books found.")  
        else:
            # Display an error message if the search keyword is missing
            st.error("Please enter a keyword.")  

# If the user selects "Display All Books" from the menu
elif choice == "Display All Books":  
    st.header("All Books in the Library")  # Display a header for the section
    # Check if the library is not empty
    if st.session_state.library:  
        # Loop through all books in the library and display their details with an index number
        for idx, book in enumerate(st.session_state.library, start=1):  
            st.write(
                f"**{idx}. Title:** {book['title']} | "
                f"**Author:** {book['author']} | "
                f"**Year:** {book['publication_year']} | "
                f"**Genre:** {book['genre']} | "
                f"**Read:** {'Yes' if book['read'] else 'No'}"
            )
    else:
        # Inform the user if the library is empty
        st.info("The library is empty. Add some books!")  

# If the user selects "Display Statistics" from the menu
elif choice == "Display Statistics":  
    st.header("Library Statistics")  # Display a header for the section
    # Retrieve statistics (total number of books and percentage read) from the library
    total_books, percent_read = display_statistics(st.session_state.library)  
    # Display the total number of books in the library
    st.write(f"**Total Books:** {total_books}")  
    # Display the percentage of books that have been read
    st.write(f"**Percentage Read:** {percent_read:.2f}%")  


# Add a footer with a link to the GitHub repository

st.markdown("------------")

st.markdown("Build ❤️ by [Muhammad Awais](https://github.com/awais995)")