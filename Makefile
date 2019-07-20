
WILL_IMAGE_NAME = unhelpful-will-bot

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
		python3 /opt/will/run_will.py

.PHONY: debug
debug: build default.env
	@docker run --rm -it \
		--volume `pwd`:/opt/will \
		${WILL_IMAGE_NAME} \
		/bin/sh