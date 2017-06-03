all: dev

export IMAGE = mybot
export MOUNT_FROM = /Users/bdrozhak/repos
export MOUNT_TO   = /repos

ifeq ($(OS),Windows_NT)
winpty = winpty
endif 

docker_run = $(winpty) docker run --rm \
    -v $(MOUNT_FROM):$(MOUNT_TO)       \
	-v ~/.aws:/root/.aws -it           \
	-e MOUNT_TO='$(MOUNT_TO)'          \
	-e TELEBOT_CONFIG="$$(cat ~/.telebot)" $(IMAGE)

build:
	docker build -t $(IMAGE) .

run: build
	$(docker_run)

in: build
	$(docker_run) /bin/bash

# temp. set up venv by yourself
checkenv:
	@which virtualenv
	[ -d "./venv" ]
	[ -f "./venv/bin/activate" ]
	[ -f "./venv/lib/python3.6/site-packages/toml.py" ]
	[ -d "./venv/lib/python3.6/site-packages/telebot" ]
	@which python3.6

local: checkenv
	source ./venv/bin/activate     ;\
	python3.6 ./src/bot.py