import sqlite3

from models import Donation, DonationType, User

_instance = None


def getDatabase() -> "DatabaseManager":
    """
    Provides a singleton instance of DatabaseManager.

    Creates a new instance if none exists, otherwise returns the existing one.
    :return: The DatabaseManager instance.
    """
    global _instance
    if _instance is None:
        _instance = DatabaseManager()
    return _instance


class DatabaseManager:
    """
    Manages database connections and operations for blood donation records.

    Handles creation, retrieval, update, and deletion of users, donations, and donation types.
    """

    PATH: str = "src/database/blood_draws.db"
    donation_types: list[DonationType]
    conn: sqlite3.Connection
    cursor: sqlite3.Cursor

    def __init__(self):
        """
        Initializes the DatabaseManager.

        Establishes a database connection and fetches initial donation types.
        """
        self.conn = sqlite3.connect(self.PATH)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self.donation_types = self.fetchDonationTypes()

    def fetchUser(self, userId: int) -> User | None:
        """
        Retrieves a user by user ID.

        :param userId: The ID of the user to fetch.
        :return: The User object if found, otherwise None.
        """
        query = "SELECT * FROM users WHERE userID = ?"
        self.cursor.execute(query, (userId,))
        row = self.cursor.fetchone()

        if row:
            user_dict = dict(zip(["name", "last_name", "age", "userID"], row))
            return User(**user_dict)

        return None

    def fetchAllDonations(self) -> list[Donation]:
        """
        Retrieves all donation records.

        :return: List of all Donation objects.
        """
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

    def fetchUserDonations(self, userId: int) -> list[Donation]:
        """
        Retrieves all donations for a specific user.

        :param userId: The ID of the user whose donations to fetch.
        :return: List of Donation objects for the specified user.
        """
        query = """
            SELECT *
            FROM donations
            WHERE userID = ?
        """
        self.cursor.execute(query, (userId,))
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
        """
        Retrieves all donation types.

        :return: List of all DonationType objects.
        """
        query = "SELECT * FROM donation_types"
        self.cursor.execute(query)

        rows = self.cursor.fetchall()
        types = []
        for row in rows:
            type_dict = dict(
                zip(
                    ["donationTypeId", "name", "maxDonationAmount"],
                    row,
                )
            )
            donation_type = DonationType(**type_dict)
            types.append(donation_type)

        return types

    def addUser(self, user: User) -> int | None:
        """
        Adds a new user to the database.

        :param user: The User object to add.
        :return: The ID of the newly added user.
        """
        query = "INSERT INTO users (name, last_name, age) VALUES (?, ?, ?)"
        self.cursor.execute(query, (user.name, user.last_name, user.age))
        self.conn.commit()
        return self.cursor.lastrowid

    def addDonation(self, donation: Donation) -> int | None:
        """
        Adds a new donation to the database.

        :param donation: The Donation object to add.
        :return: The ID of the newly added donation.
        """
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

    def editUser(self, userId: int, user: User):
        """
        Updates an existing user.

        :param userId: The ID of the user to update.
        :param user: The User object with updated data.
        """
        query = """
            UPDATE users
            SET name = ?, last_name = ?, age = ? WHERE userID = ?
        """
        self.cursor.execute(query, (user.name, user.last_name, user.age, userId))
        self.conn.commit()

    def editDonation(self, donationId: int, donation: Donation):
        """
        Updates an existing donation.

        :param donationId: The ID of the donation to update.
        :param donation: The Donation object with updated data.
        """
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
                donationId,
            ),
        )
        self.conn.commit()

    def deleteDonation(self, donationId: int):
        """
        Deletes a donation from the database.

        :param donationId: The ID of the donation to delete.
        """
        query = """
        DELETE FROM donations
            WHERE donationID = ?
        """
        self.cursor.execute(query, (donationId,))
        self.conn.commit()
