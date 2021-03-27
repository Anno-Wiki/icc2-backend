psql:
	sudo docker exec -it icc2-backend_db_1 psql -U postgres
flaskshell:
	sudo docker exec -it icc2-backend_annowiki2_1 flask shell --TerminalInteractiveShell.editing_mode=vi
