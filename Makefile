
DOCKER_IMAGE_NAME = unhelpful-slack-bot
VENV_FILE=.venv
WHICH_PYTHON=$(VENV_FILE)/bin/python
WHICH_PIP=$(VENV_FILE)/bin/pip

BLACK_ARGS=-l 100 .
.PHONY: clean
clean:
	-@rm default.env
	-@rm build
	-@find . -type d -maxdepth 3 -name ".eggs" -print0 | xargs -0 rm -rv
	-@find . -type d -maxdepth 3 -name ".tox" -print0 | xargs -0 rm -rv
	-@find . -type d -maxdepth 3 -name "__pycache__" -print0 | xargs -0 rm -rv
	-@find . -type d -maxdepth 3 -name "*egg-info" -print0 | xargs -0 rm -rv
	-@find . -type d -maxdepth 3 -name "test-results" -print0 | xargs -0 rm -rv
	-@find . -type d -maxdepth 3 -name "dist" -print0 | xargs -0 rm -rv

$(VENV_FILE): setup.py 
	@virtualenv $(VENV_FILE) -p python3
	@touch $@
$(VENV_FILE)/bin/wheel: $(VENV_FILE)
	@$(WHICH_PIP) install wheel
$(VENV_FILE)/bin/black: $(VENV_FILE)
	@$(WHICH_PIP) install black
$(VENV_FILE)/bin/twine: $(VENV_FILE)
	@$(WHICH_PIP) install twine
$(VENV_FILE)/bin/sphinx: $(VENV_FILE)
	@$(WHICH_PIP) install sphinx
$(VENV_FILE)/bin/tox: $(VENV_FILE)
	@$(WHICH_PIP) install tox

install: $(VENV_FILE) setup.py
	@$(WHICH_PIP) install -e .
	@touch $@

.PHONY: test
test: $(VENV_FILE)/bin/tox
	@tox ${TOX_ARGS}

.PHONY: black
black: $(VENV_FILE)/bin/black
	@black -S $(BLACK_ARGS)

default.env: dev.env
	@cp dev.env default.env

dev.env: 
	@cp template.env dev.env

build: Dockerfile requirements.txt VERSION
	@docker build \
		-t ${WILL_IMAGE_NAME} \
		-f Dockerfile \
		--no-cache \
		.
	@touch $@

## vv required? vv ##
.PHONY: auth
auth: dev.env
	-@rm default.env
	@cm dev.env default.env
## ^^ required? ^^ ##

.PHONY: run
run: build default.env
	@docker run --rm \
		--volume `pwd`:/opt/will \
		${WILL_IMAGE_NAME} \
		launch-unhelpful

.PHONY: debug
debug: build default.env
	@docker run --rm -it \
		--volume `pwd`:/opt/will \
		${WILL_IMAGE_NAME} \
		/bin/sh