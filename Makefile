# Makefile for Django-sekh
#
# Aim to simplify development and release process
# Be sure you have run the buildout, before using this Makefile

NO_COLOR	= \033[0m
COLOR	 	= \033[32;01m
SUCCESS_COLOR	= \033[35;01m

all: kwalitee clean package

package:
	@echo "$(COLOR)* Creating source package for Django-SEKH$(NO_COLOR)"
	@python setup.py sdist

test:
	@echo "$(COLOR)* Launching the tests suite$(NO_COLOR)"
	@./bin/test

kwalitee:
	@echo "$(COLOR)* Running pyflakes$(NO_COLOR)"
	@./bin/pyflakes sekh
	@echo "$(COLOR)* Running pep8$(NO_COLOR)"
	@./bin/pep8 --count --show-source --show-pep8 --statistics sekh
	@echo "$(SUCCESS_COLOR)* No kwalitee errors, Congratulations ! :)$(NO_COLOR)"

2to3:
	@echo "$(COLOR)* Checking Py3 code$(NO_COLOR)"
	@2to3 sekh/

clean:
	@echo "$(COLOR)* Removing useless files$(NO_COLOR)"
	@find sekh -type f \( -name "*.pyc" -o -name "\#*" -o -name "*~" \) -exec rm -f {} \;
	@rm -f \#* *~

