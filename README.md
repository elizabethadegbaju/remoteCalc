# Remote Calculator 
[![Build Status](https://travis-ci.com/elizabethadegbaju/remoteCalc.svg?token=bjVA5yVyCJTyj8dF3LYp&branch=main)](https://travis-ci.com/elizabethadegbaju/remoteCalc)
[![Coverage Status](https://coveralls.io/repos/github/elizabethadegbaju/remoteCalc/badge.svg?t=sdwVRu)](https://coveralls.io/github/elizabethadegbaju/remoteCalc)

 A simple web service to implement a calculator

### Deployment Process
 - A github repository was created for the application locally and published online.
 - Tests for the application are executed using Pytest. Configuration can be
  found in ```pytest.ini``` file in the root directory. 
 - Test coverage is monitored using Coverage and Coveralls. Configuration
  can be found in ```.coveragerc``` and ```.coveralls.yml``` respectively.
 - The github repository uses Travis Pro for Continuous Integration. Configuration can be found in ```.travis.yml``` file in the root directory.
 - Heroku is used for deployment and the application can be reached at 
 https://remote-calc.herokuapp.com/. Configuration for the Heroku
  environment can be found in ```Procfile``` and ```runtime.txt``` files
   located in the root directory.
 - The main branch of the remote github repository is automatically deployed
  when all tests pass and Travis checks are successful. 