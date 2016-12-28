test:
	python3 -m unittest discover

default:
	python3 euler_runner.py input.in

.PHONY: all test default