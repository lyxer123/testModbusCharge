# 测试工控测试软件exe文件
Write-Host "测试工控测试软件exe文件..." -ForegroundColor Green
Write-Host ""

# 检查exe文件是否存在
if (Test-Path "dist\工控测试软件.exe") {
    $fileInfo = Get-ChildItem "dist\工控测试软件.exe"
    Write-Host "找到exe文件：" -ForegroundColor Yellow
    Write-Host "  文件名: $($fileInfo.Name)" -ForegroundColor White
    Write-Host "  文件大小: $([math]::Round($fileInfo.Length / 1MB, 2)) MB" -ForegroundColor White
    Write-Host "  修改时间: $($fileInfo.LastWriteTime)" -ForegroundColor White
    Write-Host ""
    
    Write-Host "尝试启动程序..." -ForegroundColor Yellow
    Write-Host "程序将在后台启动，请检查是否出现GUI窗口" -ForegroundColor Cyan
    
    # 启动程序
    Start-Process -FilePath "dist\工控测试软件.exe" -WindowStyle Normal
    
    Write-Host "程序已启动！" -ForegroundColor Green
    Write-Host "如果看到GUI窗口，说明编译成功。" -ForegroundColor Cyan
    
} else {
    Write-Host "错误：未找到exe文件！" -ForegroundColor Red
    Write-Host "请确保已经编译了项目。" -ForegroundColor Red
}

Write-Host ""
Write-Host "按任意键继续..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown") 