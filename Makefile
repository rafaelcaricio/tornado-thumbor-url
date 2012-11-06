all: test

test:
	@nosetests tests/ --with-coverage --cover-package tornado_thumbor_url

requirements:
	@pip install -r requirements.txt
