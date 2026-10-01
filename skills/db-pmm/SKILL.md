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
> 內容整理自 PMM Skill 的 `database-query-guide.md` 與 `database-relationships.md`。

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

## 花色（BIColor）：代號 vs 語意

花色有三個層次，使用者的問法決定要查哪一欄：

| 層次 | 欄位 | 內容 | 例 |
|------|------|------|-----|
| 代號 | `BIColor.Code` | 花色代號（英數） | `W`、`BL-W`、`WSP`、`M-W` |
| 英文名 | `BIColor.Name` | 花色英文全名 | `White`、`Big Lip White`、`White with Spot` |
| 語意分類 | `BIColorCategory.Name`、`ColorType` | **中文**類別名稱；`ColorType` 1＝白花系、2＝色花系 | `白花`、`大唇瓣白花`、`MIDI-白`、`紅花`、`粉花`、`異色花` |

判斷原則：

- 使用者講的是**代號**（W、BL-W、M-W…）→ 用 `c.Code = 'W'` 精確比對，不要用 LIKE。
- 使用者講的是**中文顏色語意**（白色、紅花、粉花）→ 走 `BIColorCategory`：
  `JOIN BIColorCategory g ON c.ColorCategoryID = g.ID WHERE g.Name LIKE '%白%'`
  （白花系也可以用 `g.ColorType = 1`）。
- `BIColor.Name` 是**英文**，`Name LIKE '%白%'` 永遠查不到東西；也**不要**用 `Name LIKE '%White%'` 代表「白色」，那會抓到 `White with Spot`（類別其實是異色花）。

同樣問「白色品種」，三種寫法差很多（實際筆數）：

| 寫法 | 品種數 | 適用 |
|------|--------|------|
| `c.Code = 'W'` | 60 | 使用者指定代號 W |
| `g.ColorType = 1`（白花＋大唇瓣白花＋MIDI-白） | 121 | 使用者說「白色」的語意查詢 |
| `c.Name LIKE '%White%'` | 368 | **不要用**，含異色花 |

回答時要說明用的是哪個範圍（例如「花色代號 W」或「白花系（含大唇瓣白花、MIDI-白）」），使用者才知道涵蓋到哪裡。

## 庫存要查哪張表

庫存**不要**自己從生產批次或移轉記錄兜，系統已經有彙總檢視（欄位都已經把代號翻成名稱）：

| 問什麼 | 用哪張 | 主要欄位 |
|--------|--------|----------|
| 苗株庫存 | `View_苗株庫存數量` | `TotalQuantity`、`SpecCode`／`SpecName`、`ProductionLineName`、`ColorCode`／`ColorName`、`BreedAliasName`、`Position1`／`Position2`、`BatchNo` |
| 盆花庫存 | `View_盆花庫存數量`、依規格看用 `View_盆花規格庫存數量` | `TotalQuantity`、`SpecID`、`ColorCode`、`BreedAliasName`、`ShipWeek`、`GradeName` |
| 切花庫存 | `View_切花出貨一課庫存數量` | — |
| 溫室現況 | `View_GreenhouseStock` | 欄位是中文：`溫室`、`床位`、`移轉日期`、`品種`、`花色`、`切次`、`規格`、`數量`、`移轉原因`、`部門` |

規格的比對方式：

- 用 **`SpecCode`**（對應 `BISpec.Code`，例如 `0075`），**不要用名稱**——`BISpec.Name` 有前導零（`07.5CM`），寫 `Name = '7.5CM'` 會查不到。
- 使用者說的尺寸常常對到兩個規格，要看他問的是哪一類：`0075`＝`07.5CM`（**種苗**）、`075F`＝`7.5CM盆花`（**盆花**）。問「苗株」用 `0075`。
- 先用 `SELECT Code, Name, Remark FROM BISpec` 確認代號；`Remark` 會標示是「組培／種苗／盆花」。

範例——7.5cm 苗株庫存（實測 301,779 株）：

```sql
SELECT SpecCode, SpecName, SUM(TotalQuantity) AS 庫存數
FROM View_苗株庫存數量 WHERE SpecCode = '0075' GROUP BY SpecCode, SpecName
```

想看分佈就加 `ProductionLineName`（種苗課、台灣契作產線、切花課、彰化生產部…）到 `GROUP BY`。

## 數量異動原因（最常問的查詢之一）

每一筆數量進出都記在移轉記錄表，原因存成代號，要 JOIN 原因主檔才看得懂：

| 類別 | 移轉記錄表 | 數量欄位 | 主鍵 | 原因欄位 |
|------|-----------|----------|------|----------|
| 苗株 | `YPTransferRecord` | `Quantity` | `ID` | `ReasonID` + `ReasonDescID` |
| 切花 | `CFTransferRecord` | `TransferQuantity` | `ID` | `ReasonID` + `ReasonDescID` |
| 盆花 | `PPTransferRecord` | `TransferQuantity` | **`RecordID`** | **只有 `ReasonDescID`** |

- `ReasonID` → **`BIReason`**（主原因）：進貨、死亡、翻種、部門間移轉、部門內移轉、異動性增／減、盤盈、盤虧、海關檢疫、切花後汰除、批號變更、規格變更、瑕疵品…；`BIReason.TransferType` 區分移轉類型（1／2…），所以**同一個 `Code`（如 R09 異動性增）會有多列**，JOIN 要用 `ID` 不要用 `Code`。
- `ReasonDescID` → **`BIReasonDesc`**（細分原因，`BIReasonDesc.ReasonID` 指回主原因）。`Description` 是**越南文＋中文並列**（例如死亡底下有「Nhũn 軟腐」「Đen gốc 黑頭」「Vi rút 病毒」「Thối rễ 敗根」），用中文關鍵字查要 `LIKE N'%軟腐%'`。可能是空的，所以用 **LEFT JOIN**。
- **`PPTransferRecord` 沒有 `ReasonID`**——盆花的主原因記在**任務**上，要 `JOIN PPTransferTask ON PPTransferRecord.TaskID = PPTransferTask.TaskID`，再用 `PPTransferTask.ReasonID` 接 `BIReason`。

範例——苗株近一年各原因的異動量：

```sql
SELECT r.Name AS 原因, d.Description AS 細分原因,
       SUM(t.Quantity) AS 異動數量, COUNT(*) AS 筆數
FROM YPTransferRecord t
JOIN BIReason r ON t.ReasonID = r.ID
LEFT JOIN BIReasonDesc d ON t.ReasonDescID = d.ID
WHERE t.TransferDate >= DATEADD(year, -1, GETDATE())
GROUP BY r.Name, d.Description
ORDER BY SUM(t.Quantity) DESC
```

要查「死亡原因」就加 `WHERE r.Name = N'死亡'`，細項會落在 `d.Description`。

### 移轉記錄要搭配哪些表

移轉記錄本身只放「數量、日期、原因」，**品種／花色／規格／等級這些維度在批次表上**，所以查「某規格或某品種的異動」一定要 JOIN 回去：

| 類別 | 移轉記錄 | 搭配的表 | JOIN 條件 | 批次表提供的維度 |
|------|----------|----------|-----------|------------------|
| 苗株 | `YPTransferRecord` | `YPProductionBatch` | `.ProductionBatchID = YPProductionBatch.ID` | `BatchNo`、`SpecID`、`BreedAliasID`、`ProductionLineID`、`ProcessID`、`PotID`、`MediumID`、進貨與完成日期 |
| 盆花 | `PPTransferRecord` | `PPTransferTask`（任務，**主原因在這**）<br>`PPTransferBatch`（批次） | `.TaskID = PPTransferTask.TaskID`<br>`.BatchID = PPTransferBatch.BatchID` | 任務：`ReasonID`、`TransferDate`、`CustomerID`<br>批次：`SpecID`、`ColorID`、`BreedAliasID`、`GradeID`、`StemID`、`ShipWeek`、`TotalQuantity` |
| 切花 | `CFTransferRecord` | `CFTransferBatch` | `.BatchID = CFTransferBatch.ID` | `BatchNo`、`ColorID`、`BreedAliasID`、`GradeID`、`FlowerID`、`PackingDate`、`TotalQuantity` |

> `PPTransferRecord` 自己也有 `SpecID`、`ColorID` 等欄位（與批次表一致，實測近一年 77,080 筆全部相同），單純依規格篩選可以直接用；但要一次取到等級、週別、花色名稱等就 JOIN `PPTransferBatch` 比較省事。

範例——盆花近一年各原因／規格的異動量：

```sql
SELECT r.Name AS 原因, sp.Name AS 規格, SUM(rec.TransferQuantity) AS 異動數量
FROM PPTransferRecord rec
JOIN PPTransferTask tk ON rec.TaskID = tk.TaskID
JOIN BIReason r ON tk.ReasonID = r.ID
LEFT JOIN PPTransferBatch b ON rec.BatchID = b.BatchID
LEFT JOIN BISpec sp ON b.SpecID = sp.ID
WHERE rec.TransferDate >= DATEADD(year, -1, GETDATE())
GROUP BY r.Name, sp.Name ORDER BY SUM(rec.TransferQuantity) DESC
```

苗株要帶規格就把 `YPProductionBatch` 接上：

```sql
SELECT sp.Name AS 規格, r.Name AS 原因, SUM(t.Quantity) AS 異動數量
FROM YPTransferRecord t
JOIN YPProductionBatch pb ON t.ProductionBatchID = pb.ID
JOIN BISpec sp ON pb.SpecID = sp.ID
JOIN BIReason r ON t.ReasonID = r.ID
WHERE t.TransferDate >= DATEADD(year, -1, GETDATE())
GROUP BY sp.Name, r.Name ORDER BY SUM(t.Quantity) DESC
```

### 省事做法：原因與名稱都已併好的檢視

不想自己 JOIN 任務＋原因＋批次時，直接查這些檢視（**欄位大多是中文，可以直接寫，不必加方括號**）：

| 類別 | 用哪個 | 主要欄位 |
|------|--------|----------|
| 苗株 | `View_YPTransferRecord` | `數量`、`移轉原因`、`移轉說明`、`移轉日期`、`規格`／`規格名稱`、`品種別名`、`花色`／`花色類別`、`位置一`／`位置二`、`批號`、`製程`、`產線`、`移轉週次` |
| 盆花 | **`RB_View_PPTransferRecord`** | `移轉數量`、`移轉原因`、`移轉說明`、`移轉日期`、`產線`、`品種`、`花色`、`等級`、`梗數`、`規格`、`出貨週次`、`客戶`、`平均高度` |
| 切花 | `View_CFTransferRecord` | 英文欄名但已帶名稱：`TransferQuantity`、`ReasonName`、`ReasonDescription`、`ColorName`、`BreedName`、`GradeName`、`CustomerName`、`BatchNo`、`TransferDate` |

- 盆花**不要用 `View_PPTransferRecord`**：它與 `RB_View_PPTransferRecord` 筆數不一致（275,009 vs 496,441），**以 `RB_View_PPTransferRecord` 為準**。
- **移轉數量帶正負號**：增加為正（跨組移轉、異動性增、進貨…），減少為負（配貨出貨、死亡、切花後汰除、瑕疵品、海關檢疫…），所以 `SUM()` 直接就是**淨異動量**，不要再自己判斷方向。基礎表 `PPTransferRecord.TransferQuantity`／`YPTransferRecord.Quantity` 也是同一套正負規則。
- 這些檢視幾乎沒有 ID 欄位，要再跟別的表 JOIN 還是得回到基礎表。

範例——盆花近一年各原因的淨異動（實測：跨組移轉 +706,210、配貨出貨(內銷) −439,449、死亡 −14,468）：

```sql
SELECT 移轉原因, SUM(移轉數量) AS 淨異動數量
FROM RB_View_PPTransferRecord
WHERE 移轉日期 >= DATEADD(year, -1, GETDATE())
GROUP BY 移轉原因 ORDER BY SUM(移轉數量) DESC
```

## 關聯重點
- `BIBreed` **一列一個品種**，品種代號欄位是 **`PartNo`**（這張表沒有 `Code` 欄位）；`Code` 只有 `BIColor`、`BIColorCategory` 這些主檔才有。
- 要列「品種清單」請直接查 `BIBreed`。`View_BreedAlias` 是**品種 × 別名**，一個品種有多個別名就會出現多列（例：黃花類別 142 列，但只有 117 個品種），拿它列品種時一定要 `DISTINCT` 或 `GROUP BY BreedID`，否則筆數會虛胖、同一品種重複出現。
- 單據都是**單頭／單身**：單頭放單號、日期、客戶、狀態；單身放數量與品種／規格／製程／批次參照。
- 訂單不會直接出貨，鏈路是 **需求單 → 配貨單 → 出貨單**：
  `CFOrder → CFOrderDetail → CFDistributionOrderDetailMap → CFDistributionDetail → CFDistribution → CFShipDistributionDetailMap → CFShipDetail → CFShip`（盆花把 `CF` 換成 `PP`）。
- `Map` 結尾是多對多關聯（一張訂單分批配貨、多張訂單合併配貨），**JOIN 後資料列會重複**，算總量時要 `GROUP BY` + `SUM()`。
- 人員權限：`BIPersonel → BSPersonalRoleMap → BSRole → BSRoleFunctionMap`；可操作產線：`BIPersonel → BIPersonelProductionLineMap → BIProductionLine`。直接查 `View_PersonelPermission` 檢視更快。
- 苗株庫存：`YPPurchase`（進貨）→ `YPProductionBatch`（生產批次）→ `YPPickingPlan`（挑苗排程）；庫存彙總用 `View_YPProductionBatch_sum`。
- 契作：`SCUnderContract`（批次）→ `SCUnderContractVisit`（訪視）。

## 參考文件（需要細節時才查）

上面的對照表不夠用時，用 `read_reference` 工具查以下文件，**一定要帶 keyword**（資料表名稱、欄位名稱或中文業務詞彙），不要整份讀：

- `references/database-design-spec.md`：完整資料庫設計規格書，含每張表的欄位、型別、索引與外鍵。**檔案很大，只能用 keyword 查。**
- `references/database-relationships.md`：跨資料表關聯、JOIN 與進階查詢範例。
- `references/database-query-guide.md`：資料表清單、模組前綴與常見查詢範例。
- `references/pmm-skill-spec.md`：PMM 操作的行為規則。

例如要確認 `CFOrder` 有哪些欄位：
`read_reference(skill="db-pmm", file="references/database-design-spec.md", keyword="CFOrder")`

> 欄位名稱以 `describe_table` 從資料庫現查的結果為準；參考文件用來理解欄位的**業務意義**與表之間的關聯。

