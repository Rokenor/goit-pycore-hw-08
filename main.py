import pickle

from records import Record
from address_book import AddressBook
from decorators import input_error, book_load_error

@input_error
def add_contact(args, book: AddressBook):
    if len(args) < 2:
        raise ValueError
    
    name, phone, *_ = args
    record = book.find(name)

    if record is None:
        record = Record(name)
        book.add_record(record)
        message = f"Contact {name} added."
    else:
        message = ""

    phone_add_result = record.add_phone(phone)
    return f"{message} {phone_add_result}".strip()

@input_error
def change_contact(args, book: AddressBook):
    if len(args) < 3:
        raise ValueError
    
    name, old_phone, new_phone, *_ = args
    record = book.find(name)

    if record:
        return record.edit_phone(old_phone, new_phone)
    else:
        raise KeyError

@input_error
def show_phone(args, book: AddressBook):
    if len(args) < 1:
        raise ValueError

    name, *_ = args
    record = book.find(name)

    if record:
        return '; '.join(p.value for p in record.phones) if record.phones else "No phone numbers found for this contact."
    else:
        raise KeyError

@input_error
def show_all(book: AddressBook):
    if not book.data:
        return "The address book is empty."
    
    all_contacts = []
    for record in book.data.values():
        all_contacts.append(str(record))
    return "\n".join(all_contacts)

@input_error
def add_birthday(args, book: AddressBook):
    if len(args) < 2:
        raise ValueError
    
    name, birthday_str, *_ = args
    record = book.find(name)

    if record:
        return record.add_birthday(birthday_str)
    else:
        raise KeyError
    
@input_error
def show_birthday(args, book: AddressBook):
    if len(args) < 1:
        raise ValueError
    
    name, *_ = args
    record = book.find(name)

    if record:
        return record.show_birthday()
    else:
        raise KeyError

@input_error
def list_upcoming_birthdays(book: AddressBook):
    if not book.data:
        raise IndexError("The address book is empty.")
        
    upcoming = book.get_upcoming_birthdays()

    if upcoming:
        output = ["Upcoming birthdays:"]
        for bday in upcoming:
            output.append(f"- {bday['name']}: {bday['congratulation_date']}")
        return "\n".join(output)
    else:
        return "No upcoming birthdays in the next 7 days."

@input_error
def delete_contact(args, book: AddressBook):
    if len(args) < 1:
        raise ValueError
  
    name, *_ = args
    return book.delete(name)

def show_help():
    help_info = """
    Commands:
    hello                                 - Just text greetings.
    add [name] [phone]                    - Add a new contact with a phone number.
    change [name] [old_phone] [new_phone] - Change an existing phone number for a contact.
    phone [name]                          - Show phone numbers for a contact.
    all                                   - Show all contacts with their phone numbers and birthdays.
    add-birthday [name] [DD.MM.YYYY]      - Add a birthday for a contact.
    show-birthday [name]                  - Show the birthday for a contact.
    birthdays                             - Show upcoming birthdays within the next 7 days.
    delete [name]                         - Delete a contact from the address book.
    help                                  - Show this help message.
    close / exit                          - Close the program.
    """
    return help_info.strip()

def parse_input(user_input):
    user_input = user_input.strip()
    if not user_input:
        return "", []
    
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

def save_data(book, filename="addressbook.pkl"):
    print('Saving data...')
    with open(filename, "wb") as f:
        pickle.dump(book, f)
    print('Data saved.')

@book_load_error
def load_data(filename="addressbook.pkl"):
    print('Loading data...')
    with open(filename, "rb") as f:
        data = pickle.load(f)
        print('Data loaded successfully.')
        return data
    
def main():
    book = load_data()
    print("Welcome to the assistant bot!")
    print("Print 'help' for list of existing commands")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(show_phone(args, book))
        elif command == "all":
            print(show_all(book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(list_upcoming_birthdays(book))
        elif command == 'delete':
            print(delete_contact(args, book))
        elif command == 'help':
            print(show_help())
        elif not command:
            print('Command is empty. Print "help" for list of existing commands.')
        else:
            print("Invalid command. Print 'help' for list of existing commands.")

    save_data(book)

if __name__ == "__main__":
    main()