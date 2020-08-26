format:
	@black . -S --exclude=migrations

test:
	@pytest --cov=. -v

test-and-report:
	@pytest --cov=. --cov-report=xml

shell:
	FLASK_APP=app FLASK_ENV=development flask shell

db-%:
	FLASK_APP=app FLASK_ENV=development flask db $(*)

.PHONY: format test test-and-report shell db-%
