TEST_DIR   :=./test
PYTHON     :=python3

.PHONY: all test test-clean clean

all: test

test:
	@passed=0; failed=0; \
	for expected in $(TEST_DIR)/*-out.txt; do \
		name=`basename "$$expected" -out.txt`; \
		actual=`$(PYTHON) gee.py "$(TEST_DIR)/$${name}.gee" 2>/dev/null`; \
		if [ "$$actual" = "`cat "$$expected"`" ]; then \
			echo "PASS: $$name"; \
			passed=$$((passed+1)); \
		else \
			echo "FAIL: $$name"; \
			failed=$$((failed+1)); \
		fi; \
	done; \
	echo ""; \
	echo "Results: $$passed passed, $$failed failed"

test-clean: test

clean:
