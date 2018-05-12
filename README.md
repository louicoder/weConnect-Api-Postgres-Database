[![Build Status](https://travis-ci.org/louiCoder/weConnect-Api-Postgres-Database.svg?branch=master)](https://travis-ci.org/louiCoder/weConnect-Api-Postgres-Database)
[![Maintainability](https://api.codeclimate.com/v1/badges/b4e864ea0427cfb100a8/maintainability)](https://codeclimate.com/github/louiCoder/weConnect-Api-Postgres-Database/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/b4e864ea0427cfb100a8/test_coverage)](https://codeclimate.com/github/louiCoder/weConnect-Api-Postgres-Database/test_coverage)
[![Coverage Status](https://coveralls.io/repos/github/louiCoder/weConnect-Api-Postgres-Database/badge.svg?branch=master)](https://coveralls.io/github/louiCoder/weConnect-Api-Postgres-Database?branch=master)


# weConnect-Api-Databases

WeConnect-Api provides a platform that brings businesses and individuals together. This platform creates awareness for businesses and gives the users the ability to write reviews about the businesses they have interacted with.

## _Author_:
    Louis Musanje Michael

## __Project captures the following routes__

| REQUEST | ROUTE | FUNCTIONALITY |
| ------- | ----- | ------------- |
| POST | /api/auth/register | creating user account |
| POST | api/auth/login | logging in for a user |
| POST | api/auth/logout | Logs out a user |
| POST | api/auth/reset-password | Password reset |
| POST | api/businesses | Registering a business |
| PUT | api/businesses/_<businessId>_ | Updating a business profile |
| DELETE | api/businesses/_<businessId>_ | delete/remove a business profile |
| GET | api/businesses | gets all avaliable businesses |
| GET | api/businesses/_<businessId>_ | Get a business |
| POST | api/businesses/_<businessId>_/reviews | Add a review for a business |
| GET | api/businesses/_<businessId>_/reviews | Get all reviews for a business |


### __Technologies used to develop this site__
1. Python
2. Postgres Database
3. Postman
4. VSCODE (for editing and debugging)

### __Project dependencies Will always be found in the file below__
    requirements.txt

### __Set up project to get it up and running__
* clone repository from link below
  
      $ git clone https://github.com/louiCoder/weConnect-Api-Postgres-Database.git
* Set up Virtual environment by running commands below

      * virtualenv venv
      * source /venv/Scripts/activate (for linux/mac)
      * /venv/Scripts/activate.exe (for windows)

* Get all project dependencies by running the command below.

      $ pip freeze -r requirements.txt
      
### __To run the unit tests invoke/run the command below.__

      $ nosetests tests/tests.py

### __or for detailed output on unit tests run with verbose.__

      $ nosetests -v tests/tests.py
      
#### To run the application invoke the command below.

      $ python app.py
      
 #### Now that the server is running , open your browser and run one of the links below.

      $ localhost:5000  or  127.0.0.1:5000
