#!/bin/bash
# Script to run pytest in the Docker container
docker-compose -f infra/docker-compose.yml exec api pytest "$@"
