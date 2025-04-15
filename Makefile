.PHONY: install
install:
	@ pip install -r requirements/base.txt

.PHONY: run
run:
	@ uvicorn src.main:app --reload

.PHONY: test
test:
	@ pytest tests/

.PHONY: lint
lint:
	@ flake8 src/ tests/ services/

.PHONY: clean
clean:
	@ find . -type d -name "__pycache__" -exec rm -r {} +
	@ find . -type d -name ".pytest_cache" -exec rm -r {} +
