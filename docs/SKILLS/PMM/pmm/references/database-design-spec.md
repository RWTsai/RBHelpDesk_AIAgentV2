文件名稱：資料庫設計規格書 皇基股份有限公司 日期：109年10月30日
}
貳、資料庫與程式關聯說明
一、檔案、資料表清單
序號 表格名稱 資料表說明
資料表
1 BIBreed 品種
2 BIBreedAlias 品種別名
3 BIColor 花色
4 BIColorCategory 花色類別
5 BICustomer 客戶
6 BIMedium 介質
7 BIPPPackingCondition 盆花包裝條件
8 BIPackingColor 包裝顏色
9 BIPackingSize 包裝大小
10 BIPersonel 人員帳號
11 BIPersonelProductionLineMap 人員帳號產線多對多關聯
12 BIPosition 位置
13 BIPot 盆器
14 BIPrintField 列印標貼
15 BIProcess 製程
16 BIProductionLine 產線
17 BIProductionLinePrintFieldMap 產線列印標貼多對多關聯
18 BIProductionLineReasonMap 產線移轉原因多對多關聯
19 BIReason 移轉原因
20 BIReasonDesc 移轉詳細原因
21 BIShipPacking 出貨包裝
22 BIShipPackingMap 出貨包裝入數
23 BISpec 規格
24 BISupplier 廠商
25 BISystemOption 系統選項
26 BIUploadFile 上傳檔案
27 BSPersonalRoleMap 人員角色對應
28 BSRole 角色
29 BSRoleFunctionMap 角色功能權限
30 CFDistribution 切花配貨
機密等級：內部文件 版權所有©2020凌誠科技股份有限公司
308/391

文件名稱：資料庫設計規格書 皇基股份有限公司 日期：109年10月30日
序號 表格名稱 資料表說明
31 CFDistributionDetail 切花配貨明細
32 CFDistributionOrderDetailMap 切花配貨與需求單明細的多對多關聯
33 CFHarvest 切花採收
34 CFHarvestQuarantine 切花採收汰除
35 CFHarvestRecord 切花採收記錄
36 CFOrder 切花需求單
37 CFOrderDetail 切花需求單明細
38 CFSampleDetail 切花抽梗調查細的梗數明細
39 CFSampleRecord 切花抽梗調查明細
40 CFSampleSurvey 切花抽梗調查
41 CFShip 切花出貨
42 CFShipDetail 切花出貨明細
43 CFShipDistributionDetailMap 切花出貨配貨多對多關聯
44 CFShipSurvey 切花出貨調查
45 CFShipSurveyDetail 切花出貨調查明細
46 CFShipSurveyDetail_HF 切花出貨調查明細(高朵數)
47 CFShipSurveyMap 切花出貨調查關聯
48 CFStemSurvey 點梗調查
49 CFStemSurveyDetail 點梗調查明細
50 CFStemSurveyMap 點梗調查明細關聯
51 CFStemSurveyMapLog 點梗調查明細關聯歷程
52 CFTransferBatch 切花批次
53 CFTransferRecord 切花移轉記錄
54 LCExecutedSQL 執行過的更新SQL
55 LCVersion 資料庫版本，用來搭配期初資料匯入程式
56 PPBudSurvey 盆花打荳調查
57 PPBudSurveyDetail 盆花打荳調查明細
58 PPBudSurveyMap 打荳調查關聯
59 PPDistribution 盆花配貨
60 PPDistributionDetail 盆花配貨明細
61 PPDistributionOrderDetailMap 盆花配貨需求單明細關聯
62 PPOrder 盆花需求單
63 PPOrderDetail 盆花需求單明細
64 PPOrderNotice 盆花訂單包裝注意事項
65 PPOrderPackingSetting 盆花訂單出貨包裝設定
66 PPOrderPackingSettingDetail 盆花訂單包裝設定明細
機密等級：內部文件 版權所有©2020凌誠科技股份有限公司
309/391

文件名稱：資料庫設計規格書 皇基股份有限公司 日期：109年10月30日
序號 表格名稱 資料表說明
67 PPShipDetail 盆花出貨明細
68 PPShipPackingSetting 盆花訂單出貨包裝設定
69 PPShipPackingSettingDetail 盆花訂單出貨包裝設定明細
70 PPStemSurvey 盆花來梗調查
71 PPStemSurveyDetail 盆花來梗調查明細
72 PPStemSurveyMap 盆花來梗調查關聯
73 PPTransferBatch 盆花批次
74 PPTransferRecord 盆花移轉記錄
75 PPTransferRecordTemp 盆花移轉記錄暫時檔(未核準)
76 PPTransferTask 盆花移轉任務
77 PPTransferTaskMap 盆花移轉任務關聯
78 SCPurchaseOrder 採購單
79 SCPurchaseOrderDetail 採購單明細
80 SCUnderContract 契作批次
81 SCUnderContractRecord 契作訪視記錄
82 SCUnderContractVisit 契作訪視
83 YPDistribution 苗株配貨
84 YPDistributionPlan 苗株配貨
85 YPPicking 苗株挑苗
86 YPPickingPlan 苗株挑苗排程
87 YPPickingPlanAllocation 苗株配貨挑苗
88 YPPickingRecord 苗株挑苗記錄
89 YPPickingRegular 苗株日常挑苗
90 YPPickingRegularRecord 苗株日常挑苗記錄
91 YPProductionBatch 苗株生產批次
92 YPPurchase 苗株進貨任務
93 YPShipPlan 苗株出貨安排
94 YPShipRecord 苗株出貨記錄
95 YPTransferRecord 苗株移轉記錄
96 YPTransferRecordTemp 苗株移轉暫時記錄
97 YPTransferTask 苗株移轉任務
view
1 BreedAlias 品種、花色、花色類別關聯
2 CF_OrderAndDistribution 切花訂單、配貨單關聯
3 CF_OrderDistShipRelation 切花訂單、配貨單、出貨單關聯
機密等級：內部文件 版權所有©2020凌誠科技股份有限公司
310/391

文件名稱：資料庫設計規格書 皇基股份有限公司 日期：109年10月30日
序號 表格名稱 資料表說明
4 CF_TransferAndDistribution 切花移轉、配貨關聯
5 CFDistribution 切花配貨單、訂單關聯
6 CFDistribution_All 切花配貨明細
7 CFDistribution_Sum 切花配貨數 BY 客戶
8 CFSampleSurvey_All 切花抽梗調查明細
9 CFShipAndDetail 切花出貨明細
10 CFShipAndDist 切花出貨和配貨明細
11 CFShipSurvey 切花出貨調查明細
12 CFShipSurvey_HF_All 切花出貨調查高朵數明細
13 CFShipSurvey_Roll_All 切花出貨抽樣點花調查明細
14 CFShipSurveyMap_Roll 切花抽樣點花，點花明細
15 CFStemSurvey_All 切花點梗調查明細
16 CFShipSurveyMap_HF 切花點梗調查高朵數明細
17 CFStemSurvey 切花點梗調查
18 CFStemSurveyMap 切花點梗調查，梗數明細
19 CFTransferBatch 切花批次明細
20 CFTransferBatch_Sum 切花庫存明細
21 CFTransferRecord 切花移轉記錄明細
22 CFTransferRecord_Sync 拋轉中介所需要切花移轉記錄
23 PersonelPermission 帳號、權限、角色
24 PPBudSurvey_All 打荳調查詳細資訊
25 PPBudSurveyMap 打荳調查來源明細
26 PPDistribution_All 盆花配貨明細
盆花訂單確認頁、出貨頁，載入符合的配
27 PPDistribution_All_WithName
貨明細
28 PPDistribution_Sum 盆花配貨頁，列出庫存
29 PPOrderPackingSetting 盆花訂單包裝列表
30 PPOrderPackingSettingDetail 包裝設定明細列表
31 PPShipDetail 盆花出貨明細列表
32 PPShipPackingSetting 盆花包裝設定列表
33 PPShipPackingSettingDetail 包裝設定明細列表
34 PPStemSurvey 盆花來梗調查列表
35 PPStemSurvey_All 盆花來梗調查資訊
36 PPStemSurveyMap 盆花來梗調查來源明細
37 PPTransferBatch_Sum_P 未使用
38 PPTransferRecord_Sync 盆花移轉拋轉中介資料
機密等級：內部文件 版權所有©2020凌誠科技股份有限公司
311/391

| 文件名稱：資料庫設計規格書  |       | 皇基股份有限公司  |        | 日期：109年10月30日  |     |
| -------------- | ----- | --------- | ------ | -------------- | --- |
| 序號             | 表格名稱  |           | 資料表說明  |                |     |
39  Rpt_CF002  切花點梗出貨預估表
40  Rpt_CF004  切花高朵數出貨預估表
41  SCPurchaseOrder  採購單列表
42  SCPurchaseOrder_Sync  採購單拋轉中介列表
43  SCUnderContract_Sync  契作批次拋轉中介列表
出貨包裝明細
44  ShipPacking
45  YPProductionBatch_sum  生產批次庫存
46  YPProductionBatchProcessLog  翻種的生產批次製程記錄
配貨出貨列表
47  YPShipPlan
48  YPShipRecord  配貨出貨列表明細
49  YPTransferRecord_All  未使用
50  盆花庫存數量  盆花庫存
51  苗株庫存數量  苗株庫存
二、檔案、資料表欄項一覽表
1.  資料表名稱：BIBreed
| 索引  名稱    | 型態  非空值    | 唯一  長度   | 初始值  | 說明  |     |
| --------- | ---------- | -------- | ---- | --- | --- |
|           |            |          |      |     |     |
| True  ID  | int  True  | True  0  |      |     |     |
花色
| False  ColorID  | int  True   | False  0   | ((0))  |     |     |
| --------------- | ----------- | ---------- | ------ | --- | --- |
| False  Name     | nvarc True  | True  100  | ('')   | 名稱  |     |
har
| False  FlowerSizeType  | int  True   | False  0    | ((0))  | 花色分類   |     |
| ---------------------- | ----------- | ----------- | ------ | ------ | --- |
| False  HeightStart     | int  True   | False  0    | ((0))  | 株高(低)  |     |
| False  HeightEnd       | int  True   | False  0    | ((0))  | 株高(高)  |     |
| False  PartNo          | nvarc True  | False  100  | ('')   | 料號     |     |
har
圖片連結
| False  PicUrl  | varch True  | False  1000  | ('')  |     |     |
| -------------- | ----------- | ------------ | ----- | --- | --- |
ar
| False  Remark  | nvarc True  | False  100  | ('')  | 備註  |     |
| -------------- | ----------- | ----------- | ----- | --- | --- |
har
| False  IsEnable      | bit  True    | False  0  | ((1))      | 啟用    |     |
| -------------------- | ------------ | --------- | ---------- | ----- | --- |
| False  CreateUserID  | int  True    | False  0  | ((0))      | 創建者   | ID  |
| False  CreateDate    | dateti True  | False  0  | (sysdateti | 創建日期  |     |
|                      | me2          |           | me())      |       |     |
修改者
| False  ModifyUserID  | int  True    | False  0  | ((0))                |       | ID  |
| -------------------- | ------------ | --------- | -------------------- | ----- | --- |
| False  ModifyDate    | dateti True  | False  0  | (sysdateti           | 修改日期  |     |
| 機密等級：內部文件            |              |           | 版權所有©2020凌誠科技股份有限公司  |       |     |
312/391

| 文件名稱：資料庫設計規格書  |      | 皇基股份有限公司  |        | 日期：109年10月30日  |
| -------------- | ---- | --------- | ------ | -------------- |
|                | me2  |           | me())  |                |

約束
| 名稱              | 型態      | 欄位       |     |     |
| --------------- | ------- | -------- | --- | --- |
| PK_PropBreed_1  | Public  | ID       |     |     |
| UQ_Breed_Name   | Public  | Name     |     |     |
| FK_Breed_Color  | Public  | ColorID  |     |     |

關連
| 欄位              | 關連                       |     |     |     |
| --------------- | ------------------------ | --- | --- | --- |
| (BreedID = ID)  | 0..*                     |     |     |     |
|                 | FK_BIBreedAlias_BreedID  |     |     |     |
 1
PK_PropBreed_1
| (ColorID = ID)  | 0..*   |     |     |     |
| --------------- | ------ | --- | --- | --- |
FK_Breed_Color
 1
PK_PropColor

2.  資料表名稱：BIBreedAlias
| 索引  名稱             | 型態    | 非空值  唯一  長度       | 初始值    | 說明     |
| ------------------ | ----- | ----------------- | ------ | ------ |
|                    |       |                   |        |        |
| True  ID           | int   | True  True  0     |        |        |
| False  BreedID     | int   | True  False  0    | ((0))  | 品種 ID  |
| False  SupplierID  | int   | True  False  0    | ((0))  | 廠商 ID  |
| False  AliasName   | nvarc | True  False  100  | ('')   | 品種別名   |
har
品種類別
| False  ParticularName  | nvarc | True  False  100  | ('')  |     |
| ---------------------- | ----- | ----------------- | ----- | --- |
har
| False  Remark  | nvarc | True  False  100  | ('')  | 備註  |
| -------------- | ----- | ----------------- | ----- | --- |
har
| False  PartNo  | nvarc | True  False  100  | ('')  | 料號  |
| -------------- | ----- | ----------------- | ----- | --- |
har
| False  IsEnable  | bit  | True  False  0  | ((1))  | 停用            |
| ---------------- | ---- | --------------- | ------ | ------------- |
| False  IsBreed   | bit  | True  False  0  | ((0))  | 是否預設品種(true:  |
表示由品種自動產生)
| False  CreateUserID  | int    | True  False  0  | ((0))                | 創建者 ID  |
| -------------------- | ------ | --------------- | -------------------- | ------- |
| False  CreateDate    | dateti | True  False  0  | (sysdateti           | 創建日期    |
|                      | me2    |                 | me())                |         |
| 機密等級：內部文件            |        |                 | 版權所有©2020凌誠科技股份有限公司  |         |
313/391

| 文件名稱：資料庫設計規格書        |        | 皇基股份有限公司        |            | 日期：109年10月30日  |     |
| -------------------- | ------ | --------------- | ---------- | -------------- | --- |
| False  ModifyUserID  | int    | True  False  0  | ((0))      | 修改者            | ID  |
| False  ModifyDate    | dateti | True  False  0  | (sysdateti | 修改日期           |     |
|                      | me2    |                 | me())      |                |     |

約束
| 名稱                   | 型態      | 欄位       |     |     |     |
| -------------------- | ------- | -------- | --- | --- | --- |
| PK_PropBreedAlias    | Public  | ID       |     |     |     |
| FK_BIBreedAlias_Bree | Public  | BreedID  |     |     |     |
dID

關連
| 欄位                   | 關連                                     |     |     |     |     |
| -------------------- | -------------------------------------- | --- | --- | --- | --- |
| (BreedAliasID = ID)  | 0..*                                   |     |     |     |     |
|                      | FK_SCPurchaseOrderDetail_BreedAliasID  |     |     |     |     |
 1
PK_PropBreedAlias
| (BreedID = ID)  | 0..*                     |     |     |     |     |
| --------------- | ------------------------ | --- | --- | --- | --- |
|                 | FK_BIBreedAlias_BreedID  |     |     |     |     |
 1
PK_PropBreed_1
| (BreedAliasID = ID)  | 0..*                             |     |     |     |     |
| -------------------- | -------------------------------- | --- | --- | --- | --- |
|                      | FK_SCUnderContract_BIBreedAlias  |     |     |     |     |
 1
PK_PropBreedAlias

3.  資料表名稱：BIColor
| 索引  名稱                  | 型態    | 非空值  唯一  長度     | 初始值    | 說明   |     |
| ----------------------- | ----- | --------------- | ------ | ---- | --- |
|                         |       |                 |        |      |     |
| True  ID                | int   | True  True  0   |        |      |     |
| False  ColorCategoryID  | int   | True  False  0  | ((0))  | 花色類別 | ID  |
| False  Code             | nvarc | True  True  50  | ('')   | 代號   |     |
har
名稱
| False  Name  | nvarc | True  True  100  | ('')  |     |     |
| ------------ | ----- | ---------------- | ----- | --- | --- |
har
| False  NameShort  | nvarc | True  False  100  | ('')  | 簡稱  |     |
| ----------------- | ----- | ----------------- | ----- | --- | --- |
har
| False  Japanese  | nvarc | True  False  100  | ('')  | 日文  |     |
| ---------------- | ----- | ----------------- | ----- | --- | --- |
har
| False  Tag  | nvarc | True  False  100  | ('')                 | 標籤  |     |
| ----------- | ----- | ----------------- | -------------------- | --- | --- |
| 機密等級：內部文件   |       |                   | 版權所有©2020凌誠科技股份有限公司  |     |     |
314/391

| 文件名稱：資料庫設計規格書  |     | 皇基股份有限公司  |     | 日期：109年10月30日  |
| -------------- | --- | --------- | --- | -------------- |
har
| False  Remark  | nvarc | True  False  100  | ('')  | 備註  |
| -------------- | ----- | ----------------- | ----- | --- |
har
| False  IsEnable      | bit    | True  False  0  | ((1))      | 停用      |
| -------------------- | ------ | --------------- | ---------- | ------- |
| False  CreateUserID  | int    | True  False  0  | ((0))      | 創建者 ID  |
| False  CreateDate    | dateti | True  False  0  | (sysdateti | 創建日期    |
|                      | me2    |                 | me())      |         |
| False  ModifyUserID  | int    | True  False  0  | ((0))      | 修改者 ID  |
| False  ModifyDate    | dateti | True  False  0  | (sysdateti | 修改日期    |
|                      | me2    |                 | me())      |         |

約束
| 名稱             | 型態      | 欄位    |     |     |
| -------------- | ------- | ----- | --- | --- |
| PK_PropColor   | Public  | ID    |     |     |
| UQ_Color_Code  | Public  | Code  |     |     |
| UQ_Color_Name  | Public  | Name  |     |     |

關連
| 欄位              | 關連     |     |     |     |
| --------------- | ------ | --- | --- | --- |
| (ColorID = ID)  | 0..*   |     |     |     |
FK_Breed_Color
 1
PK_PropColor

4.  資料表名稱：BIColorCategory
| 索引  名稱       | 型態    | 非空值  唯一  長度      | 初始值   | 說明      |
| ------------ | ----- | ---------------- | ----- | ------- |
|              |       |                  |       |         |
| True  ID     | int   | True  True  0    |       |         |
| False  Name  | nvarc | True  True  100  | ('')  | 花色類別名稱  |
har

花色類型
| False  ColorType  | int   | False  False  0   |       |     |
| ----------------- | ----- | ----------------- | ----- | --- |
| False  Remark     | nvarc | True  False  100  | ('')  | 備註  |
har
停用
| False  IsEnable      | bit    | True  False  0  | ((1))                |         |
| -------------------- | ------ | --------------- | -------------------- | ------- |
| False  CreateUserID  | int    | True  False  0  | ((0))                | 創建者 ID  |
| False  CreateDate    | dateti | True  False  0  | (sysdateti           | 創建日期    |
|                      | me2    |                 | me())                |         |
| False  ModifyUserID  | int    | True  False  0  | ((0))                | 修改者 ID  |
| False  ModifyDate    | dateti | True  False  0  | (sysdateti           | 修改日期    |
| 機密等級：內部文件            |        |                 | 版權所有©2020凌誠科技股份有限公司  |         |
315/391

| 文件名稱：資料庫設計規格書  |      | 皇基股份有限公司  |        | 日期：109年10月30日  |
| -------------- | ---- | --------- | ------ | -------------- |
|                | me2  |           | me())  |                |

約束
| 名稱                     | 型態      | 欄位    |     |     |
| ---------------------- | ------- | ----- | --- | --- |
| PK_PropColorCategrory  | Public  | ID    |     |     |
| UQ_ColorCategory_Na    | Public  | Name  |     |     |
me

5.  資料表名稱：BICustomer
| 索引  名稱  | 型態  | 非空值  唯一  長度  | 初始值  | 說明  |
| ------- | --- | ------------ | ---- | --- |

客戶 ID
| True  ID          | int   | True  True  0    |        |        |
| ----------------- | ----- | ---------------- | ------ | ------ |
| False  CompanyID  | int   | True  False  0   | ((0))  | 公司 ID  |
| False  Company    | nvarc | True  False  10  | ('')   | 公司別    |
har
| False  Code  | nvarc | True  False  50  | ('')  | 客戶代號  |
| ------------ | ----- | ---------------- | ----- | ----- |
har
| False  NameShort  | nvarc | True  False  30  | ('')  | 客戶簡稱  |
| ----------------- | ----- | ---------------- | ----- | ----- |
har
客戶全名
| False  Name  | nvarc | True  False  100  | ('')  |     |
| ------------ | ----- | ----------------- | ----- | --- |
har
| False  Currency  | nvarc | True  False  4  | ('')  | 交易幣別  |
| ---------------- | ----- | --------------- | ----- | ----- |
har
| False  Department  | nvarc | True  False  10  | ('')  | 部門別  |
| ------------------ | ----- | ---------------- | ----- | ---- |
har
| False  Salesman  | nvarc | True  False  10  | ('')  | 業務人員  |
| ---------------- | ----- | ---------------- | ----- | ----- |
har
地區別
| False  AreaType  | nvarc | True  False  10  | ('')  |     |
| ---------------- | ----- | ---------------- | ----- | --- |
har
| False  Address  | nvarc | True  False  255  | ('')  | 登記地址(一)  |
| --------------- | ----- | ----------------- | ----- | -------- |
har
| False  Airport  | nvarc | True  False  50  | ('')  | 空運機場  |
| --------------- | ----- | ---------------- | ----- | ----- |
har
| False  NameEng  | nvarc | True  False  100  | ('')  | 客戶英文全名  |
| --------------- | ----- | ----------------- | ----- | ------- |
har
客戶主鍵
| False  CU_ID         | int  | True  False  0  | ((0))   | ERP     |
| -------------------- | ---- | --------------- | ------- | ------- |
| False  ShipWeekday   | int  | True  False  0  | ((-1))  | 固定出貨日   |
| False  CreateUserID  | int  | True  False  0  | ((0))   | 建立者 ID  |
創建日期
| False  CreateDate  | dateti | True  False  0  | (sysdateti           |     |
| ------------------ | ------ | --------------- | -------------------- | --- |
| 機密等級：內部文件          |        |                 | 版權所有©2020凌誠科技股份有限公司  |     |
316/391

| 文件名稱：資料庫設計規格書        |      | 皇基股份有限公司        |        | 日期：109年10月30日  |
| -------------------- | ---- | --------------- | ------ | -------------- |
|                      | me2  |                 | me())  |                |
| False  ModifyUserID  | int  | True  False  0  | ((0))  | 修改者 ID         |
修改日期
| False  ModifyDate  | dateti | True  False  0  | (sysdateti |     |
| ------------------ | ------ | --------------- | ---------- | --- |
|                    | me2    |                 | me())      |     |

約束
| 名稱             | 型態      | 欄位  |     |     |
| -------------- | ------- | --- | --- | --- |
| PK_BICustomer  | Public  | ID  |     |     |

關連
| 欄位                 | 關連     |     |     |     |
| ------------------ | ------ | --- | --- | --- |
| (CustomerID = ID)  | 0..*   |     |     |     |
FK_CustomerID
 1
PK_BICustomer
| (CustomerID = ID)  | 0..*                                |     |     |     |
| ------------------ | ----------------------------------- | --- | --- | --- |
|                    | FK_YPTransferRecordTemp_CustomerID  |     |     |     |
 1
PK_BICustomer

6.  資料表名稱：BIMedium
| 索引  名稱       | 型態    | 非空值  唯一  長度     | 初始值   | 說明    |
| ------------ | ----- | --------------- | ----- | ----- |
|              |       |                 |       |       |
| True  ID     | int   | True  True  0   |       |       |
| False  Code  | nvarc | True  True  50  | ('')  | 介質代號  |
har
| False  Name  | nvarc | True  False  100  | ('')  | 介質名稱  |
| ------------ | ----- | ----------------- | ----- | ----- |
har
| False  Remark  | nvarc | True  False  100  | ('')  | 備註  |
| -------------- | ----- | ----------------- | ----- | --- |
har
| False  IsEnable      | bit    | True  False  0  | ((1))      | 停用      |
| -------------------- | ------ | --------------- | ---------- | ------- |
| False  CreateUserID  | int    | True  False  0  | ((0))      | 創建者 ID  |
| False  CreateDate    | dateti | True  False  0  | (sysdateti | 創建日期    |
|                      | me2    |                 | me())      |         |
| False  ModifyUserID  | int    | True  False  0  | ((0))      | 修改者 ID  |
修改日期
| False  ModifyDate  | dateti | True  False  0  | (sysdateti |     |
| ------------------ | ------ | --------------- | ---------- | --- |
|                    | me2    |                 | me())      |     |

約束
| 機密等級：內部文件  |     |     | 版權所有©2020凌誠科技股份有限公司  |     |
| ---------- | --- | --- | -------------------- | --- |
317/391

| 文件名稱：資料庫設計規格書        |         | 皇基股份有限公司  |     | 日期：109年10月30日  |
| -------------------- | ------- | --------- | --- | -------------- |
| 名稱                   | 型態      | 欄位        |     |                |
| PK_PropGrowingMedia  | Public  | ID        |     |                |
| UQ_GrowingMedia_Co   | Public  | Code      |     |                |
de

7.  資料表名稱：BIPPPackingCondition
| 索引  名稱  | 型態  | 非空值  唯一  長度  | 初始值  | 說明  |
| ------- | --- | ------------ | ---- | --- |

| True  ID  | int  | True  True  0  |     | 出貨包裝/入數關聯檔 |
| --------- | ---- | -------------- | --- | ---------- |
ID
| False  ShipType  | int  | True  False  0  | ((0))  | 銷貨類別  |
| ---------------- | ---- | --------------- | ------ | ----- |
適用包裝入數
| False  ShipPackingMap | int  | True  False  0  | ((0))  |     |
| --------------------- | ---- | --------------- | ------ | --- |
ID
| False  FlowerSizeType  | int   | True  False  0    | ((0))  | 花色分類     |
| ---------------------- | ----- | ----------------- | ------ | -------- |
| False  StemID          | int   | True  False  0    | ((0))  | 梗數       |
| False  GradeIDs        | varch | True  False  200  | ('0')  | 等級 ID集合  |
ar
| False  IsEnable  | bit   | True  False  0    | ((1))  | 啟用狀態  |
| ---------------- | ----- | ----------------- | ------ | ----- |
| False  Remark    | nvarc | True  False  100  | ('')   | 備註    |
har
| False  CreateUserID  | int    | True  False  0  | ((0))      | 建立者 ID  |
| -------------------- | ------ | --------------- | ---------- | ------- |
| False  CreateDate    | dateti | True  False  0  | (sysdateti | 創建日期    |
|                      | me2    |                 | me())      |         |
| False  ModifyUserID  | int    | True  False  0  | ((0))      | 修改者 ID  |
| False  ModifyDate    | dateti | True  False  0  | (sysdateti | 修改日期    |
|                      | me2    |                 | me())      |         |

約束
| 名稱                   | 型態      | 欄位  |     |     |
| -------------------- | ------- | --- | --- | --- |
| PK_BIPPPackingCondit | Public  | ID  |     |     |
| ion                  |         |     |     |     |

8.  資料表名稱：BIPackingColor
| 索引  名稱  | 型態  | 非空值  唯一  長度  | 初始值  | 說明  |
| ------- | --- | ------------ | ---- | --- |

| True  ID     | int   | True  True  0    |       | 流水帳 ID  |
| ------------ | ----- | ---------------- | ----- | ------- |
| False  Code  | nvarc | True  False  50  | ('')  | 顏色代號    |
har
| False  Name  | nvarc | True  False  100  | ('')  | 顏色全名  |
| ------------ | ----- | ----------------- | ----- | ----- |
har
| 機密等級：內部文件  |     |     | 版權所有©2020凌誠科技股份有限公司  |     |
| ---------- | --- | --- | -------------------- | --- |
318/391

| 文件名稱：資料庫設計規格書  |       | 皇基股份有限公司        |       | 日期：109年10月30日  |
| -------------- | ----- | --------------- | ----- | -------------- |
| False  Hex     | varch | True  False  7  | ('')  | 色票編碼           |
ar
| False  Remark  | nvarc | True  False  100  | ('')  | 備註  |
| -------------- | ----- | ----------------- | ----- | --- |
har
| False  IsEnable      | bit    | True  False  0  | ((1))      | 啟用狀態    |
| -------------------- | ------ | --------------- | ---------- | ------- |
| False  CreateUserID  | int    | True  False  0  | ((0))      | 建立者 ID  |
| False  CreateDate    | dateti | True  False  0  | (sysdateti | 創建日期    |
|                      | me2    |                 | me())      |         |
| False  ModifyUserID  | int    | True  False  0  | ((0))      | 修改者 ID  |
| False  ModifyDate    | dateti | True  False  0  | (sysdateti | 修改日期    |
|                      | me2    |                 | me())      |         |

約束
| 名稱                 | 型態      | 欄位  |     |     |
| ------------------ | ------- | --- | --- | --- |
| PK_BIPackingColor  | Public  | ID  |     |     |

9.  資料表名稱：BIPackingSize
| 索引  名稱  | 型態  | 非空值  唯一  長度  | 初始值  | 說明  |
| ------- | --- | ------------ | ---- | --- |

流水帳 ID
| True  ID             | int   | True  True  0     |        |         |
| -------------------- | ----- | ----------------- | ------ | ------- |
| False  TransferType  | int   | True  False  0    | ((0))  | 移轉表類別   |
| False  Name          | nvarc | True  False  100  | ('')   | 材積規格名稱  |
har
| False  CoverLength  | int  | True  False  0  | ((0))  | 箱蓋長  |
| ------------------- | ---- | --------------- | ------ | ---- |
| False  CoverWidth   | int  | True  False  0  | ((0))  | 箱蓋寬  |
箱蓋高
| False  CoverHeight   | int   | True  False  0    | ((0))  |      |
| -------------------- | ----- | ----------------- | ------ | ---- |
| False  BottomLength  | int   | True  False  0    | ((0))  | 箱底長  |
| False  BottomWidth   | int   | True  False  0    | ((0))  | 箱底寬  |
| False  BottomHeight  | int   | True  False  0    | ((0))  | 箱底高  |
| False  Remark        | nvarc | True  False  100  | ('')   | 備註   |
har
| False  IsEnable      | bit  | True  False  0  | ((1))  | 啟用狀態    |
| -------------------- | ---- | --------------- | ------ | ------- |
| False  CreateUserID  | int  | True  False  0  | ((0))  | 建立者 ID  |
創建日期
| False  CreateDate    | dateti | True  False  0  | (sysdateti |         |
| -------------------- | ------ | --------------- | ---------- | ------- |
|                      | me2    |                 | me())      |         |
| False  ModifyUserID  | int    | True  False  0  | ((0))      | 修改者 ID  |
修改日期
| False  ModifyDate  | dateti | True  False  0  | (sysdateti |     |
| ------------------ | ------ | --------------- | ---------- | --- |
|                    | me2    |                 | me())      |     |

| 機密等級：內部文件  |     |     | 版權所有©2020凌誠科技股份有限公司  |     |
| ---------- | --- | --- | -------------------- | --- |
319/391

| 文件名稱：資料庫設計規格書  |     | 皇基股份有限公司  |     | 日期：109年10月30日  |     |
| -------------- | --- | --------- | --- | -------------- | --- |
約束
| 名稱                | 型態      | 欄位  |     |     |     |
| ----------------- | ------- | --- | --- | --- | --- |
| PK_BIPackingSize  | Public  | ID  |     |     |     |

10.  資料表名稱：BIPersonel
| 索引  名稱  | 型態  | 非空值  唯一  長度  | 初始值  | 說明  |     |
| ------- | --- | ------------ | ---- | --- | --- |

| True  ID     | int    | True  True  0   |        | 人員帳號     | ID   |
| ------------ | ------ | --------------- | ------ | -------- | ---- |
| False  Type  | tinyin | True  False  0  | ((0))  | 帳號類型，1:  | 系統,  |
|              | t      |                 |        | 2: AD    |      |

| False  PlatformType  | int  | True  False  0  | ((0))  |     |     |
| -------------------- | ---- | --------------- | ------ | --- | --- |

人員帳號
| False  Account  | nvarc | True  True  50  |     |     |     |
| --------------- | ----- | --------------- | --- | --- | --- |
har
| False  Password  | nvarc | True  False  255  | ('')  | 人員密碼  |     |
| ---------------- | ----- | ----------------- | ----- | ----- | --- |
har
| False  Name  | nvarc | True  False  50  | ('')  | 人員名稱  |     |
| ------------ | ----- | ---------------- | ----- | ----- | --- |
har
| False  Email  | nvarc | True  False  100  | ('')  | 人員 Email  |     |
| ------------- | ----- | ----------------- | ----- | --------- | --- |
har
電話國碼
| False  TelePhone_Count | nvarc | True  False  4  | ('')  |     |     |
| ---------------------- | ----- | --------------- | ----- | --- | --- |
ry  har
| False  TelePhone_Area  | nvarc | True  False  6  | ('')  | 電話區碼  |     |
| ---------------------- | ----- | --------------- | ----- | ----- | --- |
har
| False  TelePhone  | nvarc | True  False  50  | ('')  | 電話號碼  |     |
| ----------------- | ----- | ---------------- | ----- | ----- | --- |
har
| False  TelePhone_Exten | nvarc | True  False  6  | ('')  | 分機號碼  |     |
| ---------------------- | ----- | --------------- | ----- | ----- | --- |
sion  har

| False  IsEnable  | bit   | True  False  0    | ((0))  |      |     |
| ---------------- | ----- | ----------------- | ------ | ---- | --- |
| False  Company   | int   | True  False  0    | ((0))  | 公司別  |     |
| False  Remark    | nvarc | True  False  100  | ('')   | 備註   |     |
har
| False  CreateUserID  | int    | True  False  0  | ((0))      | 創建者   | ID  |
| -------------------- | ------ | --------------- | ---------- | ----- | --- |
| False  CreateDate    | dateti | True  False  0  | (sysdateti | 創建日期  |     |
|                      | me2    |                 | me())      |       |     |
| False  ModifyUserID  | int    | True  False  0  | ((0))      | 修改者   | ID  |
| False  ModifyDate    | dateti | True  False  0  | (sysdateti | 修改日期  |     |
|                      | me2    |                 | me())      |       |     |

約束
| 機密等級：內部文件  |     |     | 版權所有©2020凌誠科技股份有限公司  |     |     |
| ---------- | --- | --- | -------------------- | --- | --- |
320/391

| 文件名稱：資料庫設計規格書       |         | 皇基股份有限公司  |     | 日期：109年10月30日  |
| ------------------- | ------- | --------- | --- | -------------- |
| 名稱                  | 型態      | 欄位        |     |                |
| PK_BS_Personel      | Public  | ID        |     |                |
| UK_BI_Peronel_Accou | Public  | Account   |     |                |
nt

關連
| 欄位                   | 關連                                   |     |     |     |
| -------------------- | ------------------------------------ | --- | --- | --- |
| (ModifyUserID = ID)  | 0..*                                 |     |     |     |
|                      | FK_SCUnderContractRecord_BIPersonel  |     |     |     |
 1
PK_BS_Personel
| (VisitPersonID = ID)  | 0..*   |     |     |     |
| --------------------- | ------ | --- | --- | --- |
FK_SCUnderContractVisit_BIPersonel_VisitPerson
 1
PK_BS_Personel
| (ModifyUserID = ID)  | 0..*                                           |     |     |     |
| -------------------- | ---------------------------------------------- | --- | --- | --- |
|                      | FK_SCUnderContractVisit_BIPersonel_ModifyUser  |     |     |     |
 1
PK_BS_Personel
| (CreateUserID = ID)  | 0..*   |     |     |     |
| -------------------- | ------ | --- | --- | --- |
FK_SCUnderContractVisit_BIPersonel
 1
PK_BS_Personel
| (CreateUserID = ID)  | 0..*                                        |     |     |     |
| -------------------- | ------------------------------------------- | --- | --- | --- |
|                      | FK_SCUnderContractRecord_BIPersonel_Create  |     |     |     |
 1
PK_BS_Personel
| (CreateUserID = ID)  | 0..*                                       |     |     |     |
| -------------------- | ------------------------------------------ | --- | --- | --- |
|                      | FK_YPProductionBatchProcessLog_BIPersonel  |     |     |     |
 1
PK_BS_Personel

11.  資料表名稱：BIPersonelProductionLineMap
| 索引  名稱             | 型態   | 非空值  唯一  長度     | 初始值    | 說明     |
| ------------------ | ---- | --------------- | ------ | ------ |
|                    |      |                 |        |        |
| True  ID           | int  | True  True  0   |        |        |
| False  PersonelID  | int  | True  False  0  | ((0))  | 人員 ID  |
產線 ID
| False  ProductionLineI | int  | True  False  0  | ((0))  |     |
| ---------------------- | ---- | --------------- | ------ | --- |
D
| 機密等級：內部文件  |     |     | 版權所有©2020凌誠科技股份有限公司  |     |
| ---------- | --- | --- | -------------------- | --- |
321/391

| 文件名稱：資料庫設計規格書        |      | 皇基股份有限公司        |        | 日期：109年10月30日  |
| -------------------- | ---- | --------------- | ------ | -------------- |
| False  IsDefault     | bit  | True  False  0  | ((0))  | 預設產線           |
| False  CreateUserID  | int  | True  False  0  | ((0))  | 創建者 ID         |
創建日期
| False  CreateDate    | dateti | True  False  0  | (sysdateti |         |
| -------------------- | ------ | --------------- | ---------- | ------- |
|                      | me2    |                 | me())      |         |
| False  ModifyUserID  | int    | True  False  0  | ((0))      | 修改者 ID  |
| False  ModifyDate    | dateti | True  False  0  | (sysdateti | 修改日期    |
|                      | me2    |                 | me())      |         |

約束
| 名稱                    | 型態      | 欄位  |     |     |
| --------------------- | ------- | --- | --- | --- |
| PK_BIPersonelProducti | Public  | ID  |     |     |
onLineMap

12.  資料表名稱：BIPosition
| 索引  名稱                 | 型態   | 非空值  唯一  長度    | 初始值    | 說明     |
| ---------------------- | ---- | -------------- | ------ | ------ |
|                        |      |                |        |        |
| True  ID               | int  | True  True  0  |        |        |
| False  ProductionLineI | int  | True  True  0  | ((0))  | 產線 ID  |
D
位置一
| False  Position1  | nvarc | True  True  100  | ('')  |     |
| ----------------- | ----- | ---------------- | ----- | --- |
har
| False  Position2  | nvarc | True  True  100  | ('')  | 位置二  |
| ----------------- | ----- | ---------------- | ----- | ---- |
har
| False  IsEnable      | bit    | True  False  0  | ((1))      | 停用      |
| -------------------- | ------ | --------------- | ---------- | ------- |
| False  CreateUserID  | int    | True  False  0  | ((0))      | 創建者 ID  |
| False  CreateDate    | dateti | True  False  0  | (sysdateti | 創建日期    |
|                      | me2    |                 | me())      |         |
| False  ModifyUserID  | int    | True  False  0  | ((0))      | 修改者 ID  |
| False  ModifyDate    | dateti | True  False  0  | (sysdateti | 修改日期    |
|                      | me2    |                 | me())      |         |

約束
| 名稱             | 型態      | 欄位                |     |     |
| -------------- | ------- | ----------------- | --- | --- |
| PK_Position_1  | Public  | ID                |     |     |
| UQ_Position    | Public  | ProductionLineID  |     |     |
Position1
Position2

關連
| 機密等級：內部文件  |     |     | 版權所有©2020凌誠科技股份有限公司  |     |
| ---------- | --- | --- | -------------------- | --- |
322/391

| 文件名稱：資料庫設計規格書      |        | 皇基股份有限公司  |     | 日期：109年10月30日  |
| ------------------ | ------ | --------- | --- | -------------- |
| 欄位                 | 關連     |           |     |                |
| (PositionID = ID)  | 0..*   |           |     |                |
FK_YPTransferRecordTemp_PositionID
 1
PK_Position_1

13.  資料表名稱：BIPot
| 索引  名稱       | 型態    | 非空值  唯一  長度     | 初始值   | 說明    |
| ------------ | ----- | --------------- | ----- | ----- |
|              |       |                 |       |       |
| True  ID     | int   | True  True  0   |       |       |
| False  Code  | nvarc | True  True  50  | ('')  | 盆器代號  |
har
| False  Name  | nvarc | True  True  100  | ('')  | 盆器名稱  |
| ------------ | ----- | ---------------- | ----- | ----- |
har
| False  Remark  | nvarc | True  False  100  | ('')  | 備註  |
| -------------- | ----- | ----------------- | ----- | --- |
har
停用
| False  IsEnable      | bit    | True  False  0  | ((1))      |         |
| -------------------- | ------ | --------------- | ---------- | ------- |
| False  CreateUserID  | int    | True  False  0  | ((0))      | 創建者 ID  |
| False  CreateDate    | dateti | True  False  0  | (sysdateti | 創建日期    |
|                      | me2    |                 | me())      |         |
| False  ModifyUserID  | int    | True  False  0  | ((0))      | 修改者 ID  |
| False  ModifyDate    | dateti | True  False  0  | (sysdateti | 修改日期    |
|                      | me2    |                 | me())      |         |

約束
| 名稱           | 型態      | 欄位    |     |     |
| ------------ | ------- | ----- | --- | --- |
| PK_PropPot   | Public  | ID    |     |     |
| UQ_Pot_Code  | Public  | Code  |     |     |
| UQ_Pot_Name  | Public  | Name  |     |     |

14.  資料表名稱：BIPrintField
| 索引  名稱    | 型態   | 非空值  唯一  長度    | 初始值  | 說明  |
| --------- | ---- | -------------- | ---- | --- |
|           |      |                |      |     |
| True  ID  | int  | True  True  0  |      |     |
標貼代號
| False  Name  | nvarc | True  False  100  | ('')  |     |
| ------------ | ----- | ----------------- | ----- | --- |
har
| False  ResourceKey  | nvarc | True  False  100  | ('')  | 標貼名稱  |
| ------------------- | ----- | ----------------- | ----- | ----- |
har
| False  TransferType  | int  | True  False  0  | ((0))  | 產線類型  |
| -------------------- | ---- | --------------- | ------ | ----- |
停用
| False  IsEnable  | bit  | True  False  0  | ((1))                |     |
| ---------------- | ---- | --------------- | -------------------- | --- |
| 機密等級：內部文件        |      |                 | 版權所有©2020凌誠科技股份有限公司  |     |
323/391

| 文件名稱：資料庫設計規格書        |        | 皇基股份有限公司        |            | 日期：109年10月30日  |
| -------------------- | ------ | --------------- | ---------- | -------------- |
| False  CreateUserID  | int    | True  False  0  | ((0))      | 創建者 ID         |
| False  CreateDate    | dateti | True  False  0  | (sysdateti | 創建日期           |
|                      | me2    |                 | me())      |                |
| False  ModifyUserID  | int    | True  False  0  | ((0))      | 修改者 ID         |
| False  ModifyDate    | dateti | True  False  0  | (sysdateti | 修改日期           |
|                      | me2    |                 | me())      |                |

約束
| 名稱               | 型態      | 欄位  |     |     |
| ---------------- | ------- | --- | --- | --- |
| PK_BIPrintField  | Public  | ID  |     |     |

15.  資料表名稱：BIProcess
| 索引  名稱       | 型態    | 非空值  唯一  長度     | 初始值   | 說明    |
| ------------ | ----- | --------------- | ----- | ----- |
|              |       |                 |       |       |
| True  ID     | int   | True  True  0   |       |       |
| False  Code  | nvarc | True  True  50  | ('')  | 製程代號  |
har
| False  Name  | nvarc | True  False  100  | ('')  | 製程名稱  |
| ------------ | ----- | ----------------- | ----- | ----- |
har
備註
| False  Remark  | nvarc | True  False  100  | ('')  |     |
| -------------- | ----- | ----------------- | ----- | --- |
har
| False  WorkDay  | int  | True  False  0  | ('')  | 工天數  |
| --------------- | ---- | --------------- | ----- | ---- |
停用
| False  IsEnable         | bit    | True  False  0  | ((1))      |         |
| ----------------------- | ------ | --------------- | ---------- | ------- |
| False  CreateUserID     | int    | True  False  0  | ((0))      | 創建者 ID  |
| False  CreateDate       | dateti | True  False  0  | (sysdateti | 創建日期    |
|                         | me2    |                 | me())      |         |
| False  ModifyUserID     | int    | True  False  0  | ((0))      | 修改者 ID  |
| False  ModifyDate       | dateti | True  False  0  | (sysdateti | 修改日期    |
|                         | me2    |                 | me())      |         |
| False  IsUnderContract  | bit    | True  False  0  | ((0))      | 契作製程    |
起始規格
| False  SpecBegin  | int  | True  False  0  | ((0))  |         |
| ----------------- | ---- | --------------- | ------ | ------- |
| False  SpecEnd    | int  | True  False  0  | ((0))  | 最終規絡    |
| False  IsCheck    | bit  | True  False  0  | ((1))  | 翻種檢查數量  |

約束
| 名稱               | 型態      | 欄位    |     |     |
| ---------------- | ------- | ----- | --- | --- |
| PK_PropProcess   | Public  | ID    |     |     |
| UQ_Process_Code  | Public  | Code  |     |     |

| 機密等級：內部文件  |     |     | 版權所有©2020凌誠科技股份有限公司  |     |
| ---------- | --- | --- | -------------------- | --- |
324/391

| 文件名稱：資料庫設計規格書  |     | 皇基股份有限公司  |     | 日期：109年10月30日  |
| -------------- | --- | --------- | --- | -------------- |
關連
| 欄位                | 關連                                        |     |     |     |
| ----------------- | ----------------------------------------- | --- | --- | --- |
| (ProcessID = ID)  | 0..*                                      |     |     |     |
|                   | FK_YPProductionBatchProcessLog_BIProcess  |     |     |     |
 1
PK_PropProcess
| (ProcessID = ID)  | 0..*                          |     |     |     |
| ----------------- | ----------------------------- | --- | --- | --- |
|                   | FK_SCUnderContract_BIProcess  |     |     |     |
 1
PK_PropProcess

16.  資料表名稱：BIProductionLine
| 索引  名稱       | 型態  非空值     | 唯一  長度     | 初始值   | 說明        |
| ------------ | ----------- | ---------- | ----- | --------- |
|              |             |            |       |           |
| True  ID     | int  True   | True  0    |       |           |
| False  Code  | nvarc True  | False  10  | ('')  | ERP 產線代號  |
har
| False  Name  | nvarc True  | True  50  | ('')  | 產線名稱  |
| ------------ | ----------- | --------- | ----- | ----- |
har
| False  ERPCode  | nvarc True  | False  10  | ('')  | ERP 廠別代號  |
| --------------- | ----------- | ---------- | ----- | --------- |
har
| False  ERPName  | nvarc True  | False  50  | ('')  | ERP 廠別名稱  |
| --------------- | ----------- | ---------- | ----- | --------- |
har
| False  IsShowCutNum  | bit  True  | False  0  | ((0))  | 顯示切次  |
| -------------------- | ---------- | --------- | ------ | ----- |
顯示品種類別
| False  IsShowBreedAlia | bit  True  | False  0  | ((0))  |     |
| ---------------------- | ---------- | --------- | ------ | --- |
s
| False  IsEnable  | bit  True   | False  0    | ((1))  | 停用  |
| ---------------- | ----------- | ----------- | ------ | --- |
| False  Remark    | nvarc True  | False  100  | ('')   | 備註  |
har
| False  CreateUserID  | int  True    | False  0  | ((0))      | 創建者 ID  |
| -------------------- | ------------ | --------- | ---------- | ------- |
| False  CreateDate    | dateti True  | False  0  | (sysdateti | 創建日期    |
|                      | me2          |           | me())      |         |
修改者 ID
| False  ModifyUserID  | int  True    | False  0  | ((0))      |       |
| -------------------- | ------------ | --------- | ---------- | ----- |
| False  ModifyDate    | dateti True  | False  0  | (sysdateti | 修改日期  |
|                      | me2          |           | me())      |       |

啟用拋轉日期
| False  ThrowDate  | date  False  | False  0  |     |     |
| ----------------- | ------------ | --------- | --- | --- |

約束
| 機密等級：內部文件  |     |     | 版權所有©2020凌誠科技股份有限公司  |     |
| ---------- | --- | --- | -------------------- | --- |
325/391

| 文件名稱：資料庫設計規格書        |         | 皇基股份有限公司  |     | 日期：109年10月30日  |     |
| -------------------- | ------- | --------- | --- | -------------- | --- |
| 名稱                   | 型態      | 欄位        |     |                |     |
| PK_ProductionLine    | Public  | ID        |     |                |     |
| UQ_ProductionLine_Na | Public  | Name      |     |                |     |
me

17.  資料表名稱：BIProductionLinePrintFieldMap
| 索引  名稱                 | 型態   | 非空值  唯一  長度     | 初始值    | 說明     |     |
| ---------------------- | ---- | --------------- | ------ | ------ | --- |
|                        |      |                 |        |        |     |
| True  ID               | int  | True  True  0   |        |        |     |
| False  ProductionLineI | int  | True  False  0  | ((0))  | 產線 ID  |     |
D
|                      |        |                 |            | 標貼欄位  | ID  |
| -------------------- | ------ | --------------- | ---------- | ----- | --- |
| False  PrintFieldID  | int    | True  False  0  | ((0))      |       |     |
| False  CreateUserID  | int    | True  False  0  | ((0))      | 創建者   | ID  |
| False  CreateDate    | dateti | True  False  0  | (sysdateti | 創建日期  |     |
|                      | me2    |                 | me())      |       |     |
| False  ModifyUserID  | int    | True  False  0  | ((0))      | 修改者   | ID  |
| False  ModifyDate    | dateti | True  False  0  | (sysdateti | 修改日期  |     |
|                      | me2    |                 | me())      |       |     |

約束
| 名稱                    | 型態      | 欄位  |     |     |     |
| --------------------- | ------- | --- | --- | --- | --- |
| PK_BIProductinoLinePr | Public  | ID  |     |     |     |
intFieldMap

18.  資料表名稱：BIProductionLineReasonMap
| 索引  名稱                 | 型態   | 非空值  唯一  長度     | 初始值    | 說明     |     |
| ---------------------- | ---- | --------------- | ------ | ------ | --- |
|                        |      |                 |        |        |     |
| True  ID               | int  | True  True  0   |        |        |     |
| False  ProductionLineI | int  | True  False  0  | ((0))  | 產線 ID  |     |
D
| False  ReasonID  | int  | True  False  0  | ((0))  | 移轉原因 | ID  |
| ---------------- | ---- | --------------- | ------ | ---- | --- |
原因說明
| False  ReasonDescID  | int    | True  False  0  | ((0))      |       | ID  |
| -------------------- | ------ | --------------- | ---------- | ----- | --- |
| False  CreateUserID  | int    | True  False  0  | ((0))      | 創建者   | ID  |
| False  CreateDate    | dateti | True  False  0  | (sysdateti | 創建日期  |     |
|                      | me2    |                 | me())      |       |     |
| False  ModifyUserID  | int    | True  False  0  | ((0))      | 修改者   | ID  |
| False  ModifyDate    | dateti | True  False  0  | (sysdateti | 修改日期  |     |
|                      | me2    |                 | me())      |       |     |

約束
| 機密等級：內部文件  |     |     | 版權所有©2020凌誠科技股份有限公司  |     |     |
| ---------- | --- | --- | -------------------- | --- | --- |
326/391

| 文件名稱：資料庫設計規格書         |         | 皇基股份有限公司  |     | 日期：109年10月30日  |
| --------------------- | ------- | --------- | --- | -------------- |
| 名稱                    | 型態      | 欄位        |     |                |
| PK_ProductinoLineReas | Public  | ID        |     |                |
onMap

19.  資料表名稱：BIReason
| 索引  名稱    | 型態   | 非空值  唯一  長度    | 初始值  | 說明  |
| --------- | ---- | -------------- | ---- | --- |
|           |      |                |      |     |
| True  ID  | int  | True  True  0  |      |     |

| False  Name  | nvarc | True  False  50  |     | 移轉原因  |
| ------------ | ----- | ---------------- | --- | ----- |
har

| False  Code  | varch | True  False  3  |     | 移轉原因代號  |
| ------------ | ----- | --------------- | --- | ------- |
ar
| False  TransferType  | int  | True  False  0  | ((0))  | 產線類型  |
| -------------------- | ---- | --------------- | ------ | ----- |

| False  CreateUserID  | int    | True  False  0  |            | 創建者 ID  |
| -------------------- | ------ | --------------- | ---------- | ------- |
| False  CreateDate    | dateti | True  False  0  | (sysdateti | 創建日期    |
|                      | me2    |                 | me())      |         |
| False  ModifyUserID  | int    | True  False  0  | ((0))      | 修改者 ID  |
| False  ModifyDate    | dateti | True  False  0  | (sysdateti | 修改日期    |
|                      | me2    |                 | me())      |         |

約束
| 名稱         | 型態      | 欄位  |     |     |
| ---------- | ------- | --- | --- | --- |
| PK_Reason  | Public  | ID  |     |     |

關連
| 欄位               | 關連                                |     |     |     |
| ---------------- | --------------------------------- | --- | --- | --- |
| (ReasonID = ID)  | 0..*                              |     |     |     |
|                  | FK_YPTransferRecordTemp_ReasonID  |     |     |     |
 1
PK_Reason
| (ReasonID = ID)  | 0..*         |     |     |     |
| ---------------- | ------------ | --- | --- | --- |
|                  | FK_ReasonID  |     |     |     |
 1
PK_Reason

20.  資料表名稱：BIReasonDesc
| 索引  名稱    | 型態   | 非空值  唯一  長度    | 初始值  | 說明  |
| --------- | ---- | -------------- | ---- | --- |
|           |      |                |      |     |
| True  ID  | int  | True  True  0  |      |     |

移轉原因 ID
| False  ReasonID  | int  | True  False  0  |                      |     |
| ---------------- | ---- | --------------- | -------------------- | --- |
| 機密等級：內部文件        |      |                 | 版權所有©2020凌誠科技股份有限公司  |     |
327/391

| 文件名稱：資料庫設計規格書  |     | 皇基股份有限公司  |     | 日期：109年10月30日  |     |
| -------------- | --- | --------- | --- | -------------- | --- |

| False  Code  | nvarc | True  False  50  |     | 原因說明代號  |     |
| ------------ | ----- | ---------------- | --- | ------- | --- |
har

| False  Description  | nvarc | True  False  50  |     | 說明  |     |
| ------------------- | ----- | ---------------- | --- | --- | --- |
har
| False  Remark  | nvarc | True  False  100  | ('')  | 備註  |     |
| -------------- | ----- | ----------------- | ----- | --- | --- |
har

| False  CreateUserID  | int  | True  False  0  |     | 創建者 | ID  |
| -------------------- | ---- | --------------- | --- | --- | --- |

創建日期
| False  CreateDate  | dateti | True  False  0  |     |     |     |
| ------------------ | ------ | --------------- | --- | --- | --- |
me2

| False  ModifyUserID  | int  | True  False  0  |     | 修改者 | ID  |
| -------------------- | ---- | --------------- | --- | --- | --- |

修改日期
| False  ModifyDate  | dateti | True  False  0  |     |     |     |
| ------------------ | ------ | --------------- | --- | --- | --- |
me2

約束
| 名稱           | 型態      | 欄位  |     |     |     |
| ------------ | ------- | --- | --- | --- | --- |
| PK_BIReason  | Public  | ID  |     |     |     |

關連
| 欄位                   | 關連     |     |     |     |     |
| -------------------- | ------ | --- | --- | --- | --- |
| (ReasonDescID = ID)  | 0..*   |     |     |     |     |
FK_ReasonDescID
 1
PK_BIReason

21.  資料表名稱：BIShipPacking
| 索引  名稱  | 型態  | 非空值  唯一  長度  | 初始值  | 說明  |     |
| ------- | --- | ------------ | ---- | --- | --- |

流水帳 ID
| True  ID             | int   | True  True  0     |        |        |     |
| -------------------- | ----- | ----------------- | ------ | ------ | --- |
| False  TransferType  | int   | True  False  0    | ((0))  | 移轉表類別  |     |
| False  Name          | nvarc | True  False  100  | ('')   | 包裝名稱   |     |
har
| False  PackingColorID  | int   | True  False  0    | ((0))  | 顏色代號 | ID  |
| ---------------------- | ----- | ----------------- | ------ | ---- | --- |
| False  PackingSizeID   | int   | True  False  0    | ((0))  | 材積規格 | ID  |
| False  SystemOptionID  | int   | True  False  0    | ((0))  | 商標   |     |
| False  Remark          | nvarc | True  False  100  | ('')   | 備註   |     |
har
| False  IsEnable      | bit  | True  False  0  | ((1))  | 啟用狀態  |     |
| -------------------- | ---- | --------------- | ------ | ----- | --- |
| False  CreateUserID  | int  | True  False  0  | ((0))  | 建立者   | ID  |
創建日期
| False  CreateDate  | dateti | True  False  0  | (sysdateti           |     |     |
| ------------------ | ------ | --------------- | -------------------- | --- | --- |
| 機密等級：內部文件          |        |                 | 版權所有©2020凌誠科技股份有限公司  |     |     |
328/391

| 文件名稱：資料庫設計規格書        |      | 皇基股份有限公司        |        | 日期：109年10月30日  |     |
| -------------------- | ---- | --------------- | ------ | -------------- | --- |
|                      | me2  |                 | me())  |                |     |
| False  ModifyUserID  | int  | True  False  0  | ((0))  | 修改者 ID         |     |
修改日期
| False  ModifyDate  | dateti | True  False  0  | (sysdateti |     |     |
| ------------------ | ------ | --------------- | ---------- | --- | --- |
|                    | me2    |                 | me())      |     |     |

約束
| 名稱                | 型態      | 欄位  |     |     |     |
| ----------------- | ------- | --- | --- | --- | --- |
| PK_BIShipPacking  | Public  | ID  |     |     |     |

22.  資料表名稱：BIShipPackingMap
| 索引  名稱  | 型態  | 非空值  唯一  長度  | 初始值  | 說明  |     |
| ------- | --- | ------------ | ---- | --- | --- |

| True  ID              | int  | True  True  0   |        | 流水帳 ID  |     |
| --------------------- | ---- | --------------- | ------ | ------- | --- |
| False  ShipPackingID  | int  | True  False  0  | ((0))  | 出貨包裝主檔  | ID  |
入數
| False  Quantity      | int    | True  False  0  | ((0))      |         |     |
| -------------------- | ------ | --------------- | ---------- | ------- | --- |
| False  CreateUserID  | int    | True  False  0  | ((0))      | 建立者 ID  |     |
| False  CreateDate    | dateti | True  False  0  | (sysdateti | 創建日期    |     |
|                      | me2    |                 | me())      |         |     |
| False  ModifyUserID  | int    | True  False  0  | ((0))      | 修改者 ID  |     |
| False  ModifyDate    | dateti | True  False  0  | (sysdateti | 修改日期    |     |
|                      | me2    |                 | me())      |         |     |

約束
| 名稱                   | 型態      | 欄位  |     |     |     |
| -------------------- | ------- | --- | --- | --- | --- |
| PK_BIShipPackingMap  | Public  | ID  |     |     |     |

23.  資料表名稱：BISpec
| 索引  名稱       | 型態    | 非空值  唯一  長度     | 初始值   | 說明    |     |
| ------------ | ----- | --------------- | ----- | ----- | --- |
|              |       |                 |       |       |     |
| True  ID     | int   | True  True  0   |       |       |     |
| False  Code  | nvarc | True  True  50  | ('')  | 規格代號  |     |
har
| False  Name  | nvarc | True  False  100  | ('')  | 規格名稱  |     |
| ------------ | ----- | ----------------- | ----- | ----- | --- |
har
備註
| False  Remark  | nvarc | True  False  100  | ('')  |     |     |
| -------------- | ----- | ----------------- | ----- | --- | --- |
har
| False  IsEnable      | bit    | True  False  0  | ((1))                | 停用      |     |
| -------------------- | ------ | --------------- | -------------------- | ------- | --- |
| False  CreateUserID  | int    | True  False  0  | ((0))                | 創建者 ID  |     |
| False  CreateDate    | dateti | True  False  0  | (sysdateti           | 創建日期    |     |
|                      | me2    |                 | me())                |         |     |
| 機密等級：內部文件            |        |                 | 版權所有©2020凌誠科技股份有限公司  |         |     |
329/391

| 文件名稱：資料庫設計規格書        |        | 皇基股份有限公司        |            | 日期：109年10月30日  |
| -------------------- | ------ | --------------- | ---------- | -------------- |
| False  ModifyUserID  | int    | True  False  0  | ((0))      | 修改者 ID         |
| False  ModifyDate    | dateti | True  False  0  | (sysdateti | 修改日期           |
|                      | me2    |                 | me())      |                |

約束
| 名稱               | 型態      | 欄位    |     |     |
| ---------------- | ------- | ----- | --- | --- |
| PK_BI_Spec       | Public  | ID    |     |     |
| UQ_BI_Spec_Code  | Public  | Code  |     |     |

關連
| 欄位             | 關連                               |     |     |     |
| -------------- | -------------------------------- | --- | --- | --- |
| (SpecID = ID)  | 0..*                             |     |     |     |
|                | FK_SCPurchaseOrderDetail_SpecID  |     |     |     |
 1
PK_BI_Spec
| (CurrentSpecID = ID)  | 0..*                             |     |     |     |
| --------------------- | -------------------------------- | --- | --- | --- |
|                       | FK_SCUnderContractRecord_BISpec  |     |     |     |
 1
PK_BI_Spec

24.  資料表名稱：BISupplier
| 索引  名稱       | 型態    | 非空值  唯一  長度      | 初始值   | 說明    |
| ------------ | ----- | ---------------- | ----- | ----- |
|              |       |                  |       |       |
| True  ID     | int   | True  True  0    |       |       |
| False  Code  | nvarc | True  False  50  | ('')  | 廠商代號  |
har
| False  CompanyID  | int  | True  False  0  | ((0))  | 公司別 ID  |
| ----------------- | ---- | --------------- | ------ | ------- |
ERP 公司別名稱
| False  Company  | nvarc | True  False  24  | ('')  |     |
| --------------- | ----- | ---------------- | ----- | --- |
har
| False  Name  | nvarc | True  False  100  | ('')  | 名稱  |
| ------------ | ----- | ----------------- | ----- | --- |
har
| False  NameShort  | nvarc | True  False  50  | ('')  | 簡稱  |
| ----------------- | ----- | ---------------- | ----- | --- |
har
| False  NameEng  | nvarc | True  False  100  | ('')  | 英文名稱  |
| --------------- | ----- | ----------------- | ----- | ----- |
har
統一編號
| False  TaxID  | nvarc | True  False  50  | ('')  |     |
| ------------- | ----- | ---------------- | ----- | --- |
har
| False  Area  | nvarc | True  False  16  | ('')  | 地區  |
| ------------ | ----- | ---------------- | ----- | --- |
har
| 機密等級：內部文件  |     |     | 版權所有©2020凌誠科技股份有限公司  |     |
| ---------- | --- | --- | -------------------- | --- |
330/391

| 文件名稱：資料庫設計規格書  |             | 皇基股份有限公司   |       | 日期：109年10月30日  |
| -------------- | ----------- | ---------- | ----- | -------------- |
| False  Tel1    | nvarc True  | False  50  | ('')  | TEL(一)         |
har
| False  Tel2  | nvarc True  | False  50  | ('')  | TEL(二)  |
| ------------ | ----------- | ---------- | ----- | ------- |
har
| False  Fax  | nvarc True  | False  50  | ('')  | FAXNO  |
| ----------- | ----------- | ---------- | ----- | ------ |
har
| False  Email  | nvarc True  | False  100  | ('')  | EMAIL  |
| ------------- | ----------- | ----------- | ----- | ------ |
har
| False  Owner  | nvarc True  | False  50  | ('')  | 負責人  |
| ------------- | ----------- | ---------- | ----- | ---- |
har
聯絡人(一)
| False  ContactPerson1  | nvarc True  | False  50  | ('')  |     |
| ---------------------- | ----------- | ---------- | ----- | --- |
har
| False  ContactPerson2  | nvarc True  | False  50  | ('')  | 聯絡人(二)  |
| ---------------------- | ----------- | ---------- | ----- | ------- |
har
| False  Address1  | nvarc True  | False  150  | ('')  | 聯絡地址(一)  |
| ---------------- | ----------- | ----------- | ----- | -------- |
har
| False  Address2  | nvarc True  | False  150  | ('')  | 聯絡地址(二)  |
| ---------------- | ----------- | ----------- | ----- | -------- |
har
| False  ApproveStatus  | nvarc True  | False  50  | ('')  | 核准狀況  |
| --------------------- | ----------- | ---------- | ----- | ----- |
har
| False  Currency  | nvarc True  | False  50  | ('')  | 交易幣別  |
| ---------------- | ----------- | ---------- | ----- | ----- |
har

| False  PaymentMethod  | smalli True  | False  0  |     | 付款方式  |
| --------------------- | ------------ | --------- | --- | ----- |
nt
| False  PaymentRule  | nvarc True  | False  50  | ('')  | 付款條件  |
| ------------------- | ----------- | ---------- | ----- | ----- |
har
| False  RemittanceBank  | nvarc True  | False  50  | ('')  | 匯款銀行  |
| ---------------------- | ----------- | ---------- | ----- | ----- |
har
| False  RemittanceAccou | nvarc True  | False  50  | ('')  | 匯款帳號  |
| ---------------------- | ----------- | ---------- | ----- | ----- |
nt  har
| False  TaxCode  | nvarc True  | False  16  | ('')  | 稅別碼  |
| --------------- | ----------- | ---------- | ----- | ---- |
har
| False  Remark  | nvarc True  | False  255  | ('')  | 備註  |
| -------------- | ----------- | ----------- | ----- | --- |
har
建立者 ID
| False  CreateUserID  | int  True    | False  0  | ((0))                |         |
| -------------------- | ------------ | --------- | -------------------- | ------- |
| False  CreateDate    | dateti True  | False  0  | (sysdateti           | 創建日期    |
|                      | me2          |           | me())                |         |
| False  ModifyUserID  | int  True    | False  0  | ((0))                | 修改者 ID  |
| 機密等級：內部文件            |              |           | 版權所有©2020凌誠科技股份有限公司  |         |
331/391

| 文件名稱：資料庫設計規格書      |        | 皇基股份有限公司        |            | 日期：109年10月30日  |
| ------------------ | ------ | --------------- | ---------- | -------------- |
| False  ModifyDate  | dateti | True  False  0  | (sysdateti | 修改日期           |
|                    | me2    |                 | me())      |                |

約束
| 名稱             | 型態      | 欄位  |     |     |
| -------------- | ------- | --- | --- | --- |
| PK_BISupplier  | Public  | ID  |     |     |

關連
| 欄位                 | 關連     |     |     |     |
| ------------------ | ------ | --- | --- | --- |
| (SupplierID = ID)  | 0..*   |     |     |     |
FK_SCUnderContractVisit_BISupplier
 1
PK_BISupplier
| (SupplierID = ID)  | 0..*                           |     |     |     |
| ------------------ | ------------------------------ | --- | --- | --- |
|                    | FK_SCPurchaseOrder_SupplierID  |     |     |     |
 1
PK_BISupplier
| (BottleYPSupplierID =  | 0..*                                     |     |     |     |
| ---------------------- | ---------------------------------------- | --- | --- | --- |
| ID)                    | FK_SCUnderContract_BISupplier_BottleYP   |     |     |     |
 1
PK_BISupplier
| (SupplierID = ID)  | 0..*   |     |     |     |
| ------------------ | ------ | --- | --- | --- |
FK_SCUnderContract_BISupplier
 1
PK_BISupplier

25.  資料表名稱：BISystemOption
| 索引  名稱    | 型態   | 非空值  唯一  長度    | 初始值  | 說明  |
| --------- | ---- | -------------- | ---- | --- |
|           |      |                |      |     |
| True  ID  | int  | True  True  0  |      |     |

| False  OptionCode  | nvarc | True  False  50  |     | 選單名稱  |
| ------------------ | ----- | ---------------- | --- | ----- |
har

選項順序
| False  Sort  | int  | True  False  0  |     |     |
| ------------ | ---- | --------------- | --- | --- |

| False  Name  | nvarc | True  False  100  |     | 選項名稱  |
| ------------ | ----- | ----------------- | --- | ----- |
har
| False  ERPName  | nvarc | True  False  10  | ('')  | ERP 名稱  |
| --------------- | ----- | ---------------- | ----- | ------- |
har

| False  IsDefault     | bit  | True  False  0  |                      | 預設      |
| -------------------- | ---- | --------------- | -------------------- | ------- |
| False  CreateUserID  | int  | True  False  0  | ((0))                | 創建者 ID  |
| 機密等級：內部文件            |      |                 | 版權所有©2020凌誠科技股份有限公司  |         |
332/391

| 文件名稱：資料庫設計規格書        |        | 皇基股份有限公司        |            | 日期：109年10月30日  |
| -------------------- | ------ | --------------- | ---------- | -------------- |
| False  CreateDate    | dateti | True  False  0  | (sysdateti | 創建日期           |
|                      | me2    |                 | me())      |                |
| False  ModifyUserID  | int    | True  False  0  | ((0))      | 修改者 ID         |
| False  ModifyDate    | dateti | True  False  0  | (sysdateti | 修改日期           |
|                      | me2    |                 | me())      |                |

約束
| 名稱               | 型態      | 欄位  |     |     |
| ---------------- | ------- | --- | --- | --- |
| PK_SystemOption  | Public  | ID  |     |     |

關連
| 欄位                | 關連     |     |     |     |
| ----------------- | ------ | --- | --- | --- |
| (DiseaseID = ID)  | 0..*   |     |     |     |
FK_SCUnderContractRecord_BISystemOption_Dise...
 1
PK_SystemOption
| (CultivationID = ID)  | 0..*   |     |     |     |
| --------------------- | ------ | --- | --- | --- |
FK_SCUnderContractRecord_BISystemOption_Cult...
 1
PK_SystemOption
| (RootID = ID)  | 0..*   |     |     |     |
| -------------- | ------ | --- | --- | --- |
FK_SCPurchaseOrderDetail_RootID
 1
PK_SystemOption
| (LeafID = ID)  | 0..*                              |     |     |     |
| -------------- | --------------------------------- | --- | --- | --- |
|                | FK_SCPurchaseOrderDetail_BLeafID  |     |     |     |
 1
PK_SystemOption
| (VisitDescriptionID =  | 0..*                                            |     |     |     |
| ---------------------- | ----------------------------------------------- | --- | --- | --- |
| ID)                    | FK_SCUnderContractRecord_BISystemOption_Visit   |     |     |     |
 1
PK_SystemOption
| (RootID = ID)  | 0..*   |     |     |     |
| -------------- | ------ | --- | --- | --- |
FK_SCUnderContractRecord_BISystemOption_Root
 1
PK_SystemOption
| (LeafID = ID)  | 0..*                                          |     |                      |     |
| -------------- | --------------------------------------------- | --- | -------------------- | --- |
|                | FK_SCUnderContractRecord_BISystemOption_Leaf  |     |                      |     |
| 機密等級：內部文件      |                                               |     | 版權所有©2020凌誠科技股份有限公司  |     |
333/391

| 文件名稱：資料庫設計規格書  |     | 皇基股份有限公司  |     | 日期：109年10月30日  |     |
| -------------- | --- | --------- | --- | -------------- | --- |
| 欄位             | 關連  |           |     |                |     |
 1
PK_SystemOption

26.  資料表名稱：BIUploadFile
| 索引  名稱  | 型態  | 非空值  唯一  長度  | 初始值  | 說明  |     |
| ------- | --- | ------------ | ---- | --- | --- |

| True  ID  | int  | True  True  0  |     | 主索引  |     |
| --------- | ---- | -------------- | --- | ---- | --- |

| False  Name  | nvarc | True  False  255  |     | 檔案名稱  |     |
| ------------ | ----- | ----------------- | --- | ----- | --- |
har

| False  UploadDate  | dateti | True  False  0  |     | 新增日期  |     |
| ------------------ | ------ | --------------- | --- | ----- | --- |
me

| False  UploaderID  | int  | True  False  0  |     | 上傳者 ID  |     |
| ------------------ | ---- | --------------- | --- | ------- | --- |

| False  UploaderIP  | varch | True  False  128  |     | 上傳者 IP  |     |
| ------------------ | ----- | ----------------- | --- | ------- | --- |
ar

| False  Type  | varch | True  False  50  |     | 資料表+欄位代碼  |     |
| ------------ | ----- | ---------------- | --- | --------- | --- |
ar

| False  RefID  | int  | True  False  0  |     | 所屬資料的 | ID  |
| ------------- | ---- | --------------- | --- | ----- | --- |

| False  RealName  | nvarc | True  False  50  |     | 實際檔名  |     |
| ---------------- | ----- | ---------------- | --- | ----- | --- |
har

| False  FileSize  | varch | True  False  50  |     | 檔案大小  |     |
| ---------------- | ----- | ---------------- | --- | ----- | --- |
ar

| False  Counts        | bigint  | True  False  0  |            | 下載次數    |     |
| -------------------- | ------- | --------------- | ---------- | ------- | --- |
| False  CreateUserID  | int     | True  False  0  | ((0))      | 創建者 ID  |     |
| False  CreateDate    | dateti  | True  False  0  | (sysdateti | 創建日期    |     |
|                      | me2     |                 | me())      |         |     |
| False  ModifyUserID  | int     | True  False  0  | ((0))      | 修改者 ID  |     |
| False  ModifyDate    | dateti  | True  False  0  | (sysdateti | 修改日期    |     |
|                      | me2     |                 | me())      |         |     |

約束
| 名稱                | 型態      | 欄位  |     |     |     |
| ----------------- | ------- | --- | --- | --- | --- |
| PK_SS_UploadFile  | Public  | ID  |     |     |     |

27.  資料表名稱：BSPersonalRoleMap
| 索引  名稱    | 型態   | 非空值  唯一  長度    | 初始值  | 說明  |     |
| --------- | ---- | -------------- | ---- | --- | --- |
|           |      |                |      |     |     |
| True  ID  | int  | True  True  0  |      |     |     |

| False  PersonalID  | int  | True  False  0  |     | 人員 ID  |     |
| ------------------ | ---- | --------------- | --- | ------ | --- |

| False  RoleID  | int  | True  False  0  |                      | 角色 ID  |     |
| -------------- | ---- | --------------- | -------------------- | ------ | --- |
| 機密等級：內部文件      |      |                 | 版權所有©2020凌誠科技股份有限公司  |        |     |
334/391

| 文件名稱：資料庫設計規格書        |        | 皇基股份有限公司        |            | 日期：109年10月30日  |
| -------------------- | ------ | --------------- | ---------- | -------------- |
| False  CreateUserID  | int    | True  False  0  | ((0))      | 建立者 ID         |
| False  CreateDate    | dateti | True  False  0  | (sysdateti | 創建日期           |
|                      | me2    |                 | me())      |                |
| False  ModifyUserID  | int    | True  False  0  | ((0))      | 修改者 ID         |
| False  ModifyDate    | dateti | True  False  0  | (sysdateti | 修改日期           |
|                      | me2    |                 | me())      |                |

約束
| 名稱                  | 型態      | 欄位  |     |     |
| ------------------- | ------- | --- | --- | --- |
| PK_BSPersonalRoleMa | Public  | ID  |     |     |
p

28.  資料表名稱：BSRole
| 索引  名稱        | 型態    | 非空值  唯一  長度      | 初始值   | 說明    |
| ------------- | ----- | ---------------- | ----- | ----- |
|               |       |                  |       |       |
| True  RoleID  | int   | True  True  0    |       |       |
| False  Name   | nvarc | True  False  50  | ('')  | 角色名稱  |
har
| False  IsDefault  | bit  | True  False  0  | ((0))  | 是否為系統預設  |
| ----------------- | ---- | --------------- | ------ | -------- |
停用
| False  IsEnable      | bit    | True  False  0  | ((1))      |         |
| -------------------- | ------ | --------------- | ---------- | ------- |
| False  CreateUserID  | int    | True  False  0  | ((0))      | 建立者 ID  |
| False  CreateDate    | dateti | True  False  0  | (sysdateti | 創建日期    |
|                      | me2    |                 | me())      |         |
| False  ModifyUserID  | int    | True  False  0  | ((0))      | 修改者 ID  |
| False  ModifyDate    | dateti | True  False  0  | (sysdateti | 修改日期    |
|                      | me2    |                 | me())      |         |

約束
| 名稱         | 型態      | 欄位      |     |     |
| ---------- | ------- | ------- | --- | --- |
| PK_BSRole  | Public  | RoleID  |     |     |

29.  資料表名稱：BSRoleFunctionMap
| 索引  名稱    | 型態   | 非空值  唯一  長度    | 初始值  | 說明  |
| --------- | ---- | -------------- | ---- | --- |
|           |      |                |      |     |
| True  ID  | int  | True  True  0  |      |     |

| False  RoleID  | int   | True  False  0   |       | 角色 ID     |
| -------------- | ----- | ---------------- | ----- | --------- |
| False  Token   | varch | True  False  50  | ('')  | 權限 Token  |
ar
| False  CreateUserID  | int    | True  False  0  | ((0))                | 建立者 ID  |
| -------------------- | ------ | --------------- | -------------------- | ------- |
| False  CreateDate    | dateti | True  False  0  | (sysdateti           | 創建日期    |
| 機密等級：內部文件            |        |                 | 版權所有©2020凌誠科技股份有限公司  |         |
335/391

| 文件名稱：資料庫設計規格書        |      | 皇基股份有限公司        |        | 日期：109年10月30日  |
| -------------------- | ---- | --------------- | ------ | -------------- |
|                      | me2  |                 | me())  |                |
| False  ModifyUserID  | int  | True  False  0  | ((0))  | 修改者 ID         |
修改日期
| False  ModifyDate  | dateti | True  False  0  | (sysdateti |     |
| ------------------ | ------ | --------------- | ---------- | --- |
|                    | me2    |                 | me())      |     |

約束
| 名稱                  | 型態      | 欄位  |     |     |
| ------------------- | ------- | --- | --- | --- |
| PK_BSRoleFunctionMa | Public  | ID  |     |     |
p

30.  資料表名稱：CFDistribution
| 索引  名稱            | 型態    | 非空值  唯一  長度      | 初始值    | 說明      |
| ----------------- | ----- | ---------------- | ------ | ------- |
|                   |       |                  |        |         |
| True  ID          | int   | True  True  0    |        |         |
| False  CompanyID  | int   | True  False  0   | ((0))  | 公司別 ID  |
| False  Company    | nvarc | True  False  10  | ('')   | 公司名稱    |
har
| False  FormNo           | char  | True  False  10  | ('')              | 配貨單號  |
| ----------------------- | ----- | ---------------- | ----------------- | ----- |
| False  ShipDate         | date  | True  False  0   | (getdate()) 出貨日期  |       |
| False  ShipType         | int   | True  False  0   | ((0))             | 出貨類型  |
| False  ShipProductionLi | int   | True  False  0   | ((0))             | 出貨產線  |
neID
配貨狀態
| False  Status  | int   | True  False  0    | ((0))  |     |
| -------------- | ----- | ----------------- | ------ | --- |
| False  Remark  | nvarc | True  False  100  | ('')   | 備註  |
har
建立者 ID
| False  CreateUserID  | int    | True  False  0  | ((0))      |         |
| -------------------- | ------ | --------------- | ---------- | ------- |
| False  CreateDate    | dateti | True  False  0  | (sysdateti | 創建日期    |
|                      | me2    |                 | me())      |         |
| False  ModifyUserID  | int    | True  False  0  | ((0))      | 修改者 ID  |
| False  ModifyDate    | dateti | True  False  0  | (sysdateti | 修改日期    |
|                      | me2    |                 | me())      |         |

約束
| 名稱                 | 型態      | 欄位  |     |     |
| ------------------ | ------- | --- | --- | --- |
| PK_CFDistribution  | Public  | ID  |     |     |

31.  資料表名稱：CFDistributionDetail
| 索引  名稱     | 型態   | 非空值  唯一  長度    | 初始值                  | 說明  |
| ---------- | ---- | -------------- | -------------------- | --- |
|            |      |                |                      |     |
| True  ID   | int  | True  True  0  |                      |     |
| 機密等級：內部文件  |      |                | 版權所有©2020凌誠科技股份有限公司  |     |
336/391

| 文件名稱：資料庫設計規格書         |      | 皇基股份有限公司        |        | 日期：109年10月30日  |     |
| --------------------- | ---- | --------------- | ------ | -------------- | --- |
| False  MapID          | int  | True  False  0  | ((0))  | 配貨主檔與需求單明      |     |
|                       |      |                 |        | 細關聯檔           | ID  |
| False  ShipPackingMap | int  | True  False  0  | ((0))  | 出貨包裝/入數關聯檔     |     |
ID  ID
| False  ColorID       | int  | True  False  0  | ((0))  | 花色 ID  |     |
| -------------------- | ---- | --------------- | ------ | ------ | --- |
| False  BreedAliasID  | int  | True  False  0  | ((0))  | 品種別名   | ID  |
| False  GradeID       | int  | True  False  0  | ((0))  | 等級 ID  |     |
| False  FlowerID      | int  | True  False  0  | ((0))  | 朵數 ID  |     |
| False  Quantity      | int  | True  False  0  | ((0))  | 配貨數量   |     |
| False  CreateUserID  | int  | True  False  0  | ((0))  | 建立者    | ID  |
創建日期
| False  CreateDate    | dateti | True  False  0  | (sysdateti |     |     |
| -------------------- | ------ | --------------- | ---------- | --- | --- |
|                      | me2    |                 | me())      |     |     |
| False  ModifyUserID  | int    | True  False  0  | ((0))      | 修改者 | ID  |
修改日期
| False  ModifyDate  | dateti | True  False  0  | (sysdateti |     |     |
| ------------------ | ------ | --------------- | ---------- | --- | --- |
|                    | me2    |                 | me())      |     |     |

約束
| 名稱                    | 型態      | 欄位  |     |     |     |
| --------------------- | ------- | --- | --- | --- | --- |
| PK_CFDistributionDeta | Public  | ID  |     |     |     |
il

32.  資料表名稱：CFDistributionOrderDetailMap
| 索引  名稱  | 型態  | 非空值  唯一  長度  | 初始值  | 說明  |     |
| ------- | --- | ------------ | ---- | --- | --- |

| True  ID  | int  | True  True  0  |     | 配貨主檔與需求單關 |     |
| --------- | ---- | -------------- | --- | --------- | --- |
聯檔 ID
| False  DistributionID  | int    | True  False  0  | ((0))      | 配貨主檔  | ID  |
| ---------------------- | ------ | --------------- | ---------- | ----- | --- |
| False  OrderDetailID   | int    | True  False  0  | ((0))      | 需求單明細 | ID  |
| False  CreateUserID    | int    | True  False  0  | ((0))      | 建立者   | ID  |
| False  CreateDate      | dateti | True  False  0  | (sysdateti | 創建日期  |     |
|                        | me2    |                 | me())      |       |     |
| False  ModifyUserID    | int    | True  False  0  | ((0))      | 修改者   | ID  |
| False  ModifyDate      | dateti | True  False  0  | (sysdateti | 修改日期  |     |
|                        | me2    |                 | me())      |       |     |

約束
| 名稱                    | 型態      | 欄位  |     |     |     |
| --------------------- | ------- | --- | --- | --- | --- |
| PK_CFDistributionOrde | Public  | ID  |     |     |     |
rDetailMap
| 機密等級：內部文件  |     |     | 版權所有©2020凌誠科技股份有限公司  |     |     |
| ---------- | --- | --- | -------------------- | --- | --- |
337/391

| 文件名稱：資料庫設計規格書  |     | 皇基股份有限公司  |     | 日期：109年10月30日  |     |
| -------------- | --- | --------- | --- | -------------- | --- |

33.  資料表名稱：CFHarvest
| 索引  名稱    | 型態   | 非空值  唯一  長度    | 初始值  | 說明  |     |
| --------- | ---- | -------------- | ---- | --- | --- |
|           |      |                |      |     |     |
| True  ID  | int  | True  True  0  |      |     |     |
False  HarvestStartDate  dateti True  False  0  (sysdateti 採收周次起日
|     | me2  |     | me())  |     |     |
| --- | ---- | --- | ------ | --- | --- |
False  HarvestEndDate  dateti True  False  0  (sysdateti 採收周次迄日
|                        | me2  |                 | me())  |        |     |
| ---------------------- | ---- | --------------- | ------ | ------ | --- |
| False  ProductionLineI | int  | True  False  0  | ((0))  | 產線 ID  |     |
D
批號
| False  BatchNo  | nvarc | True  False  50  | ('')  |     |     |
| --------------- | ----- | ---------------- | ----- | --- | --- |
har
| False  BreedAliasID  | int   | True  False  0    | ((0))  | 品種別名   | ID  |
| -------------------- | ----- | ----------------- | ------ | ------ | --- |
| False  ColorID       | int   | True  False  0    | ((0))  | 花色 ID  |     |
| False  Remark        | nvarc | True  False  100  | ('')   | 備註     |     |
har
| False  CreateUserID  | int    | True  False  0  | ((0))      | 創建者   | ID  |
| -------------------- | ------ | --------------- | ---------- | ----- | --- |
| False  CreateDate    | dateti | True  False  0  | (sysdateti | 創建日期  |     |
|                      | me2    |                 | me())      |       |     |
| False  ModifyUserID  | int    | True  False  0  | ((0))      | 修改者   | ID  |
| False  ModifyDate    | dateti | True  False  0  | (sysdateti | 修改日期  |     |
|                      | me2    |                 | me())      |       |     |

約束
| 名稱          | 型態      | 欄位  |     |     |     |
| ----------- | ------- | --- | --- | --- | --- |
| PK_Harvest  | Public  | ID  |     |     |     |

34.  資料表名稱：CFHarvestQuarantine
| 索引  名稱                  | 型態   | 非空值  唯一  長度     | 初始值    | 說明   |     |
| ----------------------- | ---- | --------------- | ------ | ---- | --- |
|                         |      |                 |        |      |     |
| True  ID                | int  | True  True  0   |        |      |     |
| False  HarvestID        | int  | True  False  0  | ((0))  | 採收表頭 | ID  |
| False  HarvestRecordID  | int  | True  False  0  | ((0))  | 採收紀錄 | ID  |
檢疫日期
| False  QuarantineDate  | dateti | True  False  0  | (sysdateti |     |     |
| ---------------------- | ------ | --------------- | ---------- | --- | --- |
|                        | me2    |                 | me())      |     |     |
| False  QuarantineType  | int    | True  False  0  | ((0))      | 類型  |     |
| False  QuarantineReaso | int    | True  False  0  | ((0))      | 原因  |     |
nID
數量
| False  Quantity  | int  | True  False  0  | ((0))                |     |     |
| ---------------- | ---- | --------------- | -------------------- | --- | --- |
| 機密等級：內部文件        |      |                 | 版權所有©2020凌誠科技股份有限公司  |     |     |
338/391

| 文件名稱：資料庫設計規格書        |        | 皇基股份有限公司        |            | 日期：109年10月30日  |     |
| -------------------- | ------ | --------------- | ---------- | -------------- | --- |
| False  CreateUserID  | int    | True  False  0  | ((0))      | 創建者            | ID  |
| False  CreateDate    | dateti | True  False  0  | (sysdateti | 創建日期           |     |
|                      | me2    |                 | me())      |                |     |
| False  ModifyUserID  | int    | True  False  0  | ((0))      | 修改者            | ID  |
| False  ModifyDate    | dateti | True  False  0  | (sysdateti | 修改日期           |     |
|                      | me2    |                 | me())      |                |     |

約束
| 名稱                    | 型態      | 欄位  |     |     |     |
| --------------------- | ------- | --- | --- | --- | --- |
| PK_HarvestQuarantine  | Public  | ID  |     |     |     |

35.  資料表名稱：CFHarvestRecord
| 索引  名稱               | 型態     | 非空值  唯一  長度     | 初始值        | 說明    |     |
| -------------------- | ------ | --------------- | ---------- | ----- | --- |
|                      |        |                 |            |       |     |
| True  ID             | int    | True  True  0   |            |       |     |
| False  HarvestID     | int    | True  False  0  | ((0))      | 採收表頭  | ID  |
| False  HarvestDate   | dateti | True  False  0  | (sysdateti | 採收日期  |     |
|                      | me2    |                 | me())      |       |     |
| False  CarNo         | int    | True  False  0  | ((0))      | 車號    |     |
| False  Quantity      | int    | True  False  0  | ((0))      | 數量    |     |
| False  CreateUserID  | int    | True  False  0  | ((0))      | 創建者   | ID  |
| False  CreateDate    | dateti | True  False  0  | (sysdateti | 創建日期  |     |
|                      | me2    |                 | me())      |       |     |
| False  ModifyUserID  | int    | True  False  0  | ((0))      | 修改者   | ID  |
| False  ModifyDate    | dateti | True  False  0  | (sysdateti | 修改日期  |     |
|                      | me2    |                 | me())      |       |     |

約束
| 名稱                | 型態      | 欄位  |     |     |     |
| ----------------- | ------- | --- | --- | --- | --- |
| PK_HarvestRecord  | Public  | ID  |     |     |     |

36.  資料表名稱：CFOrder
| 索引  名稱           | 型態    | 非空值  唯一  長度     | 初始值               | 說明  |     |
| ---------------- | ----- | --------------- | ----------------- | --- | --- |
|                  |       |                 |                   |     |     |
| True  ID         | int   | True  True  0   |                   |     |     |
| False  ShipDate  | date  | True  False  0  | (getdate()) 出貨日期  |     |     |

| False  ShipType  | int  | True  False  0  |     | 出貨類型  |     |
| ---------------- | ---- | --------------- | --- | ----- | --- |

出貨產線
| False  ShipProductionLi | int  | True  False  0  |     |     |     |
| ----------------------- | ---- | --------------- | --- | --- | --- |
neID

| False  CustomerID  | int  | True  False  0  |                      | 客戶  |     |
| ------------------ | ---- | --------------- | -------------------- | --- | --- |
| 機密等級：內部文件          |      |                 | 版權所有©2020凌誠科技股份有限公司  |     |     |
339/391

| 文件名稱：資料庫設計規格書   |      | 皇基股份有限公司        |        | 日期：109年10月30日  |     |
| --------------- | ---- | --------------- | ------ | -------------- | --- |
| False  IsEarly  | bit  | True  False  0  | ((0))  | 是否提早報關         |     |

| False  OrderStatus  | int  | True  False  0  |     | 訂單狀態  |     |
| ------------------- | ---- | --------------- | --- | ----- | --- |
備註
| False  Remark  | nvarc | True  False  100  | ('')  |     |     |
| -------------- | ----- | ----------------- | ----- | --- | --- |
har
| False  CreateUserID  | int    | True  False  0  | ((0))      | 建立者   | ID  |
| -------------------- | ------ | --------------- | ---------- | ----- | --- |
| False  CreateDate    | dateti | True  False  0  | (sysdateti | 創建日期  |     |
|                      | me2    |                 | me())      |       |     |
| False  ModifyUserID  | int    | True  False  0  | ((0))      | 修改者   | ID  |
| False  ModifyDate    | dateti | True  False  0  | (sysdateti | 修改日期  |     |
|                      | me2    |                 | me())      |       |     |

約束
| 名稱          | 型態      | 欄位  |     |     |     |
| ----------- | ------- | --- | --- | --- | --- |
| PK_CFOrder  | Public  | ID  |     |     |     |

37.  資料表名稱：CFOrderDetail
| 索引  名稱          | 型態   | 非空值  唯一  長度     | 初始值    | 說明     |     |
| --------------- | ---- | --------------- | ------ | ------ | --- |
|                 |      |                 |        |        |     |
| True  ID        | int  | True  True  0   |        |        |     |
| False  OrderID  | int  | True  False  0  | ((0))  | 需求單主檔  | ID  |
| False  ColorID  | int  | True  False  0  | ((0))  | 花色 ID  |     |
False  SubColorIDList  varch True  False  200  ('')  替代花色 ID清單
ar
| False  GradeIDList  | varch | True  False  200  | ('')  | 等級 ID清單  |     |
| ------------------- | ----- | ----------------- | ----- | -------- | --- |
ar
朵數 ID清單
| False  FlowerIDList  | varch | True  False  200  | ('')  |     |     |
| -------------------- | ----- | ----------------- | ----- | --- | --- |
ar
| False  ShipPackingMap | int  | True  False  0  | ((0))  | 包裝單位 | ID  |
| --------------------- | ---- | --------------- | ------ | ---- | --- |
ID
| False  FixedQuqntity  | int  | True  False  0  | ((0))  | 固定單  |     |
| --------------------- | ---- | --------------- | ------ | ---- | --- |
一般單
| False  NormalQuqntity  | int   | True  False  0    | ((0))  |        |     |
| ---------------------- | ----- | ----------------- | ------ | ------ | --- |
| False  ShipLocation    | nvarc | True  False  100  | ('')   | 港口/機場  |     |
har
注意事項
| False  Remark  | nvarc | True  False  100  | ('')  |     |     |
| -------------- | ----- | ----------------- | ----- | --- | --- |
har

| False  Status        | int    | True  False  0  |                      | 狀態    |     |
| -------------------- | ------ | --------------- | -------------------- | ----- | --- |
| False  CreateUserID  | int    | True  False  0  | ((0))                | 建立者   | ID  |
| False  CreateDate    | dateti | True  False  0  | (sysdateti           | 創建日期  |     |
|                      | me2    |                 | me())                |       |     |
| 機密等級：內部文件            |        |                 | 版權所有©2020凌誠科技股份有限公司  |       |     |
340/391

| 文件名稱：資料庫設計規格書        |        | 皇基股份有限公司        |            | 日期：109年10月30日  |     |
| -------------------- | ------ | --------------- | ---------- | -------------- | --- |
| False  ModifyUserID  | int    | True  False  0  | ((0))      | 修改者            | ID  |
| False  ModifyDate    | dateti | True  False  0  | (sysdateti | 修改日期           |     |
|                      | me2    |                 | me())      |                |     |

約束
| 名稱                | 型態      | 欄位  |     |     |     |
| ----------------- | ------- | --- | --- | --- | --- |
| PK_CFOrderDetail  | Public  | ID  |     |     |     |

38.  資料表名稱：CFSampleDetail
| 索引  名稱                 | 型態   | 非空值  唯一  長度     | 初始值    | 說明    |     |
| ---------------------- | ---- | --------------- | ------ | ----- | --- |
|                        |      |                 |        |       |     |
| True  ID               | int  | True  True  0   |        |       |     |
| False  SampleRecordID  | int  | True  False  0  | ((0))  | 調查明細  | ID  |
| False  SampleNo        | int  | True  False  0  | ((0))  | 樣本編號  |     |
抽梗數
| False  OddNumber     | int    | True  False  0  | ((0))      |       |     |
| -------------------- | ------ | --------------- | ---------- | ----- | --- |
| False  EvenNumber    | int    | True  False  0  | ((0))      | 雙梗數   |     |
| False  CreateUserID  | int    | True  False  0  | ((0))      | 創建者   | ID  |
| False  CreateDate    | dateti | True  False  0  | (sysdateti | 創建日期  |     |
|                      | me2    |                 | me())      |       |     |
| False  ModifyUserID  | int    | True  False  0  | ((0))      | 修改者   | ID  |
| False  ModifyDate    | dateti | True  False  0  | (sysdateti | 修改日期  |     |
|                      | me2    |                 | me())      |       |     |

約束
| 名稱                 | 型態      | 欄位  |     |     |     |
| ------------------ | ------- | --- | --- | --- | --- |
| PK_CFSampleDetail  | Public  | ID  |     |     |     |

39.  資料表名稱：CFSampleRecord
| 索引  名稱                 | 型態     | 非空值  唯一  長度     | 初始值                  | 說明     |     |
| ---------------------- | ------ | --------------- | -------------------- | ------ | --- |
|                        |        |                 |                      |        |     |
| True  ID               | int    | True  True  0   |                      |        |     |
| False  SampleSurveyID  | int    | True  False  0  | ((0))                | 抽梗調查   | ID  |
| False  BreedAliasID    | int    | True  False  0  | ((0))                | 品種別名   | ID  |
| False  SampleGroup     | int    | True  False  0  | ((0))                | 調查組數   |     |
| False  SampleNumber    | int    | True  False  0  | ((0))                | 每組抽樣數  |     |
| False  CreateUserID    | int    | True  False  0  | ((0))                | 創建者    | ID  |
| False  CreateDate      | dateti | True  False  0  | (sysdateti           | 創建日期   |     |
|                        | me2    |                 | me())                |        |     |
| False  ModifyUserID    | int    | True  False  0  | ((0))                | 修改者    | ID  |
| False  ModifyDate      | dateti | True  False  0  | (sysdateti           | 修改日期   |     |
| 機密等級：內部文件              |        |                 | 版權所有©2020凌誠科技股份有限公司  |        |     |
341/391

| 文件名稱：資料庫設計規格書  |      | 皇基股份有限公司  |        | 日期：109年10月30日  |     |
| -------------- | ---- | --------- | ------ | -------------- | --- |
|                | me2  |           | me())  |                |     |

約束
| 名稱                 | 型態      | 欄位  |     |     |     |
| ------------------ | ------- | --- | --- | --- | --- |
| PK_CFSampleRecord  | Public  | ID  |     |     |     |

40.  資料表名稱：CFSampleSurvey
| 索引  名稱                 | 型態   | 非空值  唯一  長度     | 初始值    | 說明     |     |
| ---------------------- | ---- | --------------- | ------ | ------ | --- |
|                        |      |                 |        |        |     |
| True  ID               | int  | True  True  0   |        |        |     |
| False  ProductionLineI | int  | True  False  0  | ((0))  | 產線 ID  |     |
D
| False  BatchNo  | nvarc | True  False  50  | ('')  | 批號  |     |
| --------------- | ----- | ---------------- | ----- | --- | --- |
har
| False  ColorID     | int    | True  False  0  | ((0))      | 花色 ID  |     |
| ------------------ | ------ | --------------- | ---------- | ------ | --- |
| False  SurveyDate  | dateti | True  False  0  | (sysdateti | 調查日期   |     |
|                    | me2    |                 | me())      |        |     |
| False  StalkDate   | dateti | True  False  0  | (sysdateti | 催梗日期   |     |
|                    | me2    |                 | me())      |        |     |
製程完工日期
| False  CompletedDate  | dateti | True  False  0    | (sysdateti |     |     |
| --------------------- | ------ | ----------------- | ---------- | --- | --- |
|                       | me2    |                   | me())      |     |     |
| False  Remark         | nvarc  | True  False  100  | ('')       | 備註  |     |
har
| False  CreateUserID  | int    | True  False  0  | ((0))      | 創建者   | ID  |
| -------------------- | ------ | --------------- | ---------- | ----- | --- |
| False  CreateDate    | dateti | True  False  0  | (sysdateti | 創建日期  |     |
|                      | me2    |                 | me())      |       |     |
| False  ModifyUserID  | int    | True  False  0  | ((0))      | 修改者   | ID  |
| False  ModifyDate    | dateti | True  False  0  | (sysdateti | 修改日期  |     |
|                      | me2    |                 | me())      |       |     |

約束
| 名稱                 | 型態      | 欄位  |     |     |     |
| ------------------ | ------- | --- | --- | --- | --- |
| PK_CFSampleSurvey  | Public  | ID  |     |     |     |

41.  資料表名稱：CFShip
| 索引  名稱  | 型態  | 非空值  唯一  長度  | 初始值  | 說明  |     |
| ------- | --- | ------------ | ---- | --- | --- |

| True  ID       | int   | True  True  0    |       | 出貨主檔  | ID  |
| -------------- | ----- | ---------------- | ----- | ----- | --- |
| False  FormNo  | char  | True  False  13  | ('')  | 出貨單號  |     |

| False  DistributionID  | int  | True  False  0  |                      | 配貨主檔 | ID  |
| ---------------------- | ---- | --------------- | -------------------- | ---- | --- |
| 機密等級：內部文件              |      |                 | 版權所有©2020凌誠科技股份有限公司  |      |     |
342/391

| 文件名稱：資料庫設計規格書  |     | 皇基股份有限公司  |     | 日期：109年10月30日  |
| -------------- | --- | --------- | --- | -------------- |

| False  CustomerID  | int  | True  False  0  |        | 客戶 ID  |
| ------------------ | ---- | --------------- | ------ | ------ |
| False  Status      | int  | True  False  0  | ((0))  | 出貨狀態   |
備註
| False  Remark  | nvarc | True  False  100  | ('')  |     |
| -------------- | ----- | ----------------- | ----- | --- |
har
| False  CreateUserID  | int    | True  False  0  | ((0))      | 建立者 ID  |
| -------------------- | ------ | --------------- | ---------- | ------- |
| False  CreateDate    | dateti | True  False  0  | (sysdateti | 創建日期    |
|                      | me2    |                 | me())      |         |
| False  ModifyUserID  | int    | True  False  0  | ((0))      | 修改者 ID  |
| False  ModifyDate    | dateti | True  False  0  | (sysdateti | 修改日期    |
|                      | me2    |                 | me())      |         |

約束
| 名稱         | 型態      | 欄位  |     |     |
| ---------- | ------- | --- | --- | --- |
| PK_CFShip  | Public  | ID  |     |     |

42.  資料表名稱：CFShipDetail
| 索引  名稱        | 型態   | 非空值  唯一  長度     | 初始值    | 說明        |
| ------------- | ---- | --------------- | ------ | --------- |
|               |      |                 |        |           |
| True  ID      | int  | True  True  0   |        |           |
| False  MapID  | int  | True  False  0  | ((0))  | 出貨與配貨明細關連 |
檔ID
False  TransferBatchID  int  True  False  0  ((0))  移轉 BatchID
出貨數量
| False  Quantity    | int  | True  False  0  | ((0))  |         |
| ------------------ | ---- | --------------- | ------ | ------- |
| False  ShipOption  | int  | True  False  0  | ((0))  | 出貨庫存選項  |

| False  PackingDate  | date  | False  False  0  |     | 包裝日期  |
| ------------------- | ----- | ---------------- | --- | ----- |
花色名稱
| False  ColorName  | nvarc | True  False  100  | ('')  |     |
| ----------------- | ----- | ----------------- | ----- | --- |
har
| False  BreedAliasName  | nvarc | True  False  100  | ('')  | 品種別名名稱  |
| ---------------------- | ----- | ----------------- | ----- | ------- |
har
| False  ShipPackingUnit  | varch | True  False  10  | ('')  | 包裝單位  |
| ----------------------- | ----- | ---------------- | ----- | ----- |
ar
| False  GradeName  | nvarc | True  False  100  | ('')  | 等級  |
| ----------------- | ----- | ----------------- | ----- | --- |
har
朵數
| False  FlowerName  | nvarc | True  False  100  | ('')  |     |
| ------------------ | ----- | ----------------- | ----- | --- |
har
| False  PackingGroupNa | nvarc | True  False  100  | ('')  | 包裝組別名稱  |
| --------------------- | ----- | ----------------- | ----- | ------- |
me  har
| False  BatchNo  | nvarc | True  False  50  | ('')  | 批號  |
| --------------- | ----- | ---------------- | ----- | --- |
har
| 機密等級：內部文件  |     |     | 版權所有©2020凌誠科技股份有限公司  |     |
| ---------- | --- | --- | -------------------- | --- |
343/391

| 文件名稱：資料庫設計規格書  |     | 皇基股份有限公司  |     | 日期：109年10月30日  |     |
| -------------- | --- | --------- | --- | -------------- | --- |

| False  RefID         | int  | True  False  0  | ((0))  |     |     |
| -------------------- | ---- | --------------- | ------ | --- | --- |
| False  CreateUserID  | int  | True  False  0  | ((0))  | 建立者 | ID  |
創建日期
| False  CreateDate    | dateti | True  False  0  | (sysdateti |       |     |
| -------------------- | ------ | --------------- | ---------- | ----- | --- |
|                      | me2    |                 | me())      |       |     |
| False  ModifyUserID  | int    | True  False  0  | ((0))      | 修改者   | ID  |
| False  ModifyDate    | dateti | True  False  0  | (sysdateti | 修改日期  |     |
|                      | me2    |                 | me())      |       |     |

約束
| 名稱               | 型態      | 欄位  |     |     |     |
| ---------------- | ------- | --- | --- | --- | --- |
| PK_CFShipDetail  | Public  | ID  |     |     |     |

43.  資料表名稱：CFShipDistributionDetailMap
| 索引  名稱         | 型態   | 非空值  唯一  長度     | 初始值    | 說明   |     |
| -------------- | ---- | --------------- | ------ | ---- | --- |
|                |      |                 |        |      |     |
| True  ID       | int  | True  True  0   |        |      |     |
| False  ShipID  | int  | True  False  0  | ((0))  | 出貨主檔 | ID  |
False  DistributionDetai int  True  False  0  ((0))  配貨明細檔 ID
lID

| False  OrderDetailID  | int    | True  False  0  |            | 需求單明細 | ID  |
| --------------------- | ------ | --------------- | ---------- | ----- | --- |
| False  CreateUserID   | int    | True  False  0  | ((0))      | 建立者   | ID  |
| False  CreateDate     | dateti | True  False  0  | (sysdateti | 創建日期  |     |
|                       | me2    |                 | me())      |       |     |
| False  ModifyUserID   | int    | True  False  0  | ((0))      | 修改者   | ID  |
| False  ModifyDate     | dateti | True  False  0  | (sysdateti | 修改日期  |     |
|                       | me2    |                 | me())      |       |     |

約束
| 名稱                    | 型態      | 欄位  |     |     |     |
| --------------------- | ------- | --- | --- | --- | --- |
| PK_CFShipDistribution | Public  | ID  |     |     |     |
DetailMap

44.  資料表名稱：CFShipSurvey
| 索引  名稱          | 型態   | 非空值  唯一  長度    | 初始值  | 說明  |     |
| --------------- | ---- | -------------- | ---- | --- | --- |
|                 |      |                |      |     |     |
| True  SurveyID  | int  | True  True  0  |      |     |     |

| False  ProductionLineI | int  | True  False  0  |     | 產線  |     |
| ---------------------- | ---- | --------------- | --- | --- | --- |
D
| False  SurveyWeek  | nvarc | True  False  5  | ('')  | 調查周次  |     |
| ------------------ | ----- | --------------- | ----- | ----- | --- |
har
| 機密等級：內部文件  |     |     | 版權所有©2020凌誠科技股份有限公司  |     |     |
| ---------- | --- | --- | -------------------- | --- | --- |
344/391

| 文件名稱：資料庫設計規格書  |     | 皇基股份有限公司  |     | 日期：109年10月30日  |     |
| -------------- | --- | --------- | --- | -------------- | --- |

| False  RollType  | int   | True  False  0   |       | 點花類型  |     |
| ---------------- | ----- | ---------------- | ----- | ----- | --- |
| False  BatchNo   | nvarc | True  False  50  | ('')  | 批號    |     |
har

| False  ColorID  | int  | True  False  0  |     | 花色 ID  |     |
| --------------- | ---- | --------------- | --- | ------ | --- |
False  CompletedDate  dateti True  False  0  (sysdateti 製程完工日期
|                | me2   |                   | me())  |     |     |
| -------------- | ----- | ----------------- | ------ | --- | --- |
| False  Remark  | nvarc | True  False  100  | ('')   | 備註  |     |
har
| False  CreateUserID  | int    | True  False  0  | ((0))      | 建立者 ID  |     |
| -------------------- | ------ | --------------- | ---------- | ------- | --- |
| False  CreateDate    | dateti | True  False  0  | (sysdateti | 創建日期    |     |
|                      | me2    |                 | me())      |         |     |
| False  ModifyUserID  | int    | True  False  0  | ((0))      | 修改者 ID  |     |
| False  ModifyDate    | dateti | True  False  0  | (sysdateti | 修改日期    |     |
|                      | me2    |                 | me())      |         |     |

約束
| 名稱               | 型態      | 欄位        |     |     |     |
| ---------------- | ------- | --------- | --- | --- | --- |
| PK_CFShipSurvey  | Public  | SurveyID  |     |     |     |

45.  資料表名稱：CFShipSurveyDetail
| 索引  名稱  | 型態  | 非空值  唯一  長度  | 初始值  | 說明  |     |
| ------- | --- | ------------ | ---- | --- | --- |

|                       |      |                |     | 出貨調查 ID  |     |
| --------------------- | ---- | -------------- | --- | -------- | --- |
| True  SurveyDetailID  | int  | True  True  0  |     |          |     |

| False  SurveyMapID  | int  | True  False  0  |        | 出貨調查關聯檔 | ID  |
| ------------------- | ---- | --------------- | ------ | ------- | --- |
| False  Number1      | int  | True  False  0  | ((0))  | 花梗/荳數0  |     |
大荳/荳數1
| False  Number2   | int  | True  False  0  | ((0))  |           |     |
| ---------------- | ---- | --------------- | ------ | --------- | --- |
| False  Number3   | int  | True  False  0  | ((0))  | 0.5朵/荳數2  |     |
| False  Number4   | int  | True  False  0  | ((0))  | 1朵/荳數3    |     |
| False  Number5   | int  | True  False  0  | ((0))  | 2朵/荳數4    |     |
| False  Number6   | int  | True  False  0  | ((0))  | 3朵/荳數5    |     |
| False  Number7   | int  | True  False  0  | ((0))  | 4朵/荳數6    |     |
| False  Number8   | int  | True  False  0  | ((0))  | 5朵        |     |
| False  Number9   | int  | True  False  0  | ((0))  | 6朵        |     |
| False  Number10  | int  | True  False  0  | ((0))  | 7朵        |     |
| False  Number11  | int  | True  False  0  | ((0))  | 8朵        |     |
| False  Number12  | int  | True  False  0  | ((0))  | 9朵        |     |
10朵
| False  Number13      | int  | True  False  0  | ((0))                |         |     |
| -------------------- | ---- | --------------- | -------------------- | ------- | --- |
| False  Number14      | int  | True  False  0  | ((0))                | 11朵     |     |
| False  CreateUserID  | int  | True  False  0  | ((0))                | 建立者 ID  |     |
| 機密等級：內部文件            |      |                 | 版權所有©2020凌誠科技股份有限公司  |         |     |
345/391

| 文件名稱：資料庫設計規格書        |        | 皇基股份有限公司        |            | 日期：109年10月30日  |     |
| -------------------- | ------ | --------------- | ---------- | -------------- | --- |
| False  CreateDate    | dateti | True  False  0  | (sysdateti | 創建日期           |     |
|                      | me2    |                 | me())      |                |     |
| False  ModifyUserID  | int    | True  False  0  | ((0))      | 修改者            | ID  |
| False  ModifyDate    | dateti | True  False  0  | (sysdateti | 修改日期           |     |
|                      | me2    |                 | me())      |                |     |

約束
| 名稱                   | 型態      | 欄位              |     |     |     |
| -------------------- | ------- | --------------- | --- | --- | --- |
| PK_CFShipSurveyDetai | Public  | SurveyDetailID  |     |     |     |
l

46.  資料表名稱：CFShipSurveyDetail_HF
| 索引  名稱  | 型態  | 非空值  唯一  長度  | 初始值  | 說明  |     |
| ------- | --- | ------------ | ---- | --- | --- |

| True  SurveyDetailID  | int  | True  True  0  |     | 出貨調查 | ID  |
| --------------------- | ---- | -------------- | --- | ---- | --- |

| False  SurveyMapID  | int  | True  False  0  |     | 出貨調查關聯檔 | ID  |
| ------------------- | ---- | --------------- | --- | ------- | --- |

| True  FNumber   | int  | True  True  0   |        | 開花數   |     |
| --------------- | ---- | --------------- | ------ | ----- | --- |
| False  Number1  | int  | True  False  0  | ((0))  | 荳數 0  |     |
| False  Number2  | int  | True  False  0  | ((0))  | 荳數 1  |     |
| False  Number3  | int  | True  False  0  | ((0))  | 荳數 2  |     |
| False  Number4  | int  | True  False  0  | ((0))  | 荳數 3  |     |
| False  Number5  | int  | True  False  0  | ((0))  | 荳數 4  |     |
荳數 5
| False  Number6       | int  | True  False  0  | ((0))  |       |     |
| -------------------- | ---- | --------------- | ------ | ----- | --- |
| False  Number7       | int  | True  False  0  | ((0))  | 荳數 6  |     |
| False  CreateUserID  | int  | True  False  0  | ((0))  | 建立者   | ID  |
創建日期
| False  CreateDate    | dateti | True  False  0  | (sysdateti |     |     |
| -------------------- | ------ | --------------- | ---------- | --- | --- |
|                      | me2    |                 | me())      |     |     |
| False  ModifyUserID  | int    | True  False  0  | ((0))      | 修改者 | ID  |
修改日期
| False  ModifyDate  | dateti | True  False  0  | (sysdateti |     |     |
| ------------------ | ------ | --------------- | ---------- | --- | --- |
|                    | me2    |                 | me())      |     |     |

約束
| 名稱                   | 型態      | 欄位              |     |     |     |
| -------------------- | ------- | --------------- | --- | --- | --- |
| PK_CFShipSurveyDetai | Public  | SurveyDetailID  |     |     |     |
| l_HF                 |         | FNumber         |     |     |     |

47.  資料表名稱：CFShipSurveyMap
| 索引  名稱             | 型態   | 非空值  唯一  長度    | 初始值                  | 說明  |     |
| ------------------ | ---- | -------------- | -------------------- | --- | --- |
|                    |      |                |                      |     |     |
| True  SurveyMapID  | int  | True  True  0  |                      |     |     |
| 機密等級：內部文件          |      |                | 版權所有©2020凌誠科技股份有限公司  |     |     |
346/391

| 文件名稱：資料庫設計規格書  |     | 皇基股份有限公司  |     | 日期：109年10月30日  |     |
| -------------- | --- | --------- | --- | -------------- | --- |

| False  SurveyID         | int   | True  False  0  |                   | 出貨調查 | ID  |
| ----------------------- | ----- | --------------- | ----------------- | ---- | --- |
| False  SurveyDate       | date  | True  False  0  | (getdate()) 調查日期  |      |     |
|                         |       |                 |                   | 生產批次 | ID  |
| False  ProductionBatchI | int   | True  False  0  | ((0))             |      |     |
D
| False  Yield  | decim | True  False  0  | ((0))  | 良率  |     |
| ------------- | ----- | --------------- | ------ | --- | --- |
al
| False  CreateUserID  | int    | True  False  0  | ((0))      | 建立者   | ID  |
| -------------------- | ------ | --------------- | ---------- | ----- | --- |
| False  CreateDate    | dateti | True  False  0  | (sysdateti | 創建日期  |     |
|                      | me2    |                 | me())      |       |     |
| False  ModifyUserID  | int    | True  False  0  | ((0))      | 修改者   | ID  |
修改日期
| False  ModifyDate  | dateti | True  False  0  | (sysdateti |     |     |
| ------------------ | ------ | --------------- | ---------- | --- | --- |
|                    | me2    |                 | me())      |     |     |

約束
| 名稱                  | 型態      | 欄位           |     |     |     |
| ------------------- | ------- | ------------ | --- | --- | --- |
| PK_CFShipSurveyMap  | Public  | SurveyMapID  |     |     |     |

48.  資料表名稱：CFStemSurvey
| 索引  名稱  | 型態  | 非空值  唯一  長度  | 初始值  | 說明  |     |
| ------- | --- | ------------ | ---- | --- | --- |

| True  SurveyID         | int  | True  True  0   |        | 點梗調查主檔 | ID  |
| ---------------------- | ---- | --------------- | ------ | ------ | --- |
| False  ProductionLineI | int  | True  False  0  | ((0))  | 產線 ID  |     |
D
| False  SurveyWeek  | nvarc | True  False  5  | ('')  | 調查周次  |     |
| ------------------ | ----- | --------------- | ----- | ----- | --- |
har
| False  BatchNo  | nvarc | True  False  50  | ('')  | 批號  |     |
| --------------- | ----- | ---------------- | ----- | --- | --- |
har
| False  BreedAliasID  | int  | True  False  0  | ((0))  | 品種別名 | ID  |
| -------------------- | ---- | --------------- | ------ | ---- | --- |
False  CompletedDate  dateti True  False  0  (sysdateti 製程完工日期
|     | me2  |     | me())  |     |     |
| --- | ---- | --- | ------ | --- | --- |
備註
| False  Remark  | nvarc | True  False  100  | ('')  |     |     |
| -------------- | ----- | ----------------- | ----- | --- | --- |
har
| False  CreateUserID  | int  | True  False  0  | ((0))  | 建立者 | ID  |
| -------------------- | ---- | --------------- | ------ | --- | --- |
創建日期
| False  CreateDate    | dateti | True  False  0  | (sysdateti |       |     |
| -------------------- | ------ | --------------- | ---------- | ----- | --- |
|                      | me2    |                 | me())      |       |     |
| False  ModifyUserID  | int    | True  False  0  | ((0))      | 修改者   | ID  |
| False  ModifyDate    | dateti | True  False  0  | (sysdateti | 修改日期  |     |
|                      | me2    |                 | me())      |       |     |

| 機密等級：內部文件  |     |     | 版權所有©2020凌誠科技股份有限公司  |     |     |
| ---------- | --- | --- | -------------------- | --- | --- |
347/391

| 文件名稱：資料庫設計規格書  |     | 皇基股份有限公司  |     | 日期：109年10月30日  |     |
| -------------- | --- | --------- | --- | -------------- | --- |
約束
| 名稱               | 型態      | 欄位        |     |     |     |
| ---------------- | ------- | --------- | --- | --- | --- |
| PK_CFStemSurvey  | Public  | SurveyID  |     |     |     |

49.  資料表名稱：CFStemSurveyDetail
| 索引  名稱  | 型態  | 非空值  唯一  長度  | 初始值  | 說明  |     |
| ------- | --- | ------------ | ---- | --- | --- |

| True  SurveyDetailID  | int  | True  True  0   |        | 點梗調查       | ID  |
| --------------------- | ---- | --------------- | ------ | ---------- | --- |
| False  SurveyMapID    | int  | True  False  0  | ((0))  | 點梗調查關聯檔ID  |     |
| False  Number         | int  | True  False  0  | ((0))  | 花梗枝數       |     |
| False  CreateUserID   | int  | True  False  0  | ((0))  | 建立者        | ID  |
創建日期
| False  CreateDate    | dateti | True  False  0  | (sysdateti |     |     |
| -------------------- | ------ | --------------- | ---------- | --- | --- |
|                      | me2    |                 | me())      |     |     |
| False  ModifyUserID  | int    | True  False  0  | ((0))      | 修改者 | ID  |
修改日期
| False  ModifyDate  | dateti | True  False  0  | (sysdateti |     |     |
| ------------------ | ------ | --------------- | ---------- | --- | --- |
|                    | me2    |                 | me())      |     |     |

約束
| 名稱                  | 型態      | 欄位              |     |     |     |
| ------------------- | ------- | --------------- | --- | --- | --- |
| PK_CFStemSurveyDeta | Public  | SurveyDetailID  |     |     |     |
il

50.  資料表名稱：CFStemSurveyMap
| 索引  名稱  | 型態  | 非空值  唯一  長度  | 初始值  | 說明  |     |
| ------- | --- | ------------ | ---- | --- | --- |

| True  SurveyMapID       | int   | True  True  0   |                   | 點梗調查關聯檔 | ID  |
| ----------------------- | ----- | --------------- | ----------------- | ------- | --- |
|                         |       |                 |                   | 點梗調查主檔  | ID  |
| False  SurveyID         | int   | True  False  0  | ((0))             |         |     |
| False  SurveyDate       | date  | True  False  0  | (getdate()) 調查日期  |         |     |
| False  ProductionBatchI | int   | True  False  0  | ((0))             | 生產批次    | ID  |
D
| False  StockQuantity  | int  | True  False  0  | ((0))  | 庫存數(苗株當下庫存 |     |
| --------------------- | ---- | --------------- | ------ | ---------- | --- |
數)
| False  CreateUserID  | int    | True  False  0  | ((0))      | 建立者   | ID  |
| -------------------- | ------ | --------------- | ---------- | ----- | --- |
| False  CreateDate    | dateti | True  False  0  | (sysdateti | 創建日期  |     |
|                      | me2    |                 | me())      |       |     |
| False  ModifyUserID  | int    | True  False  0  | ((0))      | 修改者   | ID  |
| False  ModifyDate    | dateti | True  False  0  | (sysdateti | 修改日期  |     |
|                      | me2    |                 | me())      |       |     |

約束
| 機密等級：內部文件  |     |     | 版權所有©2020凌誠科技股份有限公司  |     |     |
| ---------- | --- | --- | -------------------- | --- | --- |
348/391

| 文件名稱：資料庫設計規格書       |         | 皇基股份有限公司     |     | 日期：109年10月30日  |     |
| ------------------- | ------- | ------------ | --- | -------------- | --- |
| 名稱                  | 型態      | 欄位           |     |                |     |
| PK_CFStemSurveyMap  | Public  | SurveyMapID  |     |                |     |

51.  資料表名稱：CFStemSurveyMapLog
| 索引  名稱  | 型態  | 非空值  唯一  長度  | 初始值  | 說明  |     |
| ------- | --- | ------------ | ---- | --- | --- |

| False  LogType  | char  | True  False  1  |     | 類型  |     |
| --------------- | ----- | --------------- | --- | --- | --- |

| False  LogDate  | dateti | True  False  0  |     | 日期  |     |
| --------------- | ------ | --------------- | --- | --- | --- |
me2

| False  SurveyMapID  | int  | True  False  0  |     | 點梗調查關聯檔 | ID  |
| ------------------- | ---- | --------------- | --- | ------- | --- |

| False  SurveyID  | int  | True  False  0  |     | 點梗調查主檔ID  |     |
| ---------------- | ---- | --------------- | --- | --------- | --- |

調查日期
| False  SurveyDate  | date  | True  False  0  |     |     |     |
| ------------------ | ----- | --------------- | --- | --- | --- |

| False  ProductionBatchI | int  | True  False  0  |     | 產線 ID  |     |
| ----------------------- | ---- | --------------- | --- | ------ | --- |
D

庫存數
| False  StockQuantity  | int  | True  False  0  |     |     |     |
| --------------------- | ---- | --------------- | --- | --- | --- |

| False  CreateUserID  | int  | True  False  0  |     | 創建者 | ID  |
| -------------------- | ---- | --------------- | --- | --- | --- |

| False  CreateDate  | dateti | True  False  0  |     | 創建日期  |     |
| ------------------ | ------ | --------------- | --- | ----- | --- |
me2

| False  ModifyUserID  | int  | True  False  0  |     | 修改者 | ID  |
| -------------------- | ---- | --------------- | --- | --- | --- |

| False  ModifyDate  | dateti | True  False  0  |     | 修改日期  |     |
| ------------------ | ------ | --------------- | --- | ----- | --- |
me2

52.  資料表名稱：CFTransferBatch
| 索引  名稱    | 型態   | 非空值  唯一  長度    | 初始值  | 說明  |     |
| --------- | ---- | -------------- | ---- | --- | --- |
|           |      |                |      |     |     |
| True  ID  | int  | True  True  0  |      |     |     |
產線 ID
| False  ProductionLineI | int  | True  False  0  | ((0))  |     |     |
| ---------------------- | ---- | --------------- | ------ | --- | --- |
D
| False  PackingDate    | date  | True  False  0  | (getdate()) 包裝日期  |            |     |
| --------------------- | ----- | --------------- | ----------------- | ---------- | --- |
| False  ShipPackingID  | int   | True  False  0  | ((0))             | 出貨包裝主檔     | ID  |
| False  ShipPackingMap | int   | True  False  0  | ((0))             | 出貨包裝/入數關聯檔 |     |
ID  ID
| False  ColorID       | int  | True  False  0  | ((0))  | 花色 ID  |     |
| -------------------- | ---- | --------------- | ------ | ------ | --- |
| False  BreedAliasID  | int  | True  False  0  | ((0))  | 品種別名   | ID  |
等級
| False  GradeID   | int  | True  False  0  | ((0))  | ID     |     |
| ---------------- | ---- | --------------- | ------ | ------ | --- |
| False  FlowerID  | int  | True  False  0  | ((0))  | 朵數 ID  |     |

| False  PackingGroupID  | int  | True  False  0  |     | 包裝組別  |     |
| ---------------------- | ---- | --------------- | --- | ----- | --- |
批號
| False  BatchNo  | nvarc | True  False  50  | ('')  |     |     |
| --------------- | ----- | ---------------- | ----- | --- | --- |
har
| False  TotalQuantity  | int  | True  False  0  | ((0))                | 庫存數  |     |
| --------------------- | ---- | --------------- | -------------------- | ---- | --- |
| 機密等級：內部文件             |      |                 | 版權所有©2020凌誠科技股份有限公司  |      |     |
349/391

| 文件名稱：資料庫設計規格書        |        | 皇基股份有限公司        |            | 日期：109年10月30日  |     |
| -------------------- | ------ | --------------- | ---------- | -------------- | --- |
| False  CreateUserID  | int    | True  False  0  | ((0))      | 建立者            | ID  |
| False  CreateDate    | dateti | True  False  0  | (sysdateti | 創建日期           |     |
|                      | me2    |                 | me())      |                |     |
| False  ModifyUserID  | int    | True  False  0  | ((0))      | 修改者            | ID  |
| False  ModifyDate    | dateti | True  False  0  | (sysdateti | 修改日期           |     |
|                      | me2    |                 | me())      |                |     |

約束
| 名稱                  | 型態      | 欄位  |     |     |     |
| ------------------- | ------- | --- | --- | --- | --- |
| PK_CFTransferBatch  | Public  | ID  |     |     |     |

53.  資料表名稱：CFTransferRecord
| 索引  名稱                 | 型態   | 非空值  唯一  長度     | 初始值    | 說明     |     |
| ---------------------- | ---- | --------------- | ------ | ------ | --- |
|                        |      |                 |        |        |     |
| True  ID               | int  | True  True  0   |        |        |     |
| False  ProductionLineI | int  | True  False  0  | ((0))  | 產線 ID  |     |
D
| False  ReasonID       | int   | True  False  0  | ((0))             | 移轉原因       | ID  |
| --------------------- | ----- | --------------- | ----------------- | ---------- | --- |
| False  ReasonDescID   | int   | True  False  0  | ((0))             | 移轉說明       | ID  |
| False  PackingDate    | date  | True  False  0  | (getdate()) 包裝日期  |            |     |
| False  ShipPackingID  | int   | True  False  0  | ((0))             | 出貨包裝主檔     | ID  |
| False  ShipPackingMap | int   | True  False  0  | ((0))             | 出貨包裝/入數關聯檔 |     |
ID  ID
| False  ColorID       | int  | True  False  0  | ((0))  | 花色 ID  |     |
| -------------------- | ---- | --------------- | ------ | ------ | --- |
| False  BreedAliasID  | int  | True  False  0  | ((0))  | 品種別名   | ID  |
等級 ID
| False  GradeID   | int  | True  False  0  | ((0))  |        |     |
| ---------------- | ---- | --------------- | ------ | ------ | --- |
| False  FlowerID  | int  | True  False  0  | ((0))  | 朵數 ID  |     |

| False  PackingGroupID  | int  | True  False  0  |     | 包裝組別  |     |
| ---------------------- | ---- | --------------- | --- | ----- | --- |
批號
| False  BatchNo  | nvarc | True  False  50  | ('')  |     |     |
| --------------- | ----- | ---------------- | ----- | --- | --- |
har
| False  TransferDate      | date  | True  False  0    | (getdate()) 移轉日期  |        |     |
| ------------------------ | ----- | ----------------- | ----------------- | ------ | --- |
| False  TransferQuantity  | int   | True  False  0    | ((0))             | 移轉箱數   |     |
| False  CustomerID        | int   | True  False  0    | ((0))             | 客戶 ID  |     |
| False  ExchangeState     | int   | True  False  0    | ((0))             | 拋轉狀態   |     |
| False  Remark            | nvarc | True  False  100  | ('')              | 備註     |     |
har
原始 ID
| False  BatchID       | int    | True  False  0  | ((0))                |       |     |
| -------------------- | ------ | --------------- | -------------------- | ----- | --- |
| False  CreateUserID  | int    | True  False  0  | ((0))                | 建立者   | ID  |
| False  CreateDate    | dateti | True  False  0  | (sysdateti           | 創建日期  |     |
| 機密等級：內部文件            |        |                 | 版權所有©2020凌誠科技股份有限公司  |       |     |
350/391

| 文件名稱：資料庫設計規格書        |      | 皇基股份有限公司        |        | 日期：109年10月30日  |     |
| -------------------- | ---- | --------------- | ------ | -------------- | --- |
|                      | me2  |                 | me())  |                |     |
| False  ModifyUserID  | int  | True  False  0  | ((0))  | 修改者 ID         |     |
修改日期
| False  ModifyDate  | dateti | True  False  0  | (sysdateti |         |     |
| ------------------ | ------ | --------------- | ---------- | ------- | --- |
|                    | me2    |                 | me())      |         |     |
| False  RefID       | int    | True  False  0  | ((0))      | 自關聯 ID  |     |

約束
| 名稱                   | 型態      | 欄位  |     |     |     |
| -------------------- | ------- | --- | --- | --- | --- |
| PK_CFTransferRecord  | Public  | ID  |     |     |     |

54.  資料表名稱：LCExecutedSQL
| 索引  名稱     | 型態   | 非空值  唯一  長度     | 初始值  | 說明  |     |
| ---------- | ---- | --------------- | ---- | --- | --- |
|            |      |                 |      |     |     |
| False  ID  | int  | True  False  0  |      |     |     |

檔案名稱
| False  FileName  | nvarc | True  False  100  |     |     |     |
| ---------------- | ----- | ----------------- | --- | --- | --- |
har
|              |       |                  |     |     |     |
| ------------ | ----- | ---------------- | --- | --- | --- |
| False  SHA1  | varch | True  False  40  |     |     |     |
ar
| False  Result  | nvarc | True  False  0  | ('')  | 執行結果  |     |
| -------------- | ----- | --------------- | ----- | ----- | --- |
har(m
ax)
| False  CreateDate  | dateti | True  False  0  | (sysdateti | 執行日期  |     |
| ------------------ | ------ | --------------- | ---------- | ----- | --- |
|                    | me2    |                 | me())      |       |     |

55.  資料表名稱：LCVersion
| 索引  名稱  | 型態  | 非空值  唯一  長度  | 初始值  | 說明  |     |
| ------- | --- | ------------ | ---- | --- | --- |

| True  Device  | nvarc | True  True  50  |     |     |     |
| ------------- | ----- | --------------- | --- | --- | --- |
har

| False  Version  | nvarc | True  False  50  |     |     |     |
| --------------- | ----- | ---------------- | --- | --- | --- |
har

約束
| 名稱            | 型態      | 欄位      |     |     |     |
| ------------- | ------- | ------- | --- | --- | --- |
| PK_LCVersion  | Public  | Device  |     |     |     |

56.  資料表名稱：PPBudSurvey
| 索引  名稱  | 型態  | 非空值  唯一  長度  | 初始值  | 說明  |     |
| ------- | --- | ------------ | ---- | --- | --- |

| True  SurveyID  | int  | True  True  0  |     | 打荳調查主檔 | ID  |
| --------------- | ---- | -------------- | --- | ------ | --- |
產線
| False  ProductionLineI | int  | True  False  0  | ((0))                |     |     |
| ---------------------- | ---- | --------------- | -------------------- | --- | --- |
| 機密等級：內部文件              |      |                 | 版權所有©2020凌誠科技股份有限公司  |     |     |
351/391

| 文件名稱：資料庫設計規格書  |     | 皇基股份有限公司  |     | 日期：109年10月30日  |     |
| -------------- | --- | --------- | --- | -------------- | --- |
D
| False  SurveyWeek  | varch | True  False  5  | ('')  | 調查周次  |     |
| ------------------ | ----- | --------------- | ----- | ----- | --- |
ar
| False  ProcessWeekNu | int  | True  False  0  | ((0))  | 滿催周數  |     |
| -------------------- | ---- | --------------- | ------ | ----- | --- |
mber
| False  BatchNo  | nvarc | True  False  50  | ('')  | 批號  |     |
| --------------- | ----- | ---------------- | ----- | --- | --- |
har
品種
| False  BreedAliasID  | int   | True  False  0    | ((0))  |     |     |
| -------------------- | ----- | ----------------- | ------ | --- | --- |
| False  Remark        | nvarc | True  False  100  | ('')   | 備註  |     |
har
建立者 ID
| False  CreateUserID  | int    | True  False  0  | ((0))      |         |     |
| -------------------- | ------ | --------------- | ---------- | ------- | --- |
| False  CreateDate    | dateti | True  False  0  | (sysdateti | 創建日期    |     |
|                      | me2    |                 | me())      |         |     |
| False  ModifyUserID  | int    | True  False  0  | ((0))      | 修改者 ID  |     |
| False  ModifyDate    | dateti | True  False  0  | (sysdateti | 修改日期    |     |
|                      | me2    |                 | me())      |         |     |

約束
| 名稱              | 型態      | 欄位        |     |     |     |
| --------------- | ------- | --------- | --- | --- | --- |
| PK_PPBudSurvey  | Public  | SurveyID  |     |     |     |

57.  資料表名稱：PPBudSurveyDetail
| 索引  名稱  | 型態  | 非空值  唯一  長度  | 初始值  | 說明  |     |
| ------- | --- | ------------ | ---- | --- | --- |

| True  SurveyDetailID  | int  | True  True  0   |        | 打荳調查關聯檔   | ID  |
| --------------------- | ---- | --------------- | ------ | --------- | --- |
| False  SurveyMapID    | int  | True  False  0  | ((0))  | 打荳調查關聯檔   | ID  |
| False  Number1        | int  | True  False  0  | ((0))  | 無荳數量      |     |
| False  Number2        | int  | True  False  0  | ((0))  | 0P 數量     |     |
| False  Number3        | int  | True  False  0  | ((0))  | 1P~2P 數量  |     |
| False  Number4        | int  | True  False  0  | ((0))  | 3P~4P 數量  |     |
| False  Number5        | int  | True  False  0  | ((0))  | 5P~6P 數量  |     |
| False  Number6        | int  | True  False  0  | ((0))  | 7P 數量     |     |
| False  CreateUserID   | int  | True  False  0  | ((0))  | 建立者 ID    |     |
創建日期
| False  CreateDate    | dateti | True  False  0  | (sysdateti |         |     |
| -------------------- | ------ | --------------- | ---------- | ------- | --- |
|                      | me2    |                 | me())      |         |     |
| False  ModifyUserID  | int    | True  False  0  | ((0))      | 修改者 ID  |     |
修改日期
| False  ModifyDate  | dateti | True  False  0  | (sysdateti |     |     |
| ------------------ | ------ | --------------- | ---------- | --- | --- |
|                    | me2    |                 | me())      |     |     |

| 機密等級：內部文件  |     |     | 版權所有©2020凌誠科技股份有限公司  |     |     |
| ---------- | --- | --- | -------------------- | --- | --- |
352/391

| 文件名稱：資料庫設計規格書  |     | 皇基股份有限公司  |     | 日期：109年10月30日  |     |
| -------------- | --- | --------- | --- | -------------- | --- |
約束
| 名稱                    | 型態      | 欄位              |     |     |     |
| --------------------- | ------- | --------------- | --- | --- | --- |
| PK_PPBudSurveyDetail  | Public  | SurveyDetailID  |     |     |     |

58.  資料表名稱：PPBudSurveyMap
| 索引  名稱  | 型態  | 非空值  唯一  長度  | 初始值  | 說明  |     |
| ------- | --- | ------------ | ---- | --- | --- |

| True  SurveyMapID  | int  | True  True  0  |     | 打荳調查關聯檔 | ID  |
| ------------------ | ---- | -------------- | --- | ------- | --- |

| False  SurveyID         | int   | True  False  0  |                   | 打荳調查主檔 | ID  |
| ----------------------- | ----- | --------------- | ----------------- | ------ | --- |
| False  SurveyDate       | date  | True  False  0  | (getdate()) 調查日期  |        |     |
| False  ProductionBatchI | int   | True  False  0  | ((0))             | 生產批次   | ID  |
D
| False  PositionID     | int  | True  False  0  | ((0))  | 位置 ID  |     |
| --------------------- | ---- | --------------- | ------ | ------ | --- |
| False  StockQuantity  | int  | True  False  0  | ((0))  | 庫存數    |     |
建立者 ID
| False  CreateUserID  | int    | True  False  0  | ((0))      |       |     |
| -------------------- | ------ | --------------- | ---------- | ----- | --- |
| False  CreateDate    | dateti | True  False  0  | (sysdateti | 創建日期  |     |
|                      | me2    |                 | me())      |       |     |
| False  ModifyUserID  | int    | True  False  0  | ((0))      | 修改者   | ID  |
| False  ModifyDate    | dateti | True  False  0  | (sysdateti | 修改日期  |     |
|                      | me2    |                 | me())      |       |     |

約束
| 名稱                 | 型態      | 欄位           |     |     |     |
| ------------------ | ------- | ------------ | --- | --- | --- |
| PK_PPBudSurveyMap  | Public  | SurveyMapID  |     |     |     |

59.  資料表名稱：PPDistribution
| 索引  名稱  | 型態  | 非空值  唯一  長度  | 初始值  | 說明  |     |
| ------- | --- | ------------ | ---- | --- | --- |

| True  DistributionID    | int   | True  True  0    |        | 配貨主檔  | ID  |
| ----------------------- | ----- | ---------------- | ------ | ----- | --- |
| False  FormNo           | char  | True  False  10  | ('')   | 配貨單號  |     |
| False  ShipType         | int   | True  False  0   | ((0))  | 出貨類型  |     |
| False  ShipProductionLi | int   | True  False  0   | ((0))  | 出貨產線  |     |
neID
| False  Remark  | nvarc | True  False  100  | ('')  | 備註  |     |
| -------------- | ----- | ----------------- | ----- | --- | --- |
har
| False  CreateUserID  | int    | True  False  0  | ((0))                | 建立者   | ID  |
| -------------------- | ------ | --------------- | -------------------- | ----- | --- |
| False  CreateDate    | dateti | True  False  0  | (sysdateti           | 創建日期  |     |
|                      | me2    |                 | me())                |       |     |
| False  ModifyUserID  | int    | True  False  0  | ((0))                | 修改者   | ID  |
| False  ModifyDate    | dateti | True  False  0  | (sysdateti           | 修改日期  |     |
| 機密等級：內部文件            |        |                 | 版權所有©2020凌誠科技股份有限公司  |       |     |
353/391

| 文件名稱：資料庫設計規格書  |      | 皇基股份有限公司  |        | 日期：109年10月30日  |     |
| -------------- | ---- | --------- | ------ | -------------- | --- |
|                | me2  |           | me())  |                |     |

約束
| 名稱                 | 型態      | 欄位              |     |     |     |
| ------------------ | ------- | --------------- | --- | --- | --- |
| PK_PPDistribution  | Public  | DistributionID  |     |     |     |

60.  資料表名稱：PPDistributionDetail
| 索引  名稱  | 型態  | 非空值  唯一  長度  | 初始值  | 說明  |     |
| ------- | --- | ------------ | ---- | --- | --- |

| True  DistributionDetai | int  | True  True  0  |     | 配貨明細 | ID  |
| ----------------------- | ---- | -------------- | --- | ---- | --- |
lID
配貨主檔與需求單明
| False  DistributionMapI | int  | True  False  0  | ((0))  |      |     |
| ----------------------- | ---- | --------------- | ------ | ---- | --- |
| D                       |      |                 |        | 細關聯檔 | ID  |
False  ShipWeekStartDa date  True  False  0  (getdate()) 出貨周次(起始日)
y
| False  ShipWeek  | varch | True  False  5  | ('')  | 出貨周次  |     |
| ---------------- | ----- | --------------- | ----- | ----- | --- |
ar
| False  ColorID       | int  | True  False  0  | ((0))  | 花色 ID  |     |
| -------------------- | ---- | --------------- | ------ | ------ | --- |
| False  BreedAliasID  | int  | True  False  0  | ((0))  | 品種別名   | ID  |
等級 ID
| False  GradeID   | int  | True  False  0  | ((0))  |        |     |
| ---------------- | ---- | --------------- | ------ | ------ | --- |
| False  StemID    | int  | True  False  0  | ((0))  | 梗數 ID  |     |
| False  MediumID  | int  | True  False  0  | ((0))  | 介質 ID  |     |
配貨數量
| False  Quantity      | int  | True  False  0  | ((0))  |     |     |
| -------------------- | ---- | --------------- | ------ | --- | --- |
| False  Status        | int  | True  False  0  | ((2))  | 狀態  |     |
| False  CreateUserID  | int  | True  False  0  | ((0))  | 建立者 | ID  |
創建日期
| False  CreateDate    | dateti | True  False  0  | (sysdateti |       |     |
| -------------------- | ------ | --------------- | ---------- | ----- | --- |
|                      | me2    |                 | me())      |       |     |
| False  ModifyUserID  | int    | True  False  0  | ((0))      | 修改者   | ID  |
| False  ModifyDate    | dateti | True  False  0  | (sysdateti | 修改日期  |     |
|                      | me2    |                 | me())      |       |     |

約束
| 名稱                     | 型態      | 欄位                    |     |     |     |
| ---------------------- | ------- | --------------------- | --- | --- | --- |
| PK_PPDistributionDetai | Public  | DistributionDetailID  |     |     |     |
l

61.  資料表名稱：PPDistributionOrderDetailMap
| 索引  名稱  | 型態  | 非空值  唯一  長度  | 初始值  | 說明  |     |
| ------- | --- | ------------ | ---- | --- | --- |

| True  DistributionMapI | int  | True  True  0  |                      | 配貨主檔與需求單明 |     |
| ---------------------- | ---- | -------------- | -------------------- | --------- | --- |
| 機密等級：內部文件              |      |                | 版權所有©2020凌誠科技股份有限公司  |           |     |
354/391

| 文件名稱：資料庫設計規格書          |        | 皇基股份有限公司        |            | 日期：109年10月30日  |     |
| ---------------------- | ------ | --------------- | ---------- | -------------- | --- |
| D                      |        |                 |            | 細關聯檔           | ID  |
| False  DistributionID  | int    | True  False  0  | ((0))      | 配貨主檔           | ID  |
|                        |        |                 |            | 需求單主檔          | ID  |
| False  OrderID         | int    | True  False  0  | ((0))      |                |     |
| False  OrderDetailID   | int    | True  False  0  | ((0))      | 需求單明細          | ID  |
| False  CreateUserID    | int    | True  False  0  | ((0))      | 建立者            | ID  |
| False  CreateDate      | dateti | True  False  0  | (sysdateti | 創建日期           |     |
|                        | me2    |                 | me())      |                |     |
| False  ModifyUserID    | int    | True  False  0  | ((0))      | 修改者            | ID  |
| False  ModifyDate      | dateti | True  False  0  | (sysdateti | 修改日期           |     |
|                        | me2    |                 | me())      |                |     |

約束
| 名稱                    | 型態      | 欄位                 |     |     |     |
| --------------------- | ------- | ------------------ | --- | --- | --- |
| PK_PPDistributionOrde | Public  | DistributionMapID  |     |     |     |
rDetailMap

62.  資料表名稱：PPOrder
| 索引  名稱  | 型態  | 非空值  唯一  長度  | 初始值  | 說明  |     |
| ------- | --- | ------------ | ---- | --- | --- |

| True  OrderID    | int   | True  True  0   |                   | 需求單主檔 | ID  |
| ---------------- | ----- | --------------- | ----------------- | ----- | --- |
| False  ShipDate  | date  | True  False  0  | (getdate()) 出貨日期  |       |     |
| False  ShipType  | int   | True  False  0  | ((0))             | 出貨類型  |     |
出貨產線
| False  ShipProductionLi | int  | True  False  0  | ((0))  |     |     |
| ----------------------- | ---- | --------------- | ------ | --- | --- |
neID
| False  CustomerID  | int  | True  False  0  | ((0))  | 客戶  |     |
| ------------------ | ---- | --------------- | ------ | --- | --- |
訂單狀態
| False  OrderStatus  | int   | True  False  0    | ((1))  |     |     |
| ------------------- | ----- | ----------------- | ------ | --- | --- |
| False  Remark       | nvarc | True  False  100  | ('')   | 備註  |     |
har
| False  CreateUserID  | int    | True  False  0    | ((0))      | 建立者   | ID  |
| -------------------- | ------ | ----------------- | ---------- | ----- | --- |
| False  CreateDate    | dateti | True  False  0    | (sysdateti | 創建日期  |     |
|                      | me2    |                   | me())      |       |     |
| False  ModifyUserID  | int    | True  False  0    | ((0))      | 修改者   | ID  |
| False  ModifyDate    | dateti | True  False  0    | (sysdateti | 修改日期  |     |
|                      | me2    |                   | me())      |       |     |
| False  ShipRemark    | nvarc  | True  False  100  | ('')       | 出貨備註  |     |
har

約束
| 機密等級：內部文件  |     |     | 版權所有©2020凌誠科技股份有限公司  |     |     |
| ---------- | --- | --- | -------------------- | --- | --- |
355/391

| 文件名稱：資料庫設計規格書  |         | 皇基股份有限公司  |     | 日期：109年10月30日  |     |
| -------------- | ------- | --------- | --- | -------------- | --- |
| 名稱             | 型態      | 欄位        |     |                |     |
| PK_PPOrder     | Public  | OrderID   |     |                |     |

63.  資料表名稱：PPOrderDetail
| 索引  名稱  | 型態  | 非空值  唯一  長度  | 初始值  | 說明  |     |
| ------- | --- | ------------ | ---- | --- | --- |

| True  OrderDetailID  | int  | True  True  0   |        | 需求單明細  | ID  |
| -------------------- | ---- | --------------- | ------ | ------ | --- |
| False  OrderID       | int  | True  False  0  | ((0))  | 需求單主檔  | ID  |
| False  ColorID       | int  | True  False  0  | ((0))  | 花色 ID  |     |
| False  BreedAliasID  | int  | True  False  0  | ((0))  | 品種別名   | ID  |
| False  GradeID       | int  | True  False  0  | ((0))  | 等級 ID  |     |
| False  StemID        | int  | True  False  0  | ((0))  | 梗數 ID  |     |
| False  MediumID      | int  | True  False  0  | ((0))  | 介質 ID  |     |
| False  MaturityID    | int  | True  False  0  | ((0))  | 開度 ID  |     |
數量(株)
| False  OrderQuantity  | int  | True  False  0  | ((0))  |        |     |
| --------------------- | ---- | --------------- | ------ | ------ | --- |
| False  DistMapID      | int  | True  False  0  | ((0))  | 配貨單關聯檔 | ID  |
| False  CreateUserID   | int  | True  False  0  | ((0))  | 建立者    | ID  |
創建日期
| False  CreateDate    | dateti | True  False  0  | (sysdateti |     |     |
| -------------------- | ------ | --------------- | ---------- | --- | --- |
|                      | me2    |                 | me())      |     |     |
| False  ModifyUserID  | int    | True  False  0  | ((0))      | 修改者 | ID  |
修改日期
| False  ModifyDate       | dateti | True  False  0  | (sysdateti |       |     |
| ----------------------- | ------ | --------------- | ---------- | ----- | --- |
|                         | me2    |                 | me())      |       |     |
| False  IsCreateByDistri | bit    | True  False  0  | ((0))      | 配貨新增  |     |
bution

約束
| 名稱                | 型態      | 欄位             |     |     |     |
| ----------------- | ------- | -------------- | --- | --- | --- |
| PK_PPOrderDetail  | Public  | OrderDetailID  |     |     |     |

64.  資料表名稱：PPOrderNotice
| 索引  名稱  | 型態  | 非空值  唯一  長度  | 初始值  | 說明  |     |
| ------- | --- | ------------ | ---- | --- | --- |

| True  OrderNoticeID  | int    | True  True  0   |                      | 訂單包裝注意事項 | ID  |
| -------------------- | ------ | --------------- | -------------------- | -------- | --- |
| False  OrderID       | int    | True  False  0  | ((0))                | 需求單主檔    | ID  |
| False  NoticeID      | int    | True  False  0  | ((0))                | 注意事項     | ID  |
| False  CreateUserID  | int    | True  False  0  | ((0))                | 建立者      | ID  |
| False  CreateDate    | dateti | True  False  0  | (sysdateti           | 創建日期     |     |
|                      | me2    |                 | me())                |          |     |
| False  ModifyUserID  | int    | True  False  0  | ((0))                | 修改者      | ID  |
| False  ModifyDate    | dateti | True  False  0  | (sysdateti           | 修改日期     |     |
| 機密等級：內部文件            |        |                 | 版權所有©2020凌誠科技股份有限公司  |          |     |
356/391

| 文件名稱：資料庫設計規格書  |      | 皇基股份有限公司  |        | 日期：109年10月30日  |     |
| -------------- | ---- | --------- | ------ | -------------- | --- |
|                | me2  |           | me())  |                |     |

約束
| 名稱                | 型態      | 欄位             |     |     |     |
| ----------------- | ------- | -------------- | --- | --- | --- |
| PK_PPOrderNotice  | Public  | OrderNoticeID  |     |     |     |

65.  資料表名稱：PPOrderPackingSetting
| 索引  名稱  | 型態  | 非空值  唯一  長度  | 初始值  | 說明  |     |
| ------- | --- | ------------ | ---- | --- | --- |

| True  SettingID  | int  | True  True  0   |        | 訂單出貨包裝設定 | ID  |
| ---------------- | ---- | --------------- | ------ | -------- | --- |
| False  OrderID   | int  | True  False  0  | ((0))  | 需求單主檔    | ID  |
出貨包裝
| False  ShipPackingMap | int  | True  False  0  | ((0))  |     | MapID  |
| --------------------- | ---- | --------------- | ------ | --- | ------ |
ID
| False  Quantity  | int  | True  False  0  | ((0))  | 數量  |     |
| ---------------- | ---- | --------------- | ------ | --- | --- |
花色
| False  ColorID       | int    | True  False  0  | ((0))      |         |     |
| -------------------- | ------ | --------------- | ---------- | ------- | --- |
| False  IsMix         | bit    | True  False  0  | ((0))      | 是否 Mix  |     |
| False  CreateUserID  | int    | True  False  0  | ((0))      | 建立者     | ID  |
| False  CreateDate    | dateti | True  False  0  | (sysdateti | 創建日期    |     |
|                      | me2    |                 | me())      |         |     |
| False  ModifyUserID  | int    | True  False  0  | ((0))      | 修改者     | ID  |
| False  ModifyDate    | dateti | True  False  0  | (sysdateti | 修改日期    |     |
|                      | me2    |                 | me())      |         |     |

約束
| 名稱                    | 型態      | 欄位         |     |     |     |
| --------------------- | ------- | ---------- | --- | --- | --- |
| PK_PPOrderPackingSett | Public  | SettingID  |     |     |     |
ing

66.  資料表名稱：PPOrderPackingSettingDetail
| 索引  名稱  | 型態  | 非空值  唯一  長度  | 初始值  | 說明  |     |
| ------- | --- | ------------ | ---- | --- | --- |

| True  SettingDetailID  | int  | True  True  0  |     | 訂單出貨包裝設定明 |     |
| ---------------------- | ---- | -------------- | --- | --------- | --- |
細ID
| False  SettingID         | int  | True  False  0  | ((0))  | 訂單出貨包裝設定 | ID  |
| ------------------------ | ---- | --------------- | ------ | -------- | --- |
|                          |      |                 |        | 配貨明細     | ID  |
| False  DistributionDetai | int  | True  False  0  | ((0))  |          |     |
lID
| False  Quantity      | int    | True  False  0  | ((0))                | 數量    |     |
| -------------------- | ------ | --------------- | -------------------- | ----- | --- |
| False  CreateUserID  | int    | True  False  0  | ((0))                | 建立者   | ID  |
| False  CreateDate    | dateti | True  False  0  | (sysdateti           | 創建日期  |     |
|                      | me2    |                 | me())                |       |     |
| 機密等級：內部文件            |        |                 | 版權所有©2020凌誠科技股份有限公司  |       |     |
357/391

| 文件名稱：資料庫設計規格書        |        | 皇基股份有限公司        |            | 日期：109年10月30日  |     |
| -------------------- | ------ | --------------- | ---------- | -------------- | --- |
| False  ModifyUserID  | int    | True  False  0  | ((0))      | 修改者 ID         |     |
| False  ModifyDate    | dateti | True  False  0  | (sysdateti | 修改日期           |     |
|                      | me2    |                 | me())      |                |     |

約束
| 名稱                    | 型態      | 欄位               |     |     |     |
| --------------------- | ------- | ---------------- | --- | --- | --- |
| PK_PPOrderPackingSett | Public  | SettingDetailID  |     |     |     |
ingDetail

67.  資料表名稱：PPShipDetail
| 索引  名稱  | 型態  | 非空值  唯一  長度  | 初始值  | 說明  |     |
| ------- | --- | ------------ | ---- | --- | --- |

| True  ShipDetailID  | int  | True  True  0   |        | 出貨明細檔 | ID  |
| ------------------- | ---- | --------------- | ------ | ----- | --- |
| False  OrderID      | int  | True  False  0  | ((0))  | 需求單主檔 | ID  |
False  DistributionDetai int  True  False  0  ((0))  配貨明細 ID
lID
| False  BatchID     | int   | True  False  0    | ((0))  | 移轉 BatchID  |     |
| ------------------ | ----- | ----------------- | ------ | ----------- | --- |
| False  Quantity    | int   | True  False  0    | ((0))  | 出貨數量        |     |
| False  IsArranged  | bit   | True  False  0    | ((0))  | 是否組長安排      |     |
| False  ColorName   | nvarc | True  False  100  | ('')   | 花色名稱        |     |
har
| False  BreedAliasName  | nvarc | True  False  100  | ('')  | 品種別名名稱  |     |
| ---------------------- | ----- | ----------------- | ----- | ------- | --- |
har
| False  GradeName  | nvarc | True  False  100  | ('')  | 等級名稱  |     |
| ----------------- | ----- | ----------------- | ----- | ----- | --- |
har
| False  StemName  | nvarc | True  False  100  | ('')  | 梗數名稱  |     |
| ---------------- | ----- | ----------------- | ----- | ----- | --- |
har
| False  SpecName  | nvarc | True  False  100  | ('')  | 規格名稱  |     |
| ---------------- | ----- | ----------------- | ----- | ----- | --- |
har
| False  MediumName  | nvarc | True  False  100  | ('')  | 介質名稱  |     |
| ------------------ | ----- | ----------------- | ----- | ----- | --- |
har
| False  RefID         | int  | False  False  0  | ((0))  | 關聯 ID(移轉記錄ID)  |     |
| -------------------- | ---- | ---------------- | ------ | -------------- | --- |
| False  CreateUserID  | int  | True  False  0   | ((0))  | 建立者 ID         |     |
創建日期
| False  CreateDate    | dateti | True  False  0  | (sysdateti |         |     |
| -------------------- | ------ | --------------- | ---------- | ------- | --- |
|                      | me2    |                 | me())      |         |     |
| False  ModifyUserID  | int    | True  False  0  | ((0))      | 修改者 ID  |     |
| False  ModifyDate    | dateti | True  False  0  | (sysdateti | 修改日期    |     |
|                      | me2    |                 | me())      |         |     |

組長確認狀態
| False  ArrangeState  | int  | True  False  0  |                      |     |     |
| -------------------- | ---- | --------------- | -------------------- | --- | --- |
| 機密等級：內部文件            |      |                 | 版權所有©2020凌誠科技股份有限公司  |     |     |
358/391

| 文件名稱：資料庫設計規格書  |     | 皇基股份有限公司  |     | 日期：109年10月30日  |     |
| -------------- | --- | --------- | --- | -------------- | --- |

| False  TempTransferRec | int  | False  False  | 0   | 暫存移轉紀錄 | ID  |
| ---------------------- | ---- | ------------- | --- | ------ | --- |
ordID

約束
| 名稱                   | 型態      | 欄位            |     |     |     |
| -------------------- | ------- | ------------- | --- | --- | --- |
| PK_PPShipDetail      | Public  | ShipDetailID  |     |     |     |
| FK_PPShipDetail_RefI | Public  | RefID         |     |     |     |
D
| FK_TempTransferRecor | Public  | TempTransferRecordID  |     |     |     |
| -------------------- | ------- | --------------------- | --- | --- | --- |
dID

關連
| 欄位                  | 關連     |     |     |     |     |
| ------------------- | ------ | --- | --- | --- | --- |
| (RefID = RecordID)  | 0..*   |     |     |     |     |
FK_PPShipDetail_RefID
 1
PK_PPTransferRecord
| (TempTransferRecordID  | 0..*                     |     |     |     |     |
| ---------------------- | ------------------------ | --- | --- | --- | --- |
| = ID)                  | FK_TempTransferRecordID  |     |     |     |     |
 1
PK_PPTransferRecordTemp

68.  資料表名稱：PPShipPackingSetting
| 索引  名稱  | 型態  | 非空值  唯一  | 長度  初始值  | 說明  |     |
| ------- | --- | -------- | -------- | --- | --- |

| True  SettingID       | int  | True  True   | 0         | 訂單出貨包裝設定 | ID     |
| --------------------- | ---- | ------------ | --------- | -------- | ------ |
| False  OrderID        | int  | True  False  | 0  ((0))  | 需求單主檔    | ID     |
|                       |      |              |           | 出貨包裝     | MapID  |
| False  ShipPackingMap | int  | True  False  | 0  ((0))  |          |        |
ID
| False  Quantity   | int   | True  False  | 0  ((0))  | 數量      |     |
| ----------------- | ----- | ------------ | --------- | ------- | --- |
| False  ColorID    | int   | True  False  | 0  ((0))  | 花色      |     |
| False  IsMix      | bit   | True  False  | 0  ((0))  | 是否 Mix  |     |
| False  IsDone     | bit   | True  False  | 0  ((0))  | 是否完成包裝  |     |
| False  BoxNumber  | varch | True  False  | 9  ('')   | 箱號      |     |
ar
建立者
| False  CreateUserID  | int    | True  False  | 0  ((0))      | ID    |     |
| -------------------- | ------ | ------------ | ------------- | ----- | --- |
| False  CreateDate    | dateti | True  False  | 0  (sysdateti | 創建日期  |     |
|                      | me2    |              | me())         |       |     |
修改者 ID
| False  ModifyUserID  | int  | True  False  | 0  ((0))             |     |     |
| -------------------- | ---- | ------------ | -------------------- | --- | --- |
| 機密等級：內部文件            |      |              | 版權所有©2020凌誠科技股份有限公司  |     |     |
359/391

| 文件名稱：資料庫設計規格書      |        | 皇基股份有限公司        |            | 日期：109年10月30日  |     |
| ------------------ | ------ | --------------- | ---------- | -------------- | --- |
| False  ModifyDate  | dateti | True  False  0  | (sysdateti | 修改日期           |     |
|                    | me2    |                 | me())      |                |     |

約束
| 名稱                    | 型態      | 欄位         |     |     |     |
| --------------------- | ------- | ---------- | --- | --- | --- |
| PK_PPShipPackingSetti | Public  | SettingID  |     |     |     |
ng

69.  資料表名稱：PPShipPackingSettingDetail
| 索引  名稱  | 型態  | 非空值  唯一  長度  | 初始值  | 說明  |     |
| ------- | --- | ------------ | ---- | --- | --- |

訂單出貨包裝設定明
| True  SettingDetailID  | int  | True  True  0  |     |     |     |
| ---------------------- | ---- | -------------- | --- | --- | --- |
細ID
| False  SettingID  | int  | True  False  0  | ((0))  | 訂單出貨包裝設定 | ID  |
| ----------------- | ---- | --------------- | ------ | -------- | --- |
False  DistributionDetai int  True  False  0  ((0))  配貨明細 ID
lID
| False  Quantity      | int    | True  False  0  | ((0))      | 數量      |     |
| -------------------- | ------ | --------------- | ---------- | ------- | --- |
| False  CreateUserID  | int    | True  False  0  | ((0))      | 建立者 ID  |     |
| False  CreateDate    | dateti | True  False  0  | (sysdateti | 創建日期    |     |
|                      | me2    |                 | me())      |         |     |
| False  ModifyUserID  | int    | True  False  0  | ((0))      | 修改者 ID  |     |
| False  ModifyDate    | dateti | True  False  0  | (sysdateti | 修改日期    |     |
|                      | me2    |                 | me())      |         |     |

約束
| 名稱                    | 型態      | 欄位               |     |     |     |
| --------------------- | ------- | ---------------- | --- | --- | --- |
| PK_PPShipPackingSetti | Public  | SettingDetailID  |     |     |     |
ngDetail

70.  資料表名稱：PPStemSurvey
| 索引  名稱  | 型態  | 非空值  唯一  長度  | 初始值  | 說明  |     |
| ------- | --- | ------------ | ---- | --- | --- |

| True  SurveyID         | int  | True  True  0   |        | 來梗調查主檔 | ID  |
| ---------------------- | ---- | --------------- | ------ | ------ | --- |
| False  ProductionLineI | int  | True  False  0  | ((0))  | 產線     |     |
D
| False  SurveyWeek  | varch | True  False  5  | ('')  | 調查周次  |     |
| ------------------ | ----- | --------------- | ----- | ----- | --- |
ar
| False  ProcessWeekNu | int  | True  False  0  | ((0))  | 滿催周數  |     |
| -------------------- | ---- | --------------- | ------ | ----- | --- |
mber
批號
| False  BatchNo  | nvarc | True  False  50  | ('')                 |     |     |
| --------------- | ----- | ---------------- | -------------------- | --- | --- |
| 機密等級：內部文件       |       |                  | 版權所有©2020凌誠科技股份有限公司  |     |     |
360/391

| 文件名稱：資料庫設計規格書  |     | 皇基股份有限公司  |     | 日期：109年10月30日  |     |
| -------------- | --- | --------- | --- | -------------- | --- |
har
| False  BreedAliasID  | int  | True  False  0  | ((0))  | 品種  |     |
| -------------------- | ---- | --------------- | ------ | --- | --- |
備註
| False  Remark  | nvarc | True  False  100  | ('')  |     |     |
| -------------- | ----- | ----------------- | ----- | --- | --- |
har
| False  CreateUserID  | int    | True  False  0  | ((0))      | 建立者 ID  |     |
| -------------------- | ------ | --------------- | ---------- | ------- | --- |
| False  CreateDate    | dateti | True  False  0  | (sysdateti | 創建日期    |     |
|                      | me2    |                 | me())      |         |     |
| False  ModifyUserID  | int    | True  False  0  | ((0))      | 修改者 ID  |     |
| False  ModifyDate    | dateti | True  False  0  | (sysdateti | 修改日期    |     |
|                      | me2    |                 | me())      |         |     |

約束
| 名稱               | 型態      | 欄位        |     |     |     |
| ---------------- | ------- | --------- | --- | --- | --- |
| PK_PPStemSurvey  | Public  | SurveyID  |     |     |     |

71.  資料表名稱：PPStemSurveyDetail
| 索引  名稱  | 型態  | 非空值  唯一  長度  | 初始值  | 說明  |     |
| ------- | --- | ------------ | ---- | --- | --- |

| True  SurveyDetailID  | int  | True  True  0   |        | 來梗調查關聯檔 | ID  |
| --------------------- | ---- | --------------- | ------ | ------- | --- |
| False  SurveyMapID    | int  | True  False  0  | ((0))  | 來梗調查關聯檔 | ID  |
| False  OddNumber      | int  | True  False  0  | ((0))  | 單梗數     |     |
| False  EvenNumber     | int  | True  False  0  | ((0))  | 雙梗數     |     |
建立者 ID
| False  CreateUserID  | int    | True  False  0  | ((0))      |       |     |
| -------------------- | ------ | --------------- | ---------- | ----- | --- |
| False  CreateDate    | dateti | True  False  0  | (sysdateti | 創建日期  |     |
|                      | me2    |                 | me())      |       |     |
修改者 ID
| False  ModifyUserID  | int    | True  False  0  | ((0))      |       |     |
| -------------------- | ------ | --------------- | ---------- | ----- | --- |
| False  ModifyDate    | dateti | True  False  0  | (sysdateti | 修改日期  |     |
|                      | me2    |                 | me())      |       |     |

約束
| 名稱                   | 型態      | 欄位              |     |     |     |
| -------------------- | ------- | --------------- | --- | --- | --- |
| PK_PPStemSurveyDetai | Public  | SurveyDetailID  |     |     |     |
l

72.  資料表名稱：PPStemSurveyMap
| 索引  名稱  | 型態  | 非空值  唯一  長度  | 初始值  | 說明  |     |
| ------- | --- | ------------ | ---- | --- | --- |

| True  SurveyMapID  | int  | True  True  0  |     | 來梗調查關聯檔 | ID  |
| ------------------ | ---- | -------------- | --- | ------- | --- |

| False  SurveyID    | int   | True  False  0  |                      | 來梗調查主檔 | ID  |
| ------------------ | ----- | --------------- | -------------------- | ------ | --- |
| False  SurveyDate  | date  | True  False  0  | (getdate()) 調查日期     |        |     |
| 機密等級：內部文件          |       |                 | 版權所有©2020凌誠科技股份有限公司  |        |     |
361/391

| 文件名稱：資料庫設計規格書           |      | 皇基股份有限公司        |        | 日期：109年10月30日  |     |
| ----------------------- | ---- | --------------- | ------ | -------------- | --- |
| False  ProductionBatchI | int  | True  False  0  | ((0))  | 生產批次           | ID  |
D
| False  PositionID     | int    | True  False  0  | ((0))      | 位置 ID  |     |
| --------------------- | ------ | --------------- | ---------- | ------ | --- |
| False  StockQuantity  | int    | True  False  0  | ((0))      | 庫存數    |     |
| False  CreateUserID   | int    | True  False  0  | ((0))      | 建立者    | ID  |
| False  CreateDate     | dateti | True  False  0  | (sysdateti | 創建日期   |     |
|                       | me2    |                 | me())      |        |     |
| False  ModifyUserID   | int    | True  False  0  | ((0))      | 修改者    | ID  |
| False  ModifyDate     | dateti | True  False  0  | (sysdateti | 修改日期   |     |
|                       | me2    |                 | me())      |        |     |

約束
| 名稱                  | 型態      | 欄位           |     |     |     |
| ------------------- | ------- | ------------ | --- | --- | --- |
| PK_PPStemSurveyMap  | Public  | SurveyMapID  |     |     |     |

73.  資料表名稱：PPTransferBatch
| 索引  名稱  | 型態  | 非空值  唯一  長度  | 初始值  | 說明  |     |
| ------- | --- | ------------ | ---- | --- | --- |

| True  BatchID          | int  | True  True  0   |        | 切花移轉統計檔 | ID  |
| ---------------------- | ---- | --------------- | ------ | ------- | --- |
| False  ProductionLineI | int  | True  False  0  | ((0))  | 產線 ID   |     |
D
False  ShipWeekStartDa date  True  False  0  (getdate()) 出貨周次(起始日)
y
| False  ShipWeek  | varch | True  False  5  | ('')  | 出貨周次  |     |
| ---------------- | ----- | --------------- | ----- | ----- | --- |
ar
| False  ProductType   | char  | True  False  1  | ('')   | 產品        |     |
| -------------------- | ----- | --------------- | ------ | --------- | --- |
| False  ColorID       | int   | True  False  0  | ((0))  | 花色 ID     |     |
| False  BreedAliasID  | int   | True  False  0  | ((0))  | 品種別名      | ID  |
| False  StemID        | int   | True  False  0  | ((0))  | 梗數 ID     |     |
| False  MediumID      | int   | True  False  0  | ((0))  | 介質 ID     |     |
| False  GradeID       | int   | True  False  0  | ((0))  | 等級 ID     |     |
| False  SpecID        | int   | True  False  0  | ((0))  | 規格 ID     |     |
| False  MinAvgHeight  | int   | True  False  0  | ((0))  | 平均高度(最小)  |     |
平均高度(最大)
| False  MaxAvgHeight   | int  | True  False  0  | ((0))  |      |     |
| --------------------- | ---- | --------------- | ------ | ---- | --- |
| False  TotalQuantity  | int  | True  False  0  | ((0))  | 庫存數  |     |
| False  CreateUserID   | int  | True  False  0  | ((0))  | 建立者  | ID  |
創建日期
| False  CreateDate    | dateti | True  False  0  | (sysdateti           |     |     |
| -------------------- | ------ | --------------- | -------------------- | --- | --- |
|                      | me2    |                 | me())                |     |     |
| False  ModifyUserID  | int    | True  False  0  | ((0))                | 修改者 | ID  |
| 機密等級：內部文件            |        |                 | 版權所有©2020凌誠科技股份有限公司  |     |     |
362/391

| 文件名稱：資料庫設計規格書      |        | 皇基股份有限公司        |            | 日期：109年10月30日  |     |
| ------------------ | ------ | --------------- | ---------- | -------------- | --- |
| False  ModifyDate  | dateti | True  False  0  | (sysdateti | 修改日期           |     |
|                    | me2    |                 | me())      |                |     |

約束
| 名稱                  | 型態      | 欄位       |     |     |     |
| ------------------- | ------- | -------- | --- | --- | --- |
| PK_PPTransferBatch  | Public  | BatchID  |     |     |     |

關連
| 欄位                   | 關連          |     |     |     |     |
| -------------------- | ----------- | --- | --- | --- | --- |
| (BatchID = BatchID)  | 0..*        |     |     |     |     |
|                      | FK_BatchID  |     |     |     |     |
 1
PK_PPTransferBatch

74.  資料表名稱：PPTransferRecord
| 索引  名稱  | 型態  | 非空值  唯一  長度  | 初始值  | 說明  |     |
| ------- | --- | ------------ | ---- | --- | --- |

| True  RecordID  | int  | True  True  0  |     | 移轉記錄明細 | ID  |
| --------------- | ---- | -------------- | --- | ------ | --- |

| False  TaskID  | int  | True  False  0  |     | 移轉記錄主檔 | ID  |
| -------------- | ---- | --------------- | --- | ------ | --- |
產線 ID
| False  ProductionLineI | int  | True  False  0  | ((0))  |     |     |
| ---------------------- | ---- | --------------- | ------ | --- | --- |
D
| False  ReasonDescID  | int  | True  False  0  | ((0))  | 移轉說明 | ID  |
| -------------------- | ---- | --------------- | ------ | ---- | --- |
False  ShipWeekStartDa date  True  False  0  (getdate()) 出貨周次(起日)
y
| False  ShipWeek      | char  | True  False  5  | ('')   | 出貨周次   |     |
| -------------------- | ----- | --------------- | ------ | ------ | --- |
| False  ProductType   | char  | True  False  1  | ('')   | 產品     |     |
| False  ColorID       | int   | True  False  0  | ((0))  | 花色 ID  |     |
| False  BreedAliasID  | int   | True  False  0  | ((0))  | 品種別名   | ID  |
| False  StemID        | int   | True  False  0  | ((0))  | 梗數 ID  |     |
| False  MediumID      | int   | True  False  0  | ((0))  | 介質 ID  |     |
等級
| False  GradeID       | int  | True  False  0  | ((0))  | ID        |     |
| -------------------- | ---- | --------------- | ------ | --------- | --- |
| False  SpecID        | int  | True  False  0  | ((0))  | 規格 ID     |     |
| False  MinAvgHeight  | int  | True  False  0  | ((0))  | 平均高度(最小)  |     |
平均高度(最大)
| False  MaxAvgHeight      | int  | True  False  0  | ((0))  |       |     |
| ------------------------ | ---- | --------------- | ------ | ----- | --- |
| False  TransferQuantity  | int  | True  False  0  | ((0))  | 移轉數量  |     |
| False  ExchangeState     | int  | True  False  0  | ((1))  | 拋轉狀態  |     |
備註
| False  Remark  | nvarc | True  False  100  | ('')  |     |     |
| -------------- | ----- | ----------------- | ----- | --- | --- |
har

| False  RefTransferType  | int  | True  False  0  |                      | 關聯的移轉表類別  |     |
| ----------------------- | ---- | --------------- | -------------------- | --------- | --- |
| 機密等級：內部文件               |      |                 | 版權所有©2020凌誠科技股份有限公司  |           |     |
363/391

| 文件名稱：資料庫設計規格書  |     | 皇基股份有限公司  |     | 日期：109年10月30日  |     |
| -------------- | --- | --------- | --- | -------------- | --- |

| False  RefID    | int  | True  False  0  |        | 關聯的     | ID  |
| --------------- | ---- | --------------- | ------ | ------- | --- |
| False  BatchID  | int  | True  False  0  | ((0))  | 盆花移轉統計檔 | ID  |
建立者 ID
| False  CreateUserID  | int    | True  False  0  | ((0))             |       |     |
| -------------------- | ------ | --------------- | ----------------- | ----- | --- |
| False  CreateDate    | dateti | True  False  0  | (sysdateti        | 創建日期  |     |
|                      | me2    |                 | me())             |       |     |
| False  ModifyUserID  | int    | True  False  0  | ((0))             | 修改者   | ID  |
| False  ModifyDate    | dateti | True  False  0  | (sysdateti        | 修改日期  |     |
|                      | me2    |                 | me())             |       |     |
| False  TransferDate  | date   | True  False  0  | (getdate()) 移轉日期  |       |     |

約束
| 名稱                   | 型態      | 欄位        |     |     |     |
| -------------------- | ------- | --------- | --- | --- | --- |
| PK_PPTransferRecord  | Public  | RecordID  |     |     |     |

關連
| 欄位                  | 關連     |     |     |     |     |
| ------------------- | ------ | --- | --- | --- | --- |
| (RefID = RecordID)  | 0..*   |     |     |     |     |
FK_PPShipDetail_RefID
 1
PK_PPTransferRecord

75.  資料表名稱：PPTransferRecordTemp
| 索引  名稱  | 型態  | 非空值  唯一  長度  | 初始值  | 說明  |     |
| ------- | --- | ------------ | ---- | --- | --- |

| True  ID  | int  | True  True  0  |     |     |     |
| --------- | ---- | -------------- | --- | --- | --- |

| False  CustomerID  | int  | True  False  0  |     | 客戶 ID  |     |
| ------------------ | ---- | --------------- | --- | ------ | --- |

| False  BatchID  | int  | True  False  0  |     | 生產批次 | ID  |
| --------------- | ---- | --------------- | --- | ---- | --- |

| False  ReasonID  | int  | True  False  0  |     | 移轉原因 | ID  |
| ---------------- | ---- | --------------- | --- | ---- | --- |

| False  ReasonDescID  | int  | False  False  0  |     | 原因說明 | ID  |
| -------------------- | ---- | ---------------- | --- | ---- | --- |

| False  TransferDate  | dateti | True  False  0  |     | 移轉日期  |     |
| -------------------- | ------ | --------------- | --- | ----- | --- |
me

| False  TransferQuantity  | int   | True  False  0    |       | 移轉數量  |     |
| ------------------------ | ----- | ----------------- | ----- | ----- | --- |
| False  Remark            | nvarc | True  False  100  | ('')  | 備註    |     |
har
| False  CreateUserID  | int    | True  False  0  | ((0))                | 創建者   | ID  |
| -------------------- | ------ | --------------- | -------------------- | ----- | --- |
| False  CreateDate    | dateti | True  False  0  | (sysdateti           | 創建日期  |     |
|                      | me2    |                 | me())                |       |     |
| False  ModifyUserID  | int    | True  False  0  | ((0))                | 修改者   | ID  |
| False  ModifyDate    | dateti | True  False  0  | (sysdateti           | 修改日期  |     |
| 機密等級：內部文件            |        |                 | 版權所有©2020凌誠科技股份有限公司  |       |     |
364/391

| 文件名稱：資料庫設計規格書  |      | 皇基股份有限公司  |        | 日期：109年10月30日  |     |
| -------------- | ---- | --------- | ------ | -------------- | --- |
|                | me2  |           | me())  |                |     |

| False  TrasnferDate  | date  | False  False  | 0   | 移轉日期  |     |
| -------------------- | ----- | ------------- | --- | ----- | --- |

約束
| 名稱                   | 型態      | 欄位  |     |     |     |
| -------------------- | ------- | --- | --- | --- | --- |
| PK_PPTransferRecordT | Public  | ID  |     |     |     |
emp
| FK_CustomerID    | Public  | CustomerID    |     |     |     |
| ---------------- | ------- | ------------- | --- | --- | --- |
| FK_ReasonID      | Public  | ReasonID      |     |     |     |
| FK_ReasonDescID  | Public  | ReasonDescID  |     |     |     |
| FK_BatchID       | Public  | BatchID       |     |     |     |

關連
| 欄位               | 關連           |     |     |     |     |
| ---------------- | ------------ | --- | --- | --- | --- |
| (ReasonID = ID)  | 0..*         |     |     |     |     |
|                  | FK_ReasonID  |     |     |     |     |
 1
PK_Reason
| (CustomerID = ID)  | 0..*   |     |     |     |     |
| ------------------ | ------ | --- | --- | --- | --- |
FK_CustomerID
 1
PK_BICustomer
| (TempTransferRecordID  | 0..*                     |     |     |     |     |
| ---------------------- | ------------------------ | --- | --- | --- | --- |
| = ID)                  | FK_TempTransferRecordID  |     |     |     |     |
 1
PK_PPTransferRecordTemp
| (BatchID = BatchID)  | 0..*        |     |     |     |     |
| -------------------- | ----------- | --- | --- | --- | --- |
|                      | FK_BatchID  |     |     |     |     |
 1
PK_PPTransferBatch
| (ReasonDescID = ID)  | 0..*   |     |     |     |     |
| -------------------- | ------ | --- | --- | --- | --- |
FK_ReasonDescID
 1
PK_BIReason

76.  資料表名稱：PPTransferTask
| 索引  名稱  | 型態  | 非空值  唯一  | 長度  初始值  | 說明  |     |
| ------- | --- | -------- | -------- | --- | --- |

| True  TaskID  | int  | True  True  | 0                    | 移轉記錄主檔 | ID  |
| ------------- | ---- | ----------- | -------------------- | ------ | --- |
| 機密等級：內部文件     |      |             | 版權所有©2020凌誠科技股份有限公司  |        |     |
365/391

| 文件名稱：資料庫設計規格書        |       | 皇基股份有限公司        |                   | 日期：109年10月30日  |     |
| -------------------- | ----- | --------------- | ----------------- | -------------- | --- |
| False  TransferDate  | date  | True  False  0  | (getdate()) 移轉日期  |                |     |
| False  ReasonID      | int   | True  False  0  | ((0))             | 移轉原因           | ID  |
客戶 ID
| False  CustomerID    | int    | True  False  0  | ((0))      |       |     |
| -------------------- | ------ | --------------- | ---------- | ----- | --- |
| False  CreateUserID  | int    | True  False  0  | ((0))      | 建立者   | ID  |
| False  CreateDate    | dateti | True  False  0  | (sysdateti | 創建日期  |     |
|                      | me2    |                 | me())      |       |     |
| False  ModifyUserID  | int    | True  False  0  | ((0))      | 修改者   | ID  |
| False  ModifyDate    | dateti | True  False  0  | (sysdateti | 修改日期  |     |
|                      | me2    |                 | me())      |       |     |

約束
| 名稱                 | 型態      | 欄位      |     |     |     |
| ------------------ | ------- | ------- | --- | --- | --- |
| PK_PPTransferTask  | Public  | TaskID  |     |     |     |

關連
| 欄位                 | 關連                           |     |     |     |     |
| ------------------ | ---------------------------- | --- | --- | --- | --- |
| (TaskID = TaskID)  | 0..*                         |     |     |     |     |
|                    | FK_PPTransferTaskMap_TaskID  |     |     |     |     |
 1
PK_PPTransferTask

77.  資料表名稱：PPTransferTaskMap
| 索引  名稱         | 型態   | 非空值  唯一  長度     | 初始值    | 說明       |     |
| -------------- | ---- | --------------- | ------ | -------- | --- |
|                |      |                 |        |          |     |
| True  ID       | int  | True  True  0   |        |          |     |
| False  TaskID  | int  | True  False  0  | ((0))  | 盆花移轉記錄主檔 | ID  |
False  YPTransferRecor int  True  False  0  ((0))  苗株移轉記錄 ID
dID
| False  CreateUserID  | int    | True  False  0  | ((0))      | 建立者   | ID  |
| -------------------- | ------ | --------------- | ---------- | ----- | --- |
| False  CreateDate    | dateti | True  False  0  | (sysdateti | 創建日期  |     |
|                      | me2    |                 | me())      |       |     |
| False  ModifyUserID  | int    | True  False  0  | ((0))      | 修改者   | ID  |
| False  ModifyDate    | dateti | True  False  0  | (sysdateti | 修改日期  |     |
|                      | me2    |                 | me())      |       |     |

約束
| 名稱                    | 型態      | 欄位      |                      |     |     |
| --------------------- | ------- | ------- | -------------------- | --- | --- |
| PK_PPTransferTaskMap  | Public  | ID      |                      |     |     |
| FK_PPTransferTaskMap  | Public  | TaskID  |                      |     |     |
| 機密等級：內部文件             |         |         | 版權所有©2020凌誠科技股份有限公司  |     |     |
366/391

| 文件名稱：資料庫設計規格書  |     | 皇基股份有限公司  |     | 日期：109年10月30日  |     |
| -------------- | --- | --------- | --- | -------------- | --- |
| 名稱             | 型態  | 欄位        |     |                |     |
_TaskID
| FK_PPTransferTaskMap | Public  | YPTransferRecordID  |     |     |     |
| -------------------- | ------- | ------------------- | --- | --- | --- |
_YPTransferRecordID

關連
| 欄位                     | 關連                                       |     |     |     |     |
| ---------------------- | ---------------------------------------- | --- | --- | --- | --- |
| (YPTransferRecordID =  | 0..*                                     |     |     |     |     |
| ID)                    | FK_PPTransferTaskMap_YPTransferRecordID  |     |     |     |     |
 1
PK_TransferRecord
| (TaskID = TaskID)  | 0..*                         |     |     |     |     |
| ------------------ | ---------------------------- | --- | --- | --- | --- |
|                    | FK_PPTransferTaskMap_TaskID  |     |     |     |     |
 1
PK_PPTransferTask

78.  資料表名稱：SCPurchaseOrder
| 索引  名稱  | 型態  | 非空值  唯一  長度  | 初始值  | 說明  |     |
| ------- | --- | ------------ | ---- | --- | --- |

| True  OrderID  | int   | True  True  0   |       | 採購單主檔 | ID  |
| -------------- | ----- | --------------- | ----- | ----- | --- |
| False  FormNo  | char  | True  False  9  | ('')  | 採購單號  |     |

| False  PurchaseDate  | date  | True  False  0  |     | 採購日期  |     |
| -------------------- | ----- | --------------- | --- | ----- | --- |

| False  ReceiveDate  | date  | False  False  0  |     | 到貨日期  |     |
| ------------------- | ----- | ---------------- | --- | ----- | --- |

| False  SupplierID  | int   | True  False  0    |       | 廠商 ID  |     |
| ------------------ | ----- | ----------------- | ----- | ------ | --- |
| False  Remark      | nvarc | True  False  100  | ('')  | 備註     |     |
har
| False  ExchangeState  | int  | True  False  0  | ((0))  | 拋轉狀態  |     |
| --------------------- | ---- | --------------- | ------ | ----- | --- |
建立者 ID
| False  CreateUserID  | int    | True  False  0  | ((0))      |       |     |
| -------------------- | ------ | --------------- | ---------- | ----- | --- |
| False  CreateDate    | dateti | True  False  0  | (sysdateti | 創建日期  |     |
|                      | me2    |                 | me())      |       |     |
修改者 ID
| False  ModifyUserID  | int    | True  False  0  | ((0))      |       |     |
| -------------------- | ------ | --------------- | ---------- | ----- | --- |
| False  ModifyDate    | dateti | True  False  0  | (sysdateti | 修改日期  |     |
|                      | me2    |                 | me())      |       |     |

約束
| 名稱                   | 型態      | 欄位          |     |     |     |
| -------------------- | ------- | ----------- | --- | --- | --- |
| PK_CMPurchaseOrder   | Public  | OrderID     |     |     |     |
| FK_SCPurchaseOrder_S | Public  | SupplierID  |     |     |     |
upplierID
| 機密等級：內部文件  |     |     | 版權所有©2020凌誠科技股份有限公司  |     |     |
| ---------- | --- | --- | -------------------- | --- | --- |
367/391

| 文件名稱：資料庫設計規格書  |     | 皇基股份有限公司  |     | 日期：109年10月30日  |     |
| -------------- | --- | --------- | --- | -------------- | --- |

關連
| 欄位                 | 關連                             |     |     |     |     |
| ------------------ | ------------------------------ | --- | --- | --- | --- |
| (SupplierID = ID)  | 0..*                           |     |     |     |     |
|                    | FK_SCPurchaseOrder_SupplierID  |     |     |     |     |
 1
PK_BISupplier
| (OrderID = OrderID)  | 0..*                              |     |     |     |     |
| -------------------- | --------------------------------- | --- | --- | --- | --- |
|                      | FK_SCPurchaseOrderDetail_OrderID  |     |     |     |     |
 1
PK_CMPurchaseOrder

79.  資料表名稱：SCPurchaseOrderDetail
| 索引  名稱  | 型態  非空值  | 唯一  長度  | 初始值  | 說明  |     |
| ------- | -------- | ------- | ---- | --- | --- |

| True  OrderDetailID  | int  True  | True  0   |        | 採購單明細  | ID  |
| -------------------- | ---------- | --------- | ------ | ------ | --- |
|                      |            |           |        | 採購單主檔  | ID  |
| False  OrderID       | int  True  | False  0  | ((0))  |        |     |
| False  BreedAliasID  | int  True  | False  0  | ((0))  | 品種別名   | ID  |
| False  SpecID        | int  True  | False  0  | ((0))  | 規格 ID  |     |
| False  YPState       | int  True  | False  0  | ((0))  | 苗株類型   |     |

| False  Quantity  | int  True  | False  0  |     | 數量  |     |
| ---------------- | ---------- | --------- | --- | --- | --- |

| False  Price  | decim True  | False  0  |     | 單價  |     |
| ------------- | ----------- | --------- | --- | --- | --- |
al
| False  SupplierBottleID  | int  True  | False  0  | ((0))  | 瓶苗來源  |     |
| ------------------------ | ---------- | --------- | ------ | ----- | --- |
| False  RootID            | int  True  | False  0  | ((0))  | 根系狀況  | ID  |
| False  LeafID            | int  True  | False  0  | ((0))  | 葉片狀況  | ID  |
| False  CultivationID     | int  True  | False  0  | ((0))  | 栽培管理  | ID  |
來梗比率
| False  StemRate  | decim False  | False  0  | ((0))  |     |     |
| ---------------- | ------------ | --------- | ------ | --- | --- |
al
| False  BlackSpotRate  | decim False  | False  0  | ((0))  | 黑頭比率  |     |
| --------------------- | ------------ | --------- | ------ | ----- | --- |
al
| False  SoftRotRate  | decim False  | False  0  | ((0))  | 軟腐比率  |     |
| ------------------- | ------------ | --------- | ------ | ----- | --- |
al
| False  DiseaseID      | int  True   | False  0    | ((0))  | 其他病蟲害 | ID  |
| --------------------- | ----------- | ----------- | ------ | ----- | --- |
| False  DescriptionID  | int  True   | False  0    | ((0))  | 其他說明  | ID  |
| False  Purpose        | nvarc True  | False  100  | ('')   | 用途    |     |
har
| False  Remark  | nvarc True  | False  100  | ('')  | 備註  |     |
| -------------- | ----------- | ----------- | ----- | --- | --- |
har
| 機密等級：內部文件  |     |     | 版權所有©2020凌誠科技股份有限公司  |     |     |
| ---------- | --- | --- | -------------------- | --- | --- |
368/391

| 文件名稱：資料庫設計規格書        |        | 皇基股份有限公司        |            | 日期：109年10月30日  |
| -------------------- | ------ | --------------- | ---------- | -------------- |
| False  CreateUserID  | int    | True  False  0  | ((0))      | 建立者 ID         |
| False  CreateDate    | dateti | True  False  0  | (sysdateti | 創建日期           |
|                      | me2    |                 | me())      |                |
| False  ModifyUserID  | int    | True  False  0  | ((0))      | 修改者 ID         |
| False  ModifyDate    | dateti | True  False  0  | (sysdateti | 修改日期           |
|                      | me2    |                 | me())      |                |

約束
| 名稱                  | 型態      | 欄位             |     |     |
| ------------------- | ------- | -------------- | --- | --- |
| PK_CMPurchaseOrderD | Public  | OrderDetailID  |     |     |
etail
| FK_SCPurchaseOrderD | Public  | BreedAliasID  |     |     |
| ------------------- | ------- | ------------- | --- | --- |
etail_BreedAliasID
| FK_SCPurchaseOrderD | Public  | SpecID  |     |     |
| ------------------- | ------- | ------- | --- | --- |
etail_SpecID
| FK_SCPurchaseOrderD | Public  | LeafID  |     |     |
| ------------------- | ------- | ------- | --- | --- |
etail_BLeafID
| FK_SCPurchaseOrderD | Public  | RootID  |     |     |
| ------------------- | ------- | ------- | --- | --- |
etail_RootID
| FK_SCPurchaseOrderD | Public  | OrderID  |     |     |
| ------------------- | ------- | -------- | --- | --- |
etail_OrderID

關連
| 欄位             | 關連     |     |     |     |
| -------------- | ------ | --- | --- | --- |
| (RootID = ID)  | 0..*   |     |     |     |
FK_SCPurchaseOrderDetail_RootID
 1
PK_SystemOption
| (LeafID = ID)  | 0..*                              |     |     |     |
| -------------- | --------------------------------- | --- | --- | --- |
|                | FK_SCPurchaseOrderDetail_BLeafID  |     |     |     |
 1
PK_SystemOption
| (SpecID = ID)  | 0..*                             |     |     |     |
| -------------- | -------------------------------- | --- | --- | --- |
|                | FK_SCPurchaseOrderDetail_SpecID  |     |     |     |
 1
PK_BI_Spec
| (BreedAliasID = ID)  | 0..*                                   |     |                      |     |
| -------------------- | -------------------------------------- | --- | -------------------- | --- |
|                      | FK_SCPurchaseOrderDetail_BreedAliasID  |     |                      |     |
| 機密等級：內部文件            |                                        |     | 版權所有©2020凌誠科技股份有限公司  |     |
369/391

| 文件名稱：資料庫設計規格書  |     | 皇基股份有限公司  |     | 日期：109年10月30日  |     |
| -------------- | --- | --------- | --- | -------------- | --- |
| 欄位             | 關連  |           |     |                |     |
 1
PK_PropBreedAlias
| (OrderID = OrderID)  | 0..*                              |     |     |     |     |
| -------------------- | --------------------------------- | --- | --- | --- | --- |
|                      | FK_SCPurchaseOrderDetail_OrderID  |     |     |     |     |
 1
PK_CMPurchaseOrder

80.  資料表名稱：SCUnderContract
| 索引  名稱  | 型態  非空值  | 唯一  長度  | 初始值  | 說明  |     |
| ------- | -------- | ------- | ---- | --- | --- |

|                    |            |           |     | 契作批次   | ID  |
| ------------------ | ---------- | --------- | --- | ------ | --- |
| True  ID           | int  True  | True  0   |     |        |     |
| False  SupplierID  | int  True  | False  0  |     | 廠商 ID  |     |

| False  OutDate  | date  True  | False  0  |     | 外送日期  |     |
| --------------- | ----------- | --------- | --- | ----- | --- |

| False  BreedAliasID  | int  True  | False  0  |     | 品種別名 | ID  |
| -------------------- | ---------- | --------- | --- | ---- | --- |

| False  BatchNo  | nvarc True  | False  50  |     | 批號  |     |
| --------------- | ----------- | ---------- | --- | --- | --- |
har

| False  BottleYPSupplier | int  False  | False  0  |     | 瓶苗來源 | ID  |
| ----------------------- | ----------- | --------- | --- | ---- | --- |
ID

送出數量
| False  OutQuantity  | int  True  | False  0  |     |     |     |
| ------------------- | ---------- | --------- | --- | --- | --- |

| False  ProcessID  | int  True  | False  0  |     | 製程 ID  |     |
| ----------------- | ---------- | --------- | --- | ------ | --- |

| False  ExpectedDate  | date  True  | False  0  |     | 預回日期  |     |
| -------------------- | ----------- | --------- | --- | ----- | --- |

實回日期
| False  ActualDate   | date  False  | False  0    |        |         |     |
| ------------------- | ------------ | ----------- | ------ | ------- | --- |
| False  BackYPState  | int  True    | False  0    | ((2))  | 回廠苗株狀態  |     |
| False  Purpose      | nvarc True   | False  100  | ('')   | 用途      |     |
har
| False  Remark  | nvarc True  | False  100  | ('')  | 備註  |     |
| -------------- | ----------- | ----------- | ----- | --- | --- |
har
| False  IsPurchaseNotice | bit  True  | False  0  | ((0))  | 進貨通知  |     |
| ----------------------- | ---------- | --------- | ------ | ----- | --- |
d

建立者 ID
| False  CreateUserID  | int  True  | False  0  |     |     |     |
| -------------------- | ---------- | --------- | --- | --- | --- |

| False  CreateDate  | dateti True  | False  0  |     | 創建日期  |     |
| ------------------ | ------------ | --------- | --- | ----- | --- |
me2

修改者 ID
| False  ModifyUserID  | int  True    | False  0  |     |       |     |
| -------------------- | ------------ | --------- | --- | ----- | --- |
| False  ModifyDate    | dateti True  | False  0  |     | 修改日期  |     |
me2

約束
| 機密等級：內部文件  |     |     | 版權所有©2020凌誠科技股份有限公司  |     |     |
| ---------- | --- | --- | -------------------- | --- | --- |
370/391

| 文件名稱：資料庫設計規格書       |         | 皇基股份有限公司      |     | 日期：109年10月30日  |     |
| ------------------- | ------- | ------------- | --- | -------------- | --- |
| 名稱                  | 型態      | 欄位            |     |                |     |
| PK_SCUnderContract  | Public  | ID            |     |                |     |
| FK_SCUnderContract_ | Public  | BreedAliasID  |     |                |     |
BIBreedAlias
| FK_SCUnderContract_ | Public  | ProcessID  |     |     |     |
| ------------------- | ------- | ---------- | --- | --- | --- |
BIProcess
| FK_SCUnderContract_ | Public  | SupplierID  |     |     |     |
| ------------------- | ------- | ----------- | --- | --- | --- |
BISupplier
| FK_SCUnderContract_ | Public  | BottleYPSupplierID  |     |     |     |
| ------------------- | ------- | ------------------- | --- | --- | --- |
BISupplier_BottleYP

關連
| 欄位                      | 關連     |     |     |     |     |
| ----------------------- | ------ | --- | --- | --- | --- |
| (UnderContractID = ID)  | 0..*   |     |     |     |     |
FK_SCUnderContractRecord_SCUnderContract
 1
PK_SCUnderContract
| (BottleYPSupplierID =  | 0..*                                     |     |     |     |     |
| ---------------------- | ---------------------------------------- | --- | --- | --- | --- |
| ID)                    | FK_SCUnderContract_BISupplier_BottleYP   |     |     |     |     |
 1
PK_BISupplier
| (SupplierID = ID)  | 0..*   |     |     |     |     |
| ------------------ | ------ | --- | --- | --- | --- |
FK_SCUnderContract_BISupplier
 1
PK_BISupplier
| (ProcessID = ID)  | 0..*                          |     |     |     |     |
| ----------------- | ----------------------------- | --- | --- | --- | --- |
|                   | FK_SCUnderContract_BIProcess  |     |     |     |     |
 1
PK_PropProcess
| (BreedAliasID = ID)  | 0..*                             |     |     |     |     |
| -------------------- | -------------------------------- | --- | --- | --- | --- |
|                      | FK_SCUnderContract_BIBreedAlias  |     |     |     |     |
 1
PK_PropBreedAlias

81.  資料表名稱：SCUnderContractRecord
| 索引  名稱  | 型態  | 非空值  唯一  長度  | 初始值  | 說明  |     |
| ------- | --- | ------------ | ---- | --- | --- |

|           |      |                |     | 契作訪視 | ID  |
| --------- | ---- | -------------- | --- | ---- | --- |
| True  ID  | int  | True  True  0  |     |      |     |

| False  UnderContractID  | int  | True  False  0  |                      | 契作批次 | ID  |
| ----------------------- | ---- | --------------- | -------------------- | ---- | --- |
| 機密等級：內部文件               |      |                 | 版權所有©2020凌誠科技股份有限公司  |      |     |
371/391

| 文件名稱：資料庫設計規格書  |     | 皇基股份有限公司  |     | 日期：109年10月30日  |     |
| -------------- | --- | --------- | --- | -------------- | --- |

| False  UnderContractVi | int  | True  | False  0  | 契作訪視 | ID  |
| ---------------------- | ---- | ----- | --------- | ---- | --- |
sitID

| False  CurrentSpecID  | int  | False  | False  0  | 目前規格 | ID  |
| --------------------- | ---- | ------ | --------- | ---- | --- |

| False  CurrentQuantity  | int  | True  | False  0  | 目前數量  |     |
| ----------------------- | ---- | ----- | --------- | ----- | --- |

| False  IsOnSchedule  | bit  | True  | False  0  | 符合排程  |     |
| -------------------- | ---- | ----- | --------- | ----- | --- |

| False  RootID  | int  | False  | False  0  | 根系狀況 | ID  |
| -------------- | ---- | ------ | --------- | ---- | --- |

| False  LeafID  | int  | False  | False  0  | 葉片狀況 | ID  |
| -------------- | ---- | ------ | --------- | ---- | --- |

| False  CultivationID  | int  | False  | False  0  | 栽培管理 | ID  |
| --------------------- | ---- | ------ | --------- | ---- | --- |

| False  StemRate  | decim | True  | False  0  | 來梗比率  |     |
| ---------------- | ----- | ----- | --------- | ----- | --- |
al

軟腐比率
| False  SoftRotRate  | decim | True  | False  0  |     |     |
| ------------------- | ----- | ----- | --------- | --- | --- |
al

| False  BlackSpotRate  | decim | True  | False  0  | 黑頭比率  |     |
| --------------------- | ----- | ----- | --------- | ----- | --- |
al

| False  DiseaseID  | int  | False  | False  0  | 其它病蟲害 | ID  |
| ----------------- | ---- | ------ | --------- | ----- | --- |

| False  VisitDescriptionI | int  | False  | False  0  | 契作訪視說明 | ID  |
| ------------------------ | ---- | ------ | --------- | ------ | --- |
D

| False  CreateUserID  | int  | True  | False  0  | 建立者 | ID  |
| -------------------- | ---- | ----- | --------- | --- | --- |

| False  CreateDate  | dateti | True  | False  0  | 創建日期  |     |
| ------------------ | ------ | ----- | --------- | ----- | --- |
me2

| False  ModifyUserID  | int  | True  | False  0  | 修改者 | ID  |
| -------------------- | ---- | ----- | --------- | --- | --- |

修改日期
| False  ModifyDate  | dateti | True  | False  0  |     |     |
| ------------------ | ------ | ----- | --------- | --- | --- |
me2

約束
| 名稱                  | 型態      | 欄位  |     |     |     |
| ------------------- | ------- | --- | --- | --- | --- |
| PK_SCUnderContractR | Public  | ID  |     |     |     |
ecord
| FK_SCUnderContractR | Public  | ModifyUserID  |     |     |     |
| ------------------- | ------- | ------------- | --- | --- | --- |
ecord_BIPersonel
| FK_SCUnderContractR | Public  | CreateUserID  |     |     |     |
| ------------------- | ------- | ------------- | --- | --- | --- |
ecord_BIPersonel_Creat
e
| FK_SCUnderContractR | Public  | CurrentSpecID  |     |     |     |
| ------------------- | ------- | -------------- | --- | --- | --- |
ecord_BISpec
| FK_SCUnderContractR | Public  | CultivationID  |     |     |     |
| ------------------- | ------- | -------------- | --- | --- | --- |
ecord_BISystemOption_
Cultivation
機密等級：內部文件  版權所有©2020凌誠科技股份有限公司
372/391

| 文件名稱：資料庫設計規格書       |         | 皇基股份有限公司   | 日期：109年10月30日  |
| ------------------- | ------- | ---------- | -------------- |
| 名稱                  | 型態      | 欄位         |                |
| FK_SCUnderContractR | Public  | DiseaseID  |                |
ecord_BISystemOption_
DiseasePest
| FK_SCUnderContractR | Public  | LeafID  |     |
| ------------------- | ------- | ------- | --- |
ecord_BISystemOption_
Leaf
| FK_SCUnderContractR | Public  | RootID  |     |
| ------------------- | ------- | ------- | --- |
ecord_BISystemOption_
Root
| FK_SCUnderContractR | Public  | VisitDescriptionID  |     |
| ------------------- | ------- | ------------------- | --- |
ecord_BISystemOption_
Visit
| FK_SCUnderContractR | Public  | UnderContractID  |     |
| ------------------- | ------- | ---------------- | --- |
ecord_SCUnderContract
| FK_SCUnderContractR | Public  | UnderContractVisitID  |     |
| ------------------- | ------- | --------------------- | --- |
ecord_SCUnderContract
Visit

關連
| 欄位                   | 關連                                   |     |     |
| -------------------- | ------------------------------------ | --- | --- |
| (ModifyUserID = ID)  | 0..*                                 |     |     |
|                      | FK_SCUnderContractRecord_BIPersonel  |     |     |
 1
PK_BS_Personel
| (DiseaseID = ID)  | 0..*   |     |     |
| ----------------- | ------ | --- | --- |
FK_SCUnderContractRecord_BISystemOption_Dise...
 1
PK_SystemOption
| (CultivationID = ID)  | 0..*   |     |     |
| --------------------- | ------ | --- | --- |
FK_SCUnderContractRecord_BISystemOption_Cult...
 1
PK_SystemOption
| (CreateUserID = ID)  | 0..*                                        |     |     |
| -------------------- | ------------------------------------------- | --- | --- |
|                      | FK_SCUnderContractRecord_BIPersonel_Create  |     |     |
 1
PK_BS_Personel
| (CurrentSpecID = ID)  | 0..*   |     |     |
| --------------------- | ------ | --- | --- |
機密等級：內部文件  版權所有©2020凌誠科技股份有限公司
373/391

| 文件名稱：資料庫設計規格書  |                                  | 皇基股份有限公司  |     | 日期：109年10月30日  |     |
| -------------- | -------------------------------- | --------- | --- | -------------- | --- |
| 欄位             | 關連                               |           |     |                |     |
|                | FK_SCUnderContractRecord_BISpec  |           |     |                |     |
 1
PK_BI_Spec
| (UnderContractVisitID =  | 0..*                                            |     |     |     |     |
| ------------------------ | ----------------------------------------------- | --- | --- | --- | --- |
| ID)                      | FK_SCUnderContractRecord_SCUnderContractVisit   |     |     |     |     |
 1
PK_SCUnderContractVisit
| (UnderContractID = ID)  | 0..*   |     |     |     |     |
| ----------------------- | ------ | --- | --- | --- | --- |
FK_SCUnderContractRecord_SCUnderContract
 1
PK_SCUnderContract
| (VisitDescriptionID =  | 0..*                                            |     |     |     |     |
| ---------------------- | ----------------------------------------------- | --- | --- | --- | --- |
| ID)                    | FK_SCUnderContractRecord_BISystemOption_Visit   |     |     |     |     |
 1
PK_SystemOption
| (RootID = ID)  | 0..*   |     |     |     |     |
| -------------- | ------ | --- | --- | --- | --- |
FK_SCUnderContractRecord_BISystemOption_Root
 1
PK_SystemOption
| (LeafID = ID)  | 0..*                                          |     |     |     |     |
| -------------- | --------------------------------------------- | --- | --- | --- | --- |
|                | FK_SCUnderContractRecord_BISystemOption_Leaf  |     |     |     |     |
 1
PK_SystemOption

82.  資料表名稱：SCUnderContractVisit
| 索引  名稱  | 型態  非空值  | 唯一  長度  | 初始值  | 說明  |     |
| ------- | -------- | ------- | ---- | --- | --- |

| True  ID  | int  True  | True  0  |     | 契作訪視 | ID  |
| --------- | ---------- | -------- | --- | ---- | --- |

廠商 ID
| False  SupplierID  | int  True  | False  0  |     |     |     |
| ------------------ | ---------- | --------- | --- | --- | --- |

| False  VisitDate  | date  True  | False  0  |     | 訪視日期  |     |
| ----------------- | ----------- | --------- | --- | ----- | --- |

| False  VisitPersonID  | int  True  | False  0  |     | 訪視人員  |     |
| --------------------- | ---------- | --------- | --- | ----- | --- |

| False  VisitState  | int  True  | False  0  |     | 訪視狀態(1:未訪視， |     |
| ------------------ | ---------- | --------- | --- | ----------- | --- |
2:已訪視)

| False  SendDate  | dateti False  | False  0  |     | 最後寄送時間  |     |
| ---------------- | ------------- | --------- | --- | ------- | --- |
me2

| False  CreateUserID  | int  True  | False  0  |     | 建立者 | ID  |
| -------------------- | ---------- | --------- | --- | --- | --- |

創建日期
| False  CreateDate  | dateti True  | False  0  |     |     |     |
| ------------------ | ------------ | --------- | --- | --- | --- |
me2
| 機密等級：內部文件  |     |     | 版權所有©2020凌誠科技股份有限公司  |     |     |
| ---------- | --- | --- | -------------------- | --- | --- |
374/391

| 文件名稱：資料庫設計規格書  |     | 皇基股份有限公司  | 日期：109年10月30日  |
| -------------- | --- | --------- | -------------- |

| False  ModifyUserID  | int  | True  False  0  | 修改者 ID  |
| -------------------- | ---- | --------------- | ------- |

| False  ModifyDate  | dateti | True  False  0  | 修改日期  |
| ------------------ | ------ | --------------- | ----- |
me2

| False  Note  | nvarc | True  False  500  | 其它訪談內容  |
| ------------ | ----- | ----------------- | ------- |
har

約束
| 名稱                   | 型態      | 欄位  |     |
| -------------------- | ------- | --- | --- |
| PK_SCUnderContractVi | Public  | ID  |     |
sit
| FK_SCUnderContractVi | Public  | CreateUserID  |     |
| -------------------- | ------- | ------------- | --- |
sit_BIPersonel
| FK_SCUnderContractVi | Public  | ModifyUserID  |     |
| -------------------- | ------- | ------------- | --- |
sit_BIPersonel_Modify
User
| FK_SCUnderContractVi | Public  | VisitPersonID  |     |
| -------------------- | ------- | -------------- | --- |
sit_BIPersonel_VisitPers
on
| FK_SCUnderContractVi | Public  | SupplierID  |     |
| -------------------- | ------- | ----------- | --- |
sit_BISupplier

關連
| 欄位                 | 關連     |     |     |
| ------------------ | ------ | --- | --- |
| (SupplierID = ID)  | 0..*   |     |     |
FK_SCUnderContractVisit_BISupplier
 1
PK_BISupplier
| (VisitPersonID = ID)  | 0..*   |     |     |
| --------------------- | ------ | --- | --- |
FK_SCUnderContractVisit_BIPersonel_VisitPerson
 1
PK_BS_Personel
| (ModifyUserID = ID)  | 0..*                                           |     |     |
| -------------------- | ---------------------------------------------- | --- | --- |
|                      | FK_SCUnderContractVisit_BIPersonel_ModifyUser  |     |     |
 1
PK_BS_Personel
| (CreateUserID = ID)  | 0..*   |     |     |
| -------------------- | ------ | --- | --- |
FK_SCUnderContractVisit_BIPersonel
 1
機密等級：內部文件  版權所有©2020凌誠科技股份有限公司
375/391

| 文件名稱：資料庫設計規格書  |     | 皇基股份有限公司  |     | 日期：109年10月30日  |
| -------------- | --- | --------- | --- | -------------- |
| 欄位             | 關連  |           |     |                |
PK_BS_Personel
| (UnderContractVisitID =  | 0..*                                            |     |     |     |
| ------------------------ | ----------------------------------------------- | --- | --- | --- |
| ID)                      | FK_SCUnderContractRecord_SCUnderContractVisit   |     |     |     |
 1
PK_SCUnderContractVisit

83.  資料表名稱：YPDistribution
| 索引  名稱    | 型態   | 非空值  唯一  長度    | 初始值  | 說明  |
| --------- | ---- | -------------- | ---- | --- |
|           |      |                |      |     |
| True  ID  | int  | True  True  0  |      |     |
配貨主檔 ID
| False  DistributionPlanI | int  | True  False  0  | ((0))  |     |
| ------------------------ | ---- | --------------- | ------ | --- |
D
| False  ShipDate          | dateti | True  False  0  | (sysdateti | 出貨日期   |
| ------------------------ | ------ | --------------- | ---------- | ------ |
|                          | me2    |                 | me())      |        |
| False  CustomerID        | int    | True  False  0  | ((0))      | 客戶 ID  |
| False  DistributionType  | int    | True  False  0  | ((0))      | 配貨類型   |
| False  ProductID         | int    | True  False  0  | ((0))      | 產品 ID  |
| False  SpecID            | int    | True  False  0  | ((0))      | 規格 ID  |
品種別名 ID
| False  BreedAliasID     | int  | True  False  0  | ((0))  |       |
| ----------------------- | ---- | --------------- | ------ | ----- |
| False  Grade            | int  | True  False  0  | ((0))  | 等級    |
| False  DistributionQuan | int  | True  False  0  | ((0))  | 需求數量  |
tity
| False  Airport  | nvarc | True  False  100  | ('')  | 機場/港口  |
| --------------- | ----- | ----------------- | ----- | ------ |
har
| False  Remark  | nvarc | True  False  100  | ('')  | 備註  |
| -------------- | ----- | ----------------- | ----- | --- |
har
| False  DistributionState  | int    | True  False  0  | ((1))      | 配貨狀態    |
| ------------------------- | ------ | --------------- | ---------- | ------- |
| False  CreateUserID       | int    | True  False  0  | ((0))      | 創建者 ID  |
| False  CreateDate         | dateti | True  False  0  | (sysdateti | 創建日期    |
|                           | me2    |                 | me())      |         |
| False  ModifyUserID       | int    | True  False  0  | ((0))      | 修改者 ID  |
| False  ModifyDate         | dateti | True  False  0  | (sysdateti | 修改日期    |
|                           | me2    |                 | me())      |         |

約束
| 名稱               | 型態      | 欄位  |     |     |
| ---------------- | ------- | --- | --- | --- |
| PK_Distribution  | Public  | ID  |     |     |

| 機密等級：內部文件  |     |     | 版權所有©2020凌誠科技股份有限公司  |     |
| ---------- | --- | --- | -------------------- | --- |
376/391

| 文件名稱：資料庫設計規格書  |     | 皇基股份有限公司  |     | 日期：109年10月30日  |     |
| -------------- | --- | --------- | --- | -------------- | --- |
84.  資料表名稱：YPDistributionPlan
| 索引  名稱                 | 型態   | 非空值  唯一  長度     | 初始值    | 說明     |     |
| ---------------------- | ---- | --------------- | ------ | ------ | --- |
|                        |      |                 |        |        |     |
| True  ID               | int  | True  True  0   |        |        |     |
| False  ProductionLineI | int  | True  False  0  | ((0))  | 產線 ID  |     |
D
| False  ShipMonth  | dateti | True  False  0  | (sysdateti | 出貨年月  |     |
| ----------------- | ------ | --------------- | ---------- | ----- | --- |
|                   | me2    |                 | me())      |       |     |
備註
| False  Remark  | nvarc | True  False  100  | ('')  |     |     |
| -------------- | ----- | ----------------- | ----- | --- | --- |
har
| False  CreateUserID  | int  | True  False  0  | ((0))  | 創建者 | ID  |
| -------------------- | ---- | --------------- | ------ | --- | --- |
創建日期
| False  CreateDate    | dateti | True  False  0  | (sysdateti |       |     |
| -------------------- | ------ | --------------- | ---------- | ----- | --- |
|                      | me2    |                 | me())      |       |     |
| False  ModifyUserID  | int    | True  False  0  | ((0))      | 修改者   | ID  |
| False  ModifyDate    | dateti | True  False  0  | (sysdateti | 修改日期  |     |
|                      | me2    |                 | me())      |       |     |

約束
| 名稱                   | 型態      | 欄位  |     |     |     |
| -------------------- | ------- | --- | --- | --- | --- |
| PK_DistributionPlan  | Public  | ID  |     |     |     |

85.  資料表名稱：YPPicking
| 索引  名稱                | 型態    | 非空值  唯一  長度      | 初始值    | 說明     |     |
| --------------------- | ----- | ---------------- | ------ | ------ | --- |
|                       |       |                  |        |        |     |
| True  ID              | int   | True  True  0    |        |        |     |
| False  PickingPlanID  | int   | True  False  0   | ((0))  | 挑苗排程主檔 | ID  |
| False  PositionID     | int   | True  False  0   | ((0))  | 位置 ID  |     |
| False  BatchNo        | nvarc | True  False  50  | ('')   | 批號     |     |
har
| False  BreedAliasID  | int  | True  False  0  | ((0))  | 品種別名   | ID  |
| -------------------- | ---- | --------------- | ------ | ------ | --- |
| False  Inventory     | int  | True  False  0  | ((0))  | 目前庫存數  |     |
創建者
| False  CreateUserID  | int    | True  False  0  | ((0))      |       | ID  |
| -------------------- | ------ | --------------- | ---------- | ----- | --- |
| False  CreateDate    | dateti | True  False  0  | (sysdateti | 創建日期  |     |
|                      | me2    |                 | me())      |       |     |
修改者 ID
| False  ModifyUserID  | int    | True  False  0  | ((0))      |       |     |
| -------------------- | ------ | --------------- | ---------- | ----- | --- |
| False  ModifyDate    | dateti | True  False  0  | (sysdateti | 修改日期  |     |
|                      | me2    |                 | me())      |       |     |

約束
| 機密等級：內部文件  |     |     | 版權所有©2020凌誠科技股份有限公司  |     |     |
| ---------- | --- | --- | -------------------- | --- | --- |
377/391

| 文件名稱：資料庫設計規格書  |         | 皇基股份有限公司  |     | 日期：109年10月30日  |     |
| -------------- | ------- | --------- | --- | -------------- | --- |
| 名稱             | 型態      | 欄位        |     |                |     |
| PK_Picking     | Public  | ID        |     |                |     |

86.  資料表名稱：YPPickingPlan
| 索引  名稱                | 型態    | 非空值  唯一  長度      | 初始值   | 說明      |     |
| --------------------- | ----- | ---------------- | ----- | ------- | --- |
|                       |       |                  |       |         |     |
| True  ID              | int   | True  True  0    |       |         |     |
| False  PickingPlanNo  | nvarc | True  False  50  | ('')  | 挑苗排程單號  |     |
har
| False  ShipMonth  | dateti | True  False  0  | (sysdateti | 出貨年月  |     |
| ----------------- | ------ | --------------- | ---------- | ----- | --- |
|                   | me2    |                 | me())      |       |     |
產線 ID
| False  ProductionLineI | int  | True  False  0  | ((0))  |     |     |
| ---------------------- | ---- | --------------- | ------ | --- | --- |
D
| False  PickingType  | int   | True  False  0    | ((0))  | 挑苗類型   |     |
| ------------------- | ----- | ----------------- | ------ | ------ | --- |
| False  ProductID    | int   | True  False  0    | ((0))  | 產品 ID  |     |
| False  SpecID       | int   | True  False  0    | ((0))  | 規格 ID  |     |
| False  Remark       | nvarc | True  False  100  | ('')   | 備註     |     |
har
| False  PickingState  | int    | True  False  0  | ((1))      | 挑苗狀態  |     |
| -------------------- | ------ | --------------- | ---------- | ----- | --- |
| False  CreateUserID  | int    | True  False  0  | ((0))      | 創建者   | ID  |
| False  CreateDate    | dateti | True  False  0  | (sysdateti | 創建日期  |     |
|                      | me2    |                 | me())      |       |     |
修改者 ID
| False  ModifyUserID  | int    | True  False  0  | ((0))      |       |     |
| -------------------- | ------ | --------------- | ---------- | ----- | --- |
| False  ModifyDate    | dateti | True  False  0  | (sysdateti | 修改日期  |     |
|                      | me2    |                 | me())      |       |     |

約束
| 名稱              | 型態      | 欄位  |     |     |     |
| --------------- | ------- | --- | --- | --- | --- |
| PK_PickingPlan  | Public  | ID  |     |     |     |

87.  資料表名稱：YPPickingPlanAllocation
| 索引  名稱                | 型態    | 非空值  唯一  長度      | 初始值    | 說明     |     |
| --------------------- | ----- | ---------------- | ------ | ------ | --- |
|                       |       |                  |        |        |     |
| True  ID              | int   | True  True  0    |        |        |     |
|                       |       |                  |        | 挑苗排程主檔 | ID  |
| False  PickingPlanID  | int   | True  False  0   | ((0))  |        |     |
| False  PickingID      | int   | True  False  0   | ((0))  | 挑苗 ID  |     |
| False  BatchNo        | nvarc | True  False  50  | ('')   | 批號     |     |
har
| False  BreedAliasID  | int  | True  False  0   | ((0))                | 品種別名  | ID  |
| -------------------- | ---- | ---------------- | -------------------- | ----- | --- |
| False  AllocateA     | int  | False  False  0  | ((0))                | 等級 A  |     |
| 機密等級：內部文件            |      |                  | 版權所有©2020凌誠科技股份有限公司  |       |     |
378/391

| 文件名稱：資料庫設計規格書     |      | 皇基股份有限公司         |        | 日期：109年10月30日  |
| ----------------- | ---- | ---------------- | ------ | -------------- |
| False  AllocateB  | int  | False  False  0  | ((0))  | 等級 B           |
| False  AllocateC  | int  | False  False  0  | ((0))  | 等級 C           |
等級 D
| False  AllocateD     | int    | False  False  0  | ((0))      |         |
| -------------------- | ------ | ---------------- | ---------- | ------- |
| False  CreateUserID  | int    | True  False  0   | ((0))      | 創建者 ID  |
| False  CreateDate    | dateti | True  False  0   | (sysdateti | 創建日期    |
|                      | me2    |                  | me())      |         |
| False  ModifyUserID  | int    | True  False  0   | ((0))      | 修改者 ID  |
| False  ModifyDate    | dateti | True  False  0   | (sysdateti | 修改日期    |
|                      | me2    |                  | me())      |         |

約束
| 名稱                     | 型態      | 欄位  |     |     |
| ---------------------- | ------- | --- | --- | --- |
| PK_PickingPlanAllocati | Public  | ID  |     |     |
on

88.  資料表名稱：YPPickingRecord
| 索引  名稱            | 型態   | 非空值  唯一  長度     | 初始值    | 說明       |
| ----------------- | ---- | --------------- | ------ | -------- |
|                   |      |                 |        |          |
| True  ID          | int  | True  True  0   |        |          |
| False  PickingID  | int  | True  False  0  | ((0))  | 挑苗 ID    |
| False  GradeA     | int  | True  False  0  | ((0))  | 等級 A     |
| False  GradeB     | int  | True  False  0  | ((0))  | 等級 B     |
等級 C
| False  GradeC  | int   | True  False  0    | ((0))  |       |
| -------------- | ----- | ----------------- | ------ | ----- |
| False  GradeD  | int   | True  False  0    | ((0))  | 等級 D  |
| False  Remark  | nvarc | True  False  100  | ('')   | 備註    |
har
| False  PickingDate   | dateti | True  False  0  | (sysdateti | 挑苗日期    |
| -------------------- | ------ | --------------- | ---------- | ------- |
|                      | me2    |                 | me())      |         |
| False  CreateUserID  | int    | True  False  0  | ((0))      | 創建者 ID  |
| False  CreateDate    | dateti | True  False  0  | (sysdateti | 創建日期    |
|                      | me2    |                 | me())      |         |
| False  ModifyUserID  | int    | True  False  0  | ((0))      | 修改者 ID  |
| False  ModifyDate    | dateti | True  False  0  | (sysdateti | 修改日期    |
|                      | me2    |                 | me())      |         |

約束
| 名稱                | 型態      | 欄位  |     |     |
| ----------------- | ------- | --- | --- | --- |
| PK_PickingRecord  | Public  | ID  |     |     |

| 機密等級：內部文件  |     |     | 版權所有©2020凌誠科技股份有限公司  |     |
| ---------- | --- | --- | -------------------- | --- |
379/391

| 文件名稱：資料庫設計規格書  |     | 皇基股份有限公司  |     | 日期：109年10月30日  |     |
| -------------- | --- | --------- | --- | -------------- | --- |
89.  資料表名稱：YPPickingRegular
| 索引  名稱    | 型態   | 非空值  唯一  長度    | 初始值  | 說明  |     |
| --------- | ---- | -------------- | ---- | --- | --- |
|           |      |                |      |     |     |
| True  ID  | int  | True  True  0  |      |     |     |
False  PickingPlanNo  nvarc True  False  50  ('')  挑苗排程主檔 ID
har
| False  ShipMonth  | dateti | True  False  0  | (sysdateti | 挑苗年月  |     |
| ----------------- | ------ | --------------- | ---------- | ----- | --- |
|                   | me2    |                 | me())      |       |     |
產線 ID
| False  ProductionBatchI | int  | True  False  0  | ((0))  |     |     |
| ----------------------- | ---- | --------------- | ------ | --- | --- |
D
| False  PositionID  | int  | True  False  0  | ((0))  | 位置 ID  |     |
| ------------------ | ---- | --------------- | ------ | ------ | --- |
調查穴盤數
| False  PlugNumber    | int   | True  False  0    | ((0))  |        |     |
| -------------------- | ----- | ----------------- | ------ | ------ | --- |
| False  SampleNumber  | int   | True  False  0    | ((0))  | 每盤抽樣數  |     |
| False  Remark        | nvarc | True  False  100  | ('')   | 備註     |     |
har
| False  CreateUserID  | int    | True  False  0  | ((0))      | 創建者   | ID  |
| -------------------- | ------ | --------------- | ---------- | ----- | --- |
| False  CreateDate    | dateti | True  False  0  | (sysdateti | 創建日期  |     |
|                      | me2    |                 | me())      |       |     |
| False  ModifyUserID  | int    | True  False  0  | ((0))      | 修改者   | ID  |
修改日期
| False  ModifyDate  | dateti | True  False  0  | (sysdateti |     |     |
| ------------------ | ------ | --------------- | ---------- | --- | --- |
|                    | me2    |                 | me())      |     |     |

約束
| 名稱                 | 型態      | 欄位  |     |     |     |
| ------------------ | ------- | --- | --- | --- | --- |
| PK_PickingRegular  | Public  | ID  |     |     |     |

90.  資料表名稱：YPPickingRegularRecord
| 索引  名稱                 | 型態   | 非空值  唯一  長度     | 初始值    | 說明   |     |
| ---------------------- | ---- | --------------- | ------ | ---- | --- |
|                        |      |                 |        |      |     |
| True  ID               | int  | True  True  0   |        |      |     |
| False  PickingRegularI | int  | True  False  0  | ((0))  | 日常挑苗 | ID  |
D
| False  PlugNumber      | int  | True  False  0  | ((0))  | 穴盤編號  |     |
| ---------------------- | ---- | --------------- | ------ | ----- | --- |
| False  DefectReasonID  | int  | True  False  0  | ((0))  | 不良原因  | ID  |
數量
| False  Quantity      | int    | True  False  0  | ((0))                |       |     |
| -------------------- | ------ | --------------- | -------------------- | ----- | --- |
| False  PickingDate   | dateti | True  False  0  | (sysdateti           | 挑苗日期  |     |
|                      | me2    |                 | me())                |       |     |
| False  CreateUserID  | int    | True  False  0  | ((0))                | 創建者   | ID  |
| False  CreateDate    | dateti | True  False  0  | (sysdateti           | 創建日期  |     |
|                      | me2    |                 | me())                |       |     |
| 機密等級：內部文件            |        |                 | 版權所有©2020凌誠科技股份有限公司  |       |     |
380/391

| 文件名稱：資料庫設計規格書        |        | 皇基股份有限公司        |            | 日期：109年10月30日  |     |
| -------------------- | ------ | --------------- | ---------- | -------------- | --- |
| False  ModifyUserID  | int    | True  False  0  | ((0))      | 修改者            | ID  |
| False  ModifyDate    | dateti | True  False  0  | (sysdateti | 修改日期           |     |
|                      | me2    |                 | me())      |                |     |

約束
| 名稱                   | 型態      | 欄位  |     |     |     |
| -------------------- | ------- | --- | --- | --- | --- |
| PK_PickingRegularRec | Public  | ID  |     |     |     |
ord

91.  資料表名稱：YPProductionBatch
| 索引  名稱                 | 型態   | 非空值  唯一  長度     | 初始值    | 說明     |     |
| ---------------------- | ---- | --------------- | ------ | ------ | --- |
|                        |      |                 |        |        |     |
| True  ID               | int  | True  True  0   |        |        |     |
| False  ProductionLineI | int  | True  False  0  | ((0))  | 產線 ID  |     |
D
| False  PurchaseID    | int    | True  False  0  | ((0))      | 進貨任務  | ID  |
| -------------------- | ------ | --------------- | ---------- | ----- | --- |
| False  PurchaseDate  | dateti | True  False  0  | (sysdateti | 進貨日期  |     |
|                      | me2    |                 | me())      |       |     |
False  SupplierBottleID  int  True  False  0  ((0))  瓶苗來源廠商 ID
|                         |      |                 |        | 苗株來源廠商 | ID  |
| ----------------------- | ---- | --------------- | ------ | ------ | --- |
| False  SupplierSeedling | int  | True  False  0  | ((0))  |        |     |
ID
| False  BatchNo  | nvarc | True  False  50  | ('')  | 批號  |     |
| --------------- | ----- | ---------------- | ----- | --- | --- |
har
| False  BreedAliasID  | int   | True  False  0   | ((0))  | 品種別名   | ID  |
| -------------------- | ----- | ---------------- | ------ | ------ | --- |
| False  SpecID        | int   | True  False  0   | ((0))  | 規格 ID  |     |
| False  BatchNoSrc    | nvarc | True  False  50  | ('')   | 來源批號   |     |
har
| False  CutNum    | int  | True  False  0  | ((0))  | 切次     |     |
| ---------------- | ---- | --------------- | ------ | ------ | --- |
| False  PotID     | int  | True  False  0  | ((0))  | 盆器 ID  |     |
| False  MediumID  | int  | True  False  0  | ((0))  | 介質 ID  |     |
製程
| False  ProcessID  | int  | True  False  0  | ((0))  | ID  |     |
| ----------------- | ---- | --------------- | ------ | --- | --- |
False  ProcessDate  dateti True  False  0  (sysdateti 製程異動日期
|     | me2  |     | me())  |     |     |
| --- | ---- | --- | ------ | --- | --- |
製程完工日期
| False  CompletedDate  | dateti | True  False  0  | (sysdateti           |       |     |
| --------------------- | ------ | --------------- | -------------------- | ----- | --- |
|                       | me2    |                 | me())                |       |     |
| False  CreateUserID   | int    | True  False  0  | ((0))                | 創建者   | ID  |
| False  CreateDate     | dateti | True  False  0  | (sysdateti           | 創建日期  |     |
|                       | me2    |                 | me())                |       |     |
| False  ModifyUserID   | int    | True  False  0  | ((0))                | 修改者   | ID  |
| 機密等級：內部文件             |        |                 | 版權所有©2020凌誠科技股份有限公司  |       |     |
381/391

| 文件名稱：資料庫設計規格書      |        | 皇基股份有限公司        |            | 日期：109年10月30日  |     |
| ------------------ | ------ | --------------- | ---------- | -------------- | --- |
| False  ModifyDate  | dateti | True  False  0  | (sysdateti | 修改日期           |     |
|                    | me2    |                 | me())      |                |     |

| False  ProcessLogID  | int  | False  False  0  |     | 目前製程記錄 | ID  |
| -------------------- | ---- | ---------------- | --- | ------ | --- |

約束
| 名稱                   | 型態      | 欄位            |     |     |     |
| -------------------- | ------- | ------------- | --- | --- | --- |
| PK_ProductionUnit    | Public  | ID            |     |     |     |
| FK_YPProductionBatch | Public  | ProcessLogID  |     |     |     |
_YPProductionBatchPro
cessLog

關連
| 欄位  | 關連  |     |     |     |     |
| --- | --- | --- | --- | --- | --- |

0..*
|     | FK_YPProductionBatch_YPProductionBatchProces...  |     |     |     |     |
| --- | ------------------------------------------------ | --- | --- | --- | --- |
 1
PK_YPProductionBatchProcessLog
| (ProductionBatchID =  | 0..*                                       |     |     |     |     |
| --------------------- | ------------------------------------------ | --- | --- | --- | --- |
| ID)                   | FK_YPTransferRecordTemp_ProductionBatchID  |     |     |     |     |
 1
PK_ProductionUnit

92.  資料表名稱：YPPurchase
| 索引  名稱                 | 型態   | 非空值  唯一  長度     | 初始值    | 說明     |     |
| ---------------------- | ---- | --------------- | ------ | ------ | --- |
|                        |      |                 |        |        |     |
| True  ID               | int  | True  True  0   |        |        |     |
| False  ProductionLineI | int  | True  False  0  | ((0))  | 產線 ID  |     |
D
| False  BatchNoPR  | nvarc | True  False  50  | ('')  | 來源批號  |     |
| ----------------- | ----- | ---------------- | ----- | ----- | --- |
har
| False  BreedAliasID  | int  | True  False  0  | ((0))  | 品種別名   | ID  |
| -------------------- | ---- | --------------- | ------ | ------ | --- |
| False  SpecID        | int  | True  False  0  | ((0))  | 規格 ID  |     |
False  SupplierBottleID  int  True  False  0  ((0))  瓶苗來源廠商 ID
False  SupplierSeedling int  True  False  0  ((0))  苗株來源廠商 ID
ID
驗收數量
| False  Quantity      | int    | True  False  0  | ((0))      |       |     |
| -------------------- | ------ | --------------- | ---------- | ----- | --- |
| False  PurchaseDate  | dateti | True  False  0  | (sysdateti | 進貨日期  |     |
|                      | me2    |                 | me())      |       |     |
驗收平台進貨單ID
| False  RB_Purchase_ID  | int  | True  False  0  | ((0))                |     |     |
| ---------------------- | ---- | --------------- | -------------------- | --- | --- |
| 機密等級：內部文件              |      |                 | 版權所有©2020凌誠科技股份有限公司  |     |     |
382/391

| 文件名稱：資料庫設計規格書        |        | 皇基股份有限公司         |            | 日期：109年10月30日  |     |
| -------------------- | ------ | ---------------- | ---------- | -------------- | --- |
| False  CreateUserID  | int    | True  False  0   | ((0))      | 創建者            | ID  |
| False  CreateDate    | dateti | True  False  0   | (sysdateti | 創建日期           |     |
|                      | me2    |                  | me())      |                |     |
| False  ModifyUserID  | int    | True  False  0   | ((0))      | 修改者            | ID  |
| False  ModifyDate    | dateti | True  False  0   | (sysdateti | 修改日期           |     |
|                      | me2    |                  | me())      |                |     |
| False  BatchNo       | nvarc  | True  False  50  | ('')       | 批號             |     |
har

約束
| 名稱           | 型態      | 欄位  |     |     |     |
| ------------ | ------- | --- | --- | --- | --- |
| PK_Purchase  | Public  | ID  |     |     |     |

93.  資料表名稱：YPShipPlan
| 索引  名稱                 | 型態    | 非空值  唯一  長度      | 初始值    | 說明     |     |
| ---------------------- | ----- | ---------------- | ------ | ------ | --- |
|                        |       |                  |        |        |     |
| True  ID               | int   | True  True  0    |        |        |     |
| False  DistributionID  | int   | True  False  0   | ((0))  | 配貨 ID  |     |
| False  BatchNo         | nvarc | True  False  50  | ('')   | 批號     |     |
har
| False  ShipPlanQuantity  | int  | True  False  0  | ((0))  | 出貨安排數量  |     |
| ------------------------ | ---- | --------------- | ------ | ------- | --- |
| False  CreateUserID      | int  | True  False  0  | ((0))  | 創建者     | ID  |
創建日期
| False  CreateDate    | dateti | True  False  0  | (sysdateti |     |     |
| -------------------- | ------ | --------------- | ---------- | --- | --- |
|                      | me2    |                 | me())      |     |     |
| False  ModifyUserID  | int    | True  False  0  | ((0))      | 修改者 | ID  |
修改日期
| False  ModifyDate  | dateti | True  False  0  | (sysdateti |     |     |
| ------------------ | ------ | --------------- | ---------- | --- | --- |
|                    | me2    |                 | me())      |     |     |

約束
| 名稱           | 型態      | 欄位  |     |     |     |
| ------------ | ------- | --- | --- | --- | --- |
| PK_ShipPlan  | Public  | ID  |     |     |     |

94.  資料表名稱：YPShipRecord
| 索引  名稱                 | 型態   | 非空值  唯一  長度      | 初始值    | 說明   |     |
| ---------------------- | ---- | ---------------- | ------ | ---- | --- |
|                        |      |                  |        |      |     |
| True  ID               | int  | True  True  0    |        |      |     |
| False  ShipPlanID      | int  | True  False  0   | ((0))  | 出貨安排 | ID  |
| False  TransferRecordI | int  | False  False  0  | ((0))  | 移轉紀錄 | ID  |
D
| False  IsArrangement  | bit  | True  False  0  | ((1))                | 組長安排  |     |
| --------------------- | ---- | --------------- | -------------------- | ----- | --- |
| 機密等級：內部文件             |      |                 | 版權所有©2020凌誠科技股份有限公司  |       |     |
383/391

| 文件名稱：資料庫設計規格書        |        | 皇基股份有限公司        |            | 日期：109年10月30日  |     |
| -------------------- | ------ | --------------- | ---------- | -------------- | --- |
| False  CreateUserID  | int    | True  False  0  | ((0))      | 創建者            | ID  |
| False  CreateDate    | dateti | True  False  0  | (sysdateti | 創建日期           |     |
|                      | me2    |                 | me())      |                |     |
| False  ModifyUserID  | int    | True  False  0  | ((0))      | 修改者            | ID  |
| False  ModifyDate    | dateti | True  False  0  | (sysdateti | 修改日期           |     |
|                      | me2    |                 | me())      |                |     |

| False  TempTransferRec | int  | False  False  0  |     | 暫存移轉紀錄 | ID  |
| ---------------------- | ---- | ---------------- | --- | ------ | --- |
ordID

| False  ArrangeState  | int  | True  False  0  |     | 組長確認狀態  |     |
| -------------------- | ---- | --------------- | --- | ------- | --- |

約束
| 名稱                  | 型態      | 欄位                |     |     |     |
| ------------------- | ------- | ----------------- | --- | --- | --- |
| PK_ShipRecord       | Public  | ID                |     |     |     |
| FK_YPShipRecord_Tra | Public  | TransferRecordID  |     |     |     |
nsferRecordID
| FK_YPShipRecord_Te | Public  | TempTransferRecordID  |     |     |     |
| ------------------ | ------- | --------------------- | --- | --- | --- |
mpTransferRecordID

關連
| 欄位                     | 關連                                    |     |     |     |     |
| ---------------------- | ------------------------------------- | --- | --- | --- | --- |
| (TempTransferRecordID  | 0..*                                  |     |     |     |     |
| = ID)                  | FK_YPShipRecord_TempTransferRecordID  |     |     |     |     |
 1
PK_YPTransferRecordTemp
| (TransferRecordID = ID)  | 0..*                              |     |     |     |     |
| ------------------------ | --------------------------------- | --- | --- | --- | --- |
|                          | FK_YPShipRecord_TransferRecordID  |     |     |     |     |
 1
PK_TransferRecord

95.  資料表名稱：YPTransferRecord
| 索引  名稱                  | 型態   | 非空值  唯一  長度     | 初始值    | 說明     |     |
| ----------------------- | ---- | --------------- | ------ | ------ | --- |
|                         |      |                 |        |        |     |
| True  ID                | int  | True  True  0   |        |        |     |
| False  ProductionBatchI | int  | True  False  0  | ((0))  | 產線 ID  |     |
D
位置 ID
| False  PositionID    | int  | True  False  0  | ((0))  |      |     |
| -------------------- | ---- | --------------- | ------ | ---- | --- |
| False  ReasonID      | int  | True  False  0  | ((0))  | 移轉原因 | ID  |
| False  ReasonDescID  | int  | True  False  0  | ((0))  | 原因說明 | ID  |
數量
| False  Quantity  | int  | True  False  0  | ((0))                |     |     |
| ---------------- | ---- | --------------- | -------------------- | --- | --- |
| 機密等級：內部文件        |      |                 | 版權所有©2020凌誠科技股份有限公司  |     |     |
384/391

| 文件名稱：資料庫設計規格書  |       | 皇基股份有限公司          |       | 日期：109年10月30日  |     |
| -------------- | ----- | ----------------- | ----- | -------------- | --- |
| False  Remark  | nvarc | True  False  100  | ('')  | 備註             |     |
har
| False  TransferDate    | dateti | True  False  0  | (sysdateti | 移轉日期   |     |
| ---------------------- | ------ | --------------- | ---------- | ------ | --- |
|                        | me2    |                 | me())      |        |     |
| False  TransferTaskID  | int    | True  False  0  | ((0))      | 移轉任務   | ID  |
| False  CustomerID      | int    | True  False  0  | ((0))      | 客戶 ID  |     |
| False  ExchangeState   | int    | True  False  0  | ((1))      | 拋轉狀態   |     |
| False  CreateUserID    | int    | True  False  0  | ((0))      | 創建者    | ID  |
| False  CreateDate      | dateti | True  False  0  | (sysdateti | 創建日期   |     |
|                        | me2    |                 | me())      |        |     |
修改者 ID
| False  ModifyUserID  | int    | True  False  0  | ((0))      |       |     |
| -------------------- | ------ | --------------- | ---------- | ----- | --- |
| False  ModifyDate    | dateti | True  False  0  | (sysdateti | 修改日期  |     |
|                      | me2    |                 | me())      |       |     |
| False  RefID         | int    | True  False  0  | ((0))      |       |     |

| False  ProcessLogID  | int  | False  False  0  |     | 製程資訊 | ID  |
| -------------------- | ---- | ---------------- | --- | ---- | --- |

約束
| 名稱                   | 型態      | 欄位            |     |     |     |
| -------------------- | ------- | ------------- | --- | --- | --- |
| PK_TransferRecord    | Public  | ID            |     |     |     |
| FK_YPTransferRecord_ | Public  | ProcessLogID  |     |     |     |
YPProductionBatchProc
essLog

關連
| 欄位                     | 關連                                       |     |     |     |     |
| ---------------------- | ---------------------------------------- | --- | --- | --- | --- |
| (YPTransferRecordID =  | 0..*                                     |     |     |     |     |
| ID)                    | FK_PPTransferTaskMap_YPTransferRecordID  |     |     |     |     |
 1
PK_TransferRecord
| (TransferRecordID = ID)  | 0..*                              |     |     |     |     |
| ------------------------ | --------------------------------- | --- | --- | --- | --- |
|                          | FK_YPShipRecord_TransferRecordID  |     |     |     |     |
 1
PK_TransferRecord
| (ProcessLogID = ID)  | 0..*   |     |     |     |     |
| -------------------- | ------ | --- | --- | --- | --- |
FK_YPTransferRecord_YPProductionBatchProcessLog
 1
PK_YPProductionBatchProcessLog

| 機密等級：內部文件  |     |     | 版權所有©2020凌誠科技股份有限公司  |     |     |
| ---------- | --- | --- | -------------------- | --- | --- |
385/391

| 文件名稱：資料庫設計規格書  |     | 皇基股份有限公司  |     | 日期：109年10月30日  |     |
| -------------- | --- | --------- | --- | -------------- | --- |
96.  資料表名稱：YPTransferRecordTemp
| 索引  名稱  | 型態  | 非空值  唯一  長度  | 初始值  | 說明  |     |
| ------- | --- | ------------ | ---- | --- | --- |

| True  ID  | int  | True  True  0  |     |     |     |
| --------- | ---- | -------------- | --- | --- | --- |

| False  ProductionBatchI | int  | True  False  0  |     | 產線 ID  |     |
| ----------------------- | ---- | --------------- | --- | ------ | --- |
D

| False  PositionID  | int  | True  False  0  |     | 位置 ID  |     |
| ------------------ | ---- | --------------- | --- | ------ | --- |

| False  ReasonID  | int  | True  False  0  |     | 移轉原因 | ID  |
| ---------------- | ---- | --------------- | --- | ---- | --- |

| False  ReasonDescID  | int  | True  False  0  |     | 原因說明 | ID  |
| -------------------- | ---- | --------------- | --- | ---- | --- |

| False  Quantity  | int   | True  False  0    |       | 數量  |     |
| ---------------- | ----- | ----------------- | ----- | --- | --- |
| False  Remark    | nvarc | True  False  100  | ('')  | 備註  |     |
har
| False  TransferDate  | dateti | True  False  0  | (sysdateti | 移轉日期  |     |
| -------------------- | ------ | --------------- | ---------- | ----- | --- |
|                      | me2    |                 | me())      |       |     |

| False  CustomerID  | int  | True  False  0  |     | 客戶 ID  |     |
| ------------------ | ---- | --------------- | --- | ------ | --- |

| False  ProcessLogID  | int  | False  False  0  |     | 製程資訊 | ID  |
| -------------------- | ---- | ---------------- | --- | ---- | --- |

| False  CreateUserID  | int    | True  False  0  |            | 創建者   | ID  |
| -------------------- | ------ | --------------- | ---------- | ----- | --- |
| False  CreateDate    | dateti | True  False  0  | (sysdateti | 創建日期  |     |
|                      | me2    |                 | me())      |       |     |

| False  ModifyUserID  | int    | True  False  0  |            | 修改者   | ID  |
| -------------------- | ------ | --------------- | ---------- | ----- | --- |
| False  ModifyDate    | dateti | True  False  0  | (sysdateti | 修改日期  |     |
|                      | me2    |                 | me())      |       |     |

約束
| 名稱                   | 型態      | 欄位  |     |     |     |
| -------------------- | ------- | --- | --- | --- | --- |
| PK_YPTransferRecordT | Public  | ID  |     |     |     |
emp
| FK_YPTransferRecordT | Public  | CustomerID  |     |     |     |
| -------------------- | ------- | ----------- | --- | --- | --- |
emp_CustomerID
| FK_YPTransferRecordT | Public  | PositionID  |     |     |     |
| -------------------- | ------- | ----------- | --- | --- | --- |
emp_PositionID
| FK_YPTransferRecordT | Public  | ReasonID  |     |     |     |
| -------------------- | ------- | --------- | --- | --- | --- |
emp_ReasonID
| FK_YPTransferRecordT | Public  | ProductionBatchID  |     |     |     |
| -------------------- | ------- | ------------------ | --- | --- | --- |
emp_ProductionBatchID

關連
| 欄位                 | 關連     |     |                      |     |     |
| ------------------ | ------ | --- | -------------------- | --- | --- |
| (PositionID = ID)  | 0..*   |     |                      |     |     |
| 機密等級：內部文件          |        |     | 版權所有©2020凌誠科技股份有限公司  |     |     |
386/391

| 文件名稱：資料庫設計規格書  |     | 皇基股份有限公司  |     | 日期：109年10月30日  |     |
| -------------- | --- | --------- | --- | -------------- | --- |
| 欄位             | 關連  |           |     |                |     |
FK_YPTransferRecordTemp_PositionID
 1
PK_Position_1
| (ReasonID = ID)  | 0..*                              |     |     |     |     |
| ---------------- | --------------------------------- | --- | --- | --- | --- |
|                  | FK_YPTransferRecordTemp_ReasonID  |     |     |     |     |
 1
PK_Reason
| (TempTransferRecordID  | 0..*                                  |     |     |     |     |
| ---------------------- | ------------------------------------- | --- | --- | --- | --- |
| = ID)                  | FK_YPShipRecord_TempTransferRecordID  |     |     |     |     |
 1
PK_YPTransferRecordTemp
| (CustomerID = ID)  | 0..*                                |     |     |     |     |
| ------------------ | ----------------------------------- | --- | --- | --- | --- |
|                    | FK_YPTransferRecordTemp_CustomerID  |     |     |     |     |
 1
PK_BICustomer
| (ProductionBatchID =  | 0..*                                       |     |     |     |     |
| --------------------- | ------------------------------------------ | --- | --- | --- | --- |
| ID)                   | FK_YPTransferRecordTemp_ProductionBatchID  |     |     |     |     |
 1
PK_ProductionUnit

97.  資料表名稱：YPTransferTask
| 索引  名稱                  | 型態  非空值    | 唯一  長度    | 初始值    | 說明      |       |
| ----------------------- | ---------- | --------- | ------ | ------- | ----- |
|                         |            |           |        |         |       |
| True  ID                | int  True  | True  0   |        |         |       |
| False  PID              | int  True  | False  0  | ((0))  | 部門間移轉轉出 | ID    |
|                         |            |           |        | (轉出時為   | 0；退回時 |
|                         |            |           |        | 為轉出     | ID)   |
| False  SourceProduction | int  True  | False  0  | ((0))  | 來源產線    | ID    |
LineID
| False  ReceiveProductio | int  True  | False  0  | ((0))  | 接收產線 | ID  |
| ----------------------- | ---------- | --------- | ------ | ---- | --- |
nLineID
| False  TaskDate      | dateti True  | False  0  | (sysdateti           | 任務日期  |     |
| -------------------- | ------------ | --------- | -------------------- | ----- | --- |
|                      | me2          |           | me())                |       |     |
| False  CreateUserID  | int  True    | False  0  | ((0))                | 創建者   | ID  |
| False  CreateDate    | dateti True  | False  0  | (sysdateti           | 創建日期  |     |
|                      | me2          |           | me())                |       |     |
|                      |              |           |                      | 修改者   | ID  |
| False  ModifyUserID  | int  True    | False  0  | ((0))                |       |     |
| False  ModifyDate    | dateti True  | False  0  | (sysdateti           | 修改日期  |     |
| 機密等級：內部文件            |              |           | 版權所有©2020凌誠科技股份有限公司  |       |     |
387/391

| 文件名稱：資料庫設計規格書  |      | 皇基股份有限公司        |        | 日期：109年10月30日  |
| -------------- | ---- | --------------- | ------ | -------------- |
|                | me2  |                 | me())  |                |
| False  State   | int  | True  False  0  | ((3))  | 狀態             |

約束
| 名稱               | 型態      | 欄位  |     |     |
| ---------------- | ------- | --- | --- | --- |
| PK_TransferTask  | Public  | ID  |     |     |

|            |     |     |                      |     |
| ---------- | --- | --- | -------------------- | --- |
| 機密等級：內部文件  |     |     | 版權所有©2020凌誠科技股份有限公司  |     |
388/391

| 文件名稱：資料庫設計規格書  |     | 皇基股份有限公司  |     | 日期：109年10月30日  |
| -------------- | --- | --------- | --- | -------------- |
三、功能、程式與資料表對照表
| 序號  | 功能代號  |     | 使用資料表  |     |
| --- | ----- | --- | ------ | --- |
BIPersonel, BSRole, BSPersonalRoleMap, BIRoleFunctionMap,
| 1   | 人員帳號  |     |     |     |
| --- | ----- | --- | --- | --- |
BIPersonelProductionLineMap
BIPersonel, BSRole, BSPersonalRoleMap, BIRoleFunctionMap,
| 2   | 角色權限  |     |     |     |
| --- | ----- | --- | --- | --- |
BIPersonelProductionLineMap
| 3   | 客戶資料  | BICustomer                |     |     |
| --- | ----- | ------------------------- | --- | --- |
| 4   | 廠商資料  | BISupplier                |     |     |
| 5   | 規格資料  | BISpec                    |     |     |
| 6   | 花色資料  | BIColor, BIColorCategory  |     |     |
| 7   | 花色類別  | BIColor, BIColorCategory  |     |     |
品種資料
| 8   |       | BIBreed, BIColor, BIColorCategory  |     |     |
| --- | ----- | ---------------------------------- | --- | --- |
| 9   | 盆器資料  | BIPot                              |     |     |
| 10  | 介質資料  | BIMedium                           |     |     |
| 11  | 製程資料  | BIProcess                          |     |     |
位置資料
| 12  |       | BIPosition                          |     |     |
| --- | ----- | ----------------------------------- | --- | --- |
| 13  | 原因說明  | BIReason, BIReasonDesc, BIPersonel  |     |     |
| 14  | 包裝顏色  | BIPackingColor, BIShipPacking       |     |     |
| 15  | 材積規格  | BIPackingSize, BIShipPacking        |     |     |
BIShipPacking, BIPackingSize, BIPackingColor,
| 16  | 出貨包裝  |     |     |     |
| --- | ----- | --- | --- | --- |
BIShipPackingMap
| 17  | 盆花包裝  | BIPPPackingCondition, BISystemOption  |     |     |
| --- | ----- | ------------------------------------- | --- | --- |
YPPurchase, YPProductionBatch, BIReason, YPTransferRecord,
18  進貨任務  BISpec, BISupplier, BIBreedAlias, BIProductionLine,
YPProductionBatchProcessLog, BIPersonel
YPTransferRecord, YPTransferRecordTemp, YPShipRecord,
YPTransferTask, , BIReason, BIReasonDesc, BIPrintField,
BIProductionLine, BIProductionLineReasonMap,
| 19  | 苗株移轉紀錄  |     |     |     |
| --- | ------- | --- | --- | --- |
BIProductionLinePrintFieldMap, BIPersonel, PPTransferRecord,
BIProcess, PPTransferTaskMap, PPTransferTask,
PPTransferBatch , PPShipDetail, PPTransferRecord, BIBreedAlias
YPProductionBatch, YPProductionBatchProcessLog,
| 20  | 苗株生產批次  | YPTransferRecord, BIPersonel, BIBreed, BIColor,  |     |     |
| --- | ------- | ------------------------------------------------ | --- | --- |
BIColorCategory, BIBreedAlias
| 機密等級：內部文件  |     |     | 版權所有©2020凌誠科技股份有限公司  |     |
| ---------- | --- | --- | -------------------- | --- |
389/391

| 文件名稱：資料庫設計規格書  |       | 皇基股份有限公司  |        | 日期：109年10月30日  |
| -------------- | ----- | --------- | ------ | -------------- |
| 序號             | 功能代號  |           | 使用資料表  |                |
YPPicking , YPPickingPlan, YPPickingPlanAllocation,
| 21  | 挑苗排程  |     |     |     |
| --- | ----- | --- | --- | --- |
YPTransferRecord
YPPickingAllocation, YPPickingRegular,
配貨挑苗
22
YPPickingRegularRecord
YPDistribution, YPDistributionPlan, YPPickingPlanAllocation,
| 23  | 苗株配貨單  |     |     |     |
| --- | ------ | --- | --- | --- |
YPShipPlan
YPShipPlan, YPShipRecord, YPDistribution,
| 24  | 苗株出貨安排  |     |     |     |
| --- | ------- | --- | --- | --- |
YPPickingPlanAllocation, YPDistributionPlan
| 25  | 切花採收作業  | CFHarvest, CFHarvestRecord, CFHarvestQuarantine  |     |     |
| --- | ------- | ------------------------------------------------ | --- | --- |
切花移轉紀錄
| 26  |        | CFTransferRecord, CFTransferBatch, CFShipDetail  |     |     |
| --- | ------ | ------------------------------------------------ | --- | --- |
| 27  | 切花需求單  | CFOrder, CFOrderDetail                           |     |     |
CFDistribution, CFDistributionOrderDetailMap,
| 28  | 切花配貨單  |     |     |     |
| --- | ------ | --- | --- | --- |
CFDistributionDetail
| 29  | 切花出貨  | CFShip, CFShipDistributionDetailMap, CFShipDetail  |     |     |
| --- | ----- | -------------------------------------------------- | --- | --- |
PPTransferRecord, PPTransferTask, PPTransferTaskMap,
30  盆花移轉紀錄  PPTransferBatch, YPTransferRecord, YPProductionBatch,
PPShipDetail, BIReason
| 31  | 盆花需求單  | PPOrder, PPOrderDetail  |     |     |
| --- | ------ | ----------------------- | --- | --- |
PPDistribution, PPDistributionDetail,
盆花配貨單
| 32  |     | PPDistributionOrderDetailMap, PPOrderPackingSetting,  |     |     |
| --- | --- | ----------------------------------------------------- | --- | --- |
PPOrderPackingSettingDetail
PPOrderPackingSetting, PPOrderPackingSettingDetail,
33  盆花訂單確認  PPOrderNotice, BIPPPackingCondition, PPDistributionDetail,
PPShipPackingSetting, PPShipPackingSettingDetail
PPOrder, PPShipDetail, PPDistributionDetail,
34  盆花出貨作業  PPShipPackingSetting, PPShipPackingSettingDetail,
PPTransferRecordTemp, PPTransferRecord
| 35  | 抽梗調查  | CFSampleSurvey, CFSampleRecord, CFSampleDetail  |     |     |
| --- | ----- | ----------------------------------------------- | --- | --- |
點梗調查
| 36  |     | CFStemSurvey, CFStemSurveyMap, CFStemSurveyDetail  |     |     |
| --- | --- | -------------------------------------------------- | --- | --- |
CFShipSurvey, CFShipSurveyMap, CFShipSurveyDetail,
切花出貨調查
37
CFShipSurveyDetail_HF
| 38         | 來梗調查  | PPStemSurvey, PPStemSurveyMap, PPStemSurveyDetail  |                      |     |
| ---------- | ----- | -------------------------------------------------- | -------------------- | --- |
| 39         | 打荳調查  | PPBudSurvey, PPBudSurveyMap, PPBudSurveyDetail     |                      |     |
| 機密等級：內部文件  |       |                                                    | 版權所有©2020凌誠科技股份有限公司  |     |
390/391

| 文件名稱：資料庫設計規格書  |        | 皇基股份有限公司                                        |        | 日期：109年10月30日  |
| -------------- | ------ | ----------------------------------------------- | ------ | -------------- |
| 序號             | 功能代號   |                                                 | 使用資料表  |                |
| 40             | 採購單管理  | SCPurchaseOrder, SCPurchaseOrderDetail, BSRole  |        |                |
SCUnderContract, SCUnderContractVisit,
| 41  | 契作批次  |     |     |     |
| --- | ----- | --- | --- | --- |
SCUnderContractRecord
SCUnderContract, SCUnderContractVisit,
| 42  | 契作訪視  |     |     |     |
| --- | ----- | --- | --- | --- |
SCUnderContractRecord
|     | 切花抽梗出貨預估 | CFSampleSurvey, CFSampleRecord, CFSampleDetail  |     |     |
| --- | -------- | ----------------------------------------------- | --- | --- |
43
表
|     | 切花點梗出貨預估 | CFStemSurvey, CFStemSurveyMap, CFStemSurveyDetail  |     |     |
| --- | -------- | -------------------------------------------------- | --- | --- |
44
表
切花點花出貨預估
CFShipSurvey, CFShipSurveyMap, CFShipSurveyDetail,
45
|     | 表        | CFShipSurveyDetail_HF                               |     |     |
| --- | -------- | --------------------------------------------------- | --- | --- |
|     | 切花高朵數出貨預 | CFShipSurvey, CFShipSurveyMap, CFShipSurveyDetail,  |     |     |
46
|     | 估表  | CFShipSurveyDetail_HF  |     |     |
| --- | --- | ---------------------- | --- | --- |
47  盆花來梗統計表  PPStemSurvey, PPStemSurveyMap, PPStemSurveyDetail
盆花打荳統計表
| 48  |     | PPBudSurvey, PPBudSurveyMap, PPBudSurveyDetail  |     |     |
| --- | --- | ----------------------------------------------- | --- | --- |

| 機密等級：內部文件  |     |     | 版權所有©2020凌誠科技股份有限公司  |     |
| ---------- | --- | --- | -------------------- | --- |
391/391