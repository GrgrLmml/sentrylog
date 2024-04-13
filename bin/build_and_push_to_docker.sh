#!/usr/bin/env bash
. .env
docker login -u $DOCKER_USER -p $DOCKER_HUB_TOKEN
docker buildx create --name mybuilder --use
docker buildx inspect --bootstrap
docker buildx build --platform linux/amd64,linux/arm64 -t grgrlmml/sentrylog:$VERSION -t grgrlmml/sentrylog:latest --push .

