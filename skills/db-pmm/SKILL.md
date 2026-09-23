---
name: db-pmm
description: PMM 蝴蝶蘭產銷管理系統：苗株／盆花／切花的生產批次、庫存移轉、需求單、配貨、出貨、採購契作、客戶、花色、死亡、移轉原因與品種主檔
db: pmm
tables: >-
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
  YPTransferRecordTemp, YPTransferTask, BreedAlias, CF_OrderAndDistribution, CF_OrderDistShipRelation,
  CF_TransferAndDistribution, CFDistribution_All, CFDistribution_Sum, CFSampleSurvey_All, CFShipAndDetail,
  CFShipAndDist, CFShipSurvey_HF_All, CFShipSurvey_Roll_All, CFShipSurveyMap_Roll, CFStemSurvey_All,
  CFShipSurveyMap_HF, CFTransferBatch_Sum, CFTransferRecord_Sync, PersonelPermission, PPBudSurvey_All,
  PPDistribution_All, PPDistribution_All_WithName, PPDistribution_Sum, PPStemSurvey_All, PPTransferBatch_Sum_P,
  PPTransferRecord_Sync, Rpt_CF002, Rpt_CF004, SCPurchaseOrder_Sync, SCUnderContract_Sync, ShipPacking,
  YPProductionBatch_sum, YPProductionBatchProcessLog, YPTransferRecord_All
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

**檢視表（關聯複雜的報表優先用這些）**：BreedAlias 品種花色關聯、PersonelPermission 帳號角色權限、CF_OrderAndDistribution 切花訂單配貨、CF_OrderDistShipRelation 切花訂單配貨出貨、CF_TransferAndDistribution 切花移轉配貨、CFDistribution_All 配貨明細、CFDistribution_Sum 配貨數 BY 客戶、CFTransferBatch_Sum 切花庫存明細、CFShipAndDetail 出貨明細、CFShipAndDist 出貨與配貨、CFSampleSurvey_All 抽梗調查明細、CFStemSurvey_All 點梗調查明細、CFShipSurvey_HF_All 高朵數出貨調查、CFShipSurvey_Roll_All／CFShipSurveyMap_Roll 抽樣點花、CFShipSurveyMap_HF 點梗高朵數、PPBudSurvey_All 打荳調查、PPStemSurvey_All 來梗調查、PPDistribution_All／PPDistribution_All_WithName 盆花配貨明細、PPDistribution_Sum 盆花庫存、YPProductionBatch_sum 生產批次庫存、YPProductionBatchProcessLog 翻種製程記錄、Rpt_CF002 切花點梗出貨預估、Rpt_CF004 切花高朵數出貨預估、CFTransferRecord_Sync／PPTransferRecord_Sync／SCPurchaseOrder_Sync／SCUnderContract_Sync 拋轉中介、ShipPacking 出貨包裝明細、PPTransferBatch_Sum_P／YPTransferRecord_All 未使用

## 關聯重點
- 單據都是**單頭／單身**：單頭放單號、日期、客戶、狀態；單身放數量與品種／規格／製程／批次參照。
- 訂單不會直接出貨，鏈路是 **需求單 → 配貨單 → 出貨單**：
  `CFOrder → CFOrderDetail → CFDistributionOrderDetailMap → CFDistributionDetail → CFDistribution → CFShipDistributionDetailMap → CFShipDetail → CFShip`（盆花把 `CF` 換成 `PP`）。
- `Map` 結尾是多對多關聯（一張訂單分批配貨、多張訂單合併配貨），**JOIN 後資料列會重複**，算總量時要 `GROUP BY` + `SUM()`。
- 人員權限：`BIPersonel → BSPersonalRoleMap → BSRole → BSRoleFunctionMap`；可操作產線：`BIPersonel → BIPersonelProductionLineMap → BIProductionLine`。直接查 `PersonelPermission` 檢視更快。
- 苗株庫存：`YPPurchase`（進貨）→ `YPProductionBatch`（生產批次）→ `YPPickingPlan`（挑苗排程）；庫存彙總用 `YPProductionBatch_sum`。
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

