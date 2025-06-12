# pylint: disable=missing-module-docstring,missing-function-docstring,missing-class-docstring

_instance = None


def get_database() -> "DatabaseManager":
    global _instance
    if _instance is None:
        _instance = DatabaseManager()
    return _instance


class DatabaseManager:
    PATH = "./database/blood_draws.db"

    def fetchUser(self, user_id: int):
        print("TODO - Implement")

    def fetchUserDonnations(self, user_id: int):
        print("TODO - Implement")

    def fetchDonnationTypes(self):
        print("TODO - Implement")

    def fetchBloodTypes(self):
        print("TODO - Implement")

    def createUser(self, user):
        print("TODO - Implement")

    def editUser(self, user_id: int, user):
        print("TODO - Implement")

    def createDonation(self, donation):
        print("TODO - Implement")

    def editDonation(self, donation_id: int, donation):
        print("TODO - Implement")
