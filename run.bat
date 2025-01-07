@echo off

REM Activate virtual environment
call ./venv/Scripts/activate.bat

REM Change to fungusnode directory
cd ./fungusnode

REM Run flwr command 100 times
for /l %%i in (1,1,10000000) do (
    echo Running iteration %%i
    flwr run .
)

echo All iterations complete
