from typing import Callable
from address_book import AddressBook, Record
from rich_output import build_table, display

def input_error(func: Callable):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return str(e)
        except KeyError as e:
            contact_name = e.args[0]
            return f"Contact {contact_name} does not exist"
        except IndexError:
            return "Please enter the contact name"
        
    return inner


def parse_input(user_input: str):
    parts = user_input.split()
    if not parts:
        return "", []
    cmd = parts[0].strip().lower()
    args = parts[1:]

    return cmd, *args


@input_error
def add_contact(args, book: AddressBook):
    if len(args) < 2:
        raise ValueError("Invalid command format. Please try: add [name] [phone]")
    
    name, phone, *_ = args
    record = book.find(name)
    message = f"Contact {name} updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = f"Contact {name} added."
    if phone:
        record.add_phone(phone)
    return message


@input_error
def get_phone_num(args: list, book: AddressBook):
    if not args:
        raise ValueError("Invalid command format, please try: phone [name]")
    name = args[0]
    record = book.find(name)
    
    if not record:
        raise KeyError(name)
    
    return "; ".join(p.value for p in record.phones)

@input_error
def show_all(book: AddressBook):
    rows = []
    for record in book.data.values():
        phones = "; ".join(p.value for p in record.phones) or "—"
        birthday = record.birthday.value.strftime("%d.%m.%Y") if record.birthday else "—"
        rows.append((record.name.value, phones, birthday))

    return build_table(
        title="Contacts",
        columns=["Name", "Phones", "Birthday"],
        rows=rows,
    )

@input_error
def update_contact(args: str, book: AddressBook):
    if len(args) < 3:
            raise ValueError("Invalid command format. Please try: change [name] [old_phone] [new_phone]")
    name, old_phone, new_phone = args
    name = args[0]
    record = book.find(name)
    message = "Phone number phone updated"
    if record is None:
        raise KeyError(name)
    
    record.edit_phone(old_phone, new_phone)
    
    return message

@input_error
def add_birthday(args: str, book: AddressBook):
    if len(args) < 2:
            raise ValueError("Invalid command format. Please try: add-birthday [name] [dd.mm.yyyy]")
    
    name, birthday_date, *_ = args
    record: Record = book.find(name)
    message = f"Birthday date was already added for {name} contact"
    if record is None:
        raise KeyError(name)
    
    if record.birthday is None:
        record.add_birthday(birthday_date)
        return f"Birthday date was added for {name}"
    
    return message

@input_error
def show_birthday(args: str, book: AddressBook):
    if len(args) < 1:
        raise ValueError("Invalid command format. Please try: show-birthday [name]")
    name = args[0]
    record: Record = book.find(name)
    if not record:
        raise KeyError(name)
    
    if record.birthday is None:
        return f"Birthday for {name} was not set"
    
    return f"Birthday date for {name} is {record.birthday}"
    
@input_error
def birthdays(book: AddressBook):
    upcoming_birthdays = book.get_upcoming_birthdays()
    if not upcoming_birthdays:
        return "No upcoming birthdays in the next 7 days"
    
    rows = [(item["name"], item["congratulation_date"]) for item in upcoming_birthdays]
    return build_table(
        title="Upcoming Birthdays",
        columns=["Name", "Congratulation Date"],
        rows=rows,
    )

def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
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
            print(update_contact(args, book))

        elif command == "phone":
            print(get_phone_num(args, book))

        elif command == "all":
            display(show_all(book))
            
        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            display(birthdays(book))

        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()