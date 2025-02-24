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
                           id INT AUTO_INCREMENT PRIMARY KEY,
                           name VARCHAR(100) NOT NULL UNIQUE,
                           email VARCHAR(100),
                           address VARCHAR(500)
                       );
                       ''')

        # Phone table for store phone numbers
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS Phone(
                           person_id INT PRIMARY KEY,
                           number VARCHAR(13) PRIMARY KEY,
                           FOREIGN KEY (person_id) REFERENCES Person(id)
                       );
                       ''')

        self.conn.commit()

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
                           VALUES ('{id}', '{phone}');
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
                           WHERE person_id = {person['id']};
                           ''')
            phones = cursor.fetchall()
            self.conn.commit()

            contacts[person['name']] = [
                phones, person['email'], person['address']]

        return contacts

    def search(self, search_by, value):
        cursor = self.conn.cursor()
        contact = {}

        if search_by == 'name':
            # Select the record which match with the given name
            cursor.execute(f'''
                           SELECT * FROM Person
                           WHERE name = {value};
                           ''')
            person = cursor.fetchone()

            self.conn.commit()

            if person == []:
                return "Given Name is not in the contact list."

            # Get all phone numbers belongs to the given name
            cursor.execute(f'''
                           SELECT * FROM Phone
                           WHERE person_id = {person['id']};
                           ''')
            phones = cursor.fetchall()

            contact[person['id']] = [person['name'],
                                     phones, person['email'], person['address']]
        elif search_by == 'phone':
            # Select the record which match with the given phone number
            cursor.execute(f'''
                           SELECT * FROM Phone
                           WHERE number = {value};
                           ''')
            phone = cursor.fetchone()
            self.conn.commit()

            if phone == []:
                return "Given Phone number is not in the contact list."

            cursor.execute(f'''
                           SELECT * FROM Person
                           WHERE id = {phone['person_id']};
                           ''')
            person = cursor.fetchone()

            contact[person['id']] = [person['name'],
                                     phone, person['email'], person['address']]

        return contact

    def update(self, id,  name, phone_numbers=[], email='', address=''):
        cursor = self.conn.cursor()

        # Update Person table
        cursor.execute(f'''
                       UPDATE Person
                       SET name = {name}, email = {email}, address = {address}
                       WHERE id = {id};
                       ''')
        self.conn.commit()

        # Delete existing phone numbers
        cursor.execute(f'''
                       DELETE FROM Phone
                       WHERE person_id = {id};
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
