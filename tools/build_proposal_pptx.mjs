import pptxgen from "pptxgenjs";
import path from "node:path";

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE";
pptx.author = "Smart Parking AI Agent Project";
pptx.subject = "Final Project Proposal";
pptx.title = "智慧停車 AI Agent";
pptx.lang = "zh-TW";
pptx.theme = { headFontFace: "Microsoft JhengHei", bodyFontFace: "Microsoft JhengHei", lang: "zh-TW" };
pptx.defineSlideMaster({
  title: "MASTER",
  background: { color: "F7F9FC" },
  objects: [
    { rect: { x: 0, y: 0, w: 13.333, h: 0.12, fill: { color: "1F4E78" }, line: { color: "1F4E78" } } },
    { text: { text: "智慧停車 AI Agent Proposal", options: { x: 0.45, y: 7.13, w: 5.5, h: 0.18, fontFace: "Microsoft JhengHei", fontSize: 8, color: "65758B" } } },
  ],
  slideNumber: { x: 12.35, y: 7.05, color: "65758B", fontSize: 9 },
});

const C = { navy: "1F4E78", blue: "2E75B6", pale: "EAF2F8", ink: "17202A", gray: "65758B", green: "2E7D5B", amber: "B06A00", red: "B23A48", white: "FFFFFF" };

function title(slide, text, kicker="") {
  if (kicker) slide.addText(kicker, { x: .55, y: .35, w: 2.2, h: .25, fontSize: 10, bold: true, color: C.blue, charSpacing: 1.5, margin: 0 });
  slide.addText(text, { x: .55, y: .66, w: 12.1, h: .55, fontSize: 25, bold: true, color: C.ink, margin: 0, breakLine: false });
}
function bullets(slide, items, x=.7, y=1.45, w=5.9, h=5.2, fs=18) {
  const runs=[];
  items.forEach((t,i)=>{ runs.push({text:t, options:{bullet:{indent:18}, hanging:4, breakLine:i<items.length-1}}); });
  slide.addText(runs,{x,y,w,h,fontSize:fs,color:C.ink,breakLine:false,margin:.08,paraSpaceAfterPt:10,fit:"shrink",valign:"top"});
}
function card(slide, x,y,w,h,head,body,color=C.blue) {
  slide.addShape(pptx.ShapeType.roundRect,{x,y,w,h,rectRadius:.05,fill:{color:C.white},line:{color:"D6E1EA",width:1}});
  slide.addShape(pptx.ShapeType.rect,{x,y,w:.08,h,fill:{color},line:{color}});
  const compact = h < 1.25;
  slide.addText(head,{x:x+.25,y:y+(compact?.12:.18),w:w-.45,h:compact?.27:.35,fontSize:compact?14.5:16,bold:true,color,margin:0,fit:"shrink"});
  slide.addText(body,{x:x+.25,y:y+(compact?.48:.68),w:w-.45,h:compact?Math.max(.22,h-.57):h-.84,fontSize:compact?10.5:13.5,color:C.ink,margin:0.02,fit:"shrink",valign:"top",breakLine:false});
}
function arrow(slide,x1,y1,x2,y2){slide.addShape(pptx.ShapeType.line,{x:x1,y:y1,w:x2-x1,h:y2-y1,line:{color:C.blue,width:2,beginArrowType:"none",endArrowType:"triangle"}})}

// 1
{
 const s=pptx.addSlide("MASTER");
 s.background={color:"F7F9FC"};
 s.addText("智慧停車 AI Agent",{x:.7,y:1.35,w:11.9,h:.75,fontSize:34,bold:true,color:C.navy,align:"center",margin:0});
 s.addText("臺中停車可用性預測與風險感知推薦",{x:.7,y:2.25,w:11.9,h:.55,fontSize:23,color:C.ink,align:"center",margin:0});
 s.addText("Final Project Proposal｜AI Agent + Domain Knowledge + Data Analytics",{x:1.3,y:3.15,w:10.7,h:.35,fontSize:15,color:C.gray,align:"center",margin:0});
 s.addShape(pptx.ShapeType.line,{x:3.1,y:3.85,w:7.1,h:0,line:{color:C.blue,width:2}});
 s.addText("Proposal 階段：控制流程與資料 QA 已驗證；臺中模型成效仍為 Planned / Unverified",{x:1.2,y:4.35,w:10.9,h:.7,fontSize:16,bold:true,color:C.green,align:"center",margin:.05,fit:"shrink"});
}

// 2
{
 const s=pptx.addSlide("MASTER"); title(s,"問題、動機與研究目標","INTRODUCTION");
 card(s,.65,1.55,3.85,2.0,"即時不等於抵達時","目前有空位，抵達時仍可能滿位；推薦必須對齊 arrival time。",C.red);
 card(s,4.75,1.55,3.85,2.0,"資料來源異質","路邊單格、路外場站與 TDX 的粒度、時間戳與狀態語意不同。",C.amber);
 card(s,8.85,1.55,3.85,2.0,"決策需要失敗處理","API timeout、stale data 或低信心時，系統須 replan、abstain 或人工確認。",C.blue);
 s.addText("研究目標",{x:.7,y:4.15,w:2,h:.4,fontSize:20,bold:true,color:C.navy,margin:0});
 bullets(s,["預測 30 / 60 分鐘可用量與滿位風險","以可追溯證據輸出 Top-k 候選","驗證 Agent 是否優於固定 pipeline"],.9,4.65,11.5,1.7,18);
}

// 3
{
 const s=pptx.addSlide("MASTER"); title(s,"Research Gap、假設與 Agent 必要性","RESEARCH DESIGN");
 card(s,.65,1.45,5.9,1.55,"Empirical data gap","臺中尚缺足夠長、穩定且跨路邊與路外的歷史序列；此為待實證缺口。",C.red);
 card(s,6.78,1.45,5.9,1.55,"Project-specific integration gap","尚需驗證品質感知、抵達風險、重規劃與可追溯推薦的端到端效益。",C.blue);
 bullets(s,["H1：樹模型 MAE 低於 Persistence","H2：校準後風險排序提高 Top-3 Success","H3：Agent 在失敗情境減少無證據建議"],.8,3.45,5.8,2.25,16);
 card(s,6.9,3.45,5.55,2.25,"為何不是固定 Pipeline","需依位置／車種選工具、檢查 freshness、失敗後換來源、低信心轉人工、抵達後再驗證。若 Agent 無增益，Go/No-Go 規則要求退回簡單 pipeline。",C.green);
 s.addText("H1–H3 皆為 Planned，未虛構實驗結果。",{x:.85,y:6.1,w:11.4,h:.35,fontSize:15,bold:true,color:C.red,align:"center",margin:0});
}

// 4
{
 const s=pptx.addSlide("MASTER"); title(s,"Related Work：AI 與停車領域知識","RELATED WORK");
 const rows=[
  ["研究路線","代表證據","本專案採用","限制"],
  ["統計／duration","[5][8]","Persistence、time-aware baseline","跨城市與感測條件不同"],
  ["時空深度模型","[6][7][9][10]","候選模型與空間特徵","需足夠歷史與相同切分比較"],
  ["風險與不確定性","[11]","分散度、freshness、校準 proxy","不宣稱自動分離 epistemic / aleatoric"],
  ["Digital Twin 與決策","[12]","資料—預測—決策—驗證閉環","部署條件不可直接移植"],
 ];
 s.addTable(rows,{x:.7,y:1.5,w:11.95,h:3.7,border:{type:"solid",color:"CBD6E0",pt:1},fill:C.white,color:C.ink,fontSize:14,margin:.08,rowH:.68,colW:[2.0,1.5,4.3,4.15],bold:false,autoFit:false,breakLine:false});
 s.addText("文獻使用原則：關鍵主張只採原始來源；[8] 頁碼與 DOI、[11] 限定語、[13] citation／donation 年份均已校正。",{x:.85,y:5.75,w:11.5,h:.75,fontSize:16,bold:true,color:C.navy,align:"center",fit:"shrink",margin:.05});
}

// 5
{
 const s=pptx.addSlide("MASTER"); title(s,"Five Mindsets 與三項爭議","DEEP RESEARCH");
 bullets(s,["資料品質先於模型複雜度","模型必須匹配 forecast horizon","保留路邊與路外的空間／營運語意","先勝過 Persistence 與 Historical Median","不確定性必須進入推薦決策"],.7,1.45,5.7,4.8,16);
 card(s,6.65,1.45,5.9,1.35,"爭議一｜簡單 vs 深度時空模型","證據：[5–10]。以相同時間切分與 baseline 決定，不預設深度模型勝出。",C.blue);
 card(s,6.65,3.0,5.9,1.35,"爭議二｜統一 vs 分開模型","證據：[6–9]。路邊與路外分開預測，只在推薦層統一分數。",C.amber);
 card(s,6.65,4.55,5.9,1.35,"爭議三｜點預測 vs 風險推薦","證據：[11]。使用校準後滿位機率，不誤稱完整 uncertainty decomposition。",C.green);
}

// 6 & 7 questions
for (const [idx,qs] of [[1,["Q1 Why｜為何 arrival-time prediction 比即時顯示更符合決策？","Q2 Evidence｜臺中歷史長度、缺口與來源穩定度是否足夠？","Q3 What-if｜主要 API timeout 或 stale 時如何 replan？","Q4 Trade-off｜較近高風險與較遠穩定如何權衡？","Q5 Failure case｜狀態錯誤或重複主鍵如何污染聚合？"]],[2,["Q6 Comparison｜Agent 的增益是否大於複雜度？","Q7 Leakage｜哪些外部／rolling 特徵在 cutoff 後才可得？","Q8 Transfer｜Birmingham 哪些結論不能移轉到臺中？","Q9 Ground truth｜抵達時間如何配對合法觀測？","Q10 Decision｜何種校準、Top-k 與延遲才符合 Go？"]]]) {
 const s=pptx.addSlide("MASTER"); title(s,`Ten Deep Questions ${idx}/2`,"DEEP RESEARCH");
 qs.forEach((q,i)=>card(s,.85,1.42+i*1.03,11.65,.82,q.split("｜")[0],q.split("｜")[1],i%2?C.green:C.blue));
}

// 8 data
{
 const s=pptx.addSlide("MASTER"); title(s,"資料來源、主鍵與品質證據","DATA");
 card(s,.65,1.4,3.85,2.25,"臺中路邊 snapshot","10,143 車格｜367 路段\nPS_ID 僅 391 unique\n複合鍵 Section_ID + PS_ID 全部唯一\nstatus 0/1/2 = 2,733/7,410/0",C.blue);
 card(s,4.75,1.4,3.85,2.25,"臺中路外與 TDX","市府路外 1,417 筆\nTDX Availability 1,121 筆\n固定更新頻率：Unverified\n以 DataCollectTime 實測，不假設 10 分鐘",C.amber);
 card(s,8.85,1.4,3.85,2.25,"UCI Birmingham QA","35,717 列｜30 場站\n0 空白 cell｜216 exact duplicates\n2016-10-04 至 12-19\n每場站 88–1,312 列且含時間缺口",C.green);
 s.addText("歷史擷取契約",{x:.7,y:4.25,w:2.5,h:.4,fontSize:20,bold:true,color:C.navy,margin:0});
 bullets(s,["Snapshot key = source + Section_ID + PS_ID + observed_at","狀態 0 / 1 / 2 / unknown 分開聚合；unknown 不當空位","只追加 raw payload；保存 source time、ingested_at、HTTP status、hash 與 schema version"],.9,4.7,11.5,1.7,15.5);
}

// 9 architecture
{
 const s=pptx.addSlide("MASTER"); title(s,"Agent Architecture","PROPOSED SCHEME");
 const nodes=["User / GIS","Planner","Tool Selection","Connectors","Quality Gate","Features","Model / Baseline","Risk Rules","Top-k + Evidence"];
 nodes.forEach((n,i)=>{const row=Math.floor(i/5), col=i%5; const x=.45+col*2.55, y=1.55+row*2.15; card(s,x,y,2.15,1.05,`${i+1}`,n,i===4?C.red:(i===1||i===2?C.green:C.blue)); if(i%5<4 && i<nodes.length-1) arrow(s,x+2.15,y+.52,x+2.48,y+.52);});
 arrow(s,10.85,2.68,2.6,3.7);
 s.addText("Quality failure → Retry / Replan → Planner　｜　Low confidence → Human Review　｜　Output → Arrival Verification → Planner",{x:.75,y:5.95,w:11.8,h:.55,fontSize:15,bold:true,color:C.red,align:"center",fit:"shrink",margin:.03});
}

// 10 flow
{
 const s=pptx.addSlide("MASTER"); title(s,"Decision、Loop、Exception 與 Human Interaction","FLOWCHART");
 const left=[["1 Plan","目的與成功條件"],["2 Select","依能力與健康度選工具"],["3 Validate","schema / time / capacity"],["4 Predict","validated model 或 baseline"]];
 left.forEach((a,i)=>card(s,.75,1.35+i*1.25,4.1,.95,a[0],a[1],i===2?C.red:C.blue));
 const right=[["Retryable?","Retry / Replan 回 Select"],["Unrecoverable?","Human Review 回 Plan"],["Confidence OK?","No → Human Review"],["Post-verify","Drift → 回 Plan"]];
 right.forEach((a,i)=>card(s,7.9,1.35+i*1.25,4.1,.95,a[0],a[1],i<3?C.amber:C.green));
 for(let i=0;i<4;i++) arrow(s,4.85,1.83+i*1.25,7.85,1.83+i*1.25);
 s.addText("所有分支均寫入 evidence log；無有效資料時 abstain，不產生建議。",{x:1.5,y:6.45,w:10.3,h:.35,fontSize:16,bold:true,color:C.navy,align:"center",margin:0});
}

// 11 pseudocode
{
 const s=pptx.addSlide("MASTER"); title(s,"Pseudocode 與 Critical Bug 修復","ALGORITHM");
 const code=["plan ← Planner(query, tools)","while task exists:","  tool ← SelectTool(plan, health)","  try raw ← tool.Call()","  catch retryable: plan ← Replan(); continue","  obs ← ValidateSchemaTimeCapacity(raw)","  if empty: replan or HumanReview","for each observation o:","  features ← BuildPastOnlyFeatures(o)","  forecast ← ValidatedModel or Persistence","  forecast.risk ← EstimateFullRisk(forecast, o.quality)","R ← CalibrateAndRankTopK(forecasts)","if LowConfidence(R): HumanReview","LogForArrivalVerification(R); return R"];
 s.addText(code.join("\n"),{x:.7,y:1.4,w:7.25,h:5.4,fontFace:"Consolas",fontSize:15,color:C.ink,fill:{color:"F0F4F8"},line:{color:"C9D6E2"},margin:.18,breakLine:false,fit:"shrink"});
 card(s,8.25,1.4,4.35,1.55,"C1 修復","每個 forecast 使用該 observation 自身的 o.quality，不再沿用上一迴圈變數。",C.red);
 card(s,8.25,3.2,4.35,1.55,"獨立測試","fresh 與 older 候選可用量相同時，older 的 full risk 必須較高。",C.green);
 card(s,8.25,5.0,4.35,1.35,"分支測試","timeout → fallback replan；stale-only → human_review_required。",C.blue);
}

// 12 evaluation
{
 const s=pptx.addSlide("MASTER"); title(s,"預測與推薦驗證方案","EVALUATION");
 card(s,.65,1.4,3.85,1.5,"時間切分","60% train / 20% validation / 20% test；duplicate group 不跨 split。",C.blue);
 card(s,4.75,1.4,3.85,1.5,"Baseline","Persistence、同星期同時段 Historical Median；複雜模型先證明增益。",C.green);
 card(s,8.85,1.4,3.85,1.5,"Leakage 防護","lag、rolling、活動與天氣只能使用 cutoff 前已知資訊。",C.red);
 card(s,.65,3.25,3.85,1.5,"風險與校準","滿位 Recall ≥ .80；PR-AUC、Brier、ECE、reliability diagram。",C.amber);
 card(s,4.75,3.25,3.85,1.5,"Ground Truth","抵達後容許窗內第一筆合法觀測；無資料即 missing。",C.blue);
 card(s,8.85,3.25,3.85,1.5,"Top-k 與 Ablation","Top-k Success、MRR、coverage；移除 feature、quality、calibration、replan、planning。",C.green);
 s.addText("Test set 僅在模型與門檻鎖定後使用一次。",{x:1.6,y:5.45,w:10.1,h:.45,fontSize:18,bold:true,color:C.navy,align:"center",margin:0});
}

// 13 feasibility
{
 const s=pptx.addSlide("MASTER"); title(s,"Go / No-Go 與資料不足替代方案","FEASIBILITY");
 bullets(s,["≥ 8 週臺中歷史，主要場站 coverage ≥ 90%","MAE 優於 Persistence ≥ 5%","滿位 Recall ≥ 0.80","Top-3 Success 優於距離排序 ≥ 5 個百分點","校準後 Brier 改善，p95 回應 ≤ 3 秒"],.75,1.4,5.65,4.6,16);
 card(s,6.75,1.45,5.55,2.05,"Go","所有關鍵資料與效能條件通過，才擴大場站與 GIS Demo。",C.green);
 card(s,6.75,3.8,5.55,2.05,"No-Go / Safe Alternative","縮小至資料穩定場站；只顯示即時資訊與風險提示；或退回固定 pipeline。",C.red);
}

// 14 implementation
{
 const s=pptx.addSlide("MASTER"); title(s,"真正的 Repository 與可執行原型","IMPLEMENTATION");
 const rows=[
  ["模組","實作","驗證"],
  ["API Connector","src/connectors/http_json.py","timeout / HTTP / JSON"],
  ["Quality","src/preprocessing/quality.py","schema / freshness / capacity"],
  ["Baseline","src/prediction/baseline.py","capacity-bounded persistence"],
  ["Agent","src/agent/orchestrator.py","replan / human / evidence"],
  ["UCI QA","tools/analyze_uci.py","duplicate / gap / coverage"],
 ];
 s.addTable(rows,{x:.8,y:1.45,w:11.7,h:4.1,border:{type:"solid",color:"CBD6E0",pt:1},fill:C.white,color:C.ink,fontSize:15,margin:.08,rowH:.62,colW:[2.3,5.1,4.3],breakLine:false});
 s.addText("python -m unittest discover -s tests -v　→　9 tests OK",{x:1.1,y:5.95,w:11.1,h:.55,fontFace:"Consolas",fontSize:18,bold:true,color:C.green,align:"center",margin:0});
}

// 15 status
{
 const s=pptx.addSlide("MASTER"); title(s,"Proposal 與期末實作界線","STATUS");
 card(s,.75,1.45,5.8,3.95,"Implemented / Verified","• Git repository\n• Connector、Quality、Persistence\n• Agent retry/replan/human/evidence\n• 9 項自動化測試\n• UCI 品質報告\n• 臺中單次 schema 與 snapshot 統計",C.green);
 card(s,6.8,1.45,5.8,3.95,"Planned / Unverified","• 臺中至少 8 週歷史\n• H1–H3 模型效果\n• Top-k 改善與 calibration\n• 線上 API SLA 與固定更新頻率\n• GIS Demo 與 p95 效能",C.amber);
 s.addText("不把 Proposal 設計或 Expected Outcome 寫成已完成實驗結果。",{x:1.2,y:5.95,w:10.9,h:.45,fontSize:18,bold:true,color:C.red,align:"center",margin:0});
}

// 16 closing
{
 const s=pptx.addSlide("MASTER"); title(s,"結論與下一個驗證里程碑","CONCLUSION");
 bullets(s,["把停車問題從『現在有位』改成『抵達時的風險決策』","Architecture、Flowchart、Pseudocode 與原型採相同 Agent 狀態語意","資料品質、baseline、校準、Top-k 與 ablation 均預先定義","先建立臺中歷史並通過 Go/No-Go，再宣稱模型與推薦效益"],.9,1.5,11.5,3.8,19);
 s.addShape(pptx.ShapeType.roundRect,{x:2.1,y:5.45,w:9.1,h:.8,fill:{color:C.navy},line:{color:C.navy},radius:.05});
 s.addText("Evidence first　｜　Abstain when uncertain　｜　Verify after arrival",{x:2.25,y:5.68,w:8.8,h:.3,fontSize:17,bold:true,color:C.white,align:"center",margin:0});
}

const out = path.resolve("proposal", "智慧停車AI_Agent_Proposal.pptx");
await pptx.writeFile({ fileName: out });
console.log(out);

