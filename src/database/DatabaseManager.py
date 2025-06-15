import sqlite3
from models import BloodType, Donation, DonationType, User
_instance = None


def getDatabase() -> "DatabaseManager":
    """

    :return:
    """
    global _instance
    if _instance is None:
        _instance = DatabaseManager()
    return _instance


class DatabaseManager:
    """

    """

    PATH: str = "database/blood_draws.db"
    blood_types: list[BloodType]
    donation_types: list[DonationType]
    conn: sqlite3.Connection
    cursor: sqlite3.Cursor

    def __init__(self):
        """

        """
        self.conn = sqlite3.connect(self.PATH)
        self.conn.row_factory = (
            sqlite3.Row
        )
        self.cursor = self.conn.cursor()
        self.donation_types = self.fetchDonationTypes()

    def fetchUser(self, userId: int) -> User | None:
        """

        :param userId: 
        :return: 
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

        :return:
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

        :param userId:
        :return:
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

        :return:
        """

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

    def addUser(self, user: User) -> int | None:
        """

        :param user:
        :return:
        """

        query = "INSERT INTO users (name, last_name, age) VALUES (?, ?, ?)"
        self.cursor.execute(query, (user.name, user.last_name, user.age))
        self.conn.commit()
        return self.cursor.lastrowid

    def addDonation(self, donation: Donation) -> int | None:
        """

        :param donation:
        :return:
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

        :param userId:
        :param user:
        """

        query = """
            UPDATE users
            SET name = ?, last_name = ?, age = ? WHERE userID = ?
        """
        self.cursor.execute(query, (user.name, user.last_name, user.age, userId))
        self.conn.commit()

    def editDonation(self, donationId: int, donation: Donation):
        """

        :param donationId:
        :param donation:
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

        :param donationId:
        """

        query = """
        DELETE FROM donations
            WHERE donationID = ?
        """
        self.cursor.execute(query, (donationId,))
        self.conn.commit()
