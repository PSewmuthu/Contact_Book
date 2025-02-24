"""
20APP4488
P.S.A.Singhe

https://github.com/PSewmuthu/Contact_Book.git
"""

import sqlite3


class ContactBook:
    def __init__(self):
        self.conn = sqlite3.connect('contacts.db')

        self.db_init()

    def db_init(self):
        cursor = self.conn.cursor()

        # Person table for store personal details
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS Person(
                           id INTEGER,
                           name VARCHAR(100) NOT NULL UNIQUE,
                           email VARCHAR(100),
                           address VARCHAR(500),
                           PRIMARY KEY('id' AUTOINCREMENT)
                       );
                       ''')

        # Phone table for store phone numbers
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS Phone(
                           person_id INT,
                           number VARCHAR(13),
                           PRIMARY KEY(person_id, number),
                           FOREIGN KEY (person_id) REFERENCES Person(id)
                       );
                       ''')

        self.conn.commit()

    def show_options(self):
        menu = ["Create Contact", "View Contacts",
                "Search", "Update", "Delete", "Exit"]

        print("\n", "Contact Book".center(20, "#"))
        print("\nWhat do you want to do?")

        for i, itm in enumerate(menu, 1):
            print(f"{i}. {itm}")

        choice = 0
        while True:
            try:
                choice = int(input("Enter you choice (1 - 6): "))

                if choice not in range(1, len(menu) + 1):
                    print("\nInvalid value entered! Try again...")
                else:
                    break
            except:
                print("\nInvalid value entered! Try again...")

        return menu[choice - 1]

    def new_contact(self, name, phone_numbers=[], email='', address=''):
        cursor = self.conn.cursor()

        # Add details to Person table
        cursor.execute(f'''
                       INSERT INTO Person(name, email, address)
                       VALUES ('{name}', '{email}', '{address}');
                       ''')
        self.conn.commit()

        # Get the id of the record
        cursor.execute(f'''
                       SELECT id FROM Person
                       WHERE name = '{name}';
                       ''')
        self.conn.commit()
        id = cursor.fetchone()

        # Add phone numbers to the Phone table
        for phone in phone_numbers:
            cursor.execute(f'''
                           INSERT INTO Phone(person_id, number)
                           VALUES ('{id[0]}', '{phone}');
                           ''')

        self.conn.commit()

    def view_all(self):
        contacts = {}
        cursor = self.conn.cursor()

        # Get all values from Person table
        cursor.execute('''
                       SELECT * FROM Person;
                       ''')
        persons = cursor.fetchall()
        self.conn.commit()

        for person in persons:
            # Get all numbers from Phone table
            cursor.execute(f'''
                           SELECT * FROM Phone
                           WHERE person_id = '{person[0]}';
                           ''')
            phones = [phone[1] for phone in cursor.fetchall()]

            contacts[person[0]] = [person[1], phones, person[2], person[3]]

        return contacts

    def search(self, search_by, value):
        cursor = self.conn.cursor()
        contact = {}

        if search_by == 'name':
            # Select the record which match with the given name
            cursor.execute(f'''
                           SELECT * FROM Person
                           WHERE name = '{value}';
                           ''')
            person = cursor.fetchone()

            self.conn.commit()

            if person is None:
                return "Given Name is not in the contact list."

            # Get all phone numbers belongs to the given name
            cursor.execute(f'''
                           SELECT * FROM Phone
                           WHERE person_id = '{person[0]}';
                           ''')
            phones = [phone[1] for phone in cursor.fetchall()]

            contact[person[0]] = [person[1],
                                  phones, person[2], person[3]]
        elif search_by == 'phone':
            # Select the record which match with the given phone number
            cursor.execute(f'''
                           SELECT * FROM Phone
                           WHERE number = '{value}';
                           ''')
            phone = cursor.fetchone()
            self.conn.commit()

            if phone is None:
                return "Given Phone number is not in the contact list."

            cursor.execute(f'''
                           SELECT * FROM Person
                           WHERE id = '{phone[0]}';
                           ''')
            person = cursor.fetchone()

            contact[person[0]] = [person[1],
                                  [phone[1]], person[2], person[3]]

        return contact

    def update(self, id,  name, phone_numbers=[], email='', address=''):
        cursor = self.conn.cursor()

        # Update Person table
        cursor.execute(f'''
                       UPDATE Person
                       SET name = '{name}', email = '{email}', address = '{address}'
                       WHERE id = '{id}';
                       ''')
        self.conn.commit()

        # Delete existing phone numbers
        cursor.execute(f'''
                       DELETE FROM Phone
                       WHERE person_id = '{id}';
                       ''')

        self.conn.commit()

        # Add updated phone numbers
        for phone in phone_numbers:
            cursor.execute(f'''
                           INSERT INTO Phone(person_id, number)
                           VALUES ('{id}', '{phone}');
                           ''')

        self.conn.commit()

    def delete(self, id):
        cursor = self.conn.cursor()

        # Delete data in Person table
        cursor.execute(f'''
                       DELETE FROM Person
                       WHERE id = {id};
                       ''')
        self.conn.commit()

        # Delete data in Phone table
        cursor.execute(f'''
                       DELETE FROM Phone
                       WHERE person_id = {id};
                       ''')
        self.conn.commit()

    def __del__(self):
        self.conn.close()


if __name__ == "__main__":
    contact_book = ContactBook()

    while True:
        option = contact_book.show_options()

        match option:
            case 'Create Contact':
                print("\nEnter new contact details below")

                name = input("Name: ")
                phone = [num.strip() for num in input(
                    "Phone Numbers (Separate with commas): ")]
                email = input("Email: ")
                address = input("Address: ")

                contact_book.new_contact(name, phone, email, address)
                print("\nNew Contact Created Successfully!")

            case 'View Contacts':
                contacts = contact_book.view_all()

                if contacts == {}:
                    print("\nNo Contacts to Display")
                else:
                    for contact in contacts.values():
                        print(
                            "############################################################")
                        print(f"Name: {contact[0]}")
                        print("Phone Numbers:")
                        for phone in contact[1]:
                            print(f"\t\t{phone}")
                        print(f"Email: {contact[2]}")
                        print(f"Address: {contact[3]}")
                        print(
                            "############################################################")

            case 'Search':
                print("\nSearch By:\n1. Name\n2. Phone Number\n")
                by = 0
                while True:
                    try:
                        by = int(input("Enter your choice (1/2): "))
                        if by not in [1, 2]:
                            print("Entered an invalid choice!")
                            break
                    except:
                        print("Entered an invalid choice!")

                val = input("Search for: ").strip()
                contact = {}

                if by == 1:
                    contact = contact_book.search('name', val)
                else:
                    contact = contact_book.search('phone', val)

                print(
                    "\n############################################################")
                print(f"Name: {contact.values()[0][0]}")
                print("Phone Numbers:")
                for phone in contact.values()[0][1]:
                    print(f"\t\t{phone}")
                print(f"Email: {contact.values()[0][2]}")
                print(f"Address: {contact.values()[0][3]}")
                print(
                    "############################################################\n")

            case 'Update':
                contacts = contact_book.view_all()
                if contacts == {}:
                    print("\nNo Contacts to Display")
                else:
                    print(
                        "\n############################################################")

                    for id, contact in contacts.items():
                        print(f"{id}. {contact[0]} - {', '.join(contact[1])}")

                    print(
                        "############################################################\n")

                    indx = 0
                    try:
                        indx = int(
                            input("Enter the contact id you want to update: "))
                    except:
                        print("\nEnter a number...")

                    print(
                        "\nEnter new contact details below. Leave empty for not changing values.")

                    name = input("Name: ")
                    phone = [num.strip() for num in input(
                        "Phone Numbers (Separate with commas): ")]
                    email = input("Email: ")
                    address = input("Address: ")

                    if name == '':
                        name = contacts[indx][0]

                    if phone == ['']:
                        phone = contacts[indx][1]

                    if email == '':
                        email = contacts[indx][2]

                    if address == '':
                        address = contacts[indx][3]

                    contact_book.update(indx, name, phone, email, address)
                    print("\nContact Updated Successfully!")

            case 'Delete':
                contacts = contact_book.view_all()
                if contacts == {}:
                    print("\nNo Contacts to Display")
                else:
                    print(
                        "\n############################################################")

                    for id, contact in contacts.items():
                        print(f"{id}. {contact[0]} - {', '.join(contact[1])}")

                    print(
                        "############################################################\n")

                    indx = 0
                    try:
                        indx = int(
                            input("Enter the contact id you want to delete: "))
                    except:
                        print("\nEnter a number...")

                    contact_book.delete(indx)
                    print("\nContact Deleted Successfully!")

            case 'Exit':
                print("\n\nExiting the program...")
                break
