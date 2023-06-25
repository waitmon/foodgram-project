import allure
import pytest
import requests
from pytest_voluptuous import S

from tests.test_api.src.base_page import BasicHttpMethods
from tests.test_api.src.endpoints import UsersEndpoints, SubscriptionsEndpoints
from tests.test_api.src.payloads import UsersPayloads
from tests.test_api.src.response_json_schemas import RequestSamplesSchemas


@allure.suite('Subscriptions')
class TestSubscriptions:
    @allure.feature('Test Script: User subscriptions')
    @pytest.mark.smoke
    class TestUserSubscription:
        @allure.title('Test case: Make subscription to the user')
        def test_subscribe_to_user(self):
            with allure.step('1. Getting token for existed user'):
                get_token_response = BasicHttpMethods.post_no_token(UsersEndpoints.url_auth_token,
                                                                    body=UsersPayloads.get_auth_token_for_test_user)
            with allure.step('2. Extracting auth token from JSON body'):
                data = get_token_response.json()
                headers = {'Content-type': 'application/json',
                           'Accept': 'application/json',
                           'Authorization': f"Token {data['auth_token']}"
                           }
            with allure.step('3. Creating another user to subscribe to'):
                user_to_subscribe = BasicHttpMethods.post_no_token(UsersEndpoints.url_user_registration,
                                                                   body=UsersPayloads.registration_for_subscription)
                subscribe_id = user_to_subscribe.json()
                with allure.step('4. Subscribing to created user'):
                    subscription_response = requests.post(url=UsersEndpoints.url_user_list +
                                                              f'{subscribe_id["id"]}/subscribe/',
                                                          json=UsersPayloads.empty_json, headers=headers)
                actual_subscription_data = subscription_response.json()
            with allure.step('5. Asserting 201 status code'):
                assert subscription_response.status_code == 201, f'Expected 201 status code, ' \
                                                                 f'got {subscription_response.status_code} instead'
            with allure.step('6. Asserting that created user id and user that is subscribed on are the same'):
                assert subscribe_id['id'] == actual_subscription_data['id']
            with allure.step('7. Validating response JSON schema'):
                assert S(RequestSamplesSchemas.json_schema_user_subscription) == actual_subscription_data, \
                    f'Expected {S(RequestSamplesSchemas.json_schema_user_subscription)}, got {data} instead'

        @allure.title('Test case: Make subscription to the user itself')
        @pytest.mark.regression
        def test_user_subscribes_to_itself(self):
            with allure.step('1. Getting token for existed user'):
                get_token_response = BasicHttpMethods.post_no_token(UsersEndpoints.url_auth_token,
                                                                    body=UsersPayloads.get_auth_token_for_test_user)
            with allure.step('2. Extracting auth token from JSON body'):
                data = get_token_response.json()
                headers = {'Content-type': 'application/json',
                           'Accept': 'application/json',
                           'Authorization': f"Token {data['auth_token']}"
                           }
            with allure.step('3. Sending GET request for getting current user profile'):
                response = requests.get(url=UsersEndpoints.url_current_user_profile, headers=headers)
                current_profile_data = response.json()
            with allure.step('4. Subscribing to the user from first step'):
                subscription_response = requests.post(url=UsersEndpoints.url_user_list +
                                                          f'{current_profile_data["id"]}/subscribe/',
                                                      json=UsersPayloads.empty_json, headers=headers)
                actual_subscription_data = subscription_response.json()
            with allure.step('5. Asserting 400 status code'):
                assert subscription_response.status_code == 400, f'Expected 400 status code, ' \
                                                                 f'got {subscription_response.status_code} instead'
            with allure.step('6. Verifying response message'):
                assert 'Невозможно подписаться на себя' in actual_subscription_data['errors']

        @allure.title('Test case: Make subscription to the same user')
        @pytest.mark.regression
        def test_repeated_subscription(self):
            with allure.step('1. Getting token for existed user'):
                get_token_response = BasicHttpMethods.post_no_token(UsersEndpoints.url_auth_token,
                                                                    body=UsersPayloads.get_auth_token_for_test_user)
            with allure.step('2. Extracting auth token from JSON body'):
                data = get_token_response.json()
                headers = {'Content-type': 'application/json',
                           'Accept': 'application/json',
                           'Authorization': f"Token {data['auth_token']}"
                           }
            with allure.step('3. Creating another user to subscribe to'):
                user_to_subscribe = BasicHttpMethods.post_no_token(UsersEndpoints.url_user_registration,
                                                                   body=UsersPayloads.registration_for_subscription)
                subscribe_id = user_to_subscribe.json()
                with allure.step('4. Subscribing to created user'):
                    subscription_response = requests.post(url=UsersEndpoints.url_user_list +
                                                              f'{subscribe_id["id"]}/subscribe/',
                                                          json=UsersPayloads.empty_json, headers=headers)
                with allure.step('5. Subscribing to the same user from previous step'):
                    repeated_subscription_response = requests.post(url=UsersEndpoints.url_user_list +
                                                                       f'{subscribe_id["id"]}/subscribe/',
                                                                   json=UsersPayloads.empty_json, headers=headers)
                    response_data = repeated_subscription_response.json()
                with allure.step('6. Asserting 400 status code'):
                    assert repeated_subscription_response.status_code == 400, f'Expected 400 status code, ' \
                                                                              f'got {subscription_response.status_code} instead'

                with allure.step('7. Verifying response message'):
                    assert 'Вы уже подписаны' in response_data['errors']

        @allure.title('Test case: Make subscription to the user without auth token')
        @pytest.mark.regression
        def test_subscription_without_auth_token(self):
            with allure.step('1. Sending POST request without authorization token'):
                response = BasicHttpMethods.post_no_token(UsersEndpoints.url_user_list + '1/subscribe/',
                                                          body=UsersPayloads.empty_json)
            with allure.step('2. Asserting 401 status code'):
                assert response.status_code == 401, \
                    f'Expected 401 status code, got {response.status_code} instead'

        @allure.title('Test case: Make subscription to the user not in DB')
        @pytest.mark.regression
        def test_subscription_to_non_existent_user(self):
            with allure.step('1. Getting token for existed user'):
                get_token_response = BasicHttpMethods.post_no_token(UsersEndpoints.url_auth_token,
                                                                    body=UsersPayloads.get_auth_token_for_test_user)
            with allure.step('2. Extracting auth token from JSON body'):
                data = get_token_response.json()
                headers = {'Content-type': 'application/json',
                           'Accept': 'application/json',
                           'Authorization': f"Token {data['auth_token']}"
                           }
                with allure.step('3. Passing POST endpoint with invalid id'):
                    subscription_response = requests.post(url=UsersEndpoints.url_user_list +
                                                              '10500/subscribe/', json=UsersPayloads.empty_json,
                                                          headers=headers)
            with allure.step('4. Asserting 404 status code'):
                assert subscription_response.status_code == 404, f'Expected 404 status code, ' \
                                                                 f'got {subscription_response.status_code} instead'

    class TestGetUserSubscriptionsList:
        @allure.feature('Test Script: Getting user subscriptions list')
        @pytest.mark.smoke
        class TestUserSubscription:
            @allure.title('Test case: Get subscription list of current user')
            def test_get_subscription_list(self):
                with allure.step('1. Getting token for existed user'):
                    get_token_response = BasicHttpMethods.post_no_token(UsersEndpoints.url_auth_token,
                                                                        body=UsersPayloads.get_auth_token_for_test_user)
                with allure.step('2. Extracting auth token from JSON body'):
                    data = get_token_response.json()
                    headers = {'Content-type': 'application/json',
                               'Accept': 'application/json',
                               'Authorization': f"Token {data['auth_token']}"
                               }
                with allure.step('3. Creating another user to subscribe to'):
                    user_to_subscribe = BasicHttpMethods.post_no_token(UsersEndpoints.url_user_registration,
                                                                       body=UsersPayloads.registration_for_subscription)
                    subscribe_id = user_to_subscribe.json()
                with allure.step('4. Subscribing to created user'):
                    subscription_response = requests.post(url=UsersEndpoints.url_user_list +
                                                              f'{subscribe_id["id"]}/subscribe/',
                                                          json=UsersPayloads.empty_json, headers=headers)
                with allure.step('5. Sending GET request for subscription list'):
                    list_request = requests.get(url=SubscriptionsEndpoints.url_subscription_list,
                                                json=UsersPayloads.empty_json, headers=headers)
                with allure.step('6. Asserting 200 status code'):
                    assert list_request.status_code == 200, f'Expected 200 status code, ' \
                                                            f'got {subscription_response.status_code} instead'

            @allure.title('Test case: Get subscription list without authorization')
            @pytest.mark.regression
            def test_get_subscription_list_without_token(self):
                with allure.step('1. Sending request without passing Token in headers'):
                    response = requests.get(url=SubscriptionsEndpoints.url_subscription_list,
                                            json=UsersPayloads.empty_json, headers='')
                with allure.step('2. Asserting 401 status code'):
                    assert response.status_code == 401, \
                        f'Expected 401 status code, got {response.status_code} instead'
