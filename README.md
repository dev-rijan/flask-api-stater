# About the project
This is flask api stater app based on flask-classful.
Why this stater app?
- Better routing
- service-pattrens for code resuablity
- migration, JWT authentication, Auto api docs generation included.
- better app structure

why flask-classful?
Flask method view doesn`t support multiple routing that belongs to same CRUD operations.
Flask-classful supports complex routing of any usecases so it is best option for middle to big projects.

Flask-classful doesn`t supports auto api docs generation, how you handle this?
I created package called flask-classful-apispec on the top of marshmallow apispec and flask classful.
with the help of this plugin you can easily generate open api documentation.



## Requirements

* python >= 3
* pipenv

## Install dependencies
 Install dependencies using `make`
```bash
make install
```
or Install dependencies using `pipenv`
```bash
pipenv install
```
Note:  In linux while installing dependencies if you encounter` pg_config executable not found` error then run
`sudo apt-get install libpq-dev` .
Details https://tutorials.technology/solved_errors/9-Error-pg_config-executable-not-found.html

## Setup the environment variables

Copy the `.env.example` and create `.env` file and setup required configurations

```bash
cp .env.example .env
```

## Migrations
Make sure you have correct DB configuration in `.env` file and excute follwing command to upgrade current migrations.

```bash
pipenv run flask db upgrade
```

## Start app
 Using make command
```bash
make run
```
 or

 ```bash
pipenv run gunicorn -c "python:config.gunicorn" "src.app:create_app()"
```
Now your app is available at http://localhost:8000

## Login

 Now admin user is created. You can’t signup an account for admin from UI.
credentials for admin user is same as defined in `env vars(SEED_ADMIN_USER, SEED_ADMIN_PASSWORD)`

## Tests
Please create database with `database name in env file + _test` suffix. eg, If name of actual database is `db`
then you need to create `db_test` database for test.

Test will automatically create tables and fixtures so empty database is ok.

Using make command
```bash
make test
```
 or

 ```bash
pipenv run flask test
```

## Test coverage
Using make command
```bash
make test-coverage
```
 or

 ```bash
pipenv run flask cov
```

## Using docker
Assume you installed docker and docker-compose in your machine.

Make up mysql container from test db dir.
 ```
make build && make start
```
 Make build and up api
 ```
make docker-start
```
