# pylint: disable=missing-module-docstring,missing-function-docstring,missing-class-docstring

import sqlite3

from ..models import BloodType, Donation, DonationType, User

_instance = None


def get_database() -> "DatabaseManager":
    global _instance
    if _instance is None:
        _instance = DatabaseManager()
    return _instance


class DatabaseManager:
    PATH: str = "database/blood_draws.db"
    blood_types: list[BloodType]
    donation_types: list[DonationType]
    conn: sqlite3.Connection
    cursor: sqlite3.Cursor

    def __init__(self):
        self.conn = sqlite3.connect(self.PATH)
        self.conn.row_factory = (
            sqlite3.Row
        )  # umożliwia dostęp do wyników po nazwach kolumn
        self.cursor = self.conn.cursor()
        self.blood_types = self.fetchBloodTypes()
        self.donation_types = self.fetchDonationTypes()

    # Fetch data methods
    def fetchUser(self, user_id: int) -> User | None:
        query = "SELECT * FROM users WHERE userID = ?"
        self.cursor.execute(query, (user_id,))
        row = self.cursor.fetchone()

        if row:
            user_dict = dict(zip(["name", "last_name", "age", "userID"], row))
            return User(**user_dict)

        return None

    def fetchAllDonations(self) -> list[Donation]:
        query = """
            SELECT *
            FROM donations
        """
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        donations = []

        for row in rows:
            donation_dict = dict(
                zip(
                    [
                        "donation_typeID",
                        "amount",
                        "date",
                        "userID",
                        "donationID",
                    ],
                    row,
                )
            )
            donation_dict["date"] = str(donation_dict["date"])
            donation = Donation(**donation_dict)
            donations.append(donation)

        return donations

    def fetchUserDonations(self, user_id: int) -> list[Donation]:
        query = """
            SELECT *
            FROM donations
            WHERE userID = ?
        """
        self.cursor.execute(query, (user_id,))
        rows = self.cursor.fetchall()
        donations = []
        for row in rows:
            donation_dict = dict(
                zip(
                    [
                        "donation_typeID",
                        "amount",
                        "date",
                        "userID",
                        "donationID",
                    ],
                    row,
                )
            )
            donation_dict["date"] = str(donation_dict["date"])
            donation = Donation(**donation_dict)
            donations.append(donation)

        return donations

    def fetchDonationTypes(self) -> list[DonationType]:
        query = "SELECT * FROM donation_types"
        self.cursor.execute(query)

        rows = self.cursor.fetchall()
        types = []
        for row in rows:
            type_dict = dict(
                zip(
                    ["donation_typeID", "name", "max_amount"],
                    row,
                )
            )
            donation_type = DonationType(**type_dict)
            types.append(donation_type)

        return types

    def fetchBloodTypes(self) -> list[BloodType]:
        query = "SELECT * FROM blood_types"
        self.cursor.execute(query)

        rows = self.cursor.fetchall()
        types = []
        for row in rows:
            type_dict = dict(
                zip(
                    ["blood_typeID", "name"],
                    row,
                )
            )
            blood_type = BloodType(**type_dict)
            types.append(blood_type)

        return types

    # Add data methods
    def addUser(self, user: User) -> int | None:
        query = "INSERT INTO users (name, last_name, age) VALUES (?, ?, ?)"
        self.cursor.execute(query, (user.name, user.last_name, user.age))
        self.conn.commit()
        return self.cursor.lastrowid

    def addDonation(self, donation: Donation) -> int | None:
        query = """
            INSERT INTO donations (donation_typeID, amount, date, userID)
            VALUES (?, ?, ?, ?)
        """
        self.cursor.execute(
            query,
            (
                donation.donation_typeID,
                donation.amount,
                donation.date,
                donation.userID,
            ),
        )
        self.conn.commit()
        return self.cursor.lastrowid

    # Edit data methods
    def editUser(self, user_id: int, user: User):
        query = "UPDATE users SET name = ?, last_name = ?, age = ? WHERE userID = ?"
        self.cursor.execute(query, (user.name, user.last_name, user.age, user_id))
        self.conn.commit()

    def editDonation(self, donation_id: int, donation: Donation):
        query = """
            UPDATE donations
            SET donation_typeID = ?, amount = ?, date = ?, userID = ?
            WHERE donationID = ?
        """
        self.cursor.execute(
            query,
            (
                donation.donation_typeID,
                donation.amount,
                donation.date,
                donation.userID,
                donation_id,
            ),
        )
        self.conn.commit()
