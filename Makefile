# Fintech Enterprise Platform Makefile

.PHONY: all build run test clean docker-build docker-run stress verify

all: test run

install:
	@echo "Installing dependencies (using pure standard library)..."
	python -m pip --version

build:
	@echo "Building Fintech Enterprise Platform artifacts..."
	python -c "import compileall; compileall.compile_dir('.', force=True, quiet=1)"
	@echo "Build complete."

run:
	@echo "Starting Fintech Enterprise Platform server..."
	python main.py

start: run

test:
	@echo "Running test suite..."
	python -m unittest discover -s tests -v

stress:
	python cli.py stress --count 50

verify:
	python cli.py verify

docker-build:
	docker build -t fintech-enterprise-platform:latest .

docker-run:
	docker run -p 8080:8080 --name fintech_core fintech-enterprise-platform:latest

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
