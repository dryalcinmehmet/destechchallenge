SHELL=/bin/bash

ifneq (,$(findstring xterm,${TERM}))
	BLACK        := $(shell tput -Txterm setaf 0)
	RED          := $(shell tput -Txterm setaf 1)
	GREEN        := $(shell tput -Txterm setaf 2)
	YELLOW       := $(shell tput -Txterm setaf 3)
	LIGHTPURPLE  := $(shell tput -Txterm setaf 4)
	PURPLE       := $(shell tput -Txterm setaf 5)
	BLUE         := $(shell tput -Txterm setaf 6)
	WHITE        := $(shell tput -Txterm setaf 7)
	RESET := $(shell tput -Txterm sgr0)
else
	BLACK        := ""
	RED          := ""
	GREEN        := ""
	YELLOW       := ""
	LIGHTPURPLE  := ""
	PURPLE       := ""
	BLUE         := ""
	WHITE        := ""
	RESET        := ""
endif

# set target color
TARGET_COLOR := $(BLUE)

POUND = \#

.PHONY: no_targets__ info help build deploy doc
	no_targets__:

.DEFAULT_GOAL := help

help:
	@echo ""
	@echo "    ${GREEN}::::::::::::::::::::::::::::::::${RED}Destech Makefile Commands${RESET} ${GREEN}::::::::::::::::::::::::::::::::${RESET}"
	@echo ""
	@echo "   ${LIGHTPURPLE}Type the commands below into the terminal. You can find examples for each other.${LIGHTPURPLE}"
	@echo ""
	@echo "Examples:"
	@echo ""
	@echo "  ${PURPLE}|${PURPLE} down:  $(POUND)$(POUND) help for down"
	@echo "  ${YELLOW}| 	--> For stopping and removing development containers, networks and volumes.${YELLOW}"
	@echo "  |  >> ${GREEN}make down${GREEN}"
	@echo ""
	@echo ""
	@echo "  ${PURPLE}|${PURPLE} dev:  $(POUND)$(POUND) help for dev"
	@echo "  ${YELLOW}| 	--> For run development containers, networks and volumes.${YELLOW}"
	@echo "  |  >> ${GREEN}make dev${GREEN}"
	@echo ""
	@echo ""
	@echo "  ${PURPLE}|${PURPLE} prod:  $(POUND)$(POUND) help for prod"
	@echo "  ${YELLOW}| 	--> For run deelopment containers, networks and volumes.${YELLOW}"
	@echo "  |  >> ${GREEN}make prod${GREEN}"
	@echo ""
	@echo ""
	@echo "  ${PURPLE}|${PURPLE} release:  $(POUND)$(POUND) help for release"
	@echo "  ${YELLOW}| 	--> For bump version.${YELLOW}"
	@echo "  |  >> ${GREEN}make release${GREEN}"
	@echo ""
	@echo "  ${PURPLE}|${PURPLE} docker-compose-install:  $(POUND)$(POUND) help for install"
	@echo "  ${YELLOW}| 	--> For necessary docker-compose installing.${YELLOW}"
	@echo "  ${RED}|  >>${RED} ${GREEN}make docker-compose-install${GREEN}"
	@echo "${PURPLE}-----------------------------------------------------------------------------------------------------------------${RESET}"
	@grep -E '^[a-zA-Z_0-9%-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "${TARGET_COLOR}%-30s${RESET} ${PURPLE}%s\n${PURPLE}${RESET}", $$1, $$2}'
	@echo "${PURPLE}-----------------------------------------------------------------------------------------------------------------${RESET}"
	@echo "${RED}-----------------------------------------------------------------------------------------------------------------${RESET}"


.PHONY : docker-compose-install
docker-compose-install:  ## Installing docker compose.
	@echo "${GREEN}-----------------------------------------------------------------------------------------------------------------${RESET}"
	@echo "${PURPLE}--> Installing Docker Compose...${RESET}"
	@echo "${GREEN}-----------------------------------------------------------------------------------------------------------------${RESET}"
	sudo rm -rf /usr/local/bin/docker-compose | true
	sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(shell uname -s)-$(shell uname -m)" -o /usr/local/bin/docker-compose
	sudo chmod +x /usr/local/bin/docker-compose
	docker-compose --version


.PHONY : get-version
get-version:  ## Get latest version
	@echo "${PURPLE}$(shell cat '.env.dev' | grep API_VERSION)${RESET}"

.PHONY : down
down:  ## Docker down
	@echo "${PURPLE}Docker compose down!..."
	docker-compose -f docker-compose..prod.yml down -v
	docker-compose -f docker-compose.prod.yml down -v	

.PHONY : dev
dev:  ## Docker dev
	@echo "${PURPLE}Creating custom_net external...${RESET}"
	docker network create custom_net || echo "${PURPLE}custom_net already exist!${RESET}"

	@echo "${RED}Docker compose down!${RESET}"
	docker-compose -f docker-compose.yml down -v

	@echo "${YELLOW}Docker compose up!...${RESET}"
	COMPOSE_DOCKER_CLI_BUILD=1 DOCKER_BUILDKIT=1 docker-compose -f docker-compose.yml up --build

.PHONY : prod
prod:  ## Docker prod
	@echo "${PURPLE}Creating custom_net external...${RESET}"
	docker network create custom_net || echo "${PURPLE}custom_net already exist!${RESET}"

	@echo "${RED}Docker compose down!${RESET}"
	docker-compose -f docker-compose.prod.yml down

	@echo "${YELLOW}Docker compose up!...${RESET}"
	COMPOSE_DOCKER_CLI_BUILD=1 DOCKER_BUILDKIT=1  docker-compose -f docker-compose.prod.yml up --build -d

.PHONY : release
release: 
	@echo "${PURPLE}Release!${RESET}"
	@bash ./bump_version.sh;

.PHONY : mg
mg: ## makemigrations & migrate
	@echo "${PURPLE}Makemigrations!${RESET}"
	python3 manage.py makemigrations
	python3 manage.py migrate


.PHONY : static
static: ## Run static! 
	@echo "${PURPLE}Black, isort and pyclean!${RESET}"
	black .
	isort .
	$(shell find . -path "*/migrations/*.py" -not -name "__init__.py" -delete)
	$(shell find . -path "*/migrations/*.pyc" -delete)
	$(shell find . | grep -E "(__pycache__|\.pytest_cache|\.pyc|\.pyo$)" | xargs rm -rf)


.PHONY: prepair-postgres
prepair-postgres: ## Create database for local no docker.
	psql postgres -c "CREATE DATABASE destech;"
	CREATE USER testuser WITH PASSWORD 'testpass';
	ALTER ROLE testuser SET client_encoding TO 'utf8';
	ALTER ROLE testuser SET default_transaction_isolation TO 'read committed';
	ALTER ROLE testuser SET timezone TO 'UTC';
	GRANT ALL PRIVILEGES ON DATABASE destech TO testuser;
