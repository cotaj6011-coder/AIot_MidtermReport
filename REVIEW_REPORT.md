# 智慧停車 AI Agent Proposal 獨立審查報告

審查日期：2026-11-08  
審查範圍：`proposal/proposal.md`、正式 DOCX、正式 PPTX、`README.md`、`DESIGN.md`、`data/README.md`、`docs/architecture.md`、`docs/flowchart.md`、資料檔與 repository 結構。  
最高標準：`指引/iLearning說明.txt`。  
原則：不採信既有 `ACCEPTANCE.md` 的 100/100；第一輪僅審查，未修改原始交付檔案。

## 1. 結論

**實際評分：71/100。建議：不直接繳交。**

內容章節大致齊全，官方 API 筆數與多數文獻 DOI 可重現；但仍有一個 Critical、八個 Major 與多個 Minor 問題。最影響成績者是：

1. Architecture、Flowchart 與 Pseudocode 在正式文件及簡報中不一致，且 Pseudocode 有候選資料品質錯配。
2. PPT 未涵蓋 Deep Research 的 10 Questions。
3. 所謂 GitHub repository 不是 Git repository，所有 `src/`、`experiments/`、`tests/` 只有 `.gitkeep`。
4. Agent 的「規劃與選擇工具」只存在文字敘述，Pseudocode 是固定管線，未呈現真實 planning、tool selection、retry 或 human-in-the-loop。
5. 路邊資料主鍵與 UCI 重複資料未處理，現有設計不能直接保證歷史累積正確。
6. 參考文獻並非「13 篇論文」：實際是 4 筆官方資料/API、8 篇學術論文、1 個資料集；其中 [8] 頁碼與 DOI 不完整，[13] 年份口徑不一致。

## 2. 六項評分

| iLearning 項目 | 滿分 | 得分 | 扣分證據 |
|---|---:|---:|---|
| Introduction：問題、動機、證據、創新 | 20 | 17 | A–F 完整；但 innovation 主要是工程整合，缺少可檢驗的研究假設與相對現有系統的必要性證明。 |
| Related Work：AI、Domain、Article Summary | 20 | 16 | AI/Domain 比例合理；但 [11] 不確定性敘述略過度、[8] 書目錯誤，Research Gap 對「臺中特有缺口」的文獻證據仍偏間接。 |
| Deep Research：5 Mindsets、3 Controversies、10 Questions | 20 | 15 | DOCX/Markdown 有 5+3+10；PPT 只呈現 5 Mindsets 與 3 Controversies，未呈現 10 Questions，且爭議頁省略 Evidence 細節。 |
| Proposed AI Agent + System Architecture | 20 | 12 | 八模組存在；但正式架構圖箭頭錯誤，Agent planning 未落到演算法，repository 無 Agent 實作。 |
| Flowchart + Pseudocode + Technical Feasibility | 15 | 9 | 方法與指標方向合理；但正式 Flowchart 缺 decision/loop/human interaction，Pseudocode 有 `quality` 錯配，風險門檻與推薦驗證未操作化。 |
| GitHub + DESIGN.md + 完整文件 | 5 | 2 | README/DESIGN 存在且誠實標示尚未實作；但目錄不是 Git repository，程式、測試與實驗皆為空殼。 |
| **總分** | **100** | **71** | **未達建議直接繳交門檻。** |

## 3. 問題清單

### C1 — Critical：Pseudocode 把最後一筆候選的品質套到所有預測

- 位置：`proposal/proposal.md` 342–378 行；DOCX 第 15 頁；PPT 第 16 頁。
- 證據：資料迴圈內建立 `quality`，但 `observations` 只保存 `observation`；第二個迴圈第 29 行呼叫 `EstimateFullRisk(forecast, quality)`，此時 `quality` 是前一迴圈最後一次迭代的殘留值。PPT 縮寫版同樣在候選迴圈外使用 `quality`。
- 影響：不同停車場可能共用錯誤的新鮮度、故障率或缺失標記，直接污染風險與排序。
- 扣分：Agent/Architecture -3；Flowchart/Pseudocode -2。
- 建議：將 quality 存入每個 observation，改成 `EstimateFullRisk(forecast, o.quality)`；增加兩候選品質不同的單元測試。

### M1 — Major：正式 Architecture 的連線與宣稱流程不一致

- 位置：DOCX 第 12 頁；PPT 第 12 頁；對照 `docs/architecture.md`。
- 證據：Markdown/Mermaid 是 1→2→3→4→5→6→7→8→1。DOCX 圖只畫 1→2、3→4、5→6、7→8；PPT 又額外畫 1→5、2→6、3→7、4→8，沒有 4→5 的正確主流程。
- 影響：教授無法從圖判斷資料、品質、模型、決策與回饋的實際依賴關係。
- 扣分：Agent/Architecture -3。
- 建議：用單一路徑或泳道圖呈現 1→2→3→4→5→6→7→8，回饋線由 8 回到 2 或 1，並標示資料流與控制流。

### M2 — Major：PPT 缺少 Deep Research 的 10 Questions

- 位置：PPT 第 10–11 頁；對照 `proposal/proposal.md` 219–230 行、DOCX 第 10–11 頁。
- 證據：18 頁 PPT 的 Deep Research 僅包含五個心法與三項爭議。第 4 頁的 Q1–Q4 是研究目標，不是 iLearning 指定的 10 個 Why/What-if/Trade-off/Failure-case 等深度問題。
- 影響：簡報未完整交付 iLearning 的明示要求，口試時也缺少深度思考證據。
- 扣分：Deep Research -4。
- 建議：新增或重編 1–2 頁，將 10 Questions 分為資料、模型、Agent/決策三群；仍保持總頁數 <20。

### M3 — Major：正式 Flowchart 不是完整決策流程

- 位置：DOCX 第 13 頁；PPT 第 13 頁；對照 `docs/flowchart.md`。
- 證據：`docs/flowchart.md` 有資料有效性、可用候選、模型可用性三個決策與分支；正式 DOCX 只用六列線性表，PPT 只有品質失效的單一旁支。兩者都沒有 loop、human interaction 或事後驗證回饋線。
- 影響：未充分符合 iLearning 對 Decision、Loop、Exception、Human Interaction 的要求。
- 扣分：Flowchart/Pseudocode -2。
- 建議：直接以 `docs/flowchart.md` 的完整邏輯重畫正式文件與簡報，增加「無候選→詢問使用者放寬限制」與「事後觀測→評估/重訓」回路。

### M4 — Major：Agent planning 僅是名稱，演算法是固定管線

- 位置：`DESIGN.md` 第 30 行、`proposal/proposal.md` 第 267 行及 Pseudocode；README。
- 證據：文字宣稱 Agent Orchestrator 會「規劃任務、選擇工具」，但 Pseudocode 固定依序執行 Find→Fetch→Validate→Predict→Rank，沒有 Plan、tool registry、依資料類型選擇 connector/model、失敗重試或重新規劃。`src/agent/` 只有 `.gitkeep`。
- 影響：容易被質疑只是帶 LLM 說明層的傳統預測管線，而非必要的 Domain AI Agent。
- 扣分：Agent/Architecture -2。
- 建議：定義明確的 planner state、工具介面、選擇條件、retry/replan、停止條件與 human approval；至少提供可執行最小 orchestrator 測試。

### M5 — Major：repository 不符合「GitHub + 完整 repository」的交付期待

- 位置：整個 workspace、README repository tree。
- 證據：`git status` 回傳「not a git repository」；`src/`、`experiments/`、`tests/` 只有 1-byte `.gitkeep`。README 明確寫「尚未提供正式應用程式」，DESIGN 的 How to Run 也沒有可執行命令。
- 影響：README 中的 repository 結構是規劃，不是可重現交付；無法驗證 Installation、How to Run、Demo 或 Experiment。
- 扣分：GitHub/DESIGN -3。
- 建議：若 Proposal 階段允許不實作，明確把此項改稱「repository blueprint」；若教授按 GitHub 實體評分，至少建立 Git、可重現 API snapshot script、schema validation、baseline notebook/script 與測試。

### M6 — Major：路邊資料主鍵未定義，歷史累積可能互相覆蓋

- 位置：`data/README.md`、`DESIGN.md` Storage Schema。
- 證據：2026-11-08 實測 10,143 筆、367 路段；`PS_ID` 只有 391 個唯一值，重複 9,752 次；`Section_ID|PS_ID` 才是 10,143 個唯一鍵。現有 schema 只寫通用 `facility_id`，沒有 mapping 或複合鍵規則。
- 影響：若直接以 PS_ID 作主鍵，會覆寫不同路段車格，造成錯誤歷史與標籤。
- 扣分：Flowchart/Feasibility -1；Agent/Architecture -1。
- 建議：路邊主鍵明定為 `(source_type, Section_ID, PS_ID)`，並對 snapshot 使用 `(source, section_id, ps_id, observed_at)` 唯一約束。

### M7 — Major：UCI 品質敘述不足，不能直接稱資料管線已驗證

- 位置：`data/historical/parking_birmingham/dataset.csv`、`data/README.md`、PPT 第 5/18 頁。
- 證據：本地 CSV 有 35,717 列、30 場、4 欄、無空字串，但存在 216 筆完全重複列；各停車場記錄數介於 88–1,312，顯示時間覆蓋不均。UCI 官方 metadata 標示 Has Missing Values = Yes，代表缺失可能是缺少時間點而非空儲存格。
- 影響：只查 null 無法證明時間序列完整；模型切分前需補做重複、時間間隔、場站覆蓋與容量一致性。
- 扣分：Technical Feasibility -1。
- 建議：新增品質報告，區分 cell-level missing、missing timestamp、duplicate row、irregular interval 與場站 coverage。

### M8 — Major：不確定性文獻的結論有過度延伸

- 位置：DOCX 第 4、5、7–10 頁；`proposal/proposal.md` Related Work、Mindset 5、Controversy 3。
- 證據：[11] 確實研究 epistemic/aleatoric uncertainty，但原文說 BNN 輸出並未內生地分離兩者，而是用資料稀缺與人工噪聲情境間接檢視；其 reviewer 也質疑只報單一 scalar metrics、沒有每筆預測的不確定分解。Proposal 使用「區分」與「可分解」語氣過強。
- 影響：Research Gap 與推薦風險設計的文獻支撐被說得比證據更強。
- 扣分：Related Work -2。
- 建議：改成「在不同資料稀缺與噪聲情境下評估兩類不確定性影響」，不要宣稱已逐筆分解；本專題若只用歷史誤差與 freshness，稱為 risk proxy，不稱 Bayesian uncertainty。

### m1 — Minor：參考文獻 [8] 頁碼與 DOI 不完整

- 位置：DOCX 第 17 頁；`proposal/proposal.md` References。
- 證據：正式出版資料是 74(4), 1128–1149，DOI `10.1093/jrsssc/qlaf017`；文件寫 1128–1151，且僅放網頁 URL。
- 扣分：Related Work -0.5（納入該項總扣分）。
- 建議：修正頁碼並補 DOI。

### m2 — Minor：UCI 年份口徑不一致

- 位置：Article Summary Table 與 References [13]。
- 證據：UCI 頁面顯示 donated 2019，但其建議 citation 為 Stolfi (2017)；文件統一寫 2019，未說明採 metadata 年或 citation 年。
- 扣分：Related Work -0.5（納入該項總扣分）。
- 建議：依 UCI 建議引用寫 2017，或註明 2019 為 repository donation year。

### m3 — Minor：市府路外更新頻率來源互相衝突

- 位置：資料可行性與限制段落。
- 證據：政府資料開放平臺中文頁目前標「每 1 月」，英文頁標「Every 10 minutes」，端點內容也沒有明確 `DataCollectTime`。文件有提到頻率描述差異，但未在表格中把該來源標為 UNVERIFIED。
- 扣分：Technical Feasibility -0.5（納入該項總扣分）。
- 建議：市府 RGB 端點的實際更新頻率標為 UNVERIFIED；由連續快照量測確認，不以 metadata 單一欄位下結論。

### m4 — Minor：PPT 可讀性與留白配置不均

- 位置：PPT 第 6、8、14、16、18 頁。
- 證據：大面積卡片下半部空白，本文卻使用約 11–14 pt 的小字；第 16 頁程式碼密度高。投影環境下可讀性不足。
- 扣分：Deep Research / Technical Feasibility 合計 -0.5（納入相關項總扣分）。
- 建議：減少卡片高度、將 body 提升至至少約 17 pt；Pseudocode 只留核心 10–12 行，細節放講者備註或備用頁。

### m5 — Minor：Research Gap 有在地合理性，但文獻鏈仍偏間接

- 位置：`proposal/proposal.md` 127–135 行；PPT 第 3 頁。
- 證據：文獻支持時空、多源、品質與不確定性的重要性；官方端點支持臺中粒度差異。但沒有系統性文獻證明「臺中尚無同類整合 Agent」，因此不能把此點表述為已證實的研究空白。
- 扣分：Introduction / Related Work 合計 -1（納入相關項總扣分）。
- 建議：把 gap 分為「empirically verified data gap」與「project-specific integration gap」，避免宣稱整個研究界尚未解決。

## 4. 13 筆來源核實

| Ref. | 類型 | 核實結果 | 審查結論 |
|---|---|---|---|
| [1] | 臺中官方統計 | 2025 年底機動車 3,103,944；官方年報頁可重現 | PASS |
| [2] | 臺中路邊資料 | 10 分鐘、OGL v1、8 欄；實測 10,143 筆 | PASS，但主鍵規則缺漏 |
| [3] | 臺中路外市府端點 | 實測 1,417 筆，只有容量與 RGB 滿車率，無精確 AvailableCar | PASS；更新頻率 UNVERIFIED |
| [4] | TDX API | 訪客模式實測 1,121 筆，含 TotalSpaces、AvailableSpaces、狀態與時間 | PASS；高頻/歷史方案 UNVERIFIED |
| [5] | Ma et al. 2024 | DOI、作者、卷期頁碼與 review 方法相符 | PASS |
| [6] | Cao et al. 2025 | DOI、作者、動態圖/GRU/GCN/attention 結論相符 | PASS |
| [7] | Qian et al. 2025 | DOI、作者、MGA-GRU 與 geography/accessibility/POI multi-view graph 相符 | PASS |
| [8] | Schneble & Kauermann 2025 | semi-Markov、Melbourne、state duration 結論相符 | PASS WITH CORRECTION：頁碼 1128–1149、DOI qlaf017 |
| [9] | Vakrinou et al. 2026 | Athens 四場、attention LSTM 短期與 Transformer 長期結論相符 | PASS |
| [10] | Kuang et al. 2025 | 58 場、Meta-HWFST、異質/即時天氣、meta-learning 相符 | PASS |
| [11] | Nezhadettehad et al. 2025 | DOI/作者相符；文件對 uncertainty decomposition 的表述過強 | PASS WITH QUALIFICATION |
| [12] | Piccialli et al. 2025 | DOI/作者、Caserta、STID、CVGAN、感測與營運決策相符 | PASS；Passing-car false signal 細節未找到直接證據 |
| [13] | UCI Birmingham | DOI、35,717、30 場、4 欄、2016-10-04 至 12-19 相符 | PASS WITH CORRECTION：年份與 missing/duplicates 說明 |

注意：這 13 筆不是 13 篇論文，而是 **4 筆官方來源 + 8 篇論文 + 1 個資料集**。

## 5. API 與資料重現紀錄

審查當日重新呼叫結果：

| 來源 | HTTP/筆數 | 欄位 | 判定 |
|---|---:|---|---|
| 臺中路邊官方端點 | 200 / 10,143 | Section_ID, PS_ID, PS_type, Lat, Lng, status, CountyCode, AgencyCodes | VERIFIED |
| 臺中路外市府端點 | 200 / 1,417 | ID, SeqNo, Position, Lng, Lat, AvailableCarRGB, AvailableMotorRGB, KeyWord, TotalCar, TotalMotor, EvRGB, EvTotal | VERIFIED |
| TDX 臺中路外 Availability | 200 / 1,121 | CarParkID, CarParkName, TotalSpaces, AvailableSpaces, Availabilities, ServiceStatus, FullStatus, ChargeStatus, DataCollectTime | VERIFIED |
| UCI 本地 CSV | 35,717 / 30 場 | SystemCodeNumber, Capacity, Occupancy, LastUpdated | VERIFIED；216 duplicate rows |

路邊當次狀態：2,733 空位、7,410 占用、0 故障。此數字只代表單次快照，不代表長期故障率。

## 6. 跨文件一致性

| 主題 | Markdown | DOCX | PPTX | README/DESIGN | 判定 |
|---|---|---|---|---|---|
| Abstract/Introduction A–F | 有 | 有 | 摘要式 | 有概述 | PASS |
| 5 Mindsets | 有 | 有 | 有 | 無需完整重複 | PASS |
| 3 Controversies | 有完整觀點/證據/共識/未解 | 有 | PPT 僅摘要共識/未解 | 無需完整重複 | PARTIAL |
| 10 Questions | 有 | 有 | 無 | 無 | FAIL |
| 八模組 Architecture | 正確 Mermaid | 圖的連線不完整 | 圖有錯誤跨列箭頭 | DESIGN 文字正確 | FAIL |
| 完整 Flowchart | Markdown 支援檔有分支 | 線性表 | 單一失效旁支 | DESIGN 有線性 Data Flow | PARTIAL |
| Pseudocode | 36 行、有 quality bug | 同 Markdown | 18 行、同 bug | 僅描述 | FAIL |
| 實作狀態 | 明示 Expected | 明示 Expected | 明示限制 | README/DESIGN 明示未實作 | 一致且誠實 |
| Repository 可執行性 | 不適用 | 不適用 | 宣稱可重現結構 | 空目錄、無命令 | FAIL |

## 7. 視覺審查

- DOCX：重新渲染 17 頁並逐頁檢查。未發現文字截斷、物件重疊或缺字。第 7 頁 Article Summary 表格字級偏小；第 15 頁 pseudocode 密度高；第 16–17 頁 References 的中英混排與字距不夠精緻，但仍可讀。
- PPTX：重新渲染 18 頁並逐頁檢查。未發現截斷或重疊；主要問題是內容覆蓋與圖意錯誤，而非檔案損壞。第 6、8、14、18 頁留白過大但字偏小；第 16 頁 code 字級不利投影。
- 講述順序：Problem→Gap→Questions→Data→Related Work→Deep Research→Scheme→Evaluation→Outcome 整體合理，但缺 10 Questions，使 Deep Research 敘事中斷。

## 8. 教授最可能追問的 10 題

| 問題 | 現有文件能否回答 | 缺口 |
|---|---|---|
| 1. 既然臺中沒有長期歷史，你如何在期限內完成可訓練且有季節性的模型？ | 部分 | 只有 phases，沒有最低資料長度、採樣頻率與 go/no-go 數值。 |
| 2. 為何需要 Agent，而不是固定 ETL + model + ranking service？ | 不足 | 沒有展示會因情境改變的 planning/tool selection/replan。 |
| 3. 你的研究創新性和一般「預測後加權排序」有何不同？ | 部分 | 工程整合有價值，但尚無 formal hypothesis 或 ablation。 |
| 4. 路邊 status 如何聚合成路段空位標籤，故障車格分母怎麼算？ | 不足 | 未定義 aggregation window、有效分母與複合主鍵。 |
| 5. 路外 AvailableSpaces 的時間頻率與可靠性如何證明？ | 不足 | 單次 API 可讀不等於頻率、缺報與延遲已驗證。 |
| 6. 滿位風險門檻如何設定、是否校準、怎麼衡量成本不對稱？ | 不足 | 只有 Precision/Recall/F1，無 threshold、calibration、PR-AUC 或 cost matrix。 |
| 7. 如何保證天氣、事件與鄰近停車資料沒有 target leakage？ | 部分 | 原則有寫，但沒有 feature availability table 與 cutoff 實作。 |
| 8. UCI Birmingham 如何驗證臺中方法，而不是只證明程式能跑？ | 部分 | 有外部效度限制，但尚無 domain shift 或 transfer protocol。 |
| 9. 推薦的 ground truth 是「抵達時仍有位」還是「使用者實際停入」？ | 不足 | 離線指標有方向，沒有 observation matching 與 arrival-time label 定義。 |
| 10. Agent 若遇到 API 200 但資料過期、模型不可用、無候選，如何重規劃並讓人介入？ | 部分 | flowchart 支援檔有部分分支，正式交付與 pseudocode 沒有完整 replan/human loop。 |

## 9. 修正優先順序

以「影響評分 × 修正成本」排序：

1. **修正 Pseudocode quality 錯配**：高影響、低成本。
2. **重畫 Architecture 與完整 Flowchart**：高影響、中低成本。
3. **在 <20 頁限制內補入 10 Questions**：高影響、中低成本，可合併或壓縮留白頁。
4. **補路邊複合主鍵與 UCI 品質報告**：高影響、低成本。
5. **把 Agent planning/replan/tool-selection 寫入架構與 pseudocode**：高影響、中成本。
6. **建立最小可執行 repository 證據**：高影響、中高成本。
7. **修正 [8]、[11]、[13] 引用與敘述**：中影響、低成本。
8. **操作化滿位風險與推薦評估**：中高影響、中成本。
9. **改善 PPT 字級與留白**：中影響、中低成本。
10. **把 Research Gap 拆成已驗證 data gap 與 project integration gap**：中影響、低成本。

## 10. 最終建議

**目前不建議直接繳交。**

若只剩短時間，至少完成優先序 1–5 與 7；這些修改能修復最明顯的邏輯錯誤、規範缺漏與學術表述問題。若教授會實際檢查 GitHub 或要求 Demo，優先序 6 也是阻斷項目。

## 11. 主要外部核實來源

- 臺中市路邊剩餘車位：https://data.gov.tw/dataset/158166
- 臺中市路外剩餘車位：https://data.gov.tw/dataset/83931
- UCI Parking Birmingham：https://archive.ics.uci.edu/dataset/482/parking+birmingham
- Ma et al.：https://doi.org/10.1016/j.jtte.2023.11.004
- Cao et al.：https://doi.org/10.1016/j.tra.2025.104391
- Qian et al.：https://doi.org/10.1016/j.asoc.2025.112781
- Schneble & Kauermann：https://doi.org/10.1093/jrsssc/qlaf017
- Vakrinou et al.：https://doi.org/10.1016/j.ijtst.2025.02.005
- Kuang et al.：https://doi.org/10.1016/j.aei.2024.102969
- Nezhadettehad et al.：https://doi.org/10.3390/s25113463
- Piccialli et al.：https://doi.org/10.1038/s41467-025-65306-w
- UCI dataset DOI：https://doi.org/10.24432/C51K5Z
