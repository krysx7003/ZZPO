# pylint: disable=missing-module-docstring,missing-function-docstring,missing-class-docstring

import sqlite3

_instance = None


def get_database() -> "DatabaseManager":
    global _instance
    if _instance is None:
        _instance = DatabaseManager()
    return _instance


class DatabaseManager:
    PATH = "database/blood_draws.db"

    def __init__(self):
        self.conn = sqlite3.connect(self.PATH)
        self.conn.row_factory = sqlite3.Row  # umożliwia dostęp do wyników po nazwach kolumn
        self.cursor = self.conn.cursor()

    def fetchUser(self, user_id: int):
        query = "SELECT * FROM users WHERE userID = ?"
        self.cursor.execute(query, (user_id,))
        return dict(self.cursor.fetchone()) if self.cursor.fetchone() else None

    def fetchUserDonnations(self, user_id: int):
        query = """
            SELECT donations.*, donation_types.name AS donation_type_name
            FROM donations
            JOIN donation_types ON donations.donation_typeID = donation_types.donation_typeID
            WHERE userID = ?
        """
        self.cursor.execute(query, (user_id,))
        return [dict(row) for row in self.cursor.fetchall()]

    def fetchDonnationTypes(self):
        query = "SELECT * FROM donation_types"
        self.cursor.execute(query)
        return [dict(row) for row in self.cursor.fetchall()]

    def fetchBloodTypes(self):
        query = "SELECT * FROM blood_types"
        self.cursor.execute(query)
        return [dict(row) for row in self.cursor.fetchall()]

    def createUser(self, user):
        query = "INSERT INTO users (name, last_name, age) VALUES (?, ?, ?)"
        self.cursor.execute(query, (user["name"], user["last_name"], user["age"]))
        self.conn.commit()
        return self.cursor.lastrowid

    def editUser(self, user_id: int, user):
        query = "UPDATE users SET name = ?, last_name = ?, age = ? WHERE userID = ?"
        self.cursor.execute(query, (user["name"], user["last_name"], user["age"], user_id))
        self.conn.commit()

    def createDonation(self, donation):
        query = """
            INSERT INTO donations (donation_typeID, amount, date, userID)
            VALUES (?, ?, ?, ?)
        """
        self.cursor.execute(query, (
            donation["donation_typeID"],
            donation["amount"],
            donation["date"],
            donation["userID"]
        ))
        self.conn.commit()
        return self.cursor.lastrowid

    def editDonation(self, donation_id: int, donation):
        query = """
            UPDATE donations
            SET donation_typeID = ?, amount = ?, date = ?, userID = ?
            WHERE donationID = ?
        """
        self.cursor.execute(query, (
            donation["donation_typeID"],
            donation["amount"],
            donation["date"],
            donation["userID"],
            donation_id
        ))
        self.conn.commit()

    def fetchUserById(self, user_id: int):
        query = "SELECT * FROM users WHERE userID = ?"
        self.cursor.execute(query, (user_id,))
        row = self.cursor.fetchone()
        return dict(row) if row else None
