#### Framework Overview
 1. tavern-pytest API Automation and Integration automation test framework for evaluating the Ask Eva API's. 
 2. This framework uses two of the most common framework available in python called Tavern(YAML based API test automation) and Pytest(simplified and easy to use unit test plugin).
 
#### Framework Limitations
 1. Still some of the important functionalities available in pytest is not implemented or have limited support in Tavern.(Simple fixtures,effective test reporting and no support 
    for using parallel test execution using pytest-xdist plugin and some other common features. Requested the features and Tavern community developers informed those features
    would be available in future iterations/Work-In-Progress).
 2. Tavern have no support for parallel test execution since fixture have no support for parameterization.
 3. To implement or enable parallel test execution have implemented the parallel test execution functionality using **subprocess and default 
    commandline argument utility(sys.argv)**.

#### Points to Remember
 1. Include or remove any environment or test related artifacts info in configs/environment.yaml.
 2. Always add/remove/edit user types under configs/environment.yaml->variables:usersInfo section
 3. Add intentTemplate Group for effective parsing and validation of different intent template scenarios under configs/environment.yaml->variables:intentTemplateGroup section
 4. Reusable yaml test stages are available in reusable_components/common.yaml
 5. Add test helper/test utility funnctions under test_utilities/helpers.py
 6. intentTemplate/Eva API combination scenarios response parsing and validation logics are available under test_utilities/type1_diabetes.json,*.json,etc.
 7. To add,modify and view pytest fixtures logic implemented, then refer tests/conftest.py
 8. Test scenarios are categorized under smoke and regression folders
 9. Test execution reports are available under reports/ directory
 10. **test_runner.py** is test driver of this framework.
 
#### PyTest CLI(Command Line Interface)

  ##### Bulk Smoke Tests Command(using default tavern and pytest CLI(Command Line Interface))
     ###### Note: use this only if you want to execute tests using tavern and it would accept one user as of now and in future it might change
        pytest -vv --html=reports/smoke/html/report.html --self-contained-html tests/smoke --user <user_type_for_test_execution>
    
  ##### Execute Specific Test Case(Using default tavern and pytest CLI(Command Line Interface))
     ###### Note: Always use this single test execution it would accept one user as of now.
        pytest -vv --html=reports/smoke/html/report.html --self-contained-html tests/smoke/<test_xxx.tavern.yaml> --user <user_type_for_test_execution>
    
  ##### Execute Smoke Test using pytest mark(-m) option
     ###### Note: Use this for single test execution or bulk execution of smoke tests and it would accept one user as of now.
        pytest -vv --html=reports/smoke/html/report.html --self-contained-html tests/smoke --user <user_type_for_test_execution>

  ##### PyTest - Run tests by keyword expressions
        pytest -vv --html=reports/smoke/html/report.html --self-contained-html tests/smoke -k "blood sugar"

#### Framework Custom CLI(Command Line Interface)
 1. CLI accepts three arguments(**"--bulk" for bulk/regression test execution,"--user" for user specific information and "--test" for smoke tests**) as of now.
 2. **--bulk** would accept only string as input and acceptable string is **"all"**
 3. **--user** would accept only list of args as input and provided users should be listed under configs/environment.yaml->variables:usersInfo section
 4. **--test** would accept only string as input and acceptable string is **"smoke"**
 5. CLI won't allow to use --bulk ,--test and --user args at the same time.
 6. CLI won't allow to use --bulk and --user args at the same time.
 7. CLI won't allow to use --bulk and --test args at the same time.
 8. CLI would allow to use --bulk and --user args separately.Refer the below command examples
 9. CLI would allow to use --test <smoke> and --user <user_type> and positional order should be maintained(--test followed by --user)

  ##### Bulk Test Execution/Regression test
     python test_runner.py --bulk all
  
  ##### Test Execution based upon UserType
     python test_runner.py --user type1_diabetes type2_diabetes
     
     where you can chain --user with one user/two user/more user by separating using space
  
  ##### Smoke Test Execution
     python test_runner.py --test smoke --user type1_diabetes
     
     where you can chain --user with one user/two user/more user by separating using space