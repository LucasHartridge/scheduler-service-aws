include .env

.PHONY: create build deploy-lambda-local up stop down reboot setup

create: down build

build: deploy-lambda-local
	@docker-compose up --build

deploy-lambda-local:
	. $(VIRTUAL_ENV_PATH)/bin/activate
	rm -rf lambda-local/deploy && mkdir -p lambda-local/deploy;
	cp -r ./$(VIRTUAL_ENV_PATH)/lib/python3.8/site-packages/* lambda-local/deploy/;
	cp -r ./app lambda-local/deploy/;
	cp ./handler.py lambda-local/deploy/;

up:
	@docker-compose up 

stop:
	@docker-compose stop 

down:
	@docker-compose down --volumes
	@rm -rf localstack_tmp 

reboot: down up

setup:
	mkdir localstack_tmp
	make build