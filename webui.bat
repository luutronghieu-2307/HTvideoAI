@echo off
setlocal
cd /d "%~dp0"
title HTvideoAI WebUI Launcher

rem Kiểm tra Python
where python >nul 2>nul
if errorlevel 1 (
    where py >nul 2>nul
    if not errorlevel 1 (
        py start.py %*
        goto end
    )
    echo [HTvideoAI] Error: Khong tim thay Python! Vui long cai dat Python 3.11+ va tick vao "Add Python to PATH".
    pause
    exit /b 1
)

python start.py %*

:end
if errorlevel 1 (
    echo [HTvideoAI] Ung dung ket thuc voi ma loi.
    pause
)

