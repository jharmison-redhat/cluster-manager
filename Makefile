.PHONY : build _build_app publish publish_dev clean clean_container clean_app_image run join start stop devel _devel_run release _build_ui _publish_ui _publish_ui_dev run_ui join_ui start_ui stop_ui devel_ui _devel_ui_run

IMAGE=cluster-manager
UI_IMAGE=config-ui
VERS=$(shell cat version.txt)
VERS_PARTIAL=$(shell awk -F. '{ print $$1"."$$2; }' version.txt)
NAME=$(IMAGE)_dev
UI_NAME=$(UI_IMAGE)_dev
DEVDIR=$(shell pwd)
UPSTREAM=$(shell cat upstream.txt)

build: clean_container _build_app _build_ui
_build_app:
	podman build -t $(UPSTREAM)/$(IMAGE):dev .
_build_ui:
	podman build -t $(UPSTREAM)/$(UI_IMAGE):dev config

clean: clean_container clean_app_image
clean_container:
	podman container rm "$(NAME)" || :
	podman container rm "$(UI_NAME)" || :
clean_app_image:
	podman image rm -f $(UPSTREAM)/$(IMAGE):dev || :
	podman image rm -f $(UPSTREAM)/$(UI_IMAGE):dev || :

release:
	TMPFILE=/tmp/release-message-v$(VERS)-$$(cat /dev/urandom | head -c 32 | tr -dc _A-Z-a-z-0-9); \
	vim $$TMPFILE; \
	MSG=$$(cat $$TMPFILE | awk '{printf "%s\\n", $$0}'); \
	rm $$TMPFILE; \
	echo "{\"tag_name\": \"v$(VERS)\", \"target_commitish\": \"master\", \"name\": \"v$(VERS)\", \"body\": \"$$MSG\", \"draft\": false, \"prerelease\": false}"; \
	echo "{\"tag_name\": \"v$(VERS)\", \"target_commitish\": \"master\", \"name\": \"v$(VERS)\", \"body\": \"$$MSG\", \"draft\": false, \"prerelease\": false}" | gh api https://api.github.com/repos/:owner/:repo/releases -X POST --input /dev/stdin

publish: _publish_ui
	podman image tag $(UPSTREAM)/$(IMAGE):dev $(UPSTREAM)/$(IMAGE):$(VERS)
	podman image tag $(UPSTREAM)/$(IMAGE):dev $(UPSTREAM)/$(IMAGE):$(VERS_PARTIAL)
	podman image tag $(UPSTREAM)/$(IMAGE):dev $(UPSTREAM)/$(IMAGE):latest
	podman push $(UPSTREAM)/$(IMAGE):$(VERS)
	podman push $(UPSTREAM)/$(IMAGE):$(VERS_PARTIAL)
	podman push $(UPSTREAM)/$(IMAGE):latest

_publish_ui:
	podman image tag $(UPSTREAM)/$(UI_IMAGE):dev $(UPSTREAM)/$(UI_IMAGE):$(VERS)
	podman image tag $(UPSTREAM)/$(UI_IMAGE):dev $(UPSTREAM)/$(UI_IMAGE):$(VERS_PARTIAL)
	podman image tag $(UPSTREAM)/$(UI_IMAGE):dev $(UPSTREAM)/$(UI_IMAGE):latest
	podman push $(UPSTREAM)/$(UI_IMAGE):$(VERS)
	podman push $(UPSTREAM)/$(UI_IMAGE):$(VERS_PARTIAL)
	podman push $(UPSTREAM)/$(UI_IMAGE):latest

publish_dev: _publish_ui_dev
	podman push $(UPSTREAM)/$(IMAGE):dev

_publish_ui_dev:
	podman push $(UPSTREAM)/$(UI_IMAGE):dev

run:
	podman run --name "$(NAME)" -it $(UPSTREAM)/$(IMAGE):dev || podman start -ia "$(NAME)"
run_ui:
	podman run --name "$(UI_NAME)" -it $(UPSTREAM)/$(UI_IMAGE):dev || podman start -ia "$(UI_NAME)"

join:
	podman exec -it "$(NAME)" /bin/bash
join_ui:
	podman exec -it "$(UI_NAME)" /bin/bash

start:
	podman start -ia "$(NAME)"
start_ui:
	podman start -ia "$(UI_NAME)"

stop:
	podman stop "$(NAME)"
stop_ui:
	podman stop "$(UI_NAME)"

devel: clean_container _devel_run
devel_ui: clean_container _devel_ui_run

_devel_run:
	podman run --name "$(NAME)" \
		--env-file ./devel.env \
		-v $(DEVDIR)/app:/app:Z -v $(DEVDIR)/data:/data:Z \
		-it $(UPSTREAM)/$(IMAGE):dev \
		/bin/bash
_devel_ui_run:
	podman build --build-arg DEVEL=true -t $(UPSTREAM)/$(UI_IMAGE):dev config
	podman run --name "$(UI_NAME)" \
		--env-file ./devel.env \
		-p 5000:5000 \
		-v $(DEVDIR)/config/faros_config_ui:/app:Z -v $(DEVDIR)/data:/data:Z \
		-it $(UPSTREAM)/$(UI_IMAGE):dev
