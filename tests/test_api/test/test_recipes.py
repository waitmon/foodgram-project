import allure
import pytest
import requests

from tests.test_api.src.base_page import BasicHttpMethods
from tests.test_api.src.endpoints import UsersEndpoints, RecipesEndpoints
from tests.test_api.src.payloads import UsersPayloads, RecipesPayloads


@allure.suite('Recipes')
class TestRecipes:
    @allure.feature('Test Script: Create new recipe')
    class TestCreateNewRecipe:
        @allure.title('Test case: Creating new recipe')
        @pytest.mark.smoke
        def test_new_recipe(self):
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
            with allure.step('4. Asserting 201 status code'):
                assert created_recipe.status_code == 201, f'Expected 201 status code, ' \
                                                          f'got {created_recipe.status_code} instead'

        @allure.title('Test case: Get subscription list without authorization')
        @pytest.mark.regression
        def test_create_new_recipe_without_auth_token(self):
            with allure.step('1. Sending request without passing Token in headers'):
                response = BasicHttpMethods.post_no_token(url=RecipesEndpoints.url_recipes,
                                                          body=RecipesPayloads.new_recipe)
            with allure.step('2. Asserting 401 status code'):
                assert response.status_code == 401, \
                    f'Expected 401 status code, got {response.status_code} instead'

    @allure.feature('Test Script: Get information of created recipes')
    class TestGetRecipes:
        @allure.title('Test case: Get list of created recipes')
        @pytest.mark.smoke
        def test_get_recipes_list(self):
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
                requests.post(url=RecipesEndpoints.url_recipes,
                              json=RecipesPayloads.new_recipe, headers=headers)
            with allure.step('4. Sending GET request for getting recipe information'):
                get_recipe_list = BasicHttpMethods.get(RecipesEndpoints.url_recipes)
            with allure.step('5. Asserting 200 status code'):
                assert get_recipe_list.status_code == 200, f'Expected 200 status code, ' \
                                                           f'got {get_recipe_list.status_code} instead'
            with allure.step('6. Verifying information list is not empty'):
                assert len(get_recipe_list.json()) != 0

        @allure.title('Test case: Get information by recipe id')
        @pytest.mark.smoke
        def test_get_recipe_info_by_id(self):
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
                new_recipe_created = requests.post(url=RecipesEndpoints.url_recipes,
                                                   json=RecipesPayloads.new_recipe, headers=headers)
                recipe_data = new_recipe_created.json()
            with allure.step('4. Sending GET request for getting recipe information'):
                get_recipe_list = BasicHttpMethods.get(RecipesEndpoints.url_recipes + f'{recipe_data["id"]}')
                get_recipe_list_data = get_recipe_list.json()
            with allure.step('5. Asserting 200 status code'):
                assert get_recipe_list.status_code == 200, f'Expected 200 status code, ' \
                                                           f'got {get_recipe_list.status_code} instead'
            with allure.step('6. Verifying that id in received list is equal to the id in created recipe'):
                assert recipe_data['id'] == get_recipe_list_data['id']

        @allure.title('Test case: Get information by invalid id')
        @pytest.mark.regression
        def test_get_recipe_by_invalid_id(self):
            with allure.step('1. Passing invalid id in GET request'):
                get_invalid_id_recipe = BasicHttpMethods.get(RecipesEndpoints.url_recipes + '9999999999')
            with allure.step('2. Asserting 404 status code'):
                assert get_invalid_id_recipe.status_code == 404, f'Expected 404 status code, ' \
                                                                 f'got {get_invalid_id_recipe.status_code} instead'

    @allure.feature('Test Script: Recipes update')
    class TestUpdateRecipe:
        @allure.title('Test case: Update created recipe')
        @pytest.mark.smoke
        def test_update_recipe(self):
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
                created_recipe_data = created_recipe.json()
            with allure.step('4. Update created recipe by passing PATCH request with new payloads'):
                update_recipe = requests.patch(url=RecipesEndpoints.url_recipes + f'{created_recipe_data["id"]}/',
                                               json=RecipesPayloads.update_recipe, headers=headers)
            with allure.step('5. Asserting 200 status code'):
                assert update_recipe.status_code == 200, f'Expected 200 status code, ' \
                                                         f'got {update_recipe.status_code} instead'
            with allure.step('6. Verifying initial recipe has been changed'):
                assert created_recipe_data != update_recipe.json()

        @allure.title('Test case: Update recipe without authorization')
        @pytest.mark.regression
        def test_update_recipe_without_auth_token(self):
            with allure.step('1. Update created recipe by passing PATCH request without token'):
                update_recipe = requests.patch(url=RecipesEndpoints.url_recipes + f'10/',
                                               json=RecipesPayloads.update_recipe)
            with allure.step('2. Asserting 401 status code'):
                assert update_recipe.status_code == 401, f'Expected 401 status code, ' \
                                                         f'got {update_recipe.status_code} instead'

        @allure.title('Test case: Update recipe for another user')
        @pytest.mark.regression
        @pytest.mark.xfail
        def test_update_recipe_for_another_user(self):
            with allure.step('1. New user registration'):
                BasicHttpMethods.post_no_token(UsersEndpoints.url_user_registration,
                                               body=UsersPayloads.full_registration_data)
            with allure.step('2. Getting token for new user'):
                get_token_response = BasicHttpMethods.post_no_token(UsersEndpoints.url_auth_token,
                                                                    body=UsersPayloads.get_auth_token)
            with allure.step('3. Extracting auth token from JSON body'):
                initial_user_data = get_token_response.json()
                initial_user_headers = {'Content-type': 'application/json',
                                        'Accept': 'application/json',
                                        'Authorization': f"Token {initial_user_data['auth_token']}"
                                        }
            with allure.step('4. Sending POST request for creating new recipe'):
                create_recipe_by_initial_user = requests.post(url=RecipesEndpoints.url_recipes,
                                                              json=RecipesPayloads.new_recipe,
                                                              headers=initial_user_headers)
                created_recipe_data = create_recipe_by_initial_user.json()
            with allure.step('5. Login by another user'):
                get_second_token = BasicHttpMethods.post_no_token(UsersEndpoints.url_auth_token,
                                                                  body=UsersPayloads.get_auth_token_for_test_user)
            with allure.step('6. Extracting auth token from JSON body'):
                new_data = get_second_token.json()
                new_user_headers = {'Content-type': 'application/json',
                                    'Accept': 'application/json',
                                    'Authorization': f"Token {new_data['auth_token']}"
                                    }
            with allure.step('7. Update recipe created by initial user on behalf of the another user'):
                update_recipe = requests.patch(url=RecipesEndpoints.url_recipes + f'{created_recipe_data["id"]}/',
                                               json=RecipesPayloads.update_recipe, headers=new_user_headers)
            with allure.step('8. Asserting 403 status code'):
                assert update_recipe.status_code == 403, f'Expected 403 status code, ' \
                                                         f'got {update_recipe.status_code} instead'

        @allure.title('Test case: Update non-existent recipe')
        @pytest.mark.regression
        def test_update_non_existent_recipe(self):
            with allure.step('1. Getting token for existed user'):
                get_token_response = BasicHttpMethods.post_no_token(UsersEndpoints.url_auth_token,
                                                                    body=UsersPayloads.get_auth_token_for_test_user)
            with allure.step('2. Extracting auth token from JSON body'):
                data = get_token_response.json()
                headers = {'Content-type': 'application/json',
                           'Accept': 'application/json',
                           'Authorization': f"Token {data['auth_token']}"
                           }
            with allure.step('3. Passing invalid recipe id in PATCH request'):
                update_recipe = requests.patch(url=RecipesEndpoints.url_recipes + '99999999999/',
                                               json=RecipesPayloads.update_recipe, headers=headers)
            with allure.step('4. Asserting 404 status code'):
                assert update_recipe.status_code == 404, f'Expected 404 status code, ' \
                                                         f'got {update_recipe.status_code} instead'

    @allure.feature('Test Script: Delete recipes')
    class TestDeleteRecipe:
        @allure.title('Test case: Delete created recipe')
        @pytest.mark.smoke
        def test_delete_recipe(self):
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
                new_recipe_created = requests.post(url=RecipesEndpoints.url_recipes,
                                                   json=RecipesPayloads.new_recipe, headers=headers)
                recipe_data = new_recipe_created.json()
            with allure.step('4. Sending DELETE request'):
                delete_req = requests.delete(url=RecipesEndpoints.url_recipes + f'{recipe_data["id"]}',
                                             headers=headers)
            with allure.step('5. Asserting 204 status code'):
                assert delete_req.status_code == 204, f'Expected 204 status code, ' \
                                                      f'got {delete_req.status_code} instead'

        @allure.title('Test case: Repeatedly delete created recipe')
        @pytest.mark.regression
        def test_repeated_recipe_delete(self):
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
                new_recipe_created = requests.post(url=RecipesEndpoints.url_recipes,
                                                   json=RecipesPayloads.new_recipe, headers=headers)
                recipe_data = new_recipe_created.json()
            with allure.step('4. Sending DELETE request'):
                requests.delete(url=RecipesEndpoints.url_recipes + f'{recipe_data["id"]}',
                                headers=headers)
            with allure.step('5. Repeated sending DELETE request'):
                second_delete_req = requests.delete(url=RecipesEndpoints.url_recipes + f'{recipe_data["id"]}',
                                                    headers=headers)
            with allure.step('6. Asserting 404 status code'):
                assert second_delete_req.status_code == 404, f'Expected 404 status code, ' \
                                                             f'got {second_delete_req.status_code} instead'

        @allure.title('Test case: Delete recipe created by another user')
        @pytest.mark.regression
        @pytest.mark.xfail
        def test_delete_recipe_created_by_another_user(self):
            with allure.step('1. New user registration'):
                BasicHttpMethods.post_no_token(UsersEndpoints.url_user_registration,
                                               body=UsersPayloads.full_registration_data)
            with allure.step('2. Getting token for new user'):
                get_token_response = BasicHttpMethods.post_no_token(UsersEndpoints.url_auth_token,
                                                                    body=UsersPayloads.get_auth_token)
            with allure.step('3. Extracting auth token from JSON body'):
                initial_user_data = get_token_response.json()
                initial_user_headers = {'Content-type': 'application/json',
                                        'Accept': 'application/json',
                                        'Authorization': f"Token {initial_user_data['auth_token']}"
                                        }
            with allure.step('4. Sending POST request for creating new recipe'):
                create_recipe_by_initial_user = requests.post(url=RecipesEndpoints.url_recipes,
                                                              json=RecipesPayloads.new_recipe,
                                                              headers=initial_user_headers)
                created_recipe_data = create_recipe_by_initial_user.json()
            with allure.step('5. Login by another user'):
                get_second_token = BasicHttpMethods.post_no_token(UsersEndpoints.url_auth_token,
                                                                  body=UsersPayloads.get_auth_token_for_test_user)
            with allure.step('6. Extracting auth token from JSON body'):
                new_data = get_second_token.json()
                new_user_headers = {'Content-type': 'application/json',
                                    'Accept': 'application/json',
                                    'Authorization': f"Token {new_data['auth_token']}"
                                    }
            with allure.step('7. Passing id of created recipe in DELETE request'):
                delete_req = requests.delete(url=RecipesEndpoints.url_recipes + f'{created_recipe_data["id"]}',
                                             headers=new_user_headers)
            with allure.step('8. Asserting 403 status code'):
                assert delete_req.status_code == 403, f'Expected 403 status code, ' \
                                                      f'got {delete_req.status_code} instead'

        @allure.title('Test case: Delete non-existent recipe')
        @pytest.mark.regression
        def test_delete_non_existent_recipe(self):
            with allure.step('1. Getting token for existed user'):
                get_token_response = BasicHttpMethods.post_no_token(UsersEndpoints.url_auth_token,
                                                                    body=UsersPayloads.get_auth_token_for_test_user)
            with allure.step('2. Extracting auth token from JSON body'):
                data = get_token_response.json()
                headers = {'Content-type': 'application/json',
                           'Accept': 'application/json',
                           'Authorization': f"Token {data['auth_token']}"
                           }
            with allure.step('3. Passing invalid recipe id in DELETE request'):
                delete_req = requests.delete(url=RecipesEndpoints.url_recipes + '99999999999/',
                                             headers=headers)
            with allure.step('4. Asserting 404 status code'):
                assert delete_req.status_code == 404, f'Expected 404 status code, ' \
                                                      f'got {delete_req.status_code} instead'

        @allure.title('Test case: Delete recipe without recipe id in endpoint')
        @pytest.mark.regression
        def test_delete_recipe_without_id(self):
            with allure.step('1. Getting token for existed user'):
                get_token_response = BasicHttpMethods.post_no_token(UsersEndpoints.url_auth_token,
                                                                    body=UsersPayloads.get_auth_token_for_test_user)
            with allure.step('2. Extracting auth token from JSON body'):
                data = get_token_response.json()
                headers = {'Content-type': 'application/json',
                           'Accept': 'application/json',
                           'Authorization': f"Token {data['auth_token']}"
                           }
            with allure.step('3. Sending DELETE endpoint without recipe id'):
                delete_req = requests.delete(url=RecipesEndpoints.url_recipes, headers=headers)
            with allure.step('4. Asserting 405 status code'):
                assert delete_req.status_code == 405, f'Expected 405 status code, ' \
                                                      f'got {delete_req.status_code} instead'

        @allure.title('Test case: Delete recipe without authorization token')
        @pytest.mark.regression
        def test_delete_recipe_without_auth_token(self):
            with allure.step('1. Sending DELETE endpoint without token'):
                delete_req = requests.delete(url=RecipesEndpoints.url_recipes, headers=UsersPayloads.empty_json)
            with allure.step('2. Asserting 401 status code'):
                assert delete_req.status_code == 401, f'Expected 401 status code, ' \
                                                      f'got {delete_req.status_code} instead'
