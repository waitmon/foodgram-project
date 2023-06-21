from faker import Faker
import random
import string


class UserDataGenerator:
    """Generator user info for registration process."""

    @staticmethod
    def username():
        res = ''.join(random.choices(string.ascii_letters.lower(), k=7))
        return res

    @staticmethod
    def first_name():
        fake = Faker()
        return fake.first_name()

    @staticmethod
    def last_name():
        fake = Faker()
        return fake.last_name()

    @staticmethod
    def email():
        fake = Faker()
        return fake.ascii_free_email()

# print(UserDataGenerator.username())
