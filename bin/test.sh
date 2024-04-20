#!/usr/bin/env sh

# install pytest-cov for tests
docker-compose -f docker-compose.yml exec sentry-log pip install pytest-cov
# run tests
docker-compose -f docker-compose.yml exec sentry-log /usr/local/bin/pytest -vv --cov=/usr/src/app /usr/src/app/