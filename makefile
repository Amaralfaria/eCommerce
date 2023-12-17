start:
	python manage.py runserver

test:
	python -m pytest --cov=app --cov-report html

.PHONY: start