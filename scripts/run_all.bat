@echo off
setlocal enabledelayedexpansion

REM Complete workflow script that chains together: run_all_tests -> run_example -> picgen
REM This script simply calls the other batch files in sequence

set SCRIPT_DIR=%~dp0
set PROJECT_ROOT=%SCRIPT_DIR%..

echo 🚀 Starting complete workflow...
echo ==================================

REM Step 0: Validate tests mapping rules
echo 🔎 Pre-check: Validating tests mapping rules...
pushd "%PROJECT_ROOT%"
python scripts\check_tests_mapping.py
if not %errorlevel%==0 (
    echo ❌ Test mapping validation failed. Aborting.
    popd
    exit /b 1
)
popd
echo ✅ Test mapping validation passed!

echo.

REM Step 1: Run all tests
echo 📋 Step 1: Running all tests...
echo ----------------------------------------
call "%SCRIPT_DIR%run_all_tests.bat"
echo ✅ All tests passed!

echo.

REM Step 2: Run example
echo 📋 Step 2: Running example...
echo ----------------------------------------
call "%SCRIPT_DIR%run_example.bat"
echo ✅ Example completed successfully!

echo.
