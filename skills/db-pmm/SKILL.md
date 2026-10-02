---
name: db-pmm
description: PMM 蝴蝶蘭產銷管理系統：苗株／盆花／切花的生產批次、庫存移轉、需求單、配貨、出貨、採購契作、客戶、花色、死亡、移轉原因與品種主檔
db: pmm
tables: >-
  View_苗株庫存數量, View_盆花庫存數量, View_盆花規格庫存數量, View_切花出貨一課庫存數量,
  View_YPTransferRecord, View_CFTransferRecord, View_PPTransferRecord,
  RB_View_PPTransferRecord, View_vpCFReasonRecord, RB_View_YPTransferDetial,
  RB_View_CFTransferDetial, RB_View_PPTransferDetial, View_vpCFRecord_sum,
  RB_View_ShippingVolume, View_CFTransferBatch, RB_View_YPBacthInfo,
  View_PPShipDetail, View_CFDistribution, RB_View_SamplingSurvey_Main,
  RB_View_SamplingSurvey_Detial, View_CFShipRequirement, View_YPProductionBatchProcessLog,
  View_PPOrderPackingSetting, View_PPOrderPackingSettingDetail, View_PPShipPackingSetting,
  View_PPShipPackingSettingDetail, View_PPStemSurvey, View_PPStemSurveyMap,
  View_CFQuarantine, RB_View_CFHarvestDetial, View_PPBudSurvey,
  View_PPBudSurveyMap, RB_View_CFStemNumberSurvey, RB_View_CFStemmingSurvey,
  View_CFStemSurvey, View_CFStemSurveyMap, View_RBYPPickingRecord,
  View_YPShipPlan, View_YPShipRecord, View_CFShipSurvey,
  RB_View_RB_PPTwelveSurvey_RawList, View_MonthlyFile, View_ShipUnThrowCount,
  View_BISpec, View_BIProcess, View_BIProductLine,
  View_BISupplier, RB_View_BreedWithAliasWithColor, View_BreedAliasWithSupplier,
  View_GreenhouseStock, RB_View_YPInventory,
  BIBreed, BIBreedAlias, BIColor, BIColorCategory, BICustomer, BIMedium, BIPPPackingCondition, BIPackingColor,
  BIPackingSize, BIPersonel, BIPersonelProductionLineMap, BIPosition, BIPot, BIPrintField, BIProcess,
  BIProductionLine, BIProductionLinePrintFieldMap, BIProductionLineReasonMap, BIReason, BIReasonDesc,
  BIShipPacking, BIShipPackingMap, BISpec, BISupplier, BISystemOption, BIUploadFile, BSPersonalRoleMap, BSRole,
  BSRoleFunctionMap, CFDistribution, CFDistributionDetail, CFDistributionOrderDetailMap, CFHarvest,
  CFHarvestQuarantine, CFHarvestRecord, CFOrder, CFOrderDetail, CFSampleDetail, CFSampleRecord, CFSampleSurvey,
  CFShip, CFShipDetail, CFShipDistributionDetailMap, CFShipSurvey, CFShipSurveyDetail, CFShipSurveyDetail_HF,
  CFShipSurveyMap, CFStemSurvey, CFStemSurveyDetail, CFStemSurveyMap, CFStemSurveyMapLog, CFTransferBatch,
  CFTransferRecord, LCExecutedSQL, LCVersion, PPBudSurvey, PPBudSurveyDetail, PPBudSurveyMap, PPDistribution,
  PPDistributionDetail, PPDistributionOrderDetailMap, PPOrder, PPOrderDetail, PPOrderNotice,
  PPOrderPackingSetting, PPOrderPackingSettingDetail, PPShipDetail, PPShipPackingSetting,
  PPShipPackingSettingDetail, PPStemSurvey, PPStemSurveyDetail, PPStemSurveyMap, PPTransferBatch,
  PPTransferRecord, PPTransferRecordTemp, PPTransferTask, PPTransferTaskMap, SCPurchaseOrder,
  SCPurchaseOrderDetail, SCUnderContract, SCUnderContractRecord, SCUnderContractVisit, YPDistribution,
  YPDistributionPlan, YPPicking, YPPickingPlan, YPPickingPlanAllocation, YPPickingRecord, YPPickingRegular,
  YPPickingRegularRecord, YPProductionBatch, YPPurchase, YPShipPlan, YPShipRecord, YPTransferRecord,
  YPTransferRecordTemp, YPTransferTask, View_BreedAlias, View_CF_OrderAndDistribution, View_CF_OrderDistShipRelation,
  View_CF_TransferAndDistribution, View_CFDistribution_All, View_CFDistribution_Sum, View_CFSampleSurvey_All, View_CFShipAndDetail,
  View_CFShipAndDist, View_CFShipSurvey_HF_All, View_CFShipSurvey_Roll_All, View_CFShipSurveyMap_Roll, View_CFStemSurvey_All,
  View_CFShipSurveyMap_HF, View_CFTransferBatch_Sum, View_CFTransferRecord_Sync, View_PersonelPermission, View_PPBudSurvey_All,
  View_PPDistribution_All, View_PPDistribution_All_WithName, View_PPDistribution_Sum, View_PPStemSurvey_All, View_PPTransferBatch_Sum_P,
  View_PPTransferRecord_Sync, View_Rpt_CF002, View_Rpt_CF004, View_SCPurchaseOrder_Sync, View_SCUnderContract_Sync, View_ShipPacking,
  View_YPProductionBatch_sum, YPProductionBatchProcessLog, YPTransferRecord_All
---
# PMM 蝴蝶蘭產銷管理系統（source=pmm，DB：RBMS）

> 可查的表以本檔標頭的 `tables:` 為準（IT 可在 `.env` 用 `SQL_PMM_DENY_TABLES` 再擋掉部分表）。
> 欄位名稱請用 `describe_table` 現查，不要憑印象寫。
> 標「實測」的數字與結論都在 RBMS 上驗證過；標「業務定義」的是業務單位給的規則，資料庫裡沒有這份對照表。

## 查詢前必做的三個判斷

PMM 同一個詞在不同階段指的是不同資料，問法不夠具體就直接查，答案會錯。先確認這三件事，缺哪一項就**先問使用者，不要自己挑一個**：

1. **哪個業務階段**——苗株栽培／採收後商品庫存／訂單出貨（見「栽培階段 vs 出貨階段」）
2. **哪條產線**——台灣／越南種苗／越南切花／越南盆花（見「產線」）
3. **哪個分析對象與期間**——良率、歷史變化、訂單供貨都必須有對象（品種／批次／規格／產線）和日期範圍

澄清要**一次把選項列出來**，不要只問「請問是哪一個」：

> 請問您要查哪個栽培階段的苗株庫存？
> 1. 台灣（彰化生產部、台灣契作產線、種原課）
> 2. 越南種苗課　3. 越南切花課　4. 越南盆花課　5. 全部產線

**這些情況不用問，直接查：**

- 使用者已經講了產線、品種、批號或日期，條件夠了。
- 問的是**主檔**（某品種是什麼、花色代號有哪些、規格有哪些、移轉原因有哪些）——主檔不分產線。
- 使用者明講「全部」「總共」——查全部，但回答要**附各產線明細**，不要只丟一個總數。

## 栽培階段 vs 出貨階段

**最容易答錯的一件事。**同一個「切花庫存」可能是兩種完全不同的資料：

| 階段 | 意思 | 主要資料表 | 單位 |
|------|------|-----------|------|
| **苗株栽培** | 還在溫室／床位／生產批次裡長的苗 | `YPProductionBatch`、`YPTransferRecord` | 株（組培規格是瓶，見下） |
| **切花商品** | 已採收、包裝、可出貨 | `CFTransferBatch`、`CFTransferRecord`、`CFHarvest`、`CFHarvestRecord` | 支 |
| **盆花商品** | 已進入出貨流程 | `PPTransferTask`、`PPTransferBatch`、`PPTransferRecord` | 盆 |

- 栽培階段的「切花課／盆花課」（`ProductionLineID` 3／4）指的是**那批苗養在切花或盆花產線**，不是採收後的商品。
- **兩者不可相加、不可互相比較**，單位和業務意義都不同。
- 使用者說「切花庫存有多少」而沒講清楚時，要先問：
  > 請問您要查的是：1. 還在溫室栽培中的切花產線苗株　2. 已採收包裝、可出貨的切花商品（單位：支）

## 模組前綴
- `BI` 基本主檔（品種、客戶、人員、產線…）｜`BS` 角色與權限｜`LC` 系統版本與異動紀錄
- `CF` 切花（Cut Flower）｜`PP` 盆花（Potted Plant）｜`YP` 苗株（Young Plant）｜`SC` 採購與契作

## 資料表對照
**BI 基本主檔**：BIBreed 品種、BIBreedAlias 品種別名、BIColor 花色、BIColorCategory 花色類別、BICustomer 客戶、BIMedium 介質、BIPPPackingCondition 盆花包裝條件、BIPackingColor 包裝顏色、BIPackingSize 包裝大小、BIPersonel 人員帳號、BIPersonelProductionLineMap 人員產線關聯、BIPosition 位置、BIPot 盆器、BIPrintField 列印標貼、BIProcess 製程、BIProductionLine 產線、BIProductionLinePrintFieldMap 產線標貼關聯、BIProductionLineReasonMap 產線移轉原因關聯、BIReason 移轉原因、BIReasonDesc 移轉詳細原因、BIShipPacking 出貨包裝、BIShipPackingMap 出貨包裝入數、BISpec 規格、BISupplier 廠商、BISystemOption 系統選項、BIUploadFile 上傳檔案

**BS／LC**：BSPersonalRoleMap 人員角色對應、BSRole 角色、BSRoleFunctionMap 角色功能權限、LCExecutedSQL 已執行的更新 SQL、LCVersion 資料庫版本

**CF 切花**：CFOrder 需求單、CFOrderDetail 需求單明細、CFDistribution 配貨單、CFDistributionDetail 配貨明細、CFDistributionOrderDetailMap 配貨↔需求單明細關聯、CFShip 出貨、CFShipDetail 出貨明細、CFShipDistributionDetailMap 出貨↔配貨關聯、CFHarvest 採收、CFHarvestRecord 採收記錄、CFHarvestQuarantine 採收汰除、CFSampleSurvey 抽梗調查、CFSampleRecord 抽梗調查明細、CFSampleDetail 抽梗梗數明細、CFStemSurvey 點梗調查、CFStemSurveyDetail 點梗明細、CFStemSurveyMap 點梗梗數明細、CFStemSurveyMapLog 點梗明細歷程、CFShipSurvey／CFShipSurveyDetail／CFShipSurveyMap 出貨調查、CFShipSurveyDetail_HF 出貨調查(高朵數)、CFTransferBatch 批次明細、CFTransferRecord 移轉記錄明細

**PP 盆花**：PPOrder 需求單、PPOrderDetail 需求單明細、PPOrderNotice 訂單包裝注意事項、PPOrderPackingSetting／PPOrderPackingSettingDetail 訂單包裝設定、PPDistribution 配貨、PPDistributionDetail 配貨明細、PPDistributionOrderDetailMap 配貨↔需求單明細關聯、PPShipDetail 出貨明細、PPShipPackingSetting／PPShipPackingSettingDetail 出貨包裝設定、PPBudSurvey 打荳調查、PPBudSurveyDetail 打荳明細、PPBudSurveyMap 打荳來源、PPStemSurvey 來梗調查、PPStemSurveyDetail 來梗明細、PPStemSurveyMap 來梗來源、PPTransferBatch 批次、PPTransferRecord 移轉記錄、PPTransferRecordTemp 移轉暫存(未核准)、PPTransferTask 移轉任務、PPTransferTaskMap 移轉任務關聯

**YP 苗株**：YPProductionBatch 生產批次、YPPurchase 進貨任務、YPPicking 挑苗、YPPickingPlan 挑苗排程、YPPickingPlanAllocation 配貨挑苗、YPPickingRecord 挑苗記錄、YPPickingRegular／YPPickingRegularRecord 日常挑苗、YPDistribution／YPDistributionPlan 配貨、YPShipPlan 配貨出貨列表、YPShipRecord 配貨出貨明細、YPTransferRecord 移轉記錄、YPTransferRecordTemp 移轉暫存、YPTransferTask 移轉任務

**SC 採購契作**：SCPurchaseOrder 採購單、SCPurchaseOrderDetail 採購單明細、SCUnderContract 契作批次、SCUnderContractVisit 契作訪視、SCUnderContractRecord 契作訪視記錄

**檢視表（關聯複雜的報表優先用這些）**：View_BreedAlias 品種花色關聯、View_PersonelPermission 帳號角色權限、View_CF_OrderAndDistribution 切花訂單配貨、View_CF_OrderDistShipRelation 切花訂單配貨出貨、View_CF_TransferAndDistribution 切花移轉配貨、View_CFDistribution_All 配貨明細、View_CFDistribution_Sum 配貨數 BY 客戶、View_CFTransferBatch_Sum 切花庫存明細、View_CFShipAndDetail 出貨明細、View_CFShipAndDist 出貨與配貨、View_CFSampleSurvey_All 抽梗調查明細、View_CFStemSurvey_All 點梗調查明細、View_CFShipSurvey_HF_All 高朵數出貨調查、View_CFShipSurvey_Roll_All／View_CFShipSurveyMap_Roll 抽樣點花、View_CFShipSurveyMap_HF 點梗高朵數、View_PPBudSurvey_All 打荳調查、View_PPStemSurvey_All 來梗調查、View_PPDistribution_All／View_PPDistribution_All_WithName 盆花配貨明細、View_PPDistribution_Sum 盆花庫存、View_YPProductionBatch_sum 生產批次庫存、YPProductionBatchProcessLog 翻種製程記錄、View_Rpt_CF002 切花點梗出貨預估、View_Rpt_CF004 切花高朵數出貨預估、View_CFTransferRecord_Sync／View_PPTransferRecord_Sync／View_SCPurchaseOrder_Sync／View_SCUnderContract_Sync 拋轉中介、View_ShipPacking 出貨包裝明細、View_PPTransferBatch_Sum_P 未使用（YPTransferRecord_All 已不存在於資料庫）

## 產線

資料庫裡**沒有 `ProductionID` 這個欄位**，實際欄位是 **`ProductionLineID`**，主檔是 `BIProductionLine`。寫 `ProductionID` 會直接噴「無效的資料行名稱」。

`ProductionLineID` 掛在**批次表**上（`YPProductionBatch`、`PPTransferBatch`、`CFTransferBatch`、`PPTransferRecord`、`BIPosition`），**`YPTransferRecord` 上沒有**——查苗株要先 JOIN `YPProductionBatch`，或直接用 `View_苗株庫存數量`（已經帶了）。

苗株實際有庫存的六條產線（實測，全部移轉記錄淨額）：

| ID | Name | ERPCode / ERPName | 國別 | 苗株庫存 |
|---:|------|------------------|------|---------:|
| 1 | 彰化生產部 | RoyalBase／皇基 | 台灣 | 727,071 |
| 2 | 種苗課 | Apollo／阿波羅 | 越南 | 3,289,729 |
| 3 | 切花課 | Apollo／阿波羅 | 越南 | 935,871 |
| 4 | 盆花課 | Apollo／阿波羅 | 越南 | 424,391 |
| 5 | 台灣契作產線 | RoyalBase／皇基 | 台灣 | 1,060,911 |
| 9 | 種原課 | RoyalBase／皇基 | 台灣 | 44,796 |

另有 6 出貨一課、8 行銷部（虛擬產線）、10 出貨三課（已停用），苗株栽培沒有庫存。

- **「台灣」不等於 `ProductionLineID = 1`。**台灣有 1、5、9 三條，只取 1 會少算六成（實際 1,832,778，只取 1 是 727,071）。
- 分國別請用 **`BIProductionLine.ERPCode`**：`'RoyalBase'`＝台灣（皇基）、`'Apollo'`＝越南（阿波羅）。不要用 ID 範圍硬猜。
- `BIProductionLine.Code` **不是唯一值**（彰化生產部與種苗課都是 `2`），不可拿來當條件或 JOIN 鍵，一律用 `ID`。
- 使用者只說「越南庫存」時，要嘛**分別列出 2／3／4**，要嘛先問要哪一條；不可以自己挑一條。

```sql
-- 台灣苗株庫存（實測合計 1,832,778）
SELECT pl.Name AS 產線, SUM(CAST(v.TotalQuantity AS bigint)) AS 庫存
FROM View_苗株庫存數量 v
JOIN BIProductionLine pl ON v.ProductionLineID = pl.ID
WHERE pl.ERPCode = 'RoyalBase'
GROUP BY pl.Name ORDER BY 2 DESC
```

## 庫存要查哪張表

庫存**不要**自己從生產批次或移轉記錄兜，系統已經有彙總檢視（代號都已翻成名稱）：

| 問什麼 | 用哪張 |
|--------|--------|
| 苗株庫存（栽培階段） | `View_苗株庫存數量` |
| 盆花庫存 | `View_盆花庫存數量`、依規格看用 `View_盆花規格庫存數量` |
| 切花商品庫存 | `View_切花出貨一課庫存數量` |
| 溫室現況（中文欄名） | `View_GreenhouseStock`：`溫室`、`床位`、`移轉日期`、`品種`、`花色`、`切次`、`規格`、`數量`、`移轉原因`、`部門` |

### `View_苗株庫存數量` 一張就夠用

這張檢視**已經把所有維度都併好了**，苗株的「現在有多少」幾乎都不必 JOIN：

| 維度 | 欄位 |
|------|------|
| 產線 | `ProductionLineID`、`ProductionLineName` |
| 溫室／床位 | `PositionID`、`Position1`（溫室）、`Position2`（床位） |
| 批次與血緣 | `BatchNo`、`BatchNoSrc`、`PurchaseDate` |
| 品種 | `BreedAliasID`、`BreedAliasName`、`ParticularName` |
| 花色 | `ColorID`、`ColorCode`、`ColorName` |
| 規格 | `SpecID`、`SpecCode`、`SpecName` |
| 製程／階段 | `ProcessID`、`ProcessName` |
| 介質／盆器 | `MediumID`／`MediumName`、`PotID`／`PotName` |
| 供應商 | `SupplierBottleID`／`Name`（瓶苗來源）、`SupplierSeedlingID`／`Name`（種苗來源） |
| 數量 | `TotalQuantity` |

所以「某溫室有多少庫存」「某批次還剩多少」「哪個溫室最多某品種」**都直接查這張**，不需要走 `YPTransferRecord` → `BIPosition`。

**實測對帳：`SUM(View_苗株庫存數量.TotalQuantity)` = `SUM(YPTransferRecord.Quantity)` = 6,482,770，完全相等。**也就是庫存就是移轉記錄的累計淨額——所以：

- 問「現在有多少」→ 查檢視（快）。
- 問「過去怎麼變化／為什麼變少」→ 查 `YPTransferRecord` 依日期重算，**不可以用現在的庫存回推過去**。

```sql
-- 越南種苗課各溫室床位庫存
SELECT Position1 AS 溫室, Position2 AS 床位, SUM(CAST(TotalQuantity AS bigint)) AS 庫存
FROM View_苗株庫存數量 WHERE ProductionLineID = 2
GROUP BY Position1, Position2 ORDER BY 3 DESC
```

## 苗株規格（BISpec）

比對方式：

- 用 **`SpecCode`**（對應 `BISpec.Code`），**不要用名稱**——`BISpec.Name` 有前導零（`07.5CM`），寫 `Name = '7.5CM'` 查不到。
- 代號是**四位零補齊**的字串：`0084` 不是 `084`、`0075` 不是 `75`。少一位就查不到。
- 同一個尺寸會有**種苗**和**盆花**兩個規格：`0075`＝`07.5CM`（種苗）、`075F`＝`7.5CM盆花`。問「苗株」用 `0075`。
- `BISpec.Remark` 標示類別：`組培`／`組培(AP)`／`種苗`／`盆花`。要抓「全部瓶苗」用 `Remark LIKE N'組培%'` 比列代號可靠。

### 大小分組（業務定義）

業務單位的分組如下。**資料庫裡沒有這張對照表**，是寫在這裡的約定：

| 分組 | `BISpec.Code` |
|------|---------------|
| 瓶苗 | 0040、0041、0042、0043、0044（＋`Remark LIKE N'組培%'` 的其餘代號：0046、1031、1040～1044、1046） |
| 小苗 | 0045、0051 |
| 中苗 | 0075、0081、**0084** |
| 大苗 | 0090、0099、0105 |

使用這份分組時必須注意（實測）：

- **`0084`（08.4CM）屬中苗，庫存 2,205,538 是第二大**。業務文件上寫成 `084` 是漏了前導零，照抄會整組漏掉。
- 分組**沒有涵蓋所有規格**。未分類的有 `0050`(05.0CM)、`0060`(06.0CM)（落在小苗與中苗之間），以及 `0114`、`0120`、`0141`、`0150`、`0210`（比大苗更大）。回答時要**說明用了哪些代號**，使用者才知道有沒有漏。
- 目前有庫存的規格（實測）：0045 ≈ 202 萬、0084 ≈ 221 萬、0099 ≈ 86 萬、0105 ≈ 61 萬、0090 ≈ 46 萬、0075 ≈ 30 萬，瓶苗類合計約 2 萬，`0120`／`0150` 各只有幾十株。`0051`、`0060`、`0081`、`0114`、`0141` 目前為 0。

### 組培與種苗的單位不同（重要）

**瓶苗（`Remark` 為 `組培`）的數量單位是「瓶」，種苗以後是「株」。**實測：翻種時組培規格出 −4,719,623，種苗規格進 +26,383,496，一瓶換出幾十株。

所以：

- **不可以把組培和種苗的數量相加**，加出來沒有意義。
- **「瓶苗到小苗的良率」不能用數量相除**，要先知道每瓶株數的換算，而資料庫裡沒有這個值。遇到這類問題要說明限制並向使用者確認換算基準，不要硬算出一個比例。

```sql
-- 7.5cm 苗株庫存（實測 302,685 株）
SELECT SpecCode, SpecName, SUM(CAST(TotalQuantity AS bigint)) AS 庫存數
FROM View_苗株庫存數量 WHERE SpecCode = '0075' GROUP BY SpecCode, SpecName
```

## 品種、別名與來源業者

同一個品種經 Clone 會產生不同個體，`BIBreedAlias` 記錄這些個體的名稱、代號與來源業者。

| 表 | 一列代表 | 關鍵欄位 |
|----|---------|----------|
| `BIBreed` | **一個品種**（父系／原始品種），實測 2,562 筆 | `Name`、`PartNo`（品種代號）、`ColorID`（花色）、`FlowerSizeType`、`HeightStart`／`HeightEnd` |
| `BIBreedAlias` | **一個品種個體／別名**，實測 2,835 筆、涵蓋全部 2,562 個品種 | `BreedID`→`BIBreed.ID`、`SupplierID`→`BISupplier`（來源業者）、`AliasName`、`ParticularName`、`PartNo`、`IsBreed` |

**所有交易表接的都是 `BreedAliasID`，不是 `BreedID`。**實測 `YPProductionBatch`、`PPTransferBatch`、`PPTransferRecord`、`CFTransferBatch`、`PPOrderDetail` 全部只有 `BreedAliasID`，沒有 `BreedID`。所以「某品種的庫存」必須走兩段：

```
BIBreed.ID → BIBreedAlias.BreedID ；BIBreedAlias.ID → 交易表.BreedAliasID
```

```sql
-- 依品種名稱查苗株庫存（品種可能有多個別名，要先展開再彙總）
SELECT b.Name AS 品種, SUM(CAST(v.TotalQuantity AS bigint)) AS 庫存
FROM BIBreed b
JOIN BIBreedAlias a ON a.BreedID = b.ID
JOIN View_苗株庫存數量 v ON v.BreedAliasID = a.ID
WHERE b.Name LIKE N'%使用者給的品種%'
GROUP BY b.Name
```

使用者可能用**品種名稱／品種代號／別名／個體代號／來源業者**任何一種來問，都要能反查到真正的品種——查不到就同時試 `BIBreed.Name`、`BIBreed.PartNo`、`BIBreedAlias.AliasName`、`BIBreedAlias.ParticularName`、`BIBreedAlias.PartNo`。

- `BIBreed` **沒有 `Code` 欄位**，品種代號是 **`PartNo`**；而且 `PartNo` **不唯一**（實測花色代號 W 的 50 筆品種共用 `2PH0000`），不可當唯一鍵。
- 要列「品種清單」直接查 `BIBreed`。`View_BreedAlias` 是**品種 × 別名**，一個品種多個別名就會多列（例：黃花類別 142 列但只有 117 個品種），拿它列品種一定要 `DISTINCT` 或 `GROUP BY BreedID`，否則筆數虛胖。

## 花色（BIColor）：代號 vs 語意

花色有三個層次，使用者的問法決定要查哪一欄：

| 層次 | 欄位 | 內容 | 例 |
|------|------|------|-----|
| 代號 | `BIColor.Code` | 花色代號（英數） | `W`、`BL-W`、`WSP`、`M-W` |
| 英文名 | `BIColor.Name` | 花色英文全名 | `White`、`Big Lip White`、`White with Spot` |
| 語意分類 | `BIColorCategory.Name`、`ColorType` | **中文**類別名稱；`ColorType` 1＝白花系、2＝色花系 | `白花`、`大唇瓣白花`、`MIDI-白`、`紅花`、`粉花`、`異色花` |

- 使用者講的是**代號**（W、BL-W、M-W…）→ 用 `c.Code = 'W'` 精確比對，不要用 LIKE。
- 使用者講的是**中文顏色語意**（白色、紅花、粉花）→ 走 `BIColorCategory`：
  `JOIN BIColorCategory g ON c.ColorCategoryID = g.ID WHERE g.Name LIKE N'%白%'`（白花系也可用 `g.ColorType = 1`）。
- `BIColor.Name` 是**英文**，`Name LIKE N'%白%'` 永遠查不到；也**不要**用 `Name LIKE '%White%'` 代表「白色」，那會抓到 `White with Spot`（類別其實是異色花）。

同樣問「白色品種」，三種寫法差很多（實測）：

| 寫法 | 品種數 | 適用 |
|------|--------|------|
| `c.Code = 'W'` | 60 | 使用者指定代號 W |
| `g.ColorType = 1`（白花＋大唇瓣白花＋MIDI-白） | 121 | 使用者說「白色」的語意查詢 |
| `c.Name LIKE '%White%'` | 368 | **不要用**，含異色花 |

回答時要說明用的是哪個範圍（例如「花色代號 W」或「白花系（含大唇瓣白花、MIDI-白）」）。

## 批次與批次血緣

`YPProductionBatch` 的 `BatchNo`＝本批批號、`BatchNoSrc`＝來源（上一階）批號。苗在生產中會「上一階批次結束 → 建立新批次」，血緣靠 `BatchNoSrc` 串。

實測三件必須知道的事：

1. **`BatchNo` 不唯一**。105,736 列只有 32,292 個不同批號——`YPProductionBatch` 其實是「批次 × 來源批次 × 規格」的粒度（例：批號 `D10005` 有 109 列、96 個來源批號、6 種規格；一個新批次是由多個來源批次併進來的）。算數量時一定要 `GROUP BY`／`SUM()`，不要以為一個批號一列。
2. **`BatchNo` 與 `BatchNoSrc` 的定序不同**，直接 JOIN 會**直接報錯**：
   `BatchNo` 是 `SQL_Latin1_General_CP1_CS_AS`、`BatchNoSrc` 是 `Chinese_Taiwan_Stroke_CI_AS`
   → `無法解析 equal to 作業中 ... 之間的定序衝突`。追血緣必須兩邊都加 `COLLATE`。
3. **`BatchNo` 的定序區分大小寫**（`..._CS_AS`）。`WHERE BatchNo = 'd10005'` 回 **0 筆**，`'D10005'` 回 109 筆。使用者打的批號大小寫不一定對，所以比對批號時**一律加 `COLLATE Chinese_Taiwan_Stroke_CI_AS`**。
4. `BatchNoSrc` **不會是 NULL 或空字串**（實測 105,736 筆全部有值），所以不能用「`BatchNoSrc` 是空的」來判斷最初批次。

```sql
-- 追某批次的上一階來源（注意兩邊都要 COLLATE）
SELECT c.BatchNo AS 本批, c.BatchNoSrc AS 來源批號,
       SUM(CAST(v.TotalQuantity AS bigint)) AS 本批庫存
FROM YPProductionBatch c
LEFT JOIN View_苗株庫存數量 v ON v.BatchNo = c.BatchNo AND v.BatchNoSrc = c.BatchNoSrc
WHERE c.BatchNo COLLATE Chinese_Taiwan_Stroke_CI_AS = N'使用者給的批號'
GROUP BY c.BatchNo, c.BatchNoSrc
```

> 跨階層一路串 `BatchNoSrc = BatchNo` 會**暴量**（實測一次自我 JOIN 就從 105,736 列變成 1,224,868 列），因為批號不唯一。要追多階請一階一階查並彙總，不要寫遞迴 CTE 一次串完。

## 溫室與床位

`BIPosition` 是位置主檔：`Position1`＝**溫室**、`Position2`＝**床位**，另有 `ProductionLineID`、`IsEnable`。
`YPTransferRecord.PositionID` → `BIPosition.ID`。

但問「現在的」溫室／床位庫存**直接用 `View_苗株庫存數量`**（已含 `Position1`／`Position2`），不必 JOIN。只有要看「某天移到哪個床位」這種歷史軌跡才回 `YPTransferRecord` + `BIPosition`。

## 數量異動原因

每一筆數量進出都記在移轉記錄表，原因存成代號，要 JOIN 原因主檔才看得懂：

| 類別 | 移轉記錄表 | 數量欄位 | 主鍵 | 原因欄位 |
|------|-----------|----------|------|----------|
| 苗株 | `YPTransferRecord` | `Quantity` | `ID` | `ReasonID` + `ReasonDescID` |
| 切花 | `CFTransferRecord` | `TransferQuantity` | `ID` | `ReasonID` + `ReasonDescID` |
| 盆花 | `PPTransferRecord` | `TransferQuantity` | **`RecordID`** | **只有 `ReasonDescID`** |

### `BIReason.TransferType` 決定是哪個模組（關鍵）

`BIReason` 57 列裡**同一個 `Code`／`Name` 會重複出現**，因為 `TransferType` 區分模組（實測，各模組只用自己那一型）：

| TransferType | 模組 | 用在 | 實測筆數 |
|---:|------|------|---------:|
| 1 | 苗株 YP | `YPTransferRecord.ReasonID` | 1,648,920 |
| 2 | 切花 CF | `CFTransferRecord.ReasonID` | 850,266 |
| 3 | 盆花 PP | `PPTransferTask.ReasonID` | 420,811 任務 |

所以：

- JOIN 一律用 **`ID`**，不要用 `Code` 或 `Name`（例：`死亡` 有 ID 3／TransferType 1 和 ID 30／TransferType 3 兩列）。
- 要**列出某模組有哪些原因**時必須加 `WHERE TransferType = ?`，否則會把別的模組的原因一起列出來。
- `ReasonDescID` → **`BIReasonDesc`**（細分原因，`BIReasonDesc.ReasonID` 指回主原因）。`Description` 是**越南文＋中文並列**（死亡底下有「Nhũn 軟腐」「Đen gốc 黑頭」「Vi rút 病毒」「Thối rễ 敗根」），用中文關鍵字要 `LIKE N'%軟腐%'`。可能為空，所以用 **LEFT JOIN**。
- **`PPTransferRecord` 沒有 `ReasonID`**——盆花主原因記在任務上，要 `JOIN PPTransferTask ON PPTransferRecord.TaskID = PPTransferTask.TaskID`，再用 `PPTransferTask.ReasonID` 接 `BIReason`。

### 苗株各原因的性質（實測全期淨額）

**數量帶正負號**：增加為正、減少為負，`SUM()` 直接就是淨異動量，不要自己判斷方向。但**負數不等於損耗**，必須照原因分類：

| 性質 | 原因（`TransferType = 1`） | 全期淨額 |
|------|------|---------:|
| **起始投入** | R08 進貨 | +34,248,998 |
| **階段轉入**（非損耗） | R05 翻種 | +21,661,940 |
| **真實損耗** | R03 死亡 | −4,888,767 |
| | R04 切花後汰除 | −6,794,860 |
| | R07 瓶苗出瓶一個月汰除 | −332,961 |
| | R38 瑕疵品 | −351,310 |
| | R16 盤虧 | −28,518 |
| | R10 異動性減 | −75,739 |
| | R06 海關檢疫 | −4,318 |
| | R36 盆花分級 | −24,422 |
| **出貨／銷售**（非損耗） | R02 其他出貨 | −16,019,448 |
| | R01 配貨出貨(外銷) | −9,563,868 |
| | R29 其他出貨(內銷) | −7,760,781 |
| **移到別的模組**（非損耗） | R21 跨組移轉 | −4,519,204 |
| **盤點調整** | R15 盤盈 | +399,325 ／ R09 異動性增 +538,012 |
| **淨額為零的純搬移** | R11 部門間移轉、R12 部門內移轉、R13 進催、R14 換床回養、R31 批號變更、R33 品種變更、R34 規格變更 | ≈ 0 |

重點：

- **R12 部門內移轉筆數最多（439,164 筆）但淨額為 0**，純粹換位置。做損耗分析時先排除這些淨零原因，查詢會快很多也不會誤導。
- **R21 跨組移轉在苗株是負的（全期 −4,519,204），在盆花是正的（全期 +4,519,324）**——兩邊幾乎完全互為鏡像，證明它就是苗株交給盆花／切花的交接，**不是損失**。做苗株損耗分析時把它算進損耗，會多算 450 萬株。
- **R05 翻種的正負不對稱**：組培規格為負、種苗規格為全正（見「組培與種苗的單位不同」），整體 +21,661,940。**不能當成淨零搬移處理。**

```sql
-- 苗株近一年各原因的異動量（含細分原因）
SELECT r.Name AS 原因, d.Description AS 細分原因,
       SUM(CAST(t.Quantity AS bigint)) AS 異動數量, COUNT(*) AS 筆數
FROM YPTransferRecord t
JOIN BIReason r ON t.ReasonID = r.ID
LEFT JOIN BIReasonDesc d ON t.ReasonDescID = d.ID
WHERE t.TransferDate >= DATEADD(year, -1, GETDATE())
GROUP BY r.Name, d.Description
ORDER BY SUM(CAST(t.Quantity AS bigint))
```

要查「死亡原因」就加 `WHERE r.Name = N'死亡' AND r.TransferType = 1`，細項落在 `d.Description`。

### 移轉記錄要搭配哪些表

移轉記錄本身只放「數量、日期、原因、位置」，**品種／花色／規格／等級這些維度在批次表上**，查「某規格或某品種的異動」一定要 JOIN 回去：

| 類別 | 移轉記錄 | 搭配的表 | JOIN 條件 | 批次表提供的維度 |
|------|----------|----------|-----------|------------------|
| 苗株 | `YPTransferRecord` | `YPProductionBatch` | `.ProductionBatchID = YPProductionBatch.ID` | `BatchNo`／`BatchNoSrc`、`SpecID`、`BreedAliasID`、`ProductionLineID`、`ProcessID`、`PotID`、`MediumID`、進貨與完成日期 |
| 盆花 | `PPTransferRecord` | `PPTransferTask`（任務，**主原因在這**）<br>`PPTransferBatch`（批次） | `.TaskID = PPTransferTask.TaskID`<br>`.BatchID = PPTransferBatch.BatchID` | 任務：`ReasonID`、`TransferDate`、`CustomerID`<br>批次：`SpecID`、`ColorID`、`BreedAliasID`、`GradeID`、`StemID`、`ShipWeek`、`TotalQuantity` |
| 切花 | `CFTransferRecord` | `CFTransferBatch` | `.BatchID = CFTransferBatch.ID` | `BatchNo`、`ColorID`、`BreedAliasID`、`GradeID`、`FlowerID`、`PackingDate`、`TotalQuantity` |

> `PPTransferRecord` 自己也有 `SpecID`、`ColorID`、`BreedAliasID`、`ProductionLineID`（與批次表一致，實測近一年 77,080 筆全部相同），單純依規格篩選可以直接用；要一次取到等級、週別、花色名稱就 JOIN `PPTransferBatch` 比較省事。

```sql
-- 盆花近一年各原因／規格的異動量
SELECT r.Name AS 原因, sp.Name AS 規格, SUM(CAST(rec.TransferQuantity AS bigint)) AS 異動數量
FROM PPTransferRecord rec
JOIN PPTransferTask tk ON rec.TaskID = tk.TaskID
JOIN BIReason r ON tk.ReasonID = r.ID
LEFT JOIN PPTransferBatch b ON rec.BatchID = b.BatchID
LEFT JOIN BISpec sp ON b.SpecID = sp.ID
WHERE rec.TransferDate >= DATEADD(year, -1, GETDATE())
GROUP BY r.Name, sp.Name ORDER BY 3 DESC
```

### 省事做法：原因與名稱都已併好的檢視

不想自己 JOIN 任務＋原因＋批次時，直接查這些檢視（**欄位大多是中文，可以直接寫，不必加方括號**）：

| 類別 | 用哪個 | 主要欄位 |
|------|--------|----------|
| 苗株 | `View_YPTransferRecord` | `數量`、`移轉原因`、`移轉說明`、`移轉日期`、`規格`／`規格名稱`、`品種別名`、`花色`／`花色類別`、`位置一`／`位置二`、`批號`、`製程`、`產線`、`移轉週次` |
| 盆花 | **`RB_View_PPTransferRecord`** | `移轉數量`、`移轉原因`、`移轉說明`、`移轉日期`、`產線`、`品種`、`花色`、`等級`、`梗數`、`規格`、`出貨週次`、`客戶`、`平均高度` |
| 切花 | `View_CFTransferRecord` | 英文欄名但已帶名稱：`TransferQuantity`、`ReasonName`、`ReasonDescription`、`ColorName`、`BreedName`、`GradeName`、`CustomerName`、`BatchNo`、`TransferDate` |

- 盆花**不要用 `View_PPTransferRecord`**：它與 `RB_View_PPTransferRecord` 筆數不一致（275,009 vs 496,441），**以 `RB_View_PPTransferRecord` 為準**。
- 這些檢視幾乎沒有 ID 欄位，要再跟別的表 JOIN 還是得回到基礎表。

```sql
-- 盆花近一年各原因的淨異動（實測：跨組移轉 +706,210、配貨出貨(內銷) −439,449、死亡 −14,468）
SELECT 移轉原因, SUM(CAST(移轉數量 AS bigint)) AS 淨異動數量
FROM RB_View_PPTransferRecord
WHERE 移轉日期 >= DATEADD(year, -1, GETDATE())
GROUP BY 移轉原因 ORDER BY 2 DESC
```

## 生產階段與製程（BIProcess）

**「生產階段」不是只看 `SpecID`。**規格是「現在多大」，階段是「從哪一個規格養到哪一個規格」，後者記在 `BIProcess`：

| 欄位 | 意思 |
|------|------|
| `Name` | 階段名稱，本身就寫明路徑：`出瓶0040->0045`、`翻種0075->0105`、`0099養苗`、`進催`、`回養10周` |
| `SpecBegin`／`SpecEnd` | 起迄規格，值是 **`BISpec.ID`**（不是 Code）——例 `翻種0075->0105` 是 14 → 18 |
| `WorkDay` | 這個階段的預計天數（例 `翻種0075->0105` 是 150 天） |
| `IsUnderContract` | 是否契作階段 |

`YPProductionBatch.ProcessID` → `BIProcess.ID`；`View_苗株庫存數量` 已帶 `ProcessID`／`ProcessName`。
`YPProductionBatchProcessLog` 記翻種製程歷程。

所以「哪個生產階段損耗最大」要 `GROUP BY` 的是 **`ProcessID`**（或 `SpecBegin`／`SpecEnd`），不是 `SpecID`。

## 良率（沒有現成公式，不可自己假設）

良率**不是**「目前庫存 ÷ 初始數量」。業務定義是：從進貨／生產起始總量開始，依後續交易的減項與**異動原因**計算有效存活比例，而且：

- 正常移轉（部門內外移轉、跨組移轉、批號／規格變更）**不是損耗**。
- 跨階段要沿 `BatchNoSrc` 追血緣，不能只看目前 `BatchNo`。
- 組培（瓶）與種苗（株）**單位不同**，跨這條界線的良率需要每瓶株數換算，**資料庫裡沒有這個值**。

資料齊備的部分（可以直接算並呈現）：

| 成分 | 來源 |
|------|------|
| 起始投入 | `ReasonID = 8`（R08 進貨） |
| 死亡 | R03 ｜ 汰除 R04、R07 ｜ 瑕疵 R38 ｜ 盤虧 R16 ｜ 檢疫 R06 |
| 出貨（不計損耗） | R01、R02、R29 |
| 交接到盆花／切花（不計損耗） | R21 跨組移轉 |
| 階段轉入 | R05 翻種（注意正負不對稱） |
| 細分死因 | `BIReasonDesc.Description` |

**要做的事：**先把上面這些成分依使用者指定的維度（品種／批次／規格／製程／產線）與日期區間**分別列出數量**，然後說明「良率的分母與是否計入哪些原因請您確認」，由使用者確認公式後再算比例。**不要自己定一個公式算出百分比**——分母選進貨或翻種、跨組移轉算不算損耗，結果會差很多倍。

```sql
-- 良率分析的素材：某產線近一年依原因分類的數量（確認公式前先給這個）
SELECT r.Code, r.Name AS 原因, SUM(CAST(t.Quantity AS bigint)) AS 數量, COUNT(*) AS 筆數
FROM YPTransferRecord t
JOIN YPProductionBatch b ON t.ProductionBatchID = b.ID
JOIN BIReason r ON t.ReasonID = r.ID
WHERE b.ProductionLineID = 2 AND t.TransferDate >= DATEADD(year, -1, GETDATE())
GROUP BY r.Code, r.Name ORDER BY 3
```

## 切花訂單需求 vs 可供貨

鏈路：**需求單 → 配貨單 → 出貨單**，採收另走一條線。

```
CFOrder → CFOrderDetail → CFDistributionOrderDetailMap → CFDistributionDetail → CFDistribution
        → CFShipDistributionDetailMap → CFShipDetail → CFShip
CFHarvest → CFHarvestRecord（採收）    CFTransferBatch → CFTransferRecord（商品庫存）
```

（盆花把 `CF` 換成 `PP`；`Map` 結尾是多對多，**JOIN 後資料列會重複**，算總量要 `GROUP BY` + `SUM()`。）

### 切花訂單的三個陷阱（實測）

1. **切花訂單是按「花色」下的，不是按品種。**`CFOrderDetail` **沒有 `BreedAliasID`**，只有 `ColorID`。所以「XX 品種 10/20 的訂單有貨嗎」在訂單層**查不到品種**——要先跟使用者確認是問花色，或只能從配貨／出貨端回推。（盆花不同：`PPOrderDetail` 有 `BreedAliasID`、`GradeID`、`StemID`、`MediumID`、`MaturityID` 和單一的 `OrderQuantity`。）
2. **數量欄位名稱拼錯了，是 `Quqntity` 不是 `Quantity`**：`CFOrderDetail.FixedQuqntity`（固定量）、`NormalQuqntity`（普通量）。訂單需求量 = 兩者相加。寫成 `FixedQuantity` 會噴「無效的資料行名稱」。
3. **`SubColorIDList`／`GradeIDList`／`FlowerIDList` 是逗號分隔的字串**（例 `'3,11'`），**不是外鍵**，不能直接 JOIN。要比對得用 `STRING_SPLIT(d.GradeIDList, ',')` 或 `','+d.GradeIDList+',' LIKE '%,3,%'`。

其他欄位：`CFOrder.ShipDate`（出貨日）、`CustomerID`→`BICustomer`、`OrderStatus`、`ShipProductionLineID`、`ShipType`、`IsEarly`。

### 供貨分析不能只比目前庫存

問「10/20 的切花訂單夠不夠出」時，不要只算 `目前庫存 >= 訂單量`，要同時看：

```
訂單需求（FixedQuqntity + NormalQuqntity）
vs 目前可供貨庫存（CFTransferBatch／CFTransferRecord）
vs 已採收數量（CFHarvestRecord.Quantity，依 HarvestDate）
vs 已出貨數量（CFShipDetail）
```

`CFHarvest` 是採收單頭（`HarvestStartDate`／`HarvestEndDate`、`ProductionLineID`、`BatchNo`、`BreedAliasID`、`ColorID`），`CFHarvestRecord` 是明細（`HarvestDate`、`Quantity`、`CarNo`）。

若採收數量 > 入庫數量，要說明「**已有採收紀錄，但部分數量尚未進入切花庫存**」，而不是直接判定缺貨。

缺出貨日或日期區間時必須先問，也要確認是台灣還是越南的需求。

## 關聯重點
- 單據都是**單頭／單身**：單頭放單號、日期、客戶、狀態；單身放數量與品種／規格／製程／批次參照。
- 人員權限：`BIPersonel → BSPersonalRoleMap → BSRole → BSRoleFunctionMap`；可操作產線：`BIPersonel → BIPersonelProductionLineMap → BIProductionLine`。直接查 `View_PersonelPermission` 更快。
- 苗株進貨：`YPPurchase`（進貨）→ `YPProductionBatch`（生產批次）→ `YPPickingPlan`（挑苗排程）。
- 契作：`SCUnderContract`（批次）→ `SCUnderContractVisit`（訪視）→ `SCUnderContractRecord`。

## 回答格式

依序寫：**結論 → 數據 → 查詢條件 → 必要說明**。查詢條件和必要說明不可省略——使用者要知道這個數字涵蓋到哪裡。

> 越南種苗課（`ProductionLineID = 2`）目前「品種 ABC」共 12,580 株。
>
> - 瓶苗（組培）：64 瓶
> - 小苗 04.5CM：5,180 株
> - 中苗 07.5CM／08.4CM：4,200 株
> - 大苗 09.0CM 以上：3,200 株
>
> 查詢條件：產線＝越南種苗課，資料來源 `View_苗株庫存數量`（即時庫存）。
>
> 說明：此為**苗株栽培階段**庫存，不含採收後的切花（支）或盆花（盆）商品庫存。瓶苗單位是瓶，未併入株數合計。

## 絕對不能做的事

1. 栽培中的苗株庫存**不可**與採收後商品庫存相加或相比。
2. **不可**把所有負數移轉當成損耗——必須照 `BIReason` 分類（出貨、跨組移轉、批號變更都不是損耗）。
3. **不可**把組培（瓶）與種苗（株）的數量相加。
4. 跨批次分析**必須**考慮 `BatchNoSrc`，且記得 `BatchNo` 不唯一、要加 `COLLATE`。
5. 跨產線分析**必須**考慮 `ProductionLineID`；「台灣」是 1、5、9 三條。
6. 歷史庫存**必須**依 `YPTransferRecord` 的交易日期重算，**不可**用目前庫存回推過去。
7. 「切花」語意不明（栽培產線 vs 採收後商品）時**必須**先問。
8. 「庫存」未指定產線而不同產線會影響結果時**必須**先問。
9. 訂單供貨分析**不可**只比目前庫存，要同時看訂單、採收、入庫、出貨。
10. 欄位、關聯或計算規則不確定時（尤其良率）**不可**自己假設業務邏輯——說明缺哪個定義，請使用者補充。

## 參考文件（需要細節時才查）

上面的對照表不夠用時，用 `read_reference` 工具查以下文件，**一定要帶 keyword**（資料表名稱、欄位名稱或中文業務詞彙），不要整份讀：

- `references/database-design-spec.md`：完整資料庫設計規格書，含每張表的欄位、型別、索引與外鍵。**檔案很大，只能用 keyword 查。**
- `references/database-relationships.md`：跨資料表關聯、JOIN 與進階查詢範例。
- `references/database-query-guide.md`：資料表清單、模組前綴與常見查詢範例。
- `references/pmm-skill-spec.md`：PMM 操作的行為規則。

例如要確認 `CFOrder` 有哪些欄位：
`read_reference(skill="db-pmm", file="references/database-design-spec.md", keyword="CFOrder")`

> 欄位名稱以 `describe_table` 從資料庫現查的結果為準；參考文件用來理解欄位的**業務意義**與表之間的關聯。
