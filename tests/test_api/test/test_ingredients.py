import allure
import pytest
from pytest_voluptuous import S

from tests.test_api.src.base_page import BasicHttpMethods
from tests.test_api.src.endpoints import IngredientsEndpoints
from tests.test_api.src.response_json_schemas import RequestSamplesSchemas


@allure.suite('Ingredients')
class TestIngredients:
    @allure.feature('Test Script: Getting available ingredients list')
    @pytest.mark.smoke
    class TestGetIngredient:
        @allure.title('Test case: Get ingredients list')
        def test_get_ingredients_list(self):
            with allure.step('1. Sending GET request for getting ingredients list'):
                response = BasicHttpMethods.get(IngredientsEndpoints.url_ingredients_list)
                data = response.json()
            with allure.step('2. Asserting 200 status code'):
                assert response.status_code == 200, f'Expected 200 status code, got {response.status_code} instead'
            with allure.step('3. Validating response JSON schema'):
                assert S(RequestSamplesSchemas.json_schema_ingredients) == data, \
                    f'Expected {S(RequestSamplesSchemas.json_schema_ingredients)}, got {data} instead'

    @allure.feature('Test Script: Getting ingredient by id')
    @pytest.mark.smoke
    class TestGetTagId:
        @allure.title('Test Case: Get ingredient by id')
        def test_get_ingredient_by_id(self):
            with allure.step('1. Passing ingredient id in GET request'):
                response = BasicHttpMethods.get(IngredientsEndpoints.url_ingredients_list + '1/')
            with allure.step('2. Asserting 200 status code'):
                assert response.status_code == 200, f'Expected 200 status code, got {response.status_code} instead'

        @allure.title('Test Case: Get ingredient by invalid id')
        @pytest.mark.regression
        def test_get_ingredient_by_invalid_id(self):
            with allure.step('1. Passing non existent ingredient id in GET request'):
                response = BasicHttpMethods.get(IngredientsEndpoints.url_ingredients_list + '100500/')
            with allure.step('2. Asserting 404 status code'):
                assert response.status_code == 404, f'Expected 200 status code, got {response.status_code} instead'