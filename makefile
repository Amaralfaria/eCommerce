start:
	python3 manage.py runserver

test:
	coverage report --omit="*/migrations/*"


.PHONY: start