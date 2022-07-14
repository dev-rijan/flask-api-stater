# About the project (Which is in development phase may have bugs)
This is flask api stater app based on [Flask classful](https://flask-classful.teracy.org)
Why this stater app?  
- Better routing
- service-pattrens for code resuablity
- migration, JWT authentication, Auto api docs generation included.
- better app structure

why flask-classful?  
Flask method view doesn`t support multiple routing that belongs to same CRUD operations.
Flask-classful supports complex routing of any usecases so it is best option for middle to big projects.

Flask-classful doesn't supports auto api docs generation, how do you handle this?  
I created package called  [Flask-classful-apispec](https://github.com/dev-rijan/flask-classful-apispec) on the top of marshmallow apispec and flask classful.
with the help of this plugin you can easily generate open api documentation.



## Requirements

* python >= 3.6
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
Config are written in `.env` file. You need to update config value in `.env` file.
| config | description  | Available options | Default |
| :-  | :- | :- | :- |
| FLASK_ENV | App enviroment, whether development or production. DEBUG mode is enabled in development mode | `production`, `development` | `development` | 
| SECRET_KEY | Application secrect key | | |
| WEB_RELOAD | Hot reloading app server | `true`, `false`| `false`|
| WEB_BIND |Address and port gunicorn bind to | | `0.0.0.0:8000` |
| WEB_CONCURRENCY | No of workers | | `1` |
| PYTHON_MAX_THREADS | No of threads | | `1` |
| FLASK_APP | Application factory path | | `src.app` | 
| FLASK_APP_VERSION | Application version | | `0.0.1` | 
| SERVER_NAME | app server name. |`{ip}:{port same as web bind}`, `{localhost}:{port same as web bind}` | `localhost:8000`| 
| DATABASE_URI | Database config `dialect+driver://username:password@host:port/database` | |  | 
| JWT_SECRET_KEY | JWT secrect key to generate tokens | |  | 
| ACCESS_TOKEN_EXPIRES_IN | Access token expire time (In minute) | | `10` |
| REFRESH_TOKEN_EXPIRES_IN | Refresh token expire time (In days) | | `5` |





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

### Seed users
seed admin user and random user using faker. Admin user credentials is same as defined in `.env` file
```
pipenv run flask seed users
```
## Authentication  
To access protected resources, you will need an access token.
You can generate an access and a refresh token using /auth/login endpoint. You can use admin user to get access and refresh token which are defined in `.env` files

## Protected resources

 Now admin user is created. You can use protected routes using admin user.
 You can list available routes using following commad
 ```
 pipenv run flask routes
 ```

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
Create docker network
```
docker network create flask_api
```

Make up mysql container from test db dir.
 ```
make build && make start
```
 Make build and up api
 ```
make docker-start
```

### Folder structure  
 Document TODO
 
### Api documentation using swagger
 Document TODO
 
### How to use service pattrens? and Why?
Document TODO
