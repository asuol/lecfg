docs:
	sphinx-apidoc -f -o docs/source/ lecfg/
	make -C docs/ html

.PHONY: docs
