# 報告閱讀順序指南

每次分析的報告會輸出到 `output/<股票代號>_<時間戳記>/`。

## 目錄結構

```
output/<股票代號>_<時間戳記>/
├── complete_report.md      # 完整合併報告（含標頭資訊）
├── 1_analysts/             # 分析師團隊
│   ├── fundamentals.md
│   ├── market.md
│   ├── news.md
│   └── sentiment.md
├── 2_research/             # 研究團隊辯論
│   ├── bull.md
│   ├── bear.md
│   └── manager.md
├── 3_trading/
│   └── trader.md
├── 4_risk/                 # 風險管理辯論
│   ├── aggressive.md
│   ├── conservative.md
│   └── neutral.md
└── 5_portfolio/
    └── decision.md
```

實際產生的檔案取決於你選的分析師；沒選的分析師不會有對應檔案。

## 建議閱讀順序

### 快速版（3 分鐘）

1. `5_portfolio/decision.md`：最終決策（買進／持有／賣出）與理由。
2. `3_trading/trader.md`：交易員的具體操作計畫。

### 完整版（由淺入深）

| 順序 | 檔案 | 看什麼 |
|------|------|--------|
| 1 | `complete_report.md` 開頭標頭 | 分析日期、使用的模型、分析師與資料來源，先確認報告條件 |
| 2 | `1_analysts/fundamentals.md` | 公司基本介紹、財報、獲利與估值，先認識這家公司 |
| 3 | `1_analysts/market.md` | 股價走勢、技術指標、支撐壓力 |
| 4 | `1_analysts/news.md` | 近期新聞與總體經濟事件 |
| 5 | `1_analysts/sentiment.md` | 市場與社群情緒 |
| 6 | `2_research/bull.md` | 看多論點 |
| 7 | `2_research/bear.md` | 看空論點 |
| 8 | `2_research/manager.md` | 研究經理整合多空後的投資建議 |
| 9 | `3_trading/trader.md` | 交易員據此擬定的交易計畫 |
| 10 | `4_risk/aggressive.md` | 激進派風險觀點 |
| 11 | `4_risk/conservative.md` | 保守派風險觀點 |
| 12 | `4_risk/neutral.md` | 中立派風險觀點 |
| 13 | `5_portfolio/decision.md` | 投資組合經理的最終決策 |

## 閱讀邏輯

資料 → 辯論 → 計畫 → 風險 → 決策

1. **先了解公司與市場**（第 2～5 項）：基本面最先看，其餘補充價格、新聞、情緒。
2. **再看多空辯論**（第 6～8 項）：了解正反兩面，以經理的結論為準。
3. **接著看交易計畫**（第 9 項）：把結論變成具體操作。
4. **然後看風險檢驗**（第 10～12 項）：三種立場對計畫的挑戰。
5. **最後看最終決策**（第 13 項）：綜合以上所有資訊的結論。

## 注意事項

- 報告是 AI 產生的分析，僅供研究參考，不構成投資建議。
- 請核對關鍵數字（財報、價格）與原始資料是否一致。
- 內部辯論使用英文推理，最終報告依 `output_language` 設定輸出（目前為繁體中文）。
- 若只想一次讀完，直接開 `complete_report.md`，章節順序為 I 分析師 → II 研究 → III 交易 → IV 風險 → V 最終決策。
