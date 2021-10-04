build:
	docker-compose build

up:
	docker container rm airflow || true
	docker-compose up --build -d airflow

create-user:
	docker-compose exec -u root airflow  airflow users create --username admin --password admin --role Admin --firstname admin --lastname admin --email admin@email.com

down:
	docker-compose down

logs-environment:
	docker-compose logs -f

db-init:
	airflow db init

setup-tests:
	pip install --upgrade pip
	pip install -r requirements.txt

test-local:
	pytest tests

test-docker:
	docker-compose -f docker-compose-test.yaml up --build --exit-code-from unit-tests

