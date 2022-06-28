import pytest
from pytest_bdd import scenarios, given, when, then, parsers
import configparser
from utilities.log import custom_logger as log
from utilities import rw_csv as csv, convert_cron
from utilities.get_using_json import get_json_value
import requests
import pytest_check as check
from utilities.resources import ApiResources
from utilities.get_using_re import get_substring
# import pdb; pdb.set_trace()


log = log()
log.info("\n\n")

# Passing feature file
scenarios("../features/test_sanity_cases.feature")


@pytest.fixture
def context():
    b = None
    yield b


@given('I set base REST API url and headers correctly')
def set_baseurl():
    config = configparser.ConfigParser()
    config.read(f'./utilities/properties.ini')
    context.base_url = config['API']['BASE_URL']
    context.headers = None


@given(parsers.parse('Set csv path to "{csv_file_path}"'))
def set_csv_path(csv_file_path='data/sanity_automation.csv'):
    try:
        context.csv_file_path = csv_file_path
        log.info(f"CSV path set to: {context.csv_file_path}")
    except Exception as e:
        log.exception(e)
        raise e


@given(parsers.parse('Get data from CSV for "{testcase_id}"'))
def get_testcase_data(testcase_id):
    try:
        context.testcase_id = testcase_id
        # Fetching all data from the provided testcase_id from the CSV file
        context.row = csv.read_csv(testcase_id, key="row", csv_file_path=context.csv_file_path)
        try:
            # Check if CSV file returned any error
            if context.row["error"]:
                raise context.row["error_msg"]
        except Exception as e:
            # If the error is not raised for "error" key not in row (context.row["error"]) log and raise error message
            if "error" not in str(e):
                log.exception(e)
                raise e
        log.info(f'<{context.testcase_id}> - CSV File row data: {context.row}')
    except Exception as e:
        log.exception(e)
        raise e


@when(parsers.parse('I set api endpoint to "{endpoint}"'))
def set_endpoint(endpoint):
    try:
        context.endpoint_name = endpoint
        context.endpoint = f"ApiResources.{endpoint}"
        context.endpoint = eval('f"' + eval(context.endpoint) + '"')
        log.info(f"<{context.testcase_id}> - Endpoint set to {context.endpoint_name}: {context.endpoint}")
    except Exception as e:
        log.exception(e)
        raise e


@when(parsers.parse('Set the body of request to "{body}"'))
def set_body(body):
    try:
        # Set body to blank
        if body.lower() == 'blank':
            context.body = "{}"
        # Set body to update
        elif body.lower() == 'update body':
            context.body = context.row[body.capitalize()]
        # Set body from CSV file
        elif body.lower() == 'body':
            context.body = context.row[body.capitalize()]
        else:
            context.body = body
        context.body_json = get_json_value(context.body)
        log.info(f"<{context.testcase_id}> - Body set to: {context.body}")

    except Exception as e:
        log.exception(e)
        raise e


# HTTP request methods

@when(u'Perform get')
def perform_get():
    try:
        log.info(f"<{context.testcase_id}> - Performing GET")
        log.info(context.base_url + context.endpoint)
        context.response = requests.get(context.base_url + context.endpoint, headers=context.headers)
        log.info(f'<{context.testcase_id}> - GET Response: {context.response.json()}')
    except Exception as e:
        log.exception(e)
        raise e


@when(u'Perform post')
def perform_post():
    try:
        log.info(f"<{context.testcase_id}> - Performing post")
        context.response = requests.post(context.base_url + context.endpoint, data=context.body.encode('utf-8'),
                                         headers=context.headers)
        log.info(f'<{context.testcase_id}> - POST Response: {context.response.json()}')
        if str(context.endpoint_name) == "create_fake_story" and int(context.response.status_code) == 201:
            get_story_id()
            context.story = True

    except Exception as e:
        log.exception(e)
        raise e


@when(u'Perform put')
def perform_put():
    try:
        log.info(f"<{context.testcase_id}> - Performing PUT")
        context.response = requests.put(context.base_url + context.endpoint, data=context.body.encode('utf-8'),
                                        headers=context.headers)
        log.info(f'<{context.testcase_id}> - PUT Response: {context.response.json()}')
    except Exception as e:
        log.exception(e)
        raise e


@when(u'Perform delete')
def perform_delete():
    try:
        log.info(f"<{context.testcase_id}> - Performing DELETE")
        context.response = requests.delete(context.base_url + context.endpoint, headers=context.headers)
        log.info(f'<{context.testcase_id}> - DELETE Response: {context.response.json()}')
    except Exception as e:
        log.exception(e)
        raise e


@then(parsers.parse('Validate HTTP response code "{response_from}"'))
def validate_response_code(response_from='from csv'):
    try:
        # Get response code from CSV file if input is "from csv" else take the provided input value.
        context.response_code = context.row[
            "Expected status code"] if response_from == "from csv" else response_from
        log.info(f"<{context.testcase_id}> - Actual Response Code: {context.response.status_code}")
        log.info(f"<{context.testcase_id}> - Expected Response Code: {context.response_code}")
        assert str(context.response.status_code) == context.response_code, \
            (f"<{context.testcase_id}> - Actual Response Code({context.response.status_code}) does not matches "
             f"Expected Response Code({context.response_code})")
    except AssertionError as e:
        log.exception(e)
        raise e
    except Exception as e:
        log.exception(e)
        raise e


@then('Get story Id')
def get_story_id():
    try:
        context.story_id = context.response.json()["id"]
        log.info(f'<{context.testcase_id}> - Story Id: {context.story_id}')
    except Exception as e:
        log.exception(e)
        raise e


@given('Test 123')
def test():
    log.info("Test 123")


@when("When statement")
def when():
    log.info("when statement")



@then('Print when data context.row')
def get_when_data():
    log.info("this is what we want")
