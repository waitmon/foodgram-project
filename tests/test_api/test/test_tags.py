import allure
import pytest
from pytest_voluptuous import S

from tests.test_api.src.base_page import BasicHttpMethods
from tests.test_api.src.endpoints import TagsEndpoints
from tests.test_api.src.response_json_schemas import RequestSamplesSchemas


@allure.suite('Tags')
class TestTags:
    @allure.feature('Test Script: Getting available tags list')
    @pytest.mark.smoke
    class TestGetTags:
        @allure.title('Test case: Get tags list')
        def test_get_tags_list(self):
            with allure.step('1. Sending GET request for getting tags list'):
                response = BasicHttpMethods.get(TagsEndpoints.url_tags_list)
                data = response.json()
            with allure.step('2. Asserting 200 status code'):
                assert response.status_code == 200, f'Expected 200 status code, got {response.status_code} instead'
            with allure.step('3. Validating response JSON schema'):
                assert S(RequestSamplesSchemas.json_schema_tags) == data, \
                    f'Expected {S(RequestSamplesSchemas.json_schema_tags)}, got {data} instead'

    @allure.feature('Test Script: Getting tag by id')
    @pytest.mark.smoke
    class TestGetTagId:
        @allure.title('Test Case: Get tag by id')
        def test_get_tag_by_id(self):
            with allure.step('1. Passing tag id in GET request'):
                response = BasicHttpMethods.get(TagsEndpoints.url_tags_list + '1/')
            with allure.step('2. Asserting 200 status code'):
                assert response.status_code == 200, f'Expected 200 status code, got {response.status_code} instead'

        @allure.title('Test Case: Get tag by invalid id')
        @pytest.mark.regression
        def test_get_tag_by_invalid_id(self):
            with allure.step('1. Passing non existent tag id in GET request'):
                response = BasicHttpMethods.get(TagsEndpoints.url_tags_list + '100500/')
            with allure.step('2. Asserting 404 status code'):
                assert response.status_code == 404, f'Expected 200 status code, got {response.status_code} instead'