CONTAINER = icc2-backend_annowiki2_1

psql:
	sudo docker exec -it icc2-backend_db_1 psql -U postgres
shell:
	sudo docker exec -it $(CONTAINER) flask shell --TerminalInteractiveShell.editing_mode=vi
build:
	sudo docker-compose up --build
run:
	sudo docker-compose up
populate:
	sudo docker exec $(CONTAINER) insertdata.py icc2-library
migrate:
	sudo docker exec $(CONTAINER) alembic revision
upgrade:
	sudo docker exec $(CONTAINER) alembic upgrade head
