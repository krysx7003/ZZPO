# pylint: disable=missing-module-docstring,missing-function-docstring
import sqlite3


def main():
    conn = sqlite3.connect("blood_draws.db")
    cursor = conn.cursor()

    query = "DROP TABLE IF EXISTS types"
    cursor.execute(query)

    query = "DROP TABLE IF EXISTS users"
    cursor.execute(query)

    query = "DROP TABLE IF EXISTS donations"
    cursor.execute(query)

    query = """CREATE TABLE types (
        typeID INT,
        name TEXT
    )"""
    cursor.execute(query)
    print("Table types created")

    query = """CREATE TABLE users (
        userID INT,
        name TEXT,
        last_name TEXT,
        age INT
    )"""
    cursor.execute(query)
    print("Table users created")

    query = """CREATE TABLE donations (
        donationID INT,
        typeID INT,
        amount FLOAT,
        date DATE,
        userID INT,
        PRIMARY KEY(donationID),
        FOREIGN KEY(typeID) REFERENCES types(typeID),
        FOREIGN KEY(userID) REFERENCES users(usersID)
    )"""
    cursor.execute(query)
    print("Table donations created")

    print("Database 'blood_draws' created successfully!")


if __name__ == "__main__":
    main()
