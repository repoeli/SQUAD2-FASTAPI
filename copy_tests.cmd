@echo off
REM This script copies the tests and pytest.ini into the running Docker container
docker cp c:\Squad2-FastAPI\tests infra-api-1:/app/
docker cp c:\Squad2-FastAPI\pytest.ini infra-api-1:/app/
echo Tests and pytest.ini copied to container
