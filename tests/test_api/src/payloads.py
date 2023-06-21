from tests.test_api.src.generator import UserDataGenerator


class UsersPayloads:
    full_registration_data = {
        "email": UserDataGenerator.email(),
        "username": UserDataGenerator.username(),
        "first_name": UserDataGenerator.first_name(),
        "last_name": UserDataGenerator.last_name(),
        "password": "apitest4343"
    }

    test_user = {
        "email": "test_us@mail.com",
        "username": "test_user",
        "first_name": "Test",
        "last_name": "Test",
        "password": "tttt7788"
    }

    get_auth_token_for_test_user = {
        "password": "tttt7788",
        "email": "test_us@mail.com"
    }

    repeated_registry = full_registration_data

    no_email = {
        "username": UserDataGenerator.username(),
        "first_name": UserDataGenerator.first_name(),
        "last_name": UserDataGenerator.last_name(),
        "password": "apitest4343"
    }

    no_username = {
        "email": UserDataGenerator.email(),
        "first_name": UserDataGenerator.first_name(),
        "last_name": UserDataGenerator.last_name(),
        "password": "apitest4343"
    }

    no_first_name = {
        "email": UserDataGenerator.email(),
        "username": UserDataGenerator.first_name(),
        "last_name": UserDataGenerator.last_name(),
        "password": "apitest4343"
    }

    no_last_name = {
        "email": UserDataGenerator.email(),
        "username": UserDataGenerator.username(),
        "first_name": UserDataGenerator.first_name(),
        "password": "apitest4343"
    }

    no_password = {
        "email": UserDataGenerator.email(),
        "username": UserDataGenerator.username(),
        "first_name": UserDataGenerator.first_name(),
        "last_name": UserDataGenerator.last_name()
    }

    empty_json = {}

    get_auth_token = {
        'password': 'apitest4343',
        'email': full_registration_data['email']
    }

    registration_for_subscription = {
        "email": UserDataGenerator.email(),
        "username": UserDataGenerator.username(),
        "first_name": UserDataGenerator.first_name(),
        "last_name": UserDataGenerator.last_name(),
        "password": "apitest4343"
    }

    get_auth_token_non_existent_user = {
        'password': 'apitest4343',
        'email': 'ttt@test.ru'
    }

    change_password = {
        "new_password": "!Apitest100500!",
        "current_password": "apitest4343"
    }
