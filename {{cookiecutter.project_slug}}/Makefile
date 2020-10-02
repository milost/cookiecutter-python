define BROWSER_PYSCRIPT
import os, webbrowser, sys
try:
	from urllib import pathname2url
except:
	from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef

export BROWSER_PYSCRIPT
BROWSER := python -c "$$BROWSER_PYSCRIPT"

# ######################### #
# Include environment files #
# ######################### #

EXTRA_INCLUDES:=$(wildcard .env*)
ifneq ($(strip $(EXTRA_INCLUDES)),)
  CONTENTS :=  $(shell echo including extra rules $(EXTRA_INCLUDES))
  include $(EXTRA_INCLUDES)
endif

# ################# #
# Define variables  #
# ################# #

.DEFAULT_GOAL := help
SHELL:={{cookiecutter.shell}}
ENV:=$(or $(and $(wildcard ./.env),1),0)
PYENV:=$(shell command -v pyenv 2> /dev/null)
PIPENV:=$(shell command -v pipenv 2> /dev/null)
PROJECT_NAME:=$(shell sed -n '/^NAME = "/s/.*"\(.*\)"/\1/p' < setup.py)
GH_USERNAME:={{cookiecutter.github_username}}
{% if cookiecutter.use_docker == "yes" -%}
DOCKER_USER:={{cookiecutter.docker_username}}
{% endif %}
PROJECT_DESCRIPTION:={{cookiecutter.project_description}}
PROJECT_HOMEPAGE:=https://{{cookiecutter.project_slug}}.github.io/
PACKAGE_VERSION:=$(shell sed -n '/^VERSION = "/s/.*"\(.*\)"/\1/p' < setup.py)
PYTHON_VERSION:=$(shell sed -n '/^python_version = "/s/.*"\(.*\)"/\1/p' < Pipfile)
PRIVATE_REPO ?= $(shell bash -c 'read -p "Do you want to create a private project [y/n]: " tmp; if [[ $$tmp  == 'y' ]] ; then echo true; else echo false; fi')
ifneq ($(PYENV),)
	INSTALLED_PYTHON_VERSIONS:=$(shell pyenv versions)
	AVAILABLE_PYTHON_VERSIONS:=$(shell pyenv install -l)
	ENV_EXISTS:=$(if $(filter $(PROJECT_NAME), $(INSTALLED_PYTHON_VERSIONS)),true,false)
	IS_INSTALLABLE:=$(if $(filter $(PYTHON_VERSION), $(AVAILABLE_PYTHON_VERSIONS)),true,false)
	IS_INSTALLED:=$(if $(filter $(PYTHON_VERSION), $(INSTALLED_PYTHON_VERSIONS)), true,false)
endif
# PASSWORD ?= $(shell bash -c 'read -s -p "Password: " pwd; echo $$pwd')

# ############## #
# Clean targets  #
# ############## #

.PHONY: clean-build
clean-build: ## Remove build artifacts
	@echo "+ $@"
	@rm -fr requirements.txt
	@rm -fr build/
	@rm -fr dist/
	@rm -fr *.egg-info

.PHONY: clean-pyc
clean-pyc: ## Remove python file artifacts
	@echo "+ $@"
	@find . -type d -name '__pycache__' -exec rm -rf {} +
	@find . -type f -name '*.py[co]' -exec rm -f {} +
	@find . -name '*~' -exec rm -f {} +

.PHONY: clean-test
clean-test: ## Remove all test artifacts
	@echo "+ $@"
	@rm -fr htmlcov
	@rm -fr .pytest_cache
	@rm -fr coverage.xml
	@rm -fr .coverage

.PHONY: clean
clean: clean-build clean-pyc clean-test ## Remove all artifacts

.PHONY: guard
guard: # this target is checking if pyenv is installed
ifndef PYENV
    $(error "pyenv is not available please install it!")
endif

.PHONY: requirements-file
requirements-file: guard # Creates requirements.txt and dev-requirements.txt
	@echo "+ $@"
	@pipenv lock -r > requirements.txt
	@pipenv lock -r --dev-only > dev-requirements.txt

# ############# #
# Setup targets #
# ############# #

.PHONY: install-pyenv
install-pyenv: ## Install pyenv
	@echo "+ $@"
ifneq ($(wildcard ~/.pyenv),) # check if pyenv is already installed
	@echo "It seems that pyenv is already installed"
else
	@echo "Installing pyenv"
	@git clone https://github.com/pyenv/pyenv.git ~/.pyenv
	@git clone https://github.com/pyenv/pyenv-virtualenv.git ~/.pyenv/plugins/pyenv-virtualenv
	@echo -e "pyenv successfully installed\n"
	@echo -e "Add the following lines to the end of your shell config:\n"
	@echo -e 'export PYENV_ROOT="$$HOME/.pyenv"'
	@echo -e 'export PATH="$$PYENV_ROOT/bin:$$PATH"'
	@echo "if command -v pyenv 1>/dev/null 2>&1; then"
	@echo 'eval "$$(pyenv init -)"'
	@echo 'eval "$$(pyenv virtualenv-init -)"'
	@echo -e "fi\n"
	@echo "Don't forget to restart your shell!"
endif


.PHONY: install
install: ## Install project dependencies
	@echo "+ $@"
ifndef PIPENV
	$(error "pipenv is not available ... installing")
	@pip install --upgrade pip
	@pip install pipenv
endif
ifeq ($(env), dev)
	@echo "Installing project dependencies including dev dependencies ..."
	@pipenv install --dev
	@echo -e "\nexport PROJECT_ENV=dev" >> .envmake
else
	@echo "Installing project dependencies ..."
	@pipenv install
	@echo -e "\nexport PROJECT_ENV=prod" >> .envmake
endif


.PHONY: activate
activate: ## Activate project environment
	@pipenv shell


.PHONY: flush-env
flush-env: guard ## Remove the environment of this project
	@echo "+ $@"
	@pipenv --rm
	@rm .envmake


.PHONY: reinstall
reinstall: flush-env ## Reinstall project environment
	@echo "+ $@"
	@pipenv uninstall --all
ifeq ($(PROJECT_ENV),prod)
	@$(MAKE) install
else
	@$(MAKE) install env=dev
endif


.PHONY: repo
repo: ## Create a repository
ifeq ($(create-remote), true)
	@curl -X POST -H 'Authorization: token $(GITHUB_ACCESS_TOKEN)' -d "{ \
	\"name\":\"$(PROJECT_NAME)\",\
	\"private\":\"$(PRIVATE_REPO)\", \
	\"description\":\"$(PROJECT_DESCRIPTION)\", \
	\"homepage\":\"$(PROJECT_HOMEPAGE)\"}" https://api.github.com/user/repos > /dev/null 2>&1
endif
	# TODO: Check if git repo already exists
	@git init
	@git add -A
	@git commit -m "Initial commit"
	@git remote add origin "https://github.com/$(GH_USERNAME)/$(PROJECT_NAME)"
	@git branch develop
	@git checkout develop
ifeq ($(push), true)
	@git push -u origin master
	@git push --set-upstream origin develop
endif

# ################### #
# Development targets #
# ################### #

.PHONY: run
run: ## Run main method of python project
	@echo "+ $@"
	@python ./$(PROJECT_NAME)/main.py


# TODO: Include black
# TODO: Include isort
# @tox -e flake8
.PHONY: lint
lint: ## Check code style with flake8
	@echo "+ $@"
	@python -m flake8


.PHONY: update
update: ## Update project dependencies
	@echo "+ $@"
# check if the environment exists
ifeq ($(mode), outdated)
	@echo "Updating outdated packages ..."
	@pipenv update --outdated
else
	@echo "Updating packages ..."
	@pipenv update
endif


.PHONY: bump_version
bump_version: # Increment package version
	@echo "+ $@"
ifneq ($(part),)
	@bump2version $(part)
else
	@bump2version minor
endif


.PHONY: release
release: ## Package and upload release
	@echo "+ $@"
ifneq ($(part),)
	@$(MAKE) bump_version part=$(part)
else
	@$(MAKE) bump_version
endif
	@git checkout master
	@git merge develop
	@git push --tags origin master develop
ifeq ($(method), local)
	@$(MAKE) publish
	@$(MAKE) docker-publish
endif
	@git checkout develop

# ############# #
# Build targets #
# ############# #

.PHONY: build
build: clean-build ## Build source and wheels archives
	@echo "+ $@"
	@pipenv run python setup.py sdist bdist_wheel --universal
	@ls -l dist


.PHONY: sdist
sdist: clean-build ## Build sdist distribution
	@echo "+ $@"
	@python setup.py sdist
	@ls -l dist


.PHONY: wheel
wheel: clean-build ## Build bdist_wheel distribution
	@echo "+ $@"
	@python setup.py bdist_wheel --universal
	@ls -l dist


.PHONY: publish
publish: | clean-build build ## Build and upload
	@echo "+ $@"
	@python setup.py sdist bdist_wheel --universal
	@ls -l dist
	@twine upload -u __token__ -p $(PYPI_PASSWORD) dist/*


# ############# #
#! Test targets #
# ############# #

.PHONY: test
test: ## Run tests quickly with the default Python
	@echo "+ $@"
ifeq ($(coverage), true)
	@python -m pytest --cov-report html --cov-report xml --cov=tests/
ifeq ($(show), true)
	@$(BROWSER) htmlcov/index.html
endif
else
	@python -m pytest
endif
	# @tox -e py

.PHONY: test-upload
test-publish: ## Upload test results to online service (codecov)
	@$(SHELL) <(curl -s https://codecov.io/bash)

# .PHONY: test-all
# test-all: ## Run tests on every Python version with tox
# 	@echo "+ $@"
# 	# @tox

# ##################### #
# Documentation targets #
# ##################### #

.PHONY: docs
docs: ## Generate Sphinx HTML documentation, including API docs
	@echo "+ $@"
	@$(MAKE) -C ./docs clean
	@sphinx-apidoc -f -o ./docs/source ./$(PROJECT_NAME)
	@$(MAKE) -C ./docs html
ifneq ($(show),)
	@$(BROWSER) docs/_build/html/index.html
endif

.PHONY: import-docs
import-docs: ## Import the current project to ReadTheDocs
	@echo "+ $@"
	@curl -X POST -H "Authorization: Token $(RTD_TOKEN)" https://readthedocs.org/api/v3/projects/ \
	-H "Content-Type: application/json" -d "{\"name\":\"$(PROJECT_NAME)\", \
	\"repository\":{\"url\":\"https://github.com/$(GH_USERNAME)/$(PROJECT_NAME)\",\"type\":\"git\"}, \
	\"url\":{\"documentation\":\"http://$(PROJECT_NAME).readthedocs.io/\",\"home\":\"http://$(PROJECT_NAME).github.io/\"}, \
	\"homepage\":\"http://$(PROJECT_NAME).readthedocs.io/\", \
	\"programming_language\":\"py\", \
	\"language\":\"en\", \
	\"default_version\":\"stable\", \
	\"default_branch\":\"master\"}"
{% if cookiecutter.use_docker == "yes" %}
# ############## #
# Docker targets #
# ############## #

.PHONY: docker-image
docker-image: ## Build Docker image
	@echo "+ $@"
	@docker build --tag "$(DOCKER_USER)/$(PROJECT_NAME):latest" --tag "$(DOCKER_USER)/$(PROJECT_NAME):$(PACKAGE_VERSION)" --build-arg package_name=$(PROJECT_NAME) .
	@docker image ls

.PHONY: docker-remove
docker-remove: ## Remove Docker image
	@echo "+ $@"
	@docker image rm --force "$(DOCKER_USER)/$(PROJECT_NAME):$(PACKAGE_VERSION)"
	@docker image rm --force "$(DOCKER_USER)/$(PROJECT_NAME):latest"
	@docker image ls

.PHONY: docker-rebuild
docker-rebuild: | docker-remove ## Rebuild Docker image
	@docker build --no-cache --tag "$(DOCKER_USER)/$(PROJECT_NAME):latest" --tag "$(DOCKER_USER)/$(PROJECT_NAME):$(PACKAGE_VERSION)" --build-arg package_name=$(PROJECT_NAME) .
	@docker image ls

.PHONY: docker-service
docker-service: ## Run Docker image as a service
{%- if cookiecutter.use_jupyterlab == "no" %}
	@docker run -d --name=$(PROJECT_NAME) "$(DOCKER_USER)/$(PROJECT_NAME)":latest
{% else %}
	@docker run -d --name=$(PROJECT_NAME) -p 8888:8888 "$(DOCKER_USER)/$(PROJECT_NAME)":latest
{% endif %}

.PHONY: docker-shell
docker-shell: ## Run Docker image as service and attach to it
	@docker run --rm -it "$(DOCKER_USER)/$(PROJECT_NAME)":latest /bin/bash

.PHONY: docker-run
docker-run: ## Execute the latest docker image
{%- if cookiecutter.use_jupyterlab == "no" %}
	@docker run --rm "$(DOCKER_USER)/$(PROJECT_NAME)":latest
{% else %}
	@docker run --name=$(PROJECT_NAME) -p 8888:8888 "$(DOCKER_USER)/$(PROJECT_NAME)":latest
{% endif %}
.PHONY: docker-hub-login
docker-hub-login: # Login to docker hub
	@echo "+ $@"
	@docker login -u $(DOCKER_USER)

.PHONY: docker-publish
docker-publish: | docker-rebuild ## Push docker image to docker hub
	@echo "+ $@"
	@docker push "$(DOCKER_USER)/$(PROJECT_NAME)"
{% endif %}
{%- if cookiecutter.use_jupyterlab == "yes" %}
.PHONY: lab
lab: ## Start jupyterlab server
	@pipenv run jupyter lab
{% endif %}
.PHONY: info
info: # Target for testing purposes
	@echo "+ $@"
	@echo "PROJECT_NAME=$(PROJECT_NAME)"
	@echo "PYENV=$(PYENV)"
	@echo "PIPENV=$(PIPENV)"
	@echo "ENV=$(ENV)"
	@echo "DOCKER_USER=$(DOCKER_USER)"
	@echo "PYTHON_VERSION=$(PYTHON_VERSION)"
	@echo "PACKAGE_VERSION=$(PACKAGE_VERSION)"
	@echo "EXTRA_INCLUDES=$(EXTRA_INCLUDES)"
	@echo "PROJECT_ENV=$(PROJECT_ENV)"
	@echo "MAKEFILE_LIST=$(MAKEFILE_LIST)"
	@echo "REQUIRED_PYTHON_VERSION=$(REQUIRED_PYTHON_VERSION)"
	@echo "INSTALLED_PYTHON_VERSIONS=$(INSTALLED_PYTHON_VERSIONS)"
	@echo "AVAILABLE_PYTHON_VERSIONS=$(AVAILABLE_PYTHON_VERSIONS)"
	@echo "IS_INSTALLABLE=$(IS_INSTALLABLE)"
	@echo "IS_INSTALLED=$(IS_INSTALLED)"

.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' Makefile | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-16s\033[0m %s\n", $$1, $$2}'
