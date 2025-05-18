@echo off
:: Test script for Squad2-FastAPI backend
echo Running tests for Squad2-FastAPI backend...
echo.

:: Environment setup
set SCRIPT_DIR=%~dp0
cd %SCRIPT_DIR%

:: Make sure we have the latest test files in the container
echo Copying test files to container...
docker cp tests infra-api-1:/app/
docker cp pytest.ini infra-api-1:/app/
echo.

:: Run all tests in tests directory
echo Running tests...
docker exec infra-api-1 python -m pytest /app/tests -v
if %ERRORLEVEL% neq 0 (
  echo.
  echo Tests FAILED!
  exit /b 1
) else (
  echo.
  echo All tests PASSED!
)
