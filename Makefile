.PHONY: test
test: clean
	coverage run --source=encryptit setup.py test
	./script/check-pep8.sh
	./script/check-todo.sh

.PHONY: clean
clean:
	find . -iname '*.pyc' -delete
	find . -name __pycache__ -type d -delete
	rm -rf openpgp.egg-info
	rm -rf dist/ MANIFEST
	rm -f .coverage

.PHONY: upversion
upversion:
	./script/upversion.sh

.PHONY: upload
upload:
	./script/upload.sh
