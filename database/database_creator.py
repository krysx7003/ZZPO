# pylint: disable=missing-module-docstring,missing-function-docstring
import sqlite3


def main():
    conn = sqlite3.connect("database/blood_draws.db")
    cursor = conn.cursor()

    query = "DROP TABLE IF EXISTS donation_types"
    cursor.execute(query)

    query = "DROP TABLE IF EXISTS blood_types"
    cursor.execute(query)

    query = "DROP TABLE IF EXISTS users"
    cursor.execute(query)

    query = "DROP TABLE IF EXISTS donations"
    cursor.execute(query)

    query = """CREATE TABLE donation_types (
        donation_typeID INT AUTO_INCREMENT,
        name TEXT,
        max_amount INT,
        PRIMARY KEY(donation_typeID)
    )"""
    cursor.execute(query)
    print("Table donation_types created")

    query = """CREATE TABLE blood_types(
        blood_typeID INT AUTO_INCREMENT,
        name TEXT,
        PRIMARY KEY(blood_typeID)
    )"""
    cursor.execute(query)
    print("Table blood_types created")

    query = """CREATE TABLE users (
        userID INT AUTO_INCREMENT,
        name TEXT,
        last_name TEXT,
        age INT,
        PRIMARY KEY(userID)
    )"""
    cursor.execute(query)
    print("Table users created")
    query = """CREATE TABLE donations (
        donationID INT AUTO_INCREMENT,
        donation_typeID INT,
        amount FLOAT,
        date DATE,
        userID INT,
        PRIMARY KEY(donationID),
        FOREIGN KEY(donation_typeID) REFERENCES donation_types(donation_typeID),
        FOREIGN KEY(userID) REFERENCES users(usersID)
    )"""
    cursor.execute(query)
    print("Table donations created")

    print("Database 'blood_draws' created successfully!")
    init_blood_types(cursor)
    init_donation_types(cursor)
    conn.commit()
    conn.close()


def init_blood_types(cursor: sqlite3.Cursor):
    query = 'INSERT INTO blood_types(name) VALUES("ARh+")'
    cursor.execute(query)
    query = 'INSERT INTO blood_types(name) VALUES("ARh-")'
    cursor.execute(query)
    query = 'INSERT INTO blood_types(name) VALUES("BRh+")'
    cursor.execute(query)
    query = 'INSERT INTO blood_types(name) VALUES("BRh-")'
    cursor.execute(query)
    query = 'INSERT INTO blood_types(name) VALUES("ABRh+")'
    cursor.execute(query)
    query = 'INSERT INTO blood_types(name) VALUES("ABRh-")'
    cursor.execute(query)

    print("Inserted initial values into blood_types")


def init_donation_types(cursor: sqlite3.Cursor):
    query = """INSERT INTO donation_types(name,max_amount)
                        VALUES("Krew pełna",450)"""
    cursor.execute(query)
    query = """INSERT INTO donation_types(name,max_amount)
                        VALUES("Osocze",600)"""
    cursor.execute(query)
    query = """INSERT INTO donation_types(name,max_amount)
                        VALUES("Płytki krwi",400)"""
    cursor.execute(query)
    query = """INSERT INTO donation_types(name,max_amount)
                        VALUES("Krwiniki czerwone",400)"""
    cursor.execute(query)
    query = """INSERT INTO donation_types(name,max_amount)
                        VALUES("Krwiniki białe",300)"""
    cursor.execute(query)
    query = """INSERT INTO donation_types(name,max_amount)
                        VALUES("Osocze i płytki",650)"""
    cursor.execute(query)

    print("Inserted initial values into donation_types")


if __name__ == "__main__":
    main()
