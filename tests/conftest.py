#Refer the below mentioned link for goog docstring implementation
# https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html

#pytest not recognising the path hence used the below line of sys path code
#https://chrisyeh96.github.io/2017/08/08/definitive-guide-python-imports.html
#https://stackoverflow.com/questions/10253826/path-issue-with-pytest-importerror-no-module-named-yadayadayada
#https://stackoverflow.com/questions/20971619/ensuring-py-test-includes-the-application-directory-in-sys-path

import logging
import pytest
import time
import json
from py._xmlgen import html

import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

from test_utilities import helpers as help_utility


def pytest_addoption(parser):
    """ Implement pytest hook that defines custom command line options to be passed to pytest.
    Args:
        parser (parser config object): Holds the pytest command line options information

    Attributes:
        --bulk option (str): Retrieve the value "all"
        --user option (list): Retrieve the user types from user

    Returns:
            parser object which can be accessible via request fixture available to pytest

    """

    diabetes_disease_group = parser.getgroup('Bulk Execution type category')
    #have to optimize the default value of first option in group
    diabetes_disease_group.addoption(
        "--bulk", action="store",required=False,help="Use this option to bulk test execution for all users"
    )
    #nargs='*' - allowed additional arguments will be accepted, and any other additional
    #https://mkaz.blog/code/python-argparse-cookbook/
    #https://stackoverflow.com/questions/15753701/argparse-option-for-passing-a-list-as-option/15753721


    user_disease_type_group = parser.getgroup('Diabetes Diseases Type User Options')
    #default='type1_diabetes' choices=['type2_diabetes','type1_diabetes','prediabetes_and_alcoholism']
    user_disease_type_group.addoption(
        "--user",required=False,action="store", nargs='+',choices=help_utility.fetch_user_type_from_environment_file(),
                help="Use this option to select the users to cover all test scenarios"
    )

def pytest_collection_modifyitems(config, items):
    """ PytestHook to verify whether commandline arguments are available to the pytest runtime for later usage

        Args:
            config (_pytest.config.Config) object: Holds command line arguments passed and other config info
            items (items object): Holds the pytest mark and parameterize objects

        Attributes:
            --bulk option (str): Retrieve the value "all"
            --user option (list): Retrieve the user types from user

        Returns:
            Fails the pytest session if requested commandline arguments is not available else return nothing
    """

    if config.getoption("--bulk") and config.getoption("--user"):
        pytest.fail("Please don't provide both command line arguments at the same time for test execution")

    if config.getoption("--bulk") or config.getoption("--user"):
        # --bulk given in cli: for bulk execution of test scenarios for all user types available in environment.yaml file
        # --user given in cli: for test execution based upon the user types available in environment.yaml file
        return
    pytest.fail("need to provide either --bulk option for bulk test execution and --user option for user type(type1_diabetes,etc) execution")


@pytest.fixture(name="time_request")
def fix_time_request():
    """
        Pytest fixture created to verify execution time. Final execution would be calculated by substracting stop - start and logging
        it to the pytest commandline/log file if provided

        Args:
            NA

        Returns:
            Log the time taken for test execution in seconds
    """
    t0= time.time()
    yield
    t1 = time.time()
    logging.info("Test took %s seconds", t1 - t0)

@pytest.fixture
def json_loader():
    """ Pytest Fixture to load data from JSON file

    Args:
        Outer function won't receive any information

    Returns:
        Returns the inner function(_loader) and it holds the loaded json data
    """
    def _loader(filename):
        """
            Function to validate and load the json file and return as fixture for later usage

            Args:
                filename (file object) : holds the necessary json filepath

            Returns:
                Returns the json file loaded and validated

        """
        with open(filename, 'r') as f:
            print(filename)
            data = json.load(f)
        return data

    return _loader

@pytest.fixture()
def custom_argument_passer():
    """
        Pytest fixture created to receive the custom positional and keyword arguments during the runtime

        Args:
            outer function won't receive any

        Returns:
            Returns the inner function (_foo)

        Examples:
            def test_example(argument_printer):
                first_case = argument_printer('a', 'b')
                assert first_case == (('a', 'b'), {})
    """
    def _foo(*args, **kwargs):
        """
            Inner function to accept the custom positional and keyword arguments and return the arguments as fixture for later purpose

            Args:
                *args (tuple): Holds tuple object like ((1,2,3))
                **kwargs (dict): Holds the dict object like ({'a':'d'})
            Attributes:
                *args (tuple): Input would be like 1,2,3
                **kwargs (dict): Input would be like 'a'='b'

            Returns:
                Returns the positional and keyword arguments
        """
        return (args, kwargs)

    return _foo

@pytest.fixture(name='user_input_cmd_option',scope='session') #Tavern would support only function and session based scopes
def retrieve_user_info_for_test_from_command_line(request):
    """
        Pytest Fixture to retrieve the --user commandline arguments value and pass it to tavern tests for execution.This would fixture
        would automatically close the session once operation is completed

        Args:
            request (fixture): Invokes pytest default request fixture to access the Configs

        Returns:
            --user option in a list

        Todo:
            Once tavern has the support for pytest-xdist plugin /parallelism/fixture parameterization remove the list indexing user_type_cmd[0]
    """

    user_type_cmd = None
    if request.config.getoption("--user"):
        user_type_cmd = request.config.getoption("--user")

    def finalizer():
        pass
    request.addfinalizer(finalizer)
    print( "\n \n *************************************************************** Executing tests for the user **********************************************************************")
    print(user_type_cmd)
    print(" *************************************************************** Executing tests for the user **********************************************************************")

    return user_type_cmd[0]

@pytest.fixture(name='bulk_input_cmd_option',scope='session') #Tavern would support only function and session based scopes
def retrieve_bulk_info_for_test_from_command_line(request):
    """
        Pytest Fixture to retrieve the --bulk commandline arguments value and pass it to tavern tests for execution.This would fixture
        would automatically close the session once operation is completed

        Args:
            request (fixture): Invokes pytest default request fixture to access the Configs

        Returns:
            --bulk option in a string having a value of "all"

    """
    bulk_test_exec_cmd = None
    if request.config.getoption("--bulk") is not None:
        bulk_test_exec_cmd = request.config.getoption("--bulk")

    def finalizer():
        pass
    request.addfinalizer(finalizer)
    return bulk_test_exec_cmd

@pytest.fixture()
def provide_user_info_for_test(request,user_input_cmd_option):
    """
        Pytest Fixture to provide the userInfo options for user identification and test scenario execution and validateion.
        This would fixture would automatically close the session once operation is completed

        Args:
            request (fixture): Invokes pytest default request fixture to access the Configs
            user_input_cmd_option (custom_fixture): used user_input_cmd_option()/retrieve_user_info_for_test_from_command_line() chaining to retrieve the output
        Returns:
            Returns the userInfo dict with username,model name,sessionId for using in tavern tests

    """
    retrieve_user_info = help_utility.retrieve_user_info_yaml_file(user_input_cmd_option)
    def finalizer():
        pass
    request.addfinalizer(finalizer)

    return {'user_info':retrieve_user_info}


@pytest.fixture(scope='session',params=['type1_diabetes', 'type2_diabetes'])
def bulk_test_execution_param_fixture(request):
    """
        Pytest Fixture to provide the userInfo options for user identification and test scenario execution and validateion.
        Also this fixture provides the mechanism to execute bulk test execution in tavern.

        Args:
            request (fixture): Invokes pytest default request fixture to access the Configs

        Returns:
            Returns the userInfo dict with username,model name,sessionId for using in tavern tests

        Todo:
            #https://hackebrot.github.io/pytest-tricks/param_id_func/
            As of now tavern don't have support fixtures parameterization

            ERROR at setup of C:\Vxxxxx\HPS_Tests\HPS_Automation\HPS_API_TESTS_QA_Integration\tests\session_clear\1111test_session_clear.tavern.yaml::Session Clear Flow
            The requested fixture has no parameter defined for test:
            tests/session_clear/1111test_session_clear.tavern.yaml::Session Clear Flow

             Requested fixture 'common_command_logic_info1' defined in:tests\conftest.py:159

            Requested here:
            c:\python27\lib\site-packages\_pytest\fixtures.py:470
    """
    return {'user_info':help_utility.retrieve_user_info_yaml_file(request.param)}


def pytest_configure(config):
  """
    Pytest hook to retrieve the metadata of tests using pytest-metadata plugin to use it in html test reports. It have the option to
    include the custom environment metadata information also.This metadata would be used while creating the html reports using pytest-html plugin.

    Args:
        config (_pytest.config.Config): Holds the config info for usage

    Returns:
        metadata information to use automatically with pytest-html plugin to create the environment info
  """
  if hasattr(config, '_metadata'):
      config._metadata['HostUrl'] = help_utility.fetch_host_from_environment_file()
      config._metadata['UserType'] = config.getoption("--user")
      config._metadata['UserName'] = help_utility.retrieve_user_info_yaml_file(config.getoption("--user")[0])['username']
      config._metadata['UserModelName'] = help_utility.retrieve_user_info_yaml_file(config.getoption("--user")[0])['user_model_name']
      config._metadata['Session_Id'] = help_utility.retrieve_user_info_yaml_file(config.getoption("--user")[0])['session_id']


@pytest.mark.optionalhook
def pytest_html_results_table_header(cells):
    cells.insert(1, html.th('Template',class_='sortable'))
    cells.insert(2, html.th('Test_Type', class_='sortable'))
    cells.insert(3, html.th('Disease_Category', class_='sortable'))
    cells.insert(4, html.th('Question_Type', class_='sortable'))
    cells.pop()

@pytest.mark.optionalhook
def pytest_html_results_table_row(report, cells):
    cells.insert(1, html.td(report.template_description))
    cells.insert(2, html.td(report.test_type))
    cells.insert(3, html.td(report.disease_category))
    cells.insert(4, html.td(report.question_type))
    cells.pop()

#https://docs.pytest.org/en/latest/_modules/_pytest/reports.html
@pytest.mark.hookwrapper
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    report.template_description = report.location[2].split("::")[1].split(' ')[1]
    report.test_type = report.location[0].split('\\')[1]
    report.disease_category = report.location[0].split('\\')[2]
    report.question_type = report.location[0].split('\\')[3]


def append_passed(report):
    xpassed = 0
    passed = 0
    if report.when == 'call':
        ##Refer for xpass/xfail https://docs.pytest.org/en/latest/skipping.html
        if hasattr(report,'wasxfail'):
            xpassed += 1
    else:
        passed += 1

    return xpassed, passed

def append_failed(report):
    xpassed = failed = errors = 0

    if getattr(report,'when',None) == 'call':
        if hasattr(report,'wasxfail'):
            # pytest < 3.0 marked xpasses as failures
            xpassed += 1
        else:
            failed += 1
    else:
        errors += 1

    return xpassed, failed, errors

def append_skipped(report):
    xfailed = skipped = 0
    if hasattr(report, "wasxfail"):
        xfailed += 1
    else:
        skipped += 1

    return xfailed , skipped

def append_other(report):
    has_rerun = pytest.Class.config.pluginmanager.hasplugin('rerunfailures')
    rerun = 0 if has_rerun else None
    # pytest-html note :: For now, the only "other" the plugin give support is rerun
    # Have to explore this one to get full info about rerun option and including them in tests
    rerun += 1
    return rerun


def pytest_runtest_logreport(report):
    """ collector finished collecting. """
    if report.passed:
        append_passed(report)
    elif report.failed:
        append_failed(report)
    elif report.skipped:
        append_skipped(report)
    else:
        append_other(report)


def pytest_collectreport(report):
    if report.failed:
        append_failed(report)














