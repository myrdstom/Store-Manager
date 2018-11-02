# Store Manager
[![Maintainability](https://api.codeclimate.com/v1/badges/2715d106d25e7164ae1d/maintainability)](https://codeclimate.com/github/myrdstom/Store-Manager/maintainability)
[![Build Status](https://travis-ci.org/myrdstom/Store-Manager.svg?branch=challenge-3)](https://travis-ci.org/myrdstom/Store-Manager)
[![Coverage Status](https://coveralls.io/repos/github/myrdstom/Store-Manager/badge.svg?branch=challenge-3)](https://coveralls.io/github/myrdstom/Store-Manager?branch=challenge-3)


Store Manager is a web application that helps store owners manage sales and product inventory records. 
This application is meant for use in a single store.

## Pre-requisites
The UI pages are static for now and have no functionality however they can be viewed [here](https://myrdstom.github.io/Store-Manager/)

## Setup

To setup,

1. You can clone the repository using the link [here](https://github.com/myrdstom/Store-Manager.git)
    ```
    $ git clone https://github.com/myrdstom/Store-Manager
    ```    

2. Download and install python 3.6 or higher

3. Install pip [here](https://pip.pypa.io/en/stable/installing/)

4. Switch to the directory that you have just cloned and set up a virtual-environment
    ```
    $ cd store manager
    $ pip install virtualenv
    $ virtualenv venv
    $ cd venv/bin/activate    
    ```    
    **Note** if you are using windows activate the environment with ```venv/scripts/activate```
5. Move to the root directory of the project

6. Install all dependencies in the ```requirements.txt``` to finalise setting up the environment.
    ```
    pip install -r requirements.txt   
    ``` 
    
 7. Download and install the postgreSQL database [here](https://www.postgresql.org/download/)
 
 8. Create two databases ```store_manager_pk```  for the production environment and  ```test_store_manager``` for the test environment

## Build

1. Run the file run.py``` python run.py ``` in the root directory and follow  the prompts

2. Test all endpoints with [POSTMAN](https://www.getpostman.com/apps)

## The endpoints:
| End Point  | Description |
| ------------- | ------------- |
|GET /api/v1/signup | Register a new user
|POST /api/v1/login  | Login a new user
|GET /api/v1/products | Get all products
|POST /api/v1/products  | Post a new product
|PUT /api/v1/products/<int:product_id>  | Edit a product
|DELETE /api/v1/products/<int:product_id>  | Delete a product
|GET /api/v1/products/<int:product_id> | Return a single product
|GET /api/v1/sales | Get all sales
|POST /api/v1/sales  | Post a new sale
|GET /api/v1/products/<int:sale_id> | Return a single sale

## Tests

1. pip install nose

2. Run ```nosetests --with-coverage --cover-package=app``` to run all tests with coverage


## Deployment
The Python application is hosted on [Heroku](https://store-manager-heroku.herokuapp.com/)

The application is documented on [Swagger](https://store-manager-heroku.herokuapp.com/apidocs/#/)

##Built with
The project has been built with the following technologies so far:
* HTML
* CSS
* Javascript
* Python/Flask
* postgreSQL
* Swagger

## Author
Paul Kayongo

