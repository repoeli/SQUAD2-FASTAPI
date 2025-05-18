@echo off
REM Script to run pytest in the Docker container
docker exec -it infra-api-1 sh -c "cd /app && python -m pytest %*"
