.PHONY: test
test: clean
	python setup.py test
	./check-pep8.sh
	./check-todo.sh

.PHONY: clean
clean:
	find . -iname '*.pyc' -delete
	find . -name __pycache__ -type d -delete
	rm -rf openpgp.egg-info
	rm -rf dist/ MANIFEST

.PHONY: upversion
upversion:
	./script/upversion.sh

.PHONY: upload
upload:
	./script/upload.sh
