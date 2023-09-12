.PHONY: clean help push release lint test
.DEFAULT_GOAL := help

define BROWSER_PYSCRIPT
import os, webbrowser, sys
from urllib.request import pathname2url
webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT


BROWSER := python -c "$$BROWSER_PYSCRIPT"
PROJECTNAME = QStyler
help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean: clean-build ## remove all build, test, coverage and Python artifacts

clean-build: ## remove build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf .eggs/
	rm -rf *.egg-info
	rm -rf *.egg
	rm -rf **/__pycache__
	rm -rf htmlcov/
	rm -rf .tox/
	rm -rf .pytest_cache
	rm -f **.pyo
	rm -f **.pyc
	rm -f .coverage
	rm -f corbertura.xml
	rm -f coverage.xml

install: ## install packages
	pip install --upgrade --no-cache --force-reinstall torrentfileQt QStyler

test: clean ## run tests quickly with the default Python
	tox

push: clean test ## push to repo
	git commit -a -m "$m"
	git push

release: test clean ## package and upload a release
	py -m build .
	twine upload dist/*

executable: test clean
	pyinstaller runner.spec
