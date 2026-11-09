# 智慧停車 AI Agent Proposal

本 repository 是臺中停車可用性預測與推薦的 Proposal 與最小可執行原型。原型證明 API 擷取、資料驗證、Persistence baseline、Agent tool selection、retry/replan、人工確認與證據紀錄可執行；臺中長期預測成效仍為 Planned／Unverified。

## Deliverables

- `proposal/proposal.md`：單一內容權威來源
- `proposal/智慧停車AI_Agent_Proposal.docx`
- `proposal/智慧停車AI_Agent_Proposal.pptx`
- `DESIGN.md`：設計與實作映射
- `REVIEW_RESOLUTION.md`：審查問題修復證據
- `ACCEPTANCE.md`：驗收與六項評分

## Run

需求：Python 3.11；核心原型只使用標準函式庫。

```powershell
python -m unittest discover -s tests -v
python tools/analyze_uci.py
```

最小使用方式：

```python
from src.agent import ParkingAgent

agent = ParkingAgent({"primary": lambda: observations, "fallback": lambda: fallback_observations})
result = agent.run({"horizon_minutes": 30, "top_k": 3})
```

## Implemented

- JSON API Connector：timeout、HTTP 狀態與 JSON 解析
- Quality Validation：schema、freshness、capacity bounds
- Persistence Baseline
- Agent Orchestrator：tool registry、retry/replan、human review、evidence log
- Domain Ranking：availability、full risk、freshness 與距離
- UCI 品質報告：duplicate、gap、coverage
- 9 項自動化測試

## Proposal versus Final Project

| 範圍 | 狀態 |
|---|---|
| 控制流程、baseline、QA 與測試 | Implemented and Verified |
| UCI 資料品質分析 | Implemented and Verified |
| 臺中單次 API schema 與 snapshot 數量 | Verified snapshot |
| 臺中至少 8 週歷史 | Planned |
| H1–H3 模型與推薦效果 | Unverified |
| GIS Demo 與線上部署 | Planned |

未設定 Git 遠端，未 commit 或 push。

