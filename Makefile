include .env
export

.PHONY: init \
	install \
	uninstall\:dev \
	serve \
	serve\:dev \
	webhook \
	webhook\:dev \
	test \
	test\:cov \
	lint \
	tree \
	build

.ONE_SHELL:

init:
	@uv venv -p python3.8

install:
	@uv pip install .
	@uv pip install -e '.[dev]'

uninstall\:dev:
	@uv pip uninstall $$(uvx tomlq -r '.project."optional-dependencies".dev | join(" ")' pyproject.toml)

serve:
	@uvicorn fastapi_lab.apps.api:app --host 0.0.0.0 --port $${PORT}

serve\:dev:
	@uvicorn fastapi_lab.apps.api:app --host 0.0.0.0 --port $${PORT} --reload

webhook:
	@uvicorn fastapi_lab.apps.webhook:app --host 0.0.0.0 --port $${PORT}

webhook\:dev:
	@uvicorn fastapi_lab.apps.webhook:app --host 0.0.0.0 --port $${PORT} --reload

test:
	@pytest

test\:cov:
	@pytest --cov=. --cov-report=html

lint:
	@uvx ruff check .

format:
	@uvx ruff format .

tree:
	@tree -I 'build|__pycache__|fastapi_lab.egg-info'

build:
	@docker build .