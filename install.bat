@echo off
setlocal

set "APP_NAME=FileOrg"
set "APP_DIR=%USERPROFILE%\%APP_NAME%"
set "EXE_NAME=FileOrg.exe"
set "SOURCE_EXE=%~dp0%EXE_NAME%"
set "TARGET_EXE=%APP_DIR%\%EXE_NAME%"
set "SOURCE_CONFIG=%~dp0dirs.txt"
set "TARGET_CONFIG=%APP_DIR%\dirs.txt"

echo.
echo ========================================
echo   Installing %APP_NAME%
echo ========================================
echo.

if not exist "%SOURCE_EXE%" (
    echo ERROR: %EXE_NAME% not found.
    echo Put install.bat and %EXE_NAME% in the same folder.
    pause
    exit /b 1
)

echo Creating application directory:
echo %APP_DIR%

if not exist "%APP_DIR%" (
    mkdir "%APP_DIR%"
)

echo.
echo Copying application...

copy /Y "%SOURCE_EXE%" "%TARGET_EXE%" >nul
copy /Y "%SOURCE_CONFIG%" "%TARGET_CONFIG%" >nul

if errorlevel 1 (
    echo ERROR: Failed to copy application.
    pause
    exit /b 1
)

echo Application copied successfully.

echo.
echo Setting application to Startup
powershell -NoProfile -Command "$s=(New-Object -ComObject WScript.Shell).CreateShortcut('%USERPROFILE%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\%APP_NAME%.lnk');$s.TargetPath='%TARGET_EXE% ';$s.Save()"

if errorlevel 1 (
    echo ERROR: Failed to set application startup.
    pause
    exit /b 1
)

echo Set application startup successfully.

echo.
echo ========================================
echo   Installation completed
echo ========================================
echo.
echo Application:
echo   %TARGET_EXE%
echo.
echo It will start automatically when you log in.
echo.

pause
endlocal