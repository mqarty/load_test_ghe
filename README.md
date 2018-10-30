# load_test_ghe
Populate GHE with repos

##

Update docker-compose.yml with;

- GITHUB_PROTOCOL=https
- GITHUB_HOSTNAME=<github.com>
- GITHUB_USER_OR_ORG_NAME=
- GITHUB_USERNAME=
- GITHUB_TOKEN=
- NUMBER_OF_REPOS=1
- FILENAME=try-num-times.txt

## Run
1. docker-compose up -d
2. docker-compose run load_test

or, `docker-compose up -d && docker-compose run load_test`
