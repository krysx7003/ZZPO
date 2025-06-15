import os
import sqlite3


def main():
    """
    Initializes the blood donation database.

    Creates all necessary tables (donation_types, users, donations),
    inserts initial data for donation types, and creates a sample user with donations.
    Does not return any value.
    """

    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, "blood_draws.db")

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS donation_types")
    cursor.execute("DROP TABLE IF EXISTS blood_types")
    cursor.execute("DROP TABLE IF EXISTS users")
    cursor.execute("DROP TABLE IF EXISTS donations")

    cursor.execute(
        """
        CREATE TABLE donation_types (
            donation_typeID INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            max_amount INT
        )
    """
    )
    print("Table donation_types created")

    cursor.execute(
        """
        CREATE TABLE users (
            userID INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            last_name TEXT,
            age INT
        )
    """
    )
    print("Table users created")

    cursor.execute(
        """
        CREATE TABLE donations (
            donation_typeID INT,
            amount FLOAT,
            date DATE,
            userID INT,
            donationID INTEGER PRIMARY KEY AUTOINCREMENT,
            FOREIGN KEY(donation_typeID) REFERENCES donation_types(donation_typeID),
            FOREIGN KEY(userID) REFERENCES users(userID)
        )
    """
    )
    print("Table donations created")

    initDonationTypes(cursor)
    initSampleUserWithDonations(cursor)

    conn.commit()
    conn.close()

    print(
        f"Database 'blood_draws.db' created and initialized successfully at: {db_path}"
    )


def initDonationTypes(cursor: sqlite3.Cursor):
    """
    Inserts initial donation types into the donation_types table.

    :param cursor: SQLite cursor object for executing database commands.
    """

    donation_types = [
        ("Krew pełna", 450),
        ("Osocze", 600),
        ("Płytki krwi", 400),
        ("Krwiniki czerwone", 400),
        ("Krwiniki białe", 300),
        ("Osocze i płytki", 650),
    ]
    cursor.executemany(
        "INSERT INTO donation_types(name, max_amount) VALUES (?, ?)", donation_types
    )
    print("Inserted initial values into donation_types")


def initSampleUserWithDonations(cursor: sqlite3.Cursor):
    """
    Inserts a sample user with associated donation records into the database.

    :param cursor: SQLite cursor object for executing database commands.
    """

    cursor.execute(
        "INSERT INTO users (name, last_name, age) VALUES (?, ?, ?)",
        ("Jan", "Kowalski", 35),
    )
    user_id = cursor.lastrowid
    print(f"Inserted sample user with userID={user_id}")

    cursor.execute("SELECT donation_typeID, name FROM donation_types")
    donation_types = {row["name"]: row["donation_typeID"] for row in cursor.fetchall()}

    sample_donations = [
        (donation_types["Krew pełna"], 450, "2023-01-15", user_id),
        (donation_types["Osocze"], 600, "2023-03-20", user_id),
        (donation_types["Płytki krwi"], 350, "2023-06-10", user_id),
    ]
    cursor.executemany(
        "INSERT INTO donations (donation_typeID, amount, date, userID) VALUES (?, ?, ?, ?)",
        sample_donations,
    )
    print("Inserted sample donations for user")


if __name__ == "__main__":
    main()
