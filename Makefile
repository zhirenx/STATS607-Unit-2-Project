PYTHON ?= python3
.PHONY: all simulate analyze figures clean test
all: figures
simulate:
	$(PYTHON) -m src.simulation
analyze: simulate
	$(PYTHON) -m src.analyze
figures: analyze
	$(PYTHON) -m src.figures
test:
	$(PYTHON) -m unittest discover -s tests -v
clean:
	rm -f results/raw/*.csv results/raw/*.json results/figures/*.png results/figures/*.pdf
