# Have to implement threading for this one(Subprocess with Threading module)
# https://stackoverflow.com/questions/984941/python-subprocess-popen-from-a-thread
# https://luckypants.weebly.com/subprocesses-and-multithreading.html
# Search term - python popen threading thread
# https://gist.github.com/kirpit/1306188
# https://medium.com/@bfortuner/python-multithreading-vs-multiprocessing-73072ce5600b
# https://stackoverflow.com/questions/10253826/path-issue-with-pytest-importerror-no-module-named-yadayadayada

import subprocess
import sys
from test_utilities import helpers as help_utility

def subprocess_test_executor_based_on_test_type(user_type_list,test_type):
    """ Function to execute the smoke tests using subprocess module and create the test reports

    Args:
        user_type_list (list): Gives [type1_diabetes,type2_diabetes,etc]
        test_type (str): Gives test_types like smoke,etc

    Returns:
            NA
    """
    if test_type in ("smoke"):
        test_type_to_use = test_type

        for user in user_type_list:
            command = "pytest -vv --html=reports/smoke/html/report_{}_{}.html --self-contained-html -m {} tests/smoke/diabetes/default_questions --user {}".format(user, help_utility.datetime_formatter(), test_type_to_use, user)
            proc = subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
            (stdout, stderr) = proc.communicate()

            if proc.returncode == 0:
                print('stdout: [%s]' % stdout)
            else:
                print('Error executing command [%s]' % command)
                print('stderr: [%s]' % stderr)
                print('stdout: [%s]' % stdout)


def subprocess_test_executor(user_type_list):
    """ Function to execute the regression tests or tests based upon the list of user_types using subprocess module and create the test reports

    Args:
        user_type_list (list): Gives [type1_diabetes,type2_diabetes,etc]

    Returns:
            NA
    """
    for user in user_type_list:
        #command = "pytest -vv --html=reports/regression/html/report_{}_{}.html --self-contained-html tests/session_clear --user {}".format(user,help_utility.datetime_formatter(), user)
        #command = "pytest -vv --html=reports/regression/html/report_{}_{}.html --self-contained-html tests/regression/diabetes --user {}".format(user, help_utility.datetime_formatter(),user)
        command = "pytest -vv --html=reports/regression/html/report_{}_{}.html --self-contained-html tests/regression/diabetes/type1_questions --user {}".format(user,help_utility.datetime_formatter(), user)
        proc = subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE, shell=True)
        (stdout, stderr) = proc.communicate()

        if proc.returncode == 0:
            print('stdout: [%s]' % stdout)
        else:
            print('Error executing command [%s]' % command)
            print('stderr: [%s]' % stderr)
            print('stdout: [%s]' % stdout)

def main():
    """ Function to generate the commandline arguments using native/default sys.argv options. Function would retrieve the commandline arguments,
        then validate whether requested arguments and its values are available and pass it to subprocess_test_executor_based_on_test_type() or
        subprocess_test_executor() function.

    Args:
        sys.argv (list): Holds the commandline arguments in list(by default but here not passed as arguments in main())

    Attributes:
        sys.argv[0] (str): Holds the python(.py) file name
        sys.argv[1] (str): "--bulk",then returns "all"
        sys.argv[user] (list): "--user",then returns a list of user_types

    Returns:
            Returns the list(sys.argv) containing positional arguments and its values
    """
    if len(sys.argv) != 0:

        if ("--bulk" in sys.argv) and ("--user" in sys.argv) and ("--test" in sys.argv):
            print("Please don't combine both --bulk ,--test and --user combined input in command line arguments...")

        elif (("--user" in sys.argv and ("--test" in sys.argv))):
            if (sys.argv[1] == "--test") and (sys.argv[3] == "--user"):
                if isinstance(sys.argv[1],str) and isinstance(sys.argv[4:], list):
                    if (sys.argv[2] in ('smoke')) and any(usr == user_retrieved for user_retrieved in sys.argv[4:] for usr in help_utility.fetch_user_type_from_environment_file()):
                        subprocess_test_executor_based_on_test_type(sys.argv[4:], sys.argv[2])
                    else:
                        print("Requested arg for --test -> {} or User {} might not in User Type list available in environment.yaml file {} ".format(sys.argv[2],sys.argv[4:], help_utility.fetch_user_type_from_environment_file()))
            else:
                print("Arguments position order should be --test <smoke> followed by --user type1_user if you are invoking smoke test execution . Please have a look at it!!!")

        elif ("--bulk" in sys.argv and ("--test" not in sys.argv)) or ("--user" in sys.argv and ("--test" not in sys.argv)):
            if sys.argv[1] == "--bulk":
                if isinstance(sys.argv[2],str):
                    if sys.argv[2] == "all":
                        subprocess_test_executor(help_utility.fetch_user_type_from_environment_file())
                    else:
                        print("CommandLine Argument --bulk accept only 'all' as input. Please correct it... ")

            elif sys.argv[1] == '--user':
                if isinstance(sys.argv[2:], list):
                    if any(usr == user_retrieved for user_retrieved in sys.argv[2:] for usr in help_utility.fetch_user_type_from_environment_file()):
                        subprocess_test_executor(sys.argv[2:])
                    else:
                        print "User {} is not in User Type list available in environment.yaml file {} ".format(sys.argv[2:], help_utility.fetch_user_type_from_environment_file())
                else:
                    print("Please provide only list input for --user commandline argument like --user type1_diabetes / --user type1_diabetes type2_diabetes ")
            else:
                print("Project CommandLine Parser only accept --bulk ,--test and --user options. Please correct it ")

        else:
            print("Provide test with or Accept only --bulk or --user or --test arg combined with --user arg commandline arguments for Test Execution. Please correct it!!!!!")
    else:
        print("You haven't provided any commandline arguments for parsing and test execution..Pleas have a look at it and fix this!!!!")

if __name__ == '__main__':
    """ This notation/dunder option is inform python interpreter to understand this is an main file/driver file"""
    main()