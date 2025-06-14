import os
import sqlite3


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))  # folder tego pliku
    db_path = os.path.join(
        base_dir, "blood_draws.db"
    )  # baza w tym folderze, bez subfolderu

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Usuwanie tabel i tworzenie jak wcześniej
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

    # cursor.execute(
    #     """
    #     CREATE TABLE blood_types(
    #         blood_typeID INTEGER PRIMARY KEY AUTOINCREMENT,
    #         name TEXT
    #     )
    # """
    # )
    # print("Table blood_types created")

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

    init_blood_types(cursor)
    init_donation_types(cursor)
    init_sample_user_with_donations(cursor)

    conn.commit()
    conn.close()

    print(
        f"Database 'blood_draws.db' created and initialized successfully at: {db_path}"
    )


def init_blood_types(cursor: sqlite3.Cursor):
    blood_types = ["ARh+", "ARh-", "BRh+", "BRh-", "ABRh+", "ABRh-"]
    for bt in blood_types:
        cursor.execute("INSERT INTO blood_types(name) VALUES (?)", (bt,))
    print("Inserted initial values into blood_types")


def init_donation_types(cursor: sqlite3.Cursor):
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


def init_sample_user_with_donations(cursor: sqlite3.Cursor):
    # Dodaj przykładowego użytkownika
    cursor.execute(
        "INSERT INTO users (name, last_name, age) VALUES (?, ?, ?)",
        ("Jan", "Kowalski", 35),
    )
    user_id = cursor.lastrowid
    print(f"Inserted sample user with userID={user_id}")

    # Pobierz id typów donacji
    cursor.execute("SELECT donation_typeID, name FROM donation_types")
    donation_types = {row["name"]: row["donation_typeID"] for row in cursor.fetchall()}

    # Dodaj kilka donacji dla użytkownika
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
