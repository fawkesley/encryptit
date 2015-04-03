.PHONY: test
test:
	nosetests -v
	./check-pep8.sh
	ack TODO && false

.PHONY: clean
clean:
	find . -iname '*.pyc' -delete
	rm -rf openpgp.egg-info
