.PHONY: all

all: test

test:
	PYTHONPATH=. pytest
