@echo off
REM Chuyển vào thư mục chứa script
cd /d "%~dp0"

REM Kiểm tra python
python --version >nul 2>&1
if errorlevel 1 (
    echo Python chưa được cài đặt! Vui lòng cài Python trước.
    pause
    exit /b 1
)

REM Cài đặt requirements (chỉ cần cài Flask 1 lần)
if not exist "venv" (
    echo Tạo virtual environment...
    python -m venv venv
)
call venv\Scripts\activate.bat

REM Kiểm tra Flask
pip list | findstr Flask >nul 2>&1
if errorlevel 1 (
    echo Cài đặt Flask...
    pip install Flask
)

echo Đang khởi động quản lý bài viết...
start http://localhost:5000
python app.py

pause