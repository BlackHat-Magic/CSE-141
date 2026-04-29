PYTHON := python3

.PHONY: all test dump-ir run-ir trace-ir clean

all: test

test:
	$(PYTHON) run_tests.py

dump-ir:
	$(PYTHON) main.py --dump-ir

run-ir:
	$(PYTHON) main.py --run-ir

trace-ir:
	$(PYTHON) main.py --trace-ir

clean:

test-clean: test
