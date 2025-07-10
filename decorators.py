from functools import wraps

def input_error(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            if func.__name__ == 'add_contact':
                return "Input error: Missing name or phone. Usage: add [name] [phone]"
            elif func.__name__ == 'change_contact':
                return "Input error: Missing name, old phone or new phone. Usage: change [name] [old_phone] [new_phone]"
            elif func.__name__ == 'show_phone' or func.__name__ == 'show_birthday':
                return "Input error: Missing name. Usage: [command] [name]"
            elif func.__name__ == 'parse_input':
                return "Input error: Command cannot be empty."
            elif func.__name__ == 'delete_contact':
                return "Input error: Missing name. Usage: delete [name]"
            else:
                return f"Input error: {e}"
        except KeyError:
            return "Error: Contact not found."
        except IndexError as e:
            return f"Error: {e}"
        except Exception as e:
            return f"An unexpected error occurred: {e}"
    return wrapper

def book_load_error(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileNotFoundError:
            print("No saved data file found. Creating a new one.")
            from address_book import AddressBook
            return AddressBook()
        except Exception as e:
            print(f"An unexpected error occurred during data loading: {e}. Starting with a new address book.")
            from address_book import AddressBook
            return AddressBook()
    return wrapper