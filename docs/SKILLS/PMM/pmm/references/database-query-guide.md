# PMM 資料庫查詢說明

本文件為 PMM 資料庫的查詢說明指南。以下列出主要的資料表綱要與欄位關聯。

## 一、主要資料表清單

| 表格名稱 | 說明 |
| -------- | ---- |
| `BIBreed` | 品種 |
| `BIBreedAlias` | 品種別名 |
| `BIColor` | 花色 |
| `BIColorCategory` | 花色類別 |
| `BICustomer` | 客戶 |
| `BIMedium` | 介質 |
| `BIPPPackingCondition` | 盆花包裝條件 |
| `BIPackingColor` | 包裝顏色 |
| `BIPackingSize` | 包裝大小 |
| `BIPersonel` | 人員帳號 |
| `BIPersonelProductionLineMap` | 人員帳號產線多對多關聯 |
| `BIPosition` | 位置 |
| `BIPot` | 盆器 |
| `BIPrintField` | 列印標貼 |
| `BIProcess` | 製程 |
| `BIProductionLine` | 產線 |
| `BIProductionLinePrintFieldMap` | 產線列印標貼多對多關聯 |
| `BIProductionLineReasonMap` | 產線移轉原因多對多關聯 |
| `BIReason` | 移轉原因 |
| `BIReasonDesc` | 移轉詳細原因 |
| `BIShipPacking` | 出貨包裝 |
| `BIShipPackingMap` | 出貨包裝入數 |
| `BISpec` | 規格 |
| `BISupplier` | 廠商 |
| `BISystemOption` | 系統選項 |
| `BIUploadFile` | 上傳檔案 |
| `BSPersonalRoleMap` | 人員角色對應 |
| `BSRole` | 角色 |
| `BSRoleFunctionMap` | 角色功能權限 |
| `CFDistribution` | 切花配貨單、訂單關聯 |
| `CFDistributionDetail` | 切花配貨明細 |
| `CFDistributionOrderDetailMap` | 切花配貨與需求單明細的多對多關聯 |
| `CFHarvest` | 切花採收 |
| `CFHarvestQuarantine` | 切花採收汰除 |
| `CFHarvestRecord` | 切花採收記錄 |
| `CFOrder` | 切花需求單 |
| `CFOrderDetail` | 切花需求單明細 |
| `CFSampleDetail` | 切花抽梗調查細的梗數明細 |
| `CFSampleRecord` | 切花抽梗調查明細 |
| `CFSampleSurvey` | 切花抽梗調查 |
| `CFShip` | 切花出貨 |
| `CFShipDetail` | 切花出貨明細 |
| `CFShipDistributionDetailMap` | 切花出貨配貨多對多關聯 |
| `CFShipSurvey` | 切花出貨調查明細 |
| `CFShipSurveyDetail` | 切花出貨調查明細 |
| `CFShipSurveyDetail_HF` | 切花出貨調查明細(高朵數) |
| `CFShipSurveyMap` | 切花出貨調查關聯 |
| `CFStemSurvey` | 切花點梗調查 |
| `CFStemSurveyDetail` | 點梗調查明細 |
| `CFStemSurveyMap` | 切花點梗調查，梗數明細 |
| `CFStemSurveyMapLog` | 點梗調查明細關聯歷程 |
| `CFTransferBatch` | 切花批次明細 |
| `CFTransferRecord` | 切花移轉記錄明細 |
| `LCExecutedSQL` | 執行過的更新SQL |
| `LCVersion` | 資料庫版本，用來搭配期初資料匯入程式 |
| `PPBudSurvey` | 盆花打荳調查 |
| `PPBudSurveyDetail` | 盆花打荳調查明細 |
| `PPBudSurveyMap` | 打荳調查來源明細 |
| `PPDistribution` | 盆花配貨 |
| `PPDistributionDetail` | 盆花配貨明細 |
| `PPDistributionOrderDetailMap` | 盆花配貨需求單明細關聯 |
| `PPOrder` | 盆花需求單 |
| `PPOrderDetail` | 盆花需求單明細 |
| `PPOrderNotice` | 盆花訂單包裝注意事項 |
| `PPOrderPackingSetting` | 盆花訂單包裝列表 |
| `PPOrderPackingSettingDetail` | 包裝設定明細列表 |
| `PPShipDetail` | 盆花出貨明細列表 |
| `PPShipPackingSetting` | 盆花包裝設定列表 |
| `PPShipPackingSettingDetail` | 包裝設定明細列表 |
| `PPStemSurvey` | 盆花來梗調查列表 |
| `PPStemSurveyDetail` | 盆花來梗調查明細 |
| `PPStemSurveyMap` | 盆花來梗調查來源明細 |
| `PPTransferBatch` | 盆花批次 |
| `PPTransferRecord` | 盆花移轉記錄 |
| `PPTransferRecordTemp` | 盆花移轉記錄暫時檔(未核準) |
| `PPTransferTask` | 盆花移轉任務 |
| `PPTransferTaskMap` | 盆花移轉任務關聯 |
| `SCPurchaseOrder` | 採購單列表 |
| `SCPurchaseOrderDetail` | 採購單明細 |
| `SCUnderContract` | 契作批次 |
| `SCUnderContractRecord` | 契作訪視記錄 |
| `SCUnderContractVisit` | 契作訪視 |
| `YPDistribution` | 苗株配貨 |
| `YPDistributionPlan` | 苗株配貨 |
| `YPPicking` | 苗株挑苗 |
| `YPPickingPlan` | 苗株挑苗排程 |
| `YPPickingPlanAllocation` | 苗株配貨挑苗 |
| `YPPickingRecord` | 苗株挑苗記錄 |
| `YPPickingRegular` | 苗株日常挑苗 |
| `YPPickingRegularRecord` | 苗株日常挑苗記錄 |
| `YPProductionBatch` | 苗株生產批次 |
| `YPPurchase` | 苗株進貨任務 |
| `YPShipPlan` | 配貨出貨列表 |
| `YPShipRecord` | 配貨出貨列表明細 |
| `YPTransferRecord` | 苗株移轉記錄 |
| `YPTransferRecordTemp` | 苗株移轉暫時記錄 |
| `YPTransferTask` | 苗株移轉任務 |
| `BreedAlias` | 品種、花色、花色類別關聯 |
| `CF_OrderAndDistribution` | 切花訂單、配貨單關聯 |
| `CF_OrderDistShipRelation` | 切花訂單、配貨單、出貨單關聯 |
| `CF_TransferAndDistribution` | 切花移轉、配貨關聯 |
| `CFDistribution_All` | 切花配貨明細 |
| `CFDistribution_Sum` | 切花配貨數 BY 客戶 |
| `CFSampleSurvey_All` | 切花抽梗調查明細 |
| `CFShipAndDetail` | 切花出貨明細 |
| `CFShipAndDist` | 切花出貨和配貨明細 |
| `CFShipSurvey_HF_All` | 切花出貨調查高朵數明細 |
| `CFShipSurvey_Roll_All` | 切花出貨抽樣點花調查明細 |
| `CFShipSurveyMap_Roll` | 切花抽樣點花，點花明細 |
| `CFStemSurvey_All` | 切花點梗調查明細 |
| `CFShipSurveyMap_HF` | 切花點梗調查高朵數明細 |
| `CFTransferBatch_Sum` | 切花庫存明細 |
| `CFTransferRecord_Sync` | 拋轉中介所需要切花移轉記錄 |
| `PersonelPermission` | 帳號、權限、角色 |
| `PPBudSurvey_All` | 打荳調查詳細資訊 |
| `PPDistribution_All` | 盆花配貨明細 |
| `PPDistribution_All_WithName` | 盆花訂單確認頁、出貨頁，載入符合的配 |
| `PPDistribution_Sum` | 盆花配貨頁，列出庫存 |
| `PPStemSurvey_All` | 盆花來梗調查資訊 |
| `PPTransferBatch_Sum_P` | 未使用 |
| `PPTransferRecord_Sync` | 盆花移轉拋轉中介資料 |
| `Rpt_CF002` | 切花點梗出貨預估表 |
| `Rpt_CF004` | 切花高朵數出貨預估表 |
| `SCPurchaseOrder_Sync` | 採購單拋轉中介列表 |
| `SCUnderContract_Sync` | 契作批次拋轉中介列表 |
| `ShipPacking` | 出貨包裝明細 |
| `YPProductionBatch_sum` | 生產批次庫存 |
| `YPProductionBatchProcessLog` | 翻種的生產批次製程記錄 |
| `YPTransferRecord_All` | 未使用 |

> **💡 進階參考：** 關於上述資料表的關聯視圖、詳細業務邏輯及複雜的跨表 `JOIN` 範例，請參閱：[PMM資料庫實體關聯與查詢增強說明.md](PMM資料庫實體關聯與查詢增強說明.md)

## 二、關鍵模組分類說明

系統資料表的命名規則非常明確，可透過前綴字元（Prefix）分為以下幾個主要模組：

### (一) 主檔與系統模組 (BI / BS / LC)
- **BI (Basic Info) 基本主檔**：如 `BIBreed` (品種)、`BICustomer` (客戶)、`BIMedium` (介質)、`BIProductionLine` (產線)，用來存放整個 PMM 系統的基礎設定資料。
- **BS (Basic System) 角色與權限**：如 `BSRole` (角色)、`BSPersonalRoleMap` (人員角色對應)。
- **LC (Log / Core)**：如 `LCVersion`、`LCExecutedSQL` 主要是系統底層版本與資料庫異動紀錄。

### (二) 切花出貨模組 (CF - Cut Flower)
包含切花從採收到出貨的所有歷程表，例如：
- `CFHarvest` (切花採收)
- `CFOrder` (切花需求單) / `CFDistribution` (配貨)
- `CFShip` (切花出貨) / `CFSampleSurvey` (切花抽梗調查)

### (三) 盆花出貨模組 (PP - Potted Plant)
包含盆花的製程調查、配貨與出貨，例如：
- `PPBudSurvey` (盆花打荳調查) / `PPStemSurvey` (盆花來梗調查)
- `PPOrder` (盆花需求單) / `PPDistribution` (盆花配貨)
- `PPTransferTask` (盆花移轉)

### (四) 苗株模組 (YP - Young Plant)
包含苗株的進貨、挑苗與排程，例如：
- `YPProductionBatch` (苗株生產批次)
- `YPPicking` (苗株挑苗) / `YPPickingPlan` (挑苗排程)
- `YPPurchase` (進貨任務)

### (五) 採購與契作模組 (SC - Subcontract)
- `SCPurchaseOrder` (採購單)
- `SCUnderContract` (契作批次) / `SCUnderContractVisit` (契作訪視)

## 三、常見查詢 SQL 範例

### 1. 查詢特定客戶之資料
```sql
SELECT 
    ID, Code, NameShort, Name
FROM 
    BICustomer 
ORDER BY
    ID;
```

### 2. 人員與產線對應查詢
```sql
SELECT 
    p.PersonelID, 
    p.Account,
    p.PersonelName, 
    l.LineName 
FROM 
    BIPersonel p
JOIN 
    BIPersonelProductionLineMap m ON p.PersonelID = m.PersonelID
JOIN 
    BIProductionLine l ON m.ProductionLineID = l.LineID;
```

### 3. 查詢切花配貨與訂單關聯
```sql
SELECT 
    o.OrderNo,
    d.DistributionNo,
    o.CustID
FROM 
    CFOrder o
JOIN 
    CFDistributionOrderDetailMap map ON o.OrderID = map.OrderID
JOIN 
    CFDistribution d ON map.DistributionID = d.DistributionID;
```

### 4. 盆花出貨包裝設定查詢
```sql
SELECT 
    s.ShipNo,
    ps.ShipPackingID,
    ps.Quantity
FROM 
    PPShipPackingSetting ps
JOIN 
    PPShipDetail sd ON ps.ShipTargetID = sd.DetailID;
```
