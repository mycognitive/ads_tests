SHELL:=/bin/bash -O globstar
SELENIUM_HOST?=http://localhost
install:
	pip3 install -r requirements.pip
test:
	# Usage: make test SELENIUM_HOST=http://localhost VERBOSE=1
	python3 selenium/run_tests.py -h $(SELENIUM_HOST) selenium/tests/**/*.py
