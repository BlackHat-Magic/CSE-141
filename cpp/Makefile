INCLUDE_DIR   =./include
SRC_DIR       =./src
OBJECTS_DIR   =./objects
BIN_DIR       =./bin
TEST_DIR      =./test_dir
RESULTS_FILE  =./RESULTS.txt

OBJS = ${OBJECTS_DIR}/first_plus.o \
       ${OBJECTS_DIR}/parser.o     \
       $(OBJECTS_DIR)/token.o      \
       $(OBJECTS_DIR)/scanner.o    \
       $(OBJECTS_DIR)/parse_main.o

ifeq ($(DEBUG),1)

  DEBUG_FLAGS = -DDEBUG

else

  DEBUG_FLAGS =

endif

CC=g++
CC_OPTS=-O3 -std=c++11 -I $(INCLUDE_DIR) $(DEBUG_FLAGS) -c

all : $(BIN_DIR) $(BIN_DIR)/parser

build : all

$(BIN_DIR)/parser : $(OBJS)
	$(CC) $^ -o $@

$(OBJECTS_DIR)/%.o : $(SRC_DIR)/%.cpp
	$(CC) $(CC_OPTS) $^ -o $@

$(BIN_DIR) :
	mkdir -p $@

clean :
	find . -name "*~" -print | xargs rm -f
	rm -f $(OBJECTS_DIR)/*
	rm -f $(BIN_DIR)/*

rebuild : clean all

test : all
	@passed=0; failed=0; \
	for f in $(TEST_DIR)/*.c; do \
		name=$$(basename "$$f"); \
		expected=$$(grep -A1 "^$${name}:" $(RESULTS_FILE) | tail -1 | sed 's/^[[:space:]]*//'); \
		actual=$$(./$(BIN_DIR)/parser "$$f" 2>&1); \
		if [ "$$expected" = "$$actual" ]; then \
			echo "PASS: $$name"; \
			passed=$$((passed+1)); \
		else \
			echo "FAIL: $$name"; \
			echo "  Expected: $$expected"; \
			echo "  Got:      $$actual"; \
			failed=$$((failed+1)); \
		fi; \
	done; \
	echo ""; \
	echo "Results: $$passed passed, $$failed failed"

test-clean : rebuild test

.PHONY : all build clean rebuild test test-clean
