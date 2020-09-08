SHELL:=/bin/bash

FUNCTION_DIR = lib/todo-api

.DEFAULT_GOAL := lint
.PHONY: bootstrap

install:
	# Install CDK dependencies
	yarn install --frozen-lockfile
	# Install Python dependencies


build:
	yarn build