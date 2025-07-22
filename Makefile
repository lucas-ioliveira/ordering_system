requirements:
	pip freeze > requirements.txt

build:
	docker compose -f docker-compose.yml up --build

enter container:
	docker exec -it ordering_system_app bash