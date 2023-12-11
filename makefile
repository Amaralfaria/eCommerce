start:
	python3 manage.py runserver

test:
	python -m pytest --cov=app


.PHONY: start