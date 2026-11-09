# 資料來源與品質規則

## 臺中路邊停車格

- 官方欄位：`Section_ID`、`PS_ID`、`PS_type`、`Lat`、`Lng`、`status`、`CountyCode`、`AgencyCodes`。
- Entity key：`(source_type, Section_ID, PS_ID)`；`PS_ID` 不可單獨作主鍵。
- Snapshot key：`(source_type, Section_ID, PS_ID, observed_at)`。
- 聚合：依路段與 snapshot time 分別計算 status 0、1、2、unknown；unknown 不得合併至空位。
- 2026-11-08 單次驗證：10,143 筆、367 路段、391 個不同 `PS_ID`；複合鍵 10,143 個皆唯一；status 0/1/2 為 2,733/7,410/0。

## 臺中路外與 TDX

臺中路外資料單次驗證 1,417 筆；TDX Availability 單次驗證 1,121 筆。固定更新頻率目前 **Unverified**，未假設每 10 分鐘；正式歷史以 `DataCollectTime` 與擷取時間分布驗證。

## 歷史擷取規則

1. 固定排程輪詢，原始 payload 只追加。
2. 保存 source timestamp、ingested_at、HTTP status、payload hash 與 schema version。
3. 相同 snapshot key 與 hash 標為重送；不同 hash 保留版本，不覆寫。
4. 分別標示 schema error、stale、capacity violation、unknown status 與 network error。
5. 主要場站至少 8 週且 coverage ≥90% 才允許模型訓練。

## UCI Parking Birmingham

檔案：`historical/parking_birmingham/dataset.csv`。可重現指令：

```powershell
python tools/analyze_uci.py
```

結果：35,717 列、30 場站、4 欄、0 空白儲存格、216 筆完全重複；日期 2016-10-04 至 2016-12-19，各場站 88–1,312 列。間隔不規則並含跨夜缺口。完整結果位於 `uci_quality_report.json`。UCI 只用於原型、QA 與方法驗證，不能當作臺中模型效果證據。

