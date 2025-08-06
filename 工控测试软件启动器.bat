@echo off
chcp 65001 >nul
title 工控测试软件启动器

:menu
cls
echo ========================================
echo        工控测试软件启动器
echo ========================================
echo.
echo 请选择运行模式：
echo.
echo 1. 测试模式 - 检查exe文件并测试运行（5秒后自动关闭）
echo 2. 正常运行 - 直接启动工控测试软件
echo 3. 退出
echo.
set /p choice=请输入选择 (1-3): 

if "%choice%"=="1" goto test_mode
if "%choice%"=="2" goto normal_mode
if "%choice%"=="3" goto exit
echo 无效选择，请重新输入...
timeout /t 2 /nobreak >nul
goto menu

:test_mode
cls
echo ========================================
echo           测试模式
echo ========================================
echo.
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
    echo 请确保已经编译了项目。
)
echo.
pause
goto menu

:normal_mode
cls
echo ========================================
echo           正常运行模式
echo ========================================
echo.
echo 正在启动工控测试软件...
echo.

cd /d "%~dp0"
if exist "dist\工控测试软件.exe" (
    echo 找到可执行文件，正在启动...
    start "" "dist\工控测试软件.exe"
    echo 程序已启动
) else (
    echo 错误：未找到可执行文件！
    echo 请确保已经编译了项目。
    pause
)
echo.
pause
goto menu

:exit
echo 正在退出...
exit 