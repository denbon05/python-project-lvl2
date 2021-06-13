install:
	poetry install

test:
	poetry run pytest -svv

test-coverage cover:
	poetry run pytest --cov=gendiff --cov-report xml

sort-imports:
	poetry run isort gendiff tests

lint: sort-imports
	poetry run flake8 gendiff

selfcheck:
	poetry check

check: selfcheck test lint

build: check
	poetry build

package-install:
	python3 -m pip install --force-reinstall --user dist/*.whl

.PHONY: install test lint selfcheck check build gendiff