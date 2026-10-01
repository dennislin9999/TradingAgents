# 一鍵執行 TradingAgents：首次會自動建立環境，之後直接啟動。
# 用法：在專案根目錄執行  .\run.ps1
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

$venvPython = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"
$exe = Join-Path $PSScriptRoot ".venv\Scripts\tradingagents.exe"

# 1. 檢查 .env
if (-not (Test-Path ".env")) {
    if (Test-Path ".env.example") {
        Copy-Item ".env.example" ".env"
    } else {
        New-Item ".env" -ItemType File | Out-Null
    }
    Write-Host "已建立 .env，請填入 OPENAI_API_KEY 後存檔，再重新執行 .\run.ps1" -ForegroundColor Yellow
    notepad .env
    exit 0
}

# 2. 建立虛擬環境並安裝（僅首次）
if (-not (Test-Path $exe)) {
    if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
        Write-Host "找不到 uv，請先安裝：https://docs.astral.sh/uv/ （或 scoop install uv）" -ForegroundColor Red
        exit 1
    }
    Write-Host "首次執行，建立環境並安裝套件（需數分鐘）..." -ForegroundColor Cyan
    if (-not (Test-Path $venvPython)) { uv venv .venv }
    uv pip install --python $venvPython -e .
}

# 3. 啟動
& $exe @args
