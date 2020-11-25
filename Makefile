SHELL := /bin/bash
# Signifies our desired python version
# Makefile macros (or variables) are defined a little bit differently than traditional bash, keep in mind that in the Makefile there's top-level Makefile-only syntax, and everything else is bash script syntax.
PYTHON = pipenv run python

# .PHONY defines parts of the makefile that are not dependant on any specific file
# This is most often used to store functions
.PHONY = help test build quickbuild deploy destroy clean synth

# Defining an array variable
FILES = input output

# Defines the default target that `make` will to try to make, or in the case of a phony target, execute the specified commands
# This target is executed whenever we just type `make`
.DEFAULT_GOAL = help

# The @ makes sure that the command itself isn't echoed in the terminal
help:
	@echo "---------------HELP-----------------"
	@echo "To test the project type make test"
	@echo "To package the python project for deployment type make build"
	@echo "To update the packaged python project for deployment type make quickbuild (doesn't run pip install)"
	@echo "To deploy to AWS type make deploy"
	@echo "To delete the stack on cloudformation type make destroy"
	@echo "To clean the build directory type make clean"
	@echo "To generate the cloudformation yaml type make synth"
	@echo "------------------------------------"


# The ${} notation is specific to the make syntax and is very similar to bash's $()
# This function uses pytest to test our source files
test:
	${PYTHON} -m pytest tests

build:
	pipenv run pip install -r <(pipenv lock -r) --target _build
	cp -R functions _build
	${PYTHON} -m zipdir _build

quickbuild:
	cp -R functions _build
	${PYTHON} -m zipdir _build

deploy:
	# set your profile as AWS_PROFILE in your shell. (Or use direnv .envrc to set it per project)
	cdk deploy --profile ${AWS_PROFILE}

destroy:
	# set your profile as AWS_PROFILE in your shell. (Or use direnv .envrc to set it per project)
	cdk destroy --profile ${AWS_PROFILE}
synth:
	cdk synth > template.yml

# In this context, the *.project pattern means "anything that has the .project extension"
clean:
	rm -r _build