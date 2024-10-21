from collections import UserDict
import re

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, value):
        if not value:
            raise ValueError("Name cannot be empty.")
        super().__init__(value)

class Phone(Field):
    def __init__(self, value):
        if not self.validate(value):
            raise ValueError("Invalid phone number. Must be 10 digits.")
        super().__init__(value)

    def validate(phone):
        return re.fullmatch(r'\d{10}', phone) is not None

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        phone_instance = Phone(phone)
        self.phones.append(phone_instance)

    def remove_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                return
        raise ValueError("Phone not found.")

    def edit_phone(self, old_phone, new_phone):
        self.remove_phone(old_phone)
        self.add_phone(new_phone)

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p.value
        raise ValueError("Phone not found.")

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]
        else:
            raise KeyError("Record not found.")

def input_error(func): 
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Contact not found."
        except ValueError as e:
            return str(e)
        except IndexError:
            return "Enter the required information correctly."
    return inner

@input_error
def add_contact(args, address_book):
    if len(args) != 2:
        raise ValueError("Please provide a name and a phone number.")
    name, phone = args
    record = Record(name)
    record.add_phone(phone)
    address_book.add_record(record)
    return f"Contact {name} added."

@input_error
def change_contact(args, address_book):
    if len(args) != 2:
        raise ValueError("Please provide a name and the new phone number.")
    name, new_phone = args
    record = address_book.find(name)
    if record:
        record.edit_phone(record.phones[0].value, new_phone)   
        return f"Contact {name} updated."
    else:
        raise KeyError("Contact not found.")

@input_error
def show_phone(args, address_book):
    if len(args) != 1:
        raise IndexError("Please provide a name.")
    name = args[0]
    record = address_book.find(name)
    if record:
        return str(record)
    else:
        raise KeyError("Contact not found.")

@input_error
def show_all(address_book):
    if not address_book:
        return "No contacts available."
    result = "Contacts list:\n"
    for name, record in address_book.items():
        result += str(record) + "\n"
    return result

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, args

def main():
    address_book = AddressBook()
    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, address_book))
        elif command == "change":
            print(change_contact(args, address_book))
        elif command == "phone":
            print(show_phone(args, address_book))
        elif command == "all":
            print(show_all(address_book))
        elif command == "delete":
            if len(args) != 1:
                print("Please provide a name.")
            else:
                try:
                    address_book.delete(args[0])
                    print(f"Contact {args[0]} deleted.")
                except KeyError as e:
                    print(str(e))
        else:
            print("Invalid command. Please try again.")

if __name__ == "__main__":
    main()
