@echo off
chcp 65001 >nul
echo 正在启动工控测试软件...
echo.

cd /d "%~dp0"
if exist "dist\工控测试软件.exe" (
    echo 找到可执行文件，正在启动...
    start "" "dist\工控测试软件.exe"
) else (
    echo 错误：未找到可执行文件！
    echo 请确保已经编译了项目。
    pause
) 