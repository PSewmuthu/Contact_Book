"""
20APP4488
P.S.A.Singhe

https://github.com/PSewmuthu/Contact_Book.git
"""

import sqlite3


class ContactBook:
    def __init__(self):
        self.conn = sqlite3.connect('contacts.db')

    def db_init(self):
        cursor = self.conn.cursor()

        # Person table for store personal details
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS Person(
                           id INT AUTO_INCREMENT PRIMARY KEY,
                           name VARCHAR(100) NOT NULL,
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
