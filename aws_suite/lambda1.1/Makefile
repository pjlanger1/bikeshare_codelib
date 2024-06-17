FUNCTION_NAME=lambda_function
VENV=venv
PYTHON_VERSION=python3.8
PACKAGE=$(FUNCTION_NAME).zip

venv:
	$(PYTHON_VERSION) -m venv $(VENV)
	$(VENV)/bin/pip install -r requirements.txt

package: venv
	cd $(VENV)/lib/$(PYTHON_VERSION)/site-packages && zip -r9 $(CURDIR)/$(PACKAGE) .
	cd $(CURDIR) && zip -g $(PACKAGE) $(FUNCTION_NAME).py

clean:
	rm -rf $(VENV)
	rm -f $(PACKAGE)
