@echo off
REM Script to run pytest directly in the container
docker exec infra-api-1 python -m pytest tests/test_health.py -v
