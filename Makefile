SHELL:=/bin/bash
PY_VERSION := 3.8

BASE := $(shell /bin/pwd)
VENV_DIR := $(BASE)/.venv

PYTHON := $(shell /usr/bin/which python$(PY_VERSION))
VIRTUALENV := $(PYTHON) -m venv

export PYTHONUNBUFFERED := 1
export PATH := var:$(PATH):$(VENV_DIR)/bin
export TABLE_NAME := todo
FUNCTION_DIR = lib/todo-api

.DEFAULT_GOAL := lint
.PHONY: bootstrap

install:
	# Install CDK dependencies
	yarn install --frozen-lockfile
	# Install Python dependencies
	@make install-python


build:
	# Build CDK
	yarn build
	# Verify Python
	@make lint
	# Execute Test
	@make test

lint:
	sh -c '. .venv/bin/activate; flake8 --tee --output-file=pylint.out --exclude=src/python-libs lib/todo-api'

test:
	sh -c '. .venv/bin/activate; py.test -x lib/todo-api/tests'

install-python: .venv
	.venv/bin/pip install -e ./lib/todo-api
ifneq ($(wildcard ./lib/todo-api/test-requirements.txt),)
	.venv/bin/pip install -r ./lib/todo-api/test-requirements.txt
endif

bootstrap:
	@make install
	# Bootstrap AWS account
	CDK_NEW_BOOTSTRAP=1 yarn cdk bootstrap --cloudformation-execution-policies arn:aws:iam::aws:policy/AdministratorAccess

deploy: 
	yarn cdk deploy

.venv:
	$(VIRTUALENV) .venv
	.venv/bin/pip install --upgrade pip
	.venv/bin/pip install --upgrade setuptools
	.venv/bin/pip install --upgrade wheel
