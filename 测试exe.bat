@echo off
echo 测试工控测试软件exe文件...
echo.

cd /d "%~dp0"
if exist "dist\工控测试软件.exe" (
    echo 找到exe文件，文件大小：
    dir "dist\工控测试软件.exe" | findstr "工控测试软件.exe"
    echo.
    echo 尝试启动程序（5秒后自动关闭）...
    timeout /t 5 /nobreak >nul
    start /wait "工控测试软件" "dist\工控测试软件.exe"
    echo 程序已退出
) else (
    echo 错误：未找到exe文件！
)
pause 