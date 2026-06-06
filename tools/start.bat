@echo off
REM Chuyển vào thư mục chứa script
cd /d "%~dp0"

REM Kiểm tra python
python --version >nul 2>&1
if errorlevel 1 (
    echo Python chưa được cài đặt! Vui lòng cài Python từ https://python.org
    pause
    exit /b 1
)

REM Tạo virtual environment nếu chưa có
if not exist "venv" (
    echo Tạo virtual environment...
    python -m venv venv
)

REM Kích hoạt venv
call venv\Scripts\activate.bat

REM Cài đặt Flask
pip list | findstr Flask >nul 2>&1
if errorlevel 1 (
    echo Cài đặt Flask...
    pip install Flask -q
)

echo.
echo ====================================================
echo Đang khởi động Quản lý bài viết Việt Hoá Game
echo ====================================================
echo.
echo Trình duyệt sẽ tự mở http://localhost:5000
echo Nhấn Ctrl+C trong terminal để dừng server
echo.
timeout /t 2

REM Mở trình duyệt và chạy Flask (ẩn console)
echo Đang chạy ngầm...
start http://localhost:5000
start /b venv\Scripts\pythonw.exe app.py
exit