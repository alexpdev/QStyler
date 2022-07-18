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
	rm -vfr build/
	rm -vfr dist/
	rm -vfr .eggs/
	rm -vfr *.egg-info
	rm -vfr *.egg
	rm -vf **.pyc
	rm -vf **.pyo
	rm -fvr **/__pycache__
	rm -fvr .tox/
	rm -fv .coverage
	rm -frv htmlcov/
	rm -frv .pytest_cache
	rm -fv corbertura.xml
	rm -fv coverage.xml

test: ## run tests quickly with the default Python
	tox

push: clean test ## push to repo
	git commit -a -m "$m"
	git push

release: test clean ## package and upload a release
	py -m build .
	twine upload dist/*
