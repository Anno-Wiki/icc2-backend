%: # for passing arguments (make sure they're double quoted '""')
	@:
psql:
	sudo docker exec -it icc2-backend_db_1 psql -U postgres
flaskshell:
	sudo docker exec -it icc2-backend_annowiki2_1 flask shell --TerminalInteractiveShell.editing_mode=vi
build:
	sudo docker-compose up --build
run:
	sudo docker-compose up
populate:
	./.venv/bin/python insertdata.py
migrate:
	sudo docker exec -it icc2-backend_annowiki2_1 alembic upgrade head
