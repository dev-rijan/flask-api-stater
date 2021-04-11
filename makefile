run:
	@printf "\033[0;32m>>> Running app\033[0m\n"
	pipenv run gunicorn -c "python:config.gunicorn" "src.app:create_app()"

test:
	@printf "\033[0;32m>>> Running tests\033[0m\n"
	pipenv run flask test

test-coverage:
	@printf "\033[0;32m>>> Running test coverage\033[0m\n"
	pipenv run flask cov

install:
	@printf "\033[0;32m>>> Installing dependencies\033[0m\n"
	pipenv install

build-assets:
	@printf "\033[0;32m>>> Compiling assets\033[0m\n"
	cd assets \
	&& yarn run build \
	&& cd .. \
	&& pipenv run flask digest compile

docker-start:
	@printf "\033[0;32m>>> Running app\033[0m\n"
	docker-compose up --build
