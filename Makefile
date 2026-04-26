PYTHON=conda run -n fruit python

.PHONY: build-data run test

build-data:
	$(PYTHON) scripts/build_taiwan_thesis_dataset.py

run:
	$(PYTHON) main.py

test:
	$(PYTHON) -m unittest discover -s tests
