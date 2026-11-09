# REVIEW REPORT 修復對照

更新日期：2026-11-08

| 編號 | 修改前證據 | 修復內容 | 修復後證據 | 狀態 |
|---|---|---|---|---|
| C1 | Pseudocode 第 29 行沿用迴圈外 `quality` | 改為 `o.quality`，實作綁定 observation-quality pair | Proposal 第 4.3 節；`test_each_candidate_uses_its_own_quality` | PASS |
| M1 | DOCX／PPT 架構連線錯誤且不一致 | 統一為 Plan→Select→Validate→Predict→Decide→Explain→Verify，含 retry/human loop | `docs/architecture.md`、DOCX pp.6–7、PPT p.9 | PASS |
| M2 | PPT 缺 10 Questions | 以兩頁列出 Q1–Q10 | PPT pp.6–7 | PASS |
| M3 | 正式流程圖缺 decision／loop／human | 加入 retryable、unrecoverable、confidence、post-verify 分支 | `docs/flowchart.md`、DOCX pp.6–7、PPT p.10 | PASS |
| M4 | Agent 只是固定 pipeline | 實作 tool registry、selection、retry/replan、human review、evidence log | `src/agent/orchestrator.py` 與分支測試 | PASS |
| M5 | 非 Git repository，目錄只有 `.gitkeep` | `git init` 並加入 connector、quality、baseline、agent、QA 與 tests | `.git/`、`src/`、`tests/`；9 tests OK | PASS |
| M6 | `PS_ID` 被誤當唯一鍵 | 定義 entity key 與 snapshot key，明列狀態聚合與歷史追加規則 | Proposal 5.1、`data/README.md`、`DESIGN.md` | PASS |
| M7 | 未分析 UCI duplicate／gap／coverage | 建立可重現分析與 JSON 報告 | `tools/analyze_uci.py`、`data/uci_quality_report.json`、2 個 QA tests | PASS |
| M8 | 過度宣稱 BNN 分離兩類 uncertainty | 改為 freshness、模型分散度、校準誤差皆為不同 proxy，不宣稱理論分解 | Proposal 2.1、3.2；PPT pp.4–5 | PASS |
| m1 | [8] 頁碼錯誤且缺 DOI | 修正為 1128–1149、doi:10.1093/jrsssc/qlaf017 | Proposal References、DOCX p.11 | PASS |
| m2 | UCI 年份含混 | 區分 recommended citation 2017 與 donation 2019 | Proposal [13]、DOCX p.11 | PASS |
| m3 | 路外固定更新頻率未驗證 | 明確標示 Unverified，以 `DataCollectTime` 實測，不假設 10 分鐘 | Proposal 5.2、PPT p.8、`data/README.md` | PASS |
| m4 | PPT 文字過小與留白不佳 | 重製 16 頁；問題頁字級回修後重新渲染 | `build/final_pptx_render/page-01..16.png` | PASS |
| m5 | Research Gap 證據過度概括 | 分成 empirical data gap 與 project-specific integration gap，均保留待驗證限制 | Proposal 1.3、PPT p.3 | PASS |

## 額外補強

- 預先定義 H1–H3、Agent 相對固定 pipeline 的必要性與退回條件。
- 補齊 temporal split、baseline、leakage、滿位門檻、calibration、arrival ground truth、Top-k 與 ablation。
- Go／No-Go 條件涵蓋歷史長度、coverage、MAE、Recall、Top-3、Brier 與 p95。
- Proposal 與期末範圍以 Implemented／Verified／Planned／Unverified 明確區分。

## 驗證證據

- `python -m unittest discover -s tests -v`：9 tests，全部通過。
- UCI：35,717 列、30 場站、0 空白 cell、216 exact duplicates、場站列數 88–1,312。
- DOCX：11 頁，已渲染並逐頁檢查；表格、流程與程式碼無截斷。
- PPTX：16 頁，少於 20 頁，已渲染並逐頁檢查；無重疊或截斷。
- 未設定 Git 遠端，未 commit、未 push。

