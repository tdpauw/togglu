all: init test
.PHONY: all

init:
	pip install -r requirements.txt

test:
	python -m unittest -v


