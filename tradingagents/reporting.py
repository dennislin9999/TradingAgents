"""Reusable report-tree writer shared by the CLI and the programmatic API.

Writes a run's per-section markdown (analysts, research, trading, risk,
portfolio) plus a consolidated ``complete_report.md`` under ``save_path``. The
CLI and ``TradingAgentsGraph.save_reports`` both call this, so a headless / API
run produces the same on-disk report tree a CLI run does.
"""

from datetime import datetime
from pathlib import Path

_READING_GUIDE = """# 報告閱讀順序指南

本資料夾為單次分析的完整輸出。沒選的分析師不會有對應檔案。

## 快速版（3 分鐘）

1. `5_portfolio/decision.md`：最終決策與理由。
2. `3_trading/trader.md`：交易員的具體操作計畫。

## 完整版（由淺入深）

| 順序 | 檔案 | 看什麼 |
|------|------|--------|
| 1 | `complete_report.md` 開頭標頭 | 分析日期、模型、分析師與資料來源 |
| 2 | `1_analysts/fundamentals.md` | 公司基本介紹、財報、獲利與估值 |
| 3 | `1_analysts/market.md` | 股價走勢、技術指標 |
| 4 | `1_analysts/news.md` | 近期新聞與總體經濟事件 |
| 5 | `1_analysts/sentiment.md` | 市場與社群情緒 |
| 6 | `2_research/bull.md` | 看多論點 |
| 7 | `2_research/bear.md` | 看空論點 |
| 8 | `2_research/manager.md` | 研究經理整合多空後的建議 |
| 9 | `3_trading/trader.md` | 交易員的交易計畫 |
| 10 | `4_risk/aggressive.md` | 激進派風險觀點 |
| 11 | `4_risk/conservative.md` | 保守派風險觀點 |
| 12 | `4_risk/neutral.md` | 中立派風險觀點 |
| 13 | `5_portfolio/decision.md` | 投資組合經理的最終決策 |

## 閱讀邏輯

資料 → 辯論 → 計畫 → 風險 → 決策。想一次讀完，直接開 `complete_report.md`
（章節順序：I 分析師 → II 研究 → III 交易 → IV 風險 → V 最終決策）。

## 注意事項

- 報告為 AI 產生的分析，僅供研究參考，不構成投資建議。
- 請核對關鍵數字（財報、價格）與原始資料是否一致。
"""


def _header(ticker: str, final_state: dict, settings: dict | None) -> str:
    """The report's title and what produced it: analysis date, version, models, analysts, vendors."""
    lines = [f"# Trading Analysis Report: {ticker}", ""]
    if final_state.get("trade_date"):
        lines.append(f"- Analysis date: {final_state['trade_date']}")
    lines.append(f"- Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    if settings:
        s = settings.get
        lines.append(f"- TradingAgents {s('version', '?')}: {s('llm_provider', '?')}, "
                     f"deep {s('deep_think_llm', '?')}, quick {s('quick_think_llm', '?')}")
        lines.append(f"- Analysts: {', '.join(s('analysts') or [])}; "
                     f"research debate rounds {s('max_debate_rounds', '?')}, "
                     f"risk debate rounds {s('max_risk_discuss_rounds', '?')}")
        vendors = {**(s("data_vendors") or {}), **(s("tool_vendors") or {})}
        if vendors:
            lines.append("- Data vendors: " + ", ".join(f"{k} {v}" for k, v in vendors.items()))
    return "\n".join(lines) + "\n\n"


def write_report_tree(final_state: dict, ticker: str, save_path, settings: dict | None = None) -> Path:
    """Save a completed run's reports to ``save_path``; return the complete-report path.

    ``settings`` (``TradingAgentsGraph.run_settings()``) adds what produced the run
    to the report's header.
    """
    save_path = Path(save_path)
    save_path.mkdir(parents=True, exist_ok=True)
    sections = []

    # 1. Analysts
    analysts_dir = save_path / "1_analysts"
    analyst_parts = []
    if final_state.get("market_report"):
        analysts_dir.mkdir(exist_ok=True)
        (analysts_dir / "market.md").write_text(final_state["market_report"], encoding="utf-8")
        analyst_parts.append(("Market Analyst", final_state["market_report"]))
    if final_state.get("sentiment_report"):
        analysts_dir.mkdir(exist_ok=True)
        (analysts_dir / "sentiment.md").write_text(final_state["sentiment_report"], encoding="utf-8")
        analyst_parts.append(("Sentiment Analyst", final_state["sentiment_report"]))
    if final_state.get("news_report"):
        analysts_dir.mkdir(exist_ok=True)
        (analysts_dir / "news.md").write_text(final_state["news_report"], encoding="utf-8")
        analyst_parts.append(("News Analyst", final_state["news_report"]))
    if final_state.get("fundamentals_report"):
        analysts_dir.mkdir(exist_ok=True)
        (analysts_dir / "fundamentals.md").write_text(final_state["fundamentals_report"], encoding="utf-8")
        analyst_parts.append(("Fundamentals Analyst", final_state["fundamentals_report"]))
    if analyst_parts:
        content = "\n\n".join(f"### {name}\n{text}" for name, text in analyst_parts)
        sections.append(f"## I. Analyst Team Reports\n\n{content}")

    # 2. Research
    if final_state.get("investment_debate_state"):
        research_dir = save_path / "2_research"
        debate = final_state["investment_debate_state"]
        research_parts = []
        if debate.get("bull_history"):
            research_dir.mkdir(exist_ok=True)
            (research_dir / "bull.md").write_text(debate["bull_history"], encoding="utf-8")
            research_parts.append(("Bull Researcher", debate["bull_history"]))
        if debate.get("bear_history"):
            research_dir.mkdir(exist_ok=True)
            (research_dir / "bear.md").write_text(debate["bear_history"], encoding="utf-8")
            research_parts.append(("Bear Researcher", debate["bear_history"]))
        if final_state.get("investment_plan"):
            research_dir.mkdir(exist_ok=True)
            (research_dir / "manager.md").write_text(final_state["investment_plan"], encoding="utf-8")
            research_parts.append(("Research Manager", final_state["investment_plan"]))
        if research_parts:
            content = "\n\n".join(f"### {name}\n{text}" for name, text in research_parts)
            sections.append(f"## II. Research Team Decision\n\n{content}")

    # 3. Trading
    if final_state.get("trader_investment_plan"):
        trading_dir = save_path / "3_trading"
        trading_dir.mkdir(exist_ok=True)
        (trading_dir / "trader.md").write_text(final_state["trader_investment_plan"], encoding="utf-8")
        sections.append(f"## III. Trading Team Plan\n\n### Trader\n{final_state['trader_investment_plan']}")

    # 4. Risk Management
    if final_state.get("risk_debate_state"):
        risk_dir = save_path / "4_risk"
        risk = final_state["risk_debate_state"]
        risk_parts = []
        if risk.get("aggressive_history"):
            risk_dir.mkdir(exist_ok=True)
            (risk_dir / "aggressive.md").write_text(risk["aggressive_history"], encoding="utf-8")
            risk_parts.append(("Aggressive Analyst", risk["aggressive_history"]))
        if risk.get("conservative_history"):
            risk_dir.mkdir(exist_ok=True)
            (risk_dir / "conservative.md").write_text(risk["conservative_history"], encoding="utf-8")
            risk_parts.append(("Conservative Analyst", risk["conservative_history"]))
        if risk.get("neutral_history"):
            risk_dir.mkdir(exist_ok=True)
            (risk_dir / "neutral.md").write_text(risk["neutral_history"], encoding="utf-8")
            risk_parts.append(("Neutral Analyst", risk["neutral_history"]))
        if risk_parts:
            content = "\n\n".join(f"### {name}\n{text}" for name, text in risk_parts)
            sections.append(f"## IV. Risk Management Team Decision\n\n{content}")

    # 5. Portfolio Manager
    if final_state.get("final_trade_decision"):
        portfolio_dir = save_path / "5_portfolio"
        portfolio_dir.mkdir(exist_ok=True)
        (portfolio_dir / "decision.md").write_text(final_state["final_trade_decision"], encoding="utf-8")
        sections.append(f"## V. Portfolio Manager Decision\n\n### Portfolio Manager\n{final_state['final_trade_decision']}")

    # Write consolidated report
    (save_path / "complete_report.md").write_text(
        _header(ticker, final_state, settings) + "\n\n".join(sections), encoding="utf-8"
    )
    (save_path / "READING_GUIDE.md").write_text(_READING_GUIDE, encoding="utf-8")
    return save_path / "complete_report.md"
