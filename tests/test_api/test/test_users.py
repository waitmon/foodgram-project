import allure
import pytest
import requests
from pytest_voluptuous import S

from tests.test_api.src.base_page import BasicHttpMethods
from tests.test_api.src.endpoints import UsersEndpoints
from tests.test_api.src.payloads import UsersPayloads
from tests.test_api.src.response_json_schemas import RequestSamplesSchemas


@allure.suite('Users')
class TestUsers:
    @allure.feature('Test Script: Mandatory fields submitting / Positive')
    class TestRegistrationFieldsRequiredPositive:
        @pytest.mark.smoke
        @allure.title('Test Case: New user registration')
        def test_new_user_registration(self):
            with allure.step('1. Sending POST request with valid data for registration of a new user'):
                response = BasicHttpMethods.post_no_token(UsersEndpoints.url_user_registration,
                                                          body=UsersPayloads.full_registration_data)
            with allure.step('2. Extracting JSON data from response'):
                data = response.json()
            with allure.step('3. Asserting 201 status code'):
                assert response.status_code == 201, f'Expected 201 status code, got {response.status_code} instead'
            with allure.step('4. Validating response JSON schema'):
                assert S(RequestSamplesSchemas.json_schema_registration_response) == data, \
                    f'Expected {S(RequestSamplesSchemas.json_schema_registration_response)}, got {data} instead'

    @allure.feature('Test Script: Mandatory fields submitting / Negative')
    class TestRegistrationFieldsRequiredNegative:
        @allure.title('Test Case: Repeated registration by the same user')
        @pytest.mark.regression
        def test_same_user_registration(self):
            with allure.step('1. Sending POST request with the same payloads already existed in DB'):
                response = BasicHttpMethods.post_no_token(UsersEndpoints.url_user_registration,
                                                          body=UsersPayloads.test_user)
            with allure.step('2. Extracting JSON data from second response'):
                data = response.json()
            with allure.step('3. Asserting 400 status code'):
                assert response.status_code == 400, \
                    f'Expected 400 status code, got {response.status_code} instead'
            with allure.step('4. Verifying that server is not able to register the same user again'):
                assert 'Пользователь с таким email уже существует.' in data['email']
                assert 'Пользователь с таким именем уже существует.' in data['username']

        @allure.title('Test Case: Registration without email')
        @pytest.mark.regression
        def test_registration_no_mail(self):
            with allure.step('1. Sending POST request without email in JSON'):
                response = BasicHttpMethods.post_no_token(UsersEndpoints.url_user_registration,
                                                          body=UsersPayloads.no_email)
            with allure.step('2. Asserting 400 status code'):
                assert response.status_code == 400, f'Expected 400 status code, got {response.status_code} instead'

        @allure.title('Test Case: Registration without username')
        @pytest.mark.regression
        def test_registration_no_username(self):
            with allure.step('1. Sending POST request without username in JSON'):
                response = BasicHttpMethods.post_no_token(UsersEndpoints.url_user_registration,
                                                          body=UsersPayloads.no_username)
            with allure.step('2. Asserting 400 status code'):
                assert response.status_code == 400, f'Expected 400 status code, got {response.status_code} instead'

        @allure.title('Test Case: Registration without first name')
        @pytest.mark.xfail
        @pytest.mark.regression
        def test_registration_no_first_name(self):
            with allure.step('1. Sending POST request without first name in JSON'):
                response = BasicHttpMethods.post_no_token(UsersEndpoints.url_user_registration,
                                                          body=UsersPayloads.no_first_name)
            with allure.step('2. Asserting 400 status code'):
                assert response.status_code == 400, f'Expected 400 status code, got {response.status_code} instead'

        @allure.title('Test Case: Registration without last name')
        @pytest.mark.xfail
        @pytest.mark.regression
        def test_registration_no_last_name(self):
            with allure.step('1. Sending POST request without last name in JSON'):
                response = BasicHttpMethods.post_no_token(UsersEndpoints.url_user_registration,
                                                          body=UsersPayloads.no_last_name)
            with allure.step('2. Asserting 400 status code'):
                assert response.status_code == 400, f'Expected 400 status code, got {response.status_code} instead'

        @allure.title('Test Case: Registration without password')
        @pytest.mark.regression
        def test_registration_no_password(self):
            with allure.step('1. Sending POST request without password in JSON'):
                response = BasicHttpMethods.post_no_token(UsersEndpoints.url_user_registration,
                                                          body=UsersPayloads.no_password)
            with allure.step('2. Asserting 400 status code'):
                assert response.status_code == 400, f'Expected 400 status code, got {response.status_code} instead'

        @allure.title('Test Case: Registration with an empty JSON body')
        @pytest.mark.regression
        def test_registration_empty_json_body(self):
            with allure.step('1. Sending POST request without an empty JSON body'):
                response = BasicHttpMethods.post_no_token(UsersEndpoints.url_user_registration,
                                                          body=UsersPayloads.empty_json)
            with allure.step('2. Asserting 400 status code'):
                assert response.status_code == 400, f'Expected 400 status code, got {response.status_code} instead'

    @allure.feature('Test Script: Getting information about all created users')
    class TestGetUsersList:
        @pytest.mark.smoke
        @allure.title('Test Case: Get users list')
        def test_get_users_list(self):
            with allure.step('1. Sending GET request for getting list of all created users'):
                response = BasicHttpMethods.get(UsersEndpoints.url_user_list)
            with allure.step('2. Asserting 200 status code'):
                assert response.status_code == 200, f'Expected 200 status code, got {response.status_code} instead'

    @allure.feature('Test Script: Creating and deleting authorization token')
    class TestAuthorizationToken:
        @pytest.mark.smoke
        @allure.title('Test Case: Get authorization token for registered user')
        def test_get_auth_token(self):
            with allure.step('1. Getting authorization token for existent user'):
                get_token_response = BasicHttpMethods.post_no_token(UsersEndpoints.url_auth_token,
                                                                    body=UsersPayloads.get_auth_token_for_test_user)
                data = get_token_response.json()
            with allure.step('2. Asserting status code is 200'):
                assert get_token_response.status_code == 200, \
                    f'Expected 200 status code, got {get_token_response.status_code} instead'
            with allure.step('3. Verifying token field in response is not empty '):
                assert len(data['auth_token']) != 0

        @allure.title('Test Case: Get authorization token for non-existent user')
        @pytest.mark.regression
        def test_get_auth_token_for_invalid_user(self):
            with allure.step('1. Sending POST request for token with non-existent user data in JSON body'):
                get_token_response = BasicHttpMethods.post_no_token(UsersEndpoints.url_auth_token,
                                                                    body=UsersPayloads.get_auth_token_non_existent_user)
                data = get_token_response.json()
            with allure.step('2. Asserting 400 status code'):
                assert get_token_response.status_code == 400, \
                    f'Expected 400 status code, got {get_token_response.status_code} instead'
            with allure.step('3. Verifying that passed credentials are invalid'):
                assert 'Невозможно войти с предоставленными учетными данными.' in data['non_field_errors']

        @allure.title('Test Case: Logout valid user')
        @pytest.mark.smoke
        def test_deleting_auth_token(self):
            with allure.step('1. New user registration'):
                BasicHttpMethods.post_no_token(UsersEndpoints.url_user_registration,
                                               body=UsersPayloads.full_registration_data)
            with allure.step('2. Getting token for new user'):
                get_token_response = BasicHttpMethods.post_no_token(UsersEndpoints.url_auth_token,
                                                                    body=UsersPayloads.get_auth_token)
            with allure.step('3. Extracting auth token from JSON body'):
                data = get_token_response.json()
                headers = {'Content-type': 'application/json',
                           'Accept': 'application/json',
                           'Authorization': f"Token {data['auth_token']}"
                           }
                logout = requests.post(url=UsersEndpoints.url_logout, headers=headers)
            with allure.step('4. Asserting 204 status code'):
                assert logout.status_code == 204, f'Expected 204 status code, got {logout.status_code} instead'

        @allure.title('Test Case: Logout without token')
        @pytest.mark.regression
        def test_logout_without_token(self):
            with allure.step('1. Sending request without passing Token in headers'):
                response = BasicHttpMethods.post_no_token(UsersEndpoints.url_logout, body=UsersPayloads.empty_json)
            with allure.step('2. Asserting 401 status code'):
                assert response.status_code == 401, \
                    f'Expected 401 status code, got {response.status_code} instead'

        @allure.title('Test Case: Repeatedly logout with previously used token')
        @pytest.mark.regression
        def test_inactive_token(self):
            with allure.step('1. New user registration'):
                BasicHttpMethods.post_no_token(UsersEndpoints.url_user_registration,
                                               body=UsersPayloads.full_registration_data)
            with allure.step('2. Getting token for new user'):
                get_token_response = BasicHttpMethods.post_no_token(UsersEndpoints.url_auth_token,
                                                                    body=UsersPayloads.get_auth_token)
            with allure.step('3. Extracting auth token from JSON body'):
                data = get_token_response.json()
                headers = {'Content-type': 'application/json',
                           'Accept': 'application/json',
                           'Authorization': f"Token {data['auth_token']}"
                           }
            with allure.step('4. Logging out with received token'):
                requests.post(url=UsersEndpoints.url_logout, headers=headers)
            with allure.step('5. Passing previously logged out token in headers for logging attempt'):
                response = requests.post(url=UsersEndpoints.url_logout, headers=headers)
                data = response.json()
            with allure.step('6. Asserting 401 status code'):
                assert response.status_code == 401, \
                    f'Expected 401 status code, got {response.status_code} instead'
            with allure.step('7. Verifying that passed token is invalid'):
                assert 'Недопустимый токен.' in data['detail']

    @allure.feature('Test Script: Getting current user information')
    class TestGetCurrentUser:
        @pytest.mark.smoke
        @allure.title('Test Case: Viewing current user profile with token')
        def test_get_current_user_profile_with_token(self):
            with allure.step('1. New user registration'):
                registration_response = BasicHttpMethods.post_no_token(UsersEndpoints.url_user_registration,
                                                                       body=UsersPayloads.full_registration_data)
                new_user_data = registration_response.json()
            with allure.step('2. Getting token for new user'):
                get_token_response = BasicHttpMethods.post_no_token(UsersEndpoints.url_auth_token,
                                                                    body=UsersPayloads.get_auth_token)
            with allure.step('3. Extracting auth token from JSON body'):
                data = get_token_response.json()
                headers = {'Content-type': 'application/json',
                           'Accept': 'application/json',
                           'Authorization': f"Token {data['auth_token']}"
                           }
            with allure.step('4. Sending GET request for getting current user profile'):
                response = requests.get(url=UsersEndpoints.url_current_user_profile, headers=headers)
                current_profile_data = response.json()
            with allure.step('5. Asserting 200 status code'):
                assert response.status_code == 200, f'Expected 200 status code, got {response.status_code} instead'
            with allure.step('6. Verifying current user profile is registered user'):
                assert new_user_data['id'] == current_profile_data['id']

        @allure.title('Test Case: Viewing current user profile without token')
        @pytest.mark.regression
        def test_get_current_user_profile_without_token(self):
            with allure.step('1. Sending GET request for getting current user profile without token'):
                response = BasicHttpMethods.get(UsersEndpoints.url_current_user_profile)
                data = response.json()
            with allure.step('2. Asserting 401 status code'):
                assert response.status_code == 401, f'Expected 401 status code, got {response.status_code} instead'
            with allure.step('3. Verifying token presence is mandatory'):
                assert 'Учетные данные не были предоставлены.' in data['detail']

    @allure.feature('Test Script: Changing password')
    @pytest.mark.smoke
    class TestPasswordChange:
        @allure.title('Test Case: Setting new password')
        @pytest.mark.regression
        def test_change_current_password(self):
            with allure.step('1. New user registration'):
                BasicHttpMethods.post_no_token(UsersEndpoints.url_user_registration,
                                               body=UsersPayloads.full_registration_data)
            with allure.step('2. Getting token for new user'):
                get_token_response = BasicHttpMethods.post_no_token(UsersEndpoints.url_auth_token,
                                                                    body=UsersPayloads.get_auth_token)
            with allure.step('3. Extracting auth token from JSON body'):
                data = get_token_response.json()
                headers = {'Content-type': 'application/json',
                           'Accept': 'application/json',
                           'Authorization': f"Token {data['auth_token']}"
                           }
            with allure.step('4. Sending new password'):
                response = requests.post(url=UsersEndpoints.url_change_password,
                                         json=UsersPayloads.change_password, headers=headers)
            with allure.step('5. Asserting 204 status code'):
                assert response.status_code == 204, f'Expected 204 status code, got {response.status_code} instead'

    @allure.feature('Test Script: Viewing user profile by user id')
    class TestViewUserProfileById:
        @pytest.mark.smoke
        @allure.title('Test Case: Viewing profile of valid user')
        def test_view_user_profile_by_id(self):
            with allure.step('1. New user registration'):
                registration_response = BasicHttpMethods.post_no_token(UsersEndpoints.url_user_registration,
                                                                       body=UsersPayloads.full_registration_data)
                new_user_data = registration_response.json()
            with allure.step('2. Getting token for new user'):
                get_token_response = BasicHttpMethods.post_no_token(UsersEndpoints.url_auth_token,
                                                                    body=UsersPayloads.get_auth_token)
            with allure.step('3. Extracting auth token from JSON body'):
                data = get_token_response.json()
                headers = {'Content-type': 'application/json',
                           'Accept': 'application/json',
                           'Authorization': f"Token {data['auth_token']}"
                           }
            with allure.step('4. Sending GET request for viewing created user profile'):
                response = requests.get(url=UsersEndpoints.url_user_list + f'{new_user_data["id"]}', headers=headers)
                current_profile_data = response.json()
            with allure.step('5. Asserting 200 status code'):
                assert response.status_code == 200, f'Expected 200 status code, got {response.status_code} instead'
            with allure.step('6. Verifying received user profile is registered user'):
                assert new_user_data['id'] == current_profile_data['id']

        @allure.title('Test Case: Viewing user profile without authorization token')
        @pytest.mark.regression
        def test_viewing_user_profile_without_token(self):
            with allure.step('1. Sending GET request for getting user profile without token'):
                response = requests.get(url=UsersEndpoints.url_user_list + '1')
                profile_data = response.json()
            with allure.step('2. Asserting 401 status code'):
                assert response.status_code == 401, f'Expected 401 status code, got {response.status_code} instead'
            with allure.step('3. Verifying token presence is mandatory'):
                assert 'Учетные данные не были предоставлены.' in profile_data['detail']