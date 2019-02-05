import os
import datetime
import json
import yaml
from datetime import datetime

#Join the current working directory/project path, connect to configs directory and access the environment.yaml file
configPath = os.path.abspath(os.path.join(os.path.dirname(__file__), '../configs'))
file_name_path = configPath + '/environment.yaml'

def datetime_formatter():
    """
        Utility function to create the timestamp with string formatting. It would take current time as
        input and output formatted datetime text

        Args:
            NA

        Returns:
            Datetime stamp returned would be 01-07-2019 and represented in the html filename as "report_type1_diabetes_01-07-2019.html"
    """
    now = datetime.now()
    return now.strftime("%m-%d-%Y")

def assert_quick_response(response):
    """
    Make sure that a request doesn't take too long

    Args:
        response (json object): Interact with the response object of the API interacted
    Returns:
        True|False
    """
    print "Validating the performance of the stages available"
    assert response.elapsed < datetime.timedelta(seconds=20)

def save_response(response):
    """
        Utility function to fetch the API response and save it as json file in the current directory.

        Args:
            response (json object): Interact with the response object of the API interacted

        Returns:
            Create a api_resp.json file in the current working directory
    """
    filename='api_resp.json'
    with open(filename, 'w') as f:
        json.dump(response.json(), f)

def parse_yaml_file(file_name):
    """
        Utility function to parse the yaml file to fetch the config options

        Args:
            file_name (file object): yaml file for loading the data

        Returns:
            Return the loaded yaml file
    """
    yaml_file = None
    with open(file_name, 'r') as stream:
        try:
            yaml_file = yaml.load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    return yaml_file

def retrieve_user_info_yaml_file(user_name):
    """
        Utility function to parse the yaml file based upon the username and returns the user information from environment.yaml file

        Args:
            user_name (str): user_type/user_name input provided during run time

        Returns:
            Return the user info dict like {'username':'username','user_model_name':'user_model_name','session_id':'session_id'}
    """
    yaml_file_loaded = parse_yaml_file(file_name_path)
    returned_info = None
    #print user_name
    for a in range(len(yaml_file_loaded['variables']['usersInfo'])):
        if user_name in yaml_file_loaded['variables']['usersInfo'][a]:
            returned_info =  yaml_file_loaded['variables']['usersInfo'][a][user_name]
            break
    #print returned_info
    return returned_info

def load_json_file(usertype_to_access_file):
    """
        Utility function to load and access the user scenarios response file available under test_utilities folder based upon the user_type

        Args:
            usertype_to_access_file (str): user type

        Returns:
            json file loaded with user_type for parsing the API response validation for different scenarios.
    """
    configPath = os.path.abspath(os.path.join(os.path.dirname(__file__), '../test_utilities'))
    file_name = configPath + '/{}.json'.format(usertype_to_access_file)
    with open(file_name,'r') as stream:
        try:
            json_loaded = json.load(stream)
        except Exception as e:
            print(e)
    return json_loaded

def parse_json_to_verify_response(response,user_type,ailments_category,question):
    """
        Utility function to retrieve the user information from environment.yaml file for test script execution and response parsing and validation

        Args:
            response (json object): response.json() from the api
            user_type (str): user_type provided during run time
            ailments_category (str): ailments category to filter the scenario for response validation
            question (str): question (It is the key in json file)

        Returns:
            Retrieve the answer information retrieved for the question provided
    """
    json_retrieved = load_json_file(user_type)
    answer_retrieved = None

    for a in range(len(json_retrieved['userType'])):
        for b in range(len(json_retrieved['userType'][a])):
            #print user_type in json_retrieved['userType'][a]
            if user_type in json_retrieved['userType'][a]:
                for c in range(len(json_retrieved['userType'][a][user_type])):
                    #print json_retrieved['userType'][a][user_type][c]
                    if ailments_category in json_retrieved['userType'][a][user_type][c]:
                        for d in  range(len(json_retrieved['userType'][a][user_type][c][ailments_category]['questions'])):
                            if question in json_retrieved['userType'][a][user_type][c][ailments_category]['questions'][d]:
                                answer_retrieved = json_retrieved['userType'][a][user_type][c][ailments_category]['questions'][d][question]

    '''
    for a in range(len(json_retrieved['userType'])):
        for b in range(len(json_retrieved['userType'][a])):
            if user_type in json_retrieved['userType'][a]:

                if ailments_category in json_retrieved['userType'][a][user_type]:
                    for c in range(len(json_retrieved['userType'][a][user_type][b][ailments_category]['questions'])):
                        if question in json_retrieved['userType'][a][user_type][b][ailments_category]['questions'][c]:
                            answer_retrieved = json_retrieved['userType'][a][user_type][b][ailments_category]['questions'][c][question]'''

    return {'response_retrieved':answer_retrieved}

def fetch_user_type_from_environment_file():
    """
        Utility function to fetch the user_type from environmenty.yaml file

        Args:
            NA

        Returns:
            Returns a user_type(like type1_diabetes)
    """
    yaml_file_loaded = parse_yaml_file(file_name_path)
    final_user_type_retrieved = []
    for a in range(len(yaml_file_loaded['variables']['usersInfo'])):
        final_user_type_retrieved.append(yaml_file_loaded['variables']['usersInfo'][a].keys()[0])
    return final_user_type_retrieved

def fetch_host_from_environment_file():
    """
        Utility function to fetch the host information from environmenty.yaml file
        Args:
            NA
        Returns:
            Returns a host from environment.yaml
    """
    yaml_file_loaded = parse_yaml_file(file_name_path)
    return yaml_file_loaded['variables']['host']['server_url']

def response_fetch_parser_from_tavern_tests(response,user_type,ailments_category,question,endpoint_tag):
    """  Tavern helper/External function to validate the type1 questions API responses.

        Args:
            response (json object):
            user_type (str): user_type provided during run time
            ailments_category (str): ailments category to filter the scenario for response validation
            question (str): question (It is the key in json file)

        Returns:
            True|False to the Tavern test suite/tests

    """
    print("\n\n################################################################################### Start - Response Retrieved from Tavern Test Stages###################################################################################")
    print json.dumps(response.json(),indent=4)
    print("################################################################################### End - Response Retrieved from Tavern Test Stages###################################################################################")

    response_info_fetched = parse_json_to_verify_response(response.json(),user_type,ailments_category,question)

    assert response.json()['stage'] == response_info_fetched['response_retrieved']['stage']
    assert response.json()['success'] == response_info_fetched['response_retrieved']['success']
    assert response.json()['template'] == response_info_fetched['response_retrieved']['template']
    assert response.json()['endpoint'] == endpoint_tag
    #print type(response.json()['nl'])
    assert isinstance(response.json()['nl'],unicode) == True



def validate_unicode_type_string_in_resp(response):
    """
        Utility function to validate unicode object type for api response validation

        Args:
            response (json object): response.json() from the api

        Returns:
            True|False to the Tavern test suite/tests
    """
    print("\n\n################################################################################### Response Retrieved from Tavern Test Stages###################################################################################")
    print json.dumps(response.json(),indent=4)
    print
    print("\n\n################################################################################### Response Retrieved from Tavern Test Stages###################################################################################")
    assert isinstance(response.json()['nl'],unicode) == True


def response_fetch_parser_from_tavern_tests_for_blood_tests(response):
    """  Tavern helper/External function to print type2/blood sugar flow question responses.

        Args:
            response (json object):
        Returns:
            NA

    """
    print("\n\n################################################################################### Start - Response Retrieved from Tavern Test Stages###################################################################################")
    print json.dumps(response.json(),indent=4)
    print("################################################################################### End - Response Retrieved from Tavern Test Stages###################################################################################")


    assert response.json()['final_answer'] == "Remember that I am not a medical professional and the information I provide is not meant to be used to diagnose or determine treatment for any condition. That said, the results of your test seem to suggest elevated blood glucose levels"



def provide_intermediate_resp_based_on_user_test(response,userType):

    intermediate_question_term = None
    if userType == "type2_diabetes":
        intermediate_question_term = 'type 2 diabetes'

    elif userType == "type1_diabetes":
        intermediate_question_term = 'type 1 diabetes'

    elif userType == 'prediabetes_and_alcoholism':
        intermediate_question_term = 'prediabetes'

    else:
        pass

    return {'inter_ques':intermediate_question_term}


def retrieve_resp_from_steps(response):
    return {'json_dict': {key: value for key,value in response.json().items()}}

