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
