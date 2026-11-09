# 智慧停車 AI Agent Proposal 執行計畫

## 目標

完成符合 iLearning 規範的 Proposal 文件、正式簡報、GitHub 專案骨架與 DESIGN.md，並以逐項證據驗收。專題題目為「智慧停車 AI Agent：臺中市剩餘車位預測與推薦」。

## 優先級與評分配置

| 階段 | 工作 | 對應評分 | 權重 |
|---|---|---|---:|
| 1 | Introduction 與公共證據 | 重要性、動機、Evidence、Innovation | 20% |
| 2 | Related Work 與 Article Summary Table | AI、Domain、Research Gap | 20% |
| 3 | Deep Research | 5 Mindsets、3 Controversies、10 Questions | 20% |
| 4 | Proposed AI Agent 與 Architecture | Agent 能力、模組責任、資料流 | 20% |
| 5 | Flowchart、Pseudocode 與可行性 | 決策、例外、模型與資料驗證 | 15% |
| 6 | Repository 與 DESIGN.md | 完整度、可追溯性 | 5% |

## 執行階段

### Phase 0 盤點與驗收框架

- 讀取三份權威文件。
- 建立 PLAN.md、PROGRESS.md、ACCEPTANCE.md。
- 建立專案目錄、README.md 與 DESIGN.md 骨架。

### Phase 1 證據與資料驗證

- 核實 2025 至 2026 原始研究論文。
- 核實臺中市政府與 TDX 資料頁、API、欄位、更新頻率、授權及歷史限制。
- 建立來源紀錄與資料可行性表。
- 明確區分臺中即時資料、UCI 公開歷史資料與不可取得的新北私人資料。

### Phase 2 Proposal 內容

- 完成 Abstract A 至 F。
- 完成 Introduction A 至 F。
- 完成 AI 與 Domain 各約 50% 的 Related Work。
- 完成 Article Summary Table 及 Research Gap 鏈結。
- 完成 5 Mindsets、3 Controversies、10 Questions。
- 完成編號 Architecture、Flowchart、行號 Pseudocode。
- 完成 References。

### Phase 3 專案設計文件

- 完成 README.md。
- 完成 DESIGN.md，涵蓋 Problem、Requirements、Architecture、Components、Data、AI、Domain Knowledge、Algorithm、Implementation Mapping、How to Run、Results、Limitations。
- 建立 Proposal 階段所需的 repository 結構與資料說明。

### Phase 4 正式交付物

- 建立 Proposal Markdown 主文件。
- 建立經過渲染與逐頁檢查的 DOCX。
- 建立正式 PPTX，完整呈現規範要求。
- 渲染並逐頁檢查簡報。

### Phase 5 驗收與修正

- 逐項檢查 ACCEPTANCE.md。
- 交叉核對 Proposal、PPT 與 DESIGN.md 的架構、用語、資料與引用。
- 依六項評分構面自評，目標至少 95 分。
- 修正所有未通過項目後才標記 COMPLETE。

## 寫作與研究原則

- 所有事實使用可追溯的原始來源。
- Proposal 未執行的實驗只寫預期結果，不寫虛構數值。
- 不將 UCI 或新北資料的結果宣稱為臺中成果。
- LLM 負責需求解析與工具協調；數值預測由可重現模型執行。
- 路外與路邊資料分開建模及評估，再由決策引擎整合。
- 使用時間序列切分，避免未來資訊洩漏。

## 完成條件

只有 ACCEPTANCE.md 所有必要項目均有可檢查證據、DOCX 與 PPTX 通過渲染檢查、評分自評至少 95 分，且沒有未揭露的必要缺口，才可宣告完成。
