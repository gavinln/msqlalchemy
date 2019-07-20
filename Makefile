# Using Makefiles in Python
# https://krzysztofzuraw.com/blog/2016/makefiles-in-python-projects.html
#
# Listing targets in the Makefile
# http://stackoverflow.com/questions/4219255/how-do-you-get-the-list-of-targets-in-a-makefile

SHELL='c:/Program Files/Git/usr/bin/sh.exe'

.PHONY: list
list:
	@$(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '{if ($$1 !~ "^[#.]") {print $$1}}'

quickstart-run:
	pipenv run python quickstart/mlflow_tracking.py

run:
	@python python/msqlalchemy.py

pylint:
	pylint --rcfile .pylint.rc python/*.py

yapf:
	yapf -i python/*.py

flake8:
	flake8 python/*

mypy:
	@mypy --follow-imports=skip --ignore-missing-imports python

clean:
	echo 'not implemented'
