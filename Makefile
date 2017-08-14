info:
	@python --version
	@pyenv --version
	@pip --version

clean:
	rm -fr build
	rm -fr dist
	find . -name '*.pyc' -exec rm -f {} \;
	find . -name '*.pyo' -exec rm -f {} \;
	find . -name '*~' ! -name '*.un~' -exec rm -f {} \;

lint:
	pre-commit run -a

test:
	pytest --cov
	coverage html

install:
	pip install -Ur requirements/testing.txt

build: clean
	python setup.py sdist
	python setup.py bdist_wheel

distribute: build
	twine upload dist/* -r pypi

ci: clean info test
	codecov
