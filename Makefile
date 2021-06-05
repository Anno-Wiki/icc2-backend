CONTAINER = icc2-backend_annowiki2_1

psql:
	sudo docker exec -it icc2-backend_db_1 psql -U postgres
shell:
	sudo docker exec -it $(CONTAINER) flask shell --TerminalInteractiveShell.editing_mode=vi
context:
	sudo docker exec -it $(CONTAINER) /bin/bash
build:
	sudo docker-compose up --build
run:
	sudo docker-compose up
migrate:
	sudo docker exec $(CONTAINER) alembic revision --autogenerate
upgrade:
	sudo docker exec $(CONTAINER) alembic upgrade head
populate: upgrade
	sudo docker exec $(CONTAINER) python insertdata.py icc2-library
