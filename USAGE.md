# TradingAgents 操作說明

## 一、第一次使用（新機器）

### 1. 事前準備

- 安裝 Git
- 安裝 `uv`（Python 套件管理工具）：`winget install astral-sh.uv` 或 `scoop install uv`
- 準備好 OpenAI API Key

### 2. 取得程式碼

```powershell
git clone <你的 repo 網址>
cd TradingAgents
```

### 3. 允許執行腳本（只需一次）

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

### 4. 第一次執行

```powershell
.\run.ps1
```

腳本會自動：

1. 建立 `.env`（複製自 `.env.example`）並開啟記事本。
2. 你在記事本填入金鑰後存檔，關閉。
3. 再執行一次 `.\run.ps1`，會自動建立 `.venv` 並安裝套件（約數分鐘）。
4. 安裝完成後自動啟動 CLI。

`.env` 最少需要：

```
OPENAI_API_KEY=你的金鑰
```

報告語言預設已是繁體中文，不用另外設定。

## 二、日常使用

```powershell
.\run.ps1
```

## 三、CLI 操作步驟

依畫面提示依序選擇：

| 步驟 | 內容 | 建議 |
|------|------|------|
| 1 | 股票代號 | 例如 `INTC`、`SPY`、`0700.HK`、`BTC-USD` |
| 2 | 分析日期 | 按 Enter 使用今天 |
| 3 | 輸出語言 | 已由 `.env`／預設決定，會自動略過 |
| 4 | 分析師團隊 | 預設全選：market、social、news、fundamentals |
| 5 | 研究深度 | Shallow 最快最省；Deep 較完整但耗時、耗費用 |
| 6 | LLM 供應商 | 選 OpenAI |
| 7 | 模型 | 快思模型與深思模型各選一個 |
| 8 | 推理強度 | Medium 為預設 |

分析完成後會問 **Save report?**，**務必按 Enter 或輸入 `Y`**。按 Ctrl+C 或中止則報告不會存檔。

## 四、報告在哪裡

```
output\<股票代號>_<時間戳記>\
```

資料夾內有 `READING_GUIDE.md`，說明各檔案的閱讀順序。建議先看：

1. `READING_GUIDE.md`
2. `5_portfolio\decision.md`（最終決策）
3. `complete_report.md`（完整報告）

## 五、常見問題

| 問題 | 處理方式 |
|------|----------|
| 無法執行 `.ps1` | 執行第一章第 3 步的 `Set-ExecutionPolicy` |
| 找不到 `uv` | 依第一章第 1 步安裝 `uv`，重開終端機 |
| API 金鑰錯誤 | 檢查 `.env` 的 `OPENAI_API_KEY`，不要加引號或多餘空白 |
| 想改報告語言 | 修改 `.env` 的 `TRADINGAGENTS_OUTPUT_LANGUAGE` |
| 想改報告輸出位置 | 在 `.env` 加 `TRADINGAGENTS_RESULTS_DIR=路徑` |
| 重裝環境 | 刪除 `.venv` 資料夾後再執行 `.\run.ps1` |

## 六、注意事項

- 不要把 `.env` 提交到 Git，裡面有金鑰（已被 `.gitignore` 排除）。
- 每次分析會呼叫 OpenAI API 並產生費用，深度越高、分析師越多越貴。
- 報告為 AI 產生的分析，僅供研究參考，不構成投資建議。
