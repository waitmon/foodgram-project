import allure
import pytest
import requests

from tests.test_api.src.base_page import BasicHttpMethods
from tests.test_api.src.endpoints import UsersEndpoints, RecipesEndpoints, ShoppingListEndpoints
from tests.test_api.src.payloads import UsersPayloads, RecipesPayloads


@allure.suite('Shopping List')
class TestShoppingList:
    class TestAddToShoppingList:
        @allure.title('Test Case: Adding recipe to shopping list')
        @pytest.mark.smoke
        def test_add_recipe_to_shopping_list(self):
            with allure.step('1. Getting token for existed user'):
                get_token_response = BasicHttpMethods.post_no_token(UsersEndpoints.url_auth_token,
                                                                    body=UsersPayloads.get_auth_token_for_test_user)
            with allure.step('2. Extracting auth token from JSON body'):
                data = get_token_response.json()
                headers = {'Content-type': 'application/json',
                           'Accept': 'application/json',
                           'Authorization': f"Token {data['auth_token']}"
                           }
            with allure.step('3. Sending POST request for creating new recipe'):
                created_recipe = requests.post(url=RecipesEndpoints.url_recipes,
                                               json=RecipesPayloads.new_recipe, headers=headers)
                recipe_data = created_recipe.json()
            with allure.step('4. Sending POST request for adding created recipe to shopping list'):
                req_add_to_shopping_list = requests.post(url=RecipesEndpoints.url_recipes + f'{recipe_data["id"]}' +
                                                             '/shopping_cart/', headers=headers)
            with allure.step('5. Asserting 201 status code'):
                assert req_add_to_shopping_list.status_code == 201, f'Expected 201 status code, ' \
                                                                    f'got {req_add_to_shopping_list.status_code} instead'

        @allure.title('Test Case: Repeatedly adding same recipe to shopping list')
        @pytest.mark.regression
        def test_add_recipe_to_shopping_list_repeatedly(self):
            with allure.step('1. Getting token for existed user'):
                get_token_response = BasicHttpMethods.post_no_token(UsersEndpoints.url_auth_token,
                                                                    body=UsersPayloads.get_auth_token_for_test_user)
            with allure.step('2. Extracting auth token from JSON body'):
                data = get_token_response.json()
                headers = {'Content-type': 'application/json',
                           'Accept': 'application/json',
                           'Authorization': f"Token {data['auth_token']}"
                           }
            with allure.step('3. Sending POST request for creating new recipe'):
                created_recipe = requests.post(url=RecipesEndpoints.url_recipes,
                                               json=RecipesPayloads.new_recipe, headers=headers)
                recipe_data = created_recipe.json()
            with allure.step('4. Sending POST request for adding created recipe to shopping list'):
                requests.post(url=RecipesEndpoints.url_recipes + f'{recipe_data["id"]}' + '/shopping_cart/',
                              headers=headers)
            with allure.step('5. Sending POST request with previous used payloads'):
                same_req = requests.post(url=RecipesEndpoints.url_recipes + f'{recipe_data["id"]}' + '/shopping_cart/',
                                         headers=headers)
            with allure.step('6. Asserting 400 status code'):
                assert same_req.status_code == 400, f'Expected 400 status code, ' \
                                                    f'got {same_req.status_code} instead'

        @allure.title('Test Case: Adding non-existent recipe to shopping list')
        @pytest.mark.regression
        @pytest.mark.xfail
        def test_add_non_existent_recipe_to_shopping_list(self):
            with allure.step('1. Getting token for existed user'):
                get_token_response = BasicHttpMethods.post_no_token(UsersEndpoints.url_auth_token,
                                                                    body=UsersPayloads.get_auth_token_for_test_user)
            with allure.step('2. Extracting auth token from JSON body'):
                data = get_token_response.json()
                headers = {'Content-type': 'application/json',
                           'Accept': 'application/json',
                           'Authorization': f"Token {data['auth_token']}"
                           }
            with allure.step('3. Sending POST request for adding non-existent recipe to shopping list'):
                req_add_to_shopping_list = requests.post(url=RecipesEndpoints.url_recipes + '999999/shopping_cart/',
                                                         headers=headers)
            with allure.step('4. Asserting 400 status code'):
                assert req_add_to_shopping_list.status_code == 400, f'Expected 400 status code, ' \
                                                                    f'got {req_add_to_shopping_list.status_code} instead'

        @allure.title('Test case: Add recipe to shopping list without authorization token')
        @pytest.mark.regression
        def test_add_recipe_to_shopping_list_without_auth_token(self):
            with allure.step('1. Sending POST endpoint without token'):
                no_token_request = requests.post(url=RecipesEndpoints.url_recipes + '1/shopping_cart/',
                                                 headers=UsersPayloads.empty_json)
            with allure.step('2. Asserting 401 status code'):
                assert no_token_request.status_code == 401, f'Expected 401 status code, ' \
                                                            f'got {no_token_request.status_code} instead'

    class TestDeleteRecipeFromShoppingList:

        @allure.title('Test Case: Delete recipe from shopping list')
        @pytest.mark.smoke
        def test_delete_recipe_from_shopping(self):
            with allure.step('1. Getting token for existed user'):
                get_token_response = BasicHttpMethods.post_no_token(UsersEndpoints.url_auth_token,
                                                                    body=UsersPayloads.get_auth_token_for_test_user)
            with allure.step('2. Extracting auth token from JSON body'):
                data = get_token_response.json()
                headers = {'Content-type': 'application/json',
                           'Accept': 'application/json',
                           'Authorization': f"Token {data['auth_token']}"
                           }
            with allure.step('3. Sending POST request for creating new recipe'):
                created_recipe = requests.post(url=RecipesEndpoints.url_recipes,
                                               json=RecipesPayloads.new_recipe, headers=headers)
                recipe_data = created_recipe.json()
            with allure.step('4. Sending POST request for adding created recipe to shopping list'):
                requests.post(url=RecipesEndpoints.url_recipes + f'{recipe_data["id"]}' + '/shopping_cart/',
                              headers=headers)
            with allure.step('5. Sending DELETE request for deleting recipe from shopping list'):
                delete_req = requests.delete(url=RecipesEndpoints.url_recipes + f'{recipe_data["id"]}' +
                                                 '/shopping_cart/', headers=headers)
            with allure.step('6. Asserting 204 status code'):
                assert delete_req.status_code == 204, f'Expected 204 status code, ' \
                                                      f'got {delete_req.status_code} instead'

        @allure.title('Test Case: Repeatedly delete recipe from shopping list')
        @pytest.mark.regression
        def test_repeatedly_delete_recipe_from_shopping_list(self):
            with allure.step('1. Getting token for existed user'):
                get_token_response = BasicHttpMethods.post_no_token(UsersEndpoints.url_auth_token,
                                                                    body=UsersPayloads.get_auth_token_for_test_user)
            with allure.step('2. Extracting auth token from JSON body'):
                data = get_token_response.json()
                headers = {'Content-type': 'application/json',
                           'Accept': 'application/json',
                           'Authorization': f"Token {data['auth_token']}"
                           }
            with allure.step('3. Sending POST request for creating new recipe'):
                created_recipe = requests.post(url=RecipesEndpoints.url_recipes,
                                               json=RecipesPayloads.new_recipe, headers=headers)
                recipe_data = created_recipe.json()
            with allure.step('4. Sending POST request for adding created recipe to shopping list'):
                requests.post(url=RecipesEndpoints.url_recipes + f'{recipe_data["id"]}' +
                                  '/shopping_cart/', headers=headers)
            with allure.step('5. Sending DELETE request for deleting recipe from shopping list'):
                requests.delete(url=RecipesEndpoints.url_recipes + f'{recipe_data["id"]}' + '/shopping_cart/',
                                headers=headers)
            with allure.step('6. Sending DELETE request with previous used payloads'):
                new_delete_req = requests.delete(
                    url=RecipesEndpoints.url_recipes + f'{recipe_data["id"]}' + '/shopping_cart/',
                    headers=headers)
            with allure.step('7. Asserting 400 status code'):
                assert new_delete_req.status_code == 400, f'Expected 204 status code, ' \
                                                          f'got {new_delete_req.status_code} instead'

    @allure.title('Test Case: Delete recipe from shopping list that has not been previously added to shopping list')
    @pytest.mark.regression
    def test_delete_not_added_recipe_from_shopping_list(self):
        with allure.step('1. Getting token for existed user'):
            get_token_response = BasicHttpMethods.post_no_token(UsersEndpoints.url_auth_token,
                                                                body=UsersPayloads.get_auth_token_for_test_user)
        with allure.step('2. Extracting auth token from JSON body'):
            data = get_token_response.json()
            headers = {'Content-type': 'application/json',
                       'Accept': 'application/json',
                       'Authorization': f"Token {data['auth_token']}"
                       }
        with allure.step('3. Sending DELETE request for deleting recipe that was not added to shopping list'):
            delete_req = requests.delete(url=RecipesEndpoints.url_recipes + '1/shopping_cart/', headers=headers)
        with allure.step('4. Asserting 400 status code'):
            assert delete_req.status_code == 400, f'Expected 400 status code, ' \
                                                  f'got {delete_req.status_code} instead'

    @allure.title('Test Case: Delete non-existent recipe from shopping list')
    @pytest.mark.regression
    @pytest.mark.xfail
    def test_delete_non_existent_recipe_from_shopping_list(self):
        with allure.step('1. Getting token for existed user'):
            get_token_response = BasicHttpMethods.post_no_token(UsersEndpoints.url_auth_token,
                                                                body=UsersPayloads.get_auth_token_for_test_user)
        with allure.step('2. Extracting auth token from JSON body'):
            data = get_token_response.json()
            headers = {'Content-type': 'application/json',
                       'Accept': 'application/json',
                       'Authorization': f"Token {data['auth_token']}"
                       }
        with allure.step('3. Sending DELETE request for deleting non-existent recipe'):
            delete_req = requests.delete(url=RecipesEndpoints.url_recipes + '10005000/shopping_cart/', headers=headers)
        with allure.step('4. Asserting 400 status code'):
            assert delete_req.status_code == 400, f'Expected 400 status code, ' \
                                                  f'got {delete_req.status_code} instead'

    @allure.title('Test Case: Delete recipe from shopping list without passing id in endpoint')
    @pytest.mark.regression
    def test_delete_recipe_from_shopping_list_without_id(self):
        with allure.step('1. Getting token for existed user'):
            get_token_response = BasicHttpMethods.post_no_token(UsersEndpoints.url_auth_token,
                                                                body=UsersPayloads.get_auth_token_for_test_user)
        with allure.step('2. Extracting auth token from JSON body'):
            data = get_token_response.json()
            headers = {'Content-type': 'application/json',
                       'Accept': 'application/json',
                       'Authorization': f"Token {data['auth_token']}"
                       }
        with allure.step('3. Sending DELETE request without id'):
            delete_req = requests.delete(url=RecipesEndpoints.url_recipes + '/shopping_cart/', headers=headers)
        with allure.step('4. Asserting 404 status code'):
            assert delete_req.status_code == 404, f'Expected 404 status code, ' \
                                                  f'got {delete_req.status_code} instead'

    @allure.title('Test Case: Delete recipe from shopping list without passing auth token')
    @pytest.mark.regression
    def test_delete_non_existent_recipe_from_shopping_list(self):
        with allure.step('1. Sending DELETE request without auth token'):
            delete_req = requests.delete(url=RecipesEndpoints.url_recipes + '1/shopping_cart/')
        with allure.step('2. Asserting 401 status code'):
            assert delete_req.status_code == 401, f'Expected 401 status code, ' \
                                                  f'got {delete_req.status_code} instead'

    class TestGetShoppingList:
        @allure.title('Test Case: Get shopping list')
        @pytest.mark.smoke
        def test_get_shopping_list(self):
            with allure.step('1. Getting token for existed user'):
                get_token_response = BasicHttpMethods.post_no_token(UsersEndpoints.url_auth_token,
                                                                    body=UsersPayloads.get_auth_token_for_test_user)
            with allure.step('2. Extracting auth token from JSON body'):
                data = get_token_response.json()
                headers = {'Content-type': 'application/json',
                           'Accept': 'application/json',
                           'Authorization': f"Token {data['auth_token']}"
                           }
            with allure.step('3. Sending POST request for creating new recipe'):
                created_recipe = requests.post(url=RecipesEndpoints.url_recipes,
                                               json=RecipesPayloads.new_recipe, headers=headers)
                recipe_data = created_recipe.json()
            with allure.step('4. Sending POST request for adding created recipe to shopping list'):
                requests.post(url=RecipesEndpoints.url_recipes + f'{recipe_data["id"]}' +
                                  '/shopping_cart/', headers=headers)
            with allure.step('5. Sending GET request for getting shopping list'):
                get_shopping_list_req = requests.get(url=ShoppingListEndpoints.url_download_shopping_list,
                                                     headers=headers)
            with allure.step('6. Asserting 200 status code'):
                assert get_shopping_list_req.status_code == 200, f'Expected 200 status code, ' \
                                                                 f'got {get_shopping_list_req.status_code} instead'

        @allure.title('Test Case: Get shopping list without passing auth token')
        @pytest.mark.regression
        def test_get_shopping_list_without_token(self):
            with allure.step('1. Sending GET request without auth token'):
                get_shopping_list_req = requests.get(url=ShoppingListEndpoints.url_download_shopping_list)
            with allure.step('2. Asserting 401 status code'):
                assert get_shopping_list_req.status_code == 401, f'Expected 401 status code, ' \
                                                      f'got {get_shopping_list_req.status_code} instead'
