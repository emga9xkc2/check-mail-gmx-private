@taskkill /IM "chromedriver.exe" /F
@rmdir /s /q "%appdata%\myscript"
@rmdir /s /q "%appdata%\nightowl\myscript"
@rmdir /s /q "%temp%\gen_py"
python -c "import sys; exit(0) if sys.version_info[:3] == (3, 9, 9) else exit(1)"
IF "%ERRORLEVEL%"=="0" (
    pip install -r requirements.txt
)
powershell.exe -executionpolicy ByPass -File python.ps1
IF "%ERRORLEVEL%"=="0" (
    @py ../main.pyc
)
@timeout /t 100
