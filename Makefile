.PHONY: test
test:
	nosetests -v
	./check-pep8.sh
	./check-todo.sh

.PHONY: clean
clean:
	find . -iname '*.pyc' -delete
	rm -rf openpgp.egg-info

.PHONY: upversion
upversion:
	./script/upversion.sh

.PHONY: upload
upload:
	./script/upload.sh
