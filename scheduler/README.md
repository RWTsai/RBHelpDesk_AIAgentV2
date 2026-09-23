# 文件匯入與同步規則（scheduler/ingest_docs.py）

```bash
python scheduler/ingest_docs.py --loop      # 常駐，每 INGEST_INTERVAL_SEC 秒（預設 300）跑一輪
python scheduler/ingest_docs.py --once      # 只跑一輪
python scheduler/ingest_docs.py --doc 12    # 只重跑指定文件
```

一輪的順序：**收件（資料夾 → Google Drive → OneDrive）→ 處理刪除 → 處理待匯入**。
收件只負責比對「有哪些檔案、變了沒」，真正的解析、分塊、抽圖譜、向量化都在最後一步。

---

## 一、四種來源

| 來源 | `SourceType` | 認定同一份文件的依據（`SourceRef`） | 設定 |
|---|---|---|---|
| 後台上傳 | `upload` | 檔名（原檔存在資料庫裡） | `appsettings.json` 的 `DocUpload` |
| 本機資料夾 | `folder` | 相對路徑，例如 `SOP/請假.docx` | `.env` `DOC_DROP_FOLDER` |
| Google Drive | `gdrive` | Drive 的 file id | `.env` `GDRIVE_SA_JSON`、`GDRIVE_FOLDER_IDS` |
| OneDrive／SharePoint | `onedrive` | `driveId:itemId` | `.env` `M365_*`、`ONEDRIVE_SHARE_URLS` |

副檔名不在 `DOC_ALLOWED_EXT`（預設 pdf/docx/xlsx/pptx/md/txt）的一律跳過；資料夾來源另外會略過 Office 暫存檔（`~$` 開頭）。
`DOC_DROP_FOLDER` 是**跑匯入程式那台主機**看得到的路徑，和 IIS 無關。

---

## 二、已同步的文件會再同步嗎？

**不會。**每一輪都會重新列出來源端的檔案，但只比對指紋，指紋沒變就完全不動它——
不下載、不解析、不呼叫 OpenAI。所以放著幾百份文件每 5 分鐘跑一輪也不會產生費用。

各來源的「指紋」：

| 來源 | 指紋 | 什麼情況會重新索引 |
|---|---|---|
| 後台上傳 | 檔案內容的 SHA256 | 上傳同名但內容不同的檔案 |
| 資料夾 | 檔案內容的 SHA256 | 檔案內容被改過 |
| Google Drive | `md5Checksum`；Google 文件／試算表／簡報沒有 md5，改用 `modifiedTime` | 內容變更；Google 原生檔只要被編輯過就算 |
| OneDrive | `quickXorHash` → `sha256Hash` → `cTag` → `eTag`（取第一個有值的） | 內容變更 |

比對結果只有三種：

- **沒看過的檔案** → 新增一筆，狀態 `Pending`，這一輪就會解析。
- **指紋變了** → 狀態改回 `Pending`，重新解析。舊的 chunk／關係會在同一個交易裡先刪掉再寫入新的，不會留下半新半舊的內容。
- **指紋一樣** → 只更新檔名與原始連結（欄位有變才更新），**不重新索引**。

### 改名與搬移

| 動作 | 資料夾 | Google Drive／OneDrive |
|---|---|---|
| 改檔名 | 路徑變了 → 視為舊的刪除 + 新的一份，會重新索引 | id 沒變 → 只更新顯示的檔名，**不重新索引** |
| 在同步範圍內搬移 | 同上，重新索引 | id 沒變，不重新索引 |
| 搬出同步範圍 | 視為刪除 | 視為刪除 |

雲端來源是用 id 認人，所以改名搬移都很便宜；資料夾來源是用路徑認人，整理目錄結構會造成重新索引（結果正確，只是多花時間與 API 費用）。

---

## 三、刪除的規則

來源端的檔案不見了，對應的知識會一起移除：

1. 同步時發現檔案消失 → 該筆標成 `Deleting`
2. 同一輪的「處理刪除」階段 → 在一個交易裡刪掉它的 chunk、關係、實體對應，再刪掉文件本身
3. 最後清掉沒有被任何文件引用的孤兒實體

各來源怎麼判斷「消失了」：

- **資料夾**：這一輪掃到的路徑 vs 資料庫裡的紀錄，少掉的就是被刪了。
- **Google Drive**：**所有**設定的資料夾都成功列出來，才會判斷刪除。只要有一個資料夾出錯（網路、權限），這一輪就完全不刪，避免暫時性失敗造成誤刪。
- **OneDrive**：delta 查詢會直接告訴我們哪些項目被刪除。退回完整列表模式時（見下），才用清單比對。
- **後台上傳**：只有在後台按「刪除」才會標成 `Deleting`，同步程式不會碰它。

**防呆**：資料夾路徑不存在時只記錄錯誤、跳過整個資料夾來源，不會刪東西；路徑存在但一個檔案都掃不到、而先前有文件時，也會拒絕刪除並在 log 提醒（網路磁碟掉線或權限被改的典型徵兆）。

---

## 四、刪掉之後再放回去

分兩種情況，差別在「有沒有被處理掉」：

**還沒跑到刪除階段就放回去**（例如檔案剛刪掉就後悔，同一輪或下一輪之前放回來）
→ 程式看到這筆是 `Deleting` 狀態，會直接改回 `Pending` **重新索引一次**。
就算內容一模一樣也會重做，因為那時候知識可能已經被刪了一半，重做才保險。

**已經刪乾淨之後再放回去**
→ 資料庫裡那筆已經整個消失，所以是一份**全新的文件**，會拿到新的 `DocumentID`，從頭解析一次。

放回去時能不能認回原本那筆，看 id 對不對得上：

| 來源 | 刪掉再放回 | 認得出來嗎 |
|---|---|---|
| 資料夾 | 放回**同一個相對路徑** | 認得（同一個 `SourceRef`） |
| 資料夾 | 放到不同子目錄 | 認不得，算新文件 |
| Google Drive／OneDrive | 從**資源回收筒還原** | 認得（id 沒變） |
| Google Drive／OneDrive | 重新上傳一份 | 認不得，id 是新的，算新文件 |

不論哪一種，最後的知識內容都一樣正確，差別只在 `DocumentID` 會不會換、以及要不要重新花一次解析成本。

---

## 五、失敗與重試

- 解析或抽取失敗 → 狀態 `Failed`，錯誤訊息寫進 `ErrorMsg`（後台文件管理頁看得到）。金鑰類內容會先遮蔽。
- **`Failed` 不會自動重試**，避免壞檔每 5 分鐘燒一次 API。要重試就在後台按「重新索引」，或把狀態改回 `Pending`。
- 掃描版 PDF（純圖片、沒有文字層）解析不出文字，會直接判定失敗。
- 卡在 `Processing` 超過一小時的（程式中途被砍），下一輪啟動時會自動放回 `Pending`。
- 某個來源同步失敗不影響其他來源，錯誤記在 `IT_KB_SyncState.LastError`。

## 六、Google Drive 怎麼設定

用 service account（服務帳戶）存取，不需要任何人登入授權，適合常駐程式。

### 1. 建立 service account 並下載金鑰

1. 到 [Google Cloud Console](https://console.cloud.google.com/) 建立或選一個專案。
2. 「API 和服務」→「程式庫」→ 搜尋 **Google Drive API** → 啟用。
3. 「API 和服務」→「憑證」→「建立憑證」→ **服務帳戶**，名稱隨意（例如 `rbit-doc-sync`），角色可以不給（它只靠資料夾分享取得權限）。
4. 點進剛建立的服務帳戶 →「金鑰」→「新增金鑰」→ **JSON** → 下載。
5. 把這個 JSON 檔放到**跑匯入程式那台主機**，例如 `D:\keys\rbit-gdrive.json`，
   權限設成只有執行匯入程式的帳號讀得到。這個檔案等同密碼，不要放進版控、不要放在網站目錄下。
6. 記下服務帳戶的 email，長得像 `rbit-doc-sync@專案名.iam.gserviceaccount.com`
   （JSON 裡的 `client_email` 欄位）。

```ini
GDRIVE_SA_JSON=D:\keys\rbit-gdrive.json
```

路徑照 Windows 寫法即可，`.env` 裡不用加引號、也不用跳脫反斜線。

### 2. 把資料夾分享給服務帳戶

服務帳戶是一個獨立的「人」，預設看不到公司任何檔案。到 Google Drive：

1. 在要同步的資料夾上按右鍵 →「共用」
2. 貼上服務帳戶的 email，權限選 **檢視者**（唯讀就夠）
3. 送出。不用等對方接受，服務帳戶不會收信也不需要同意

> 共用雲端硬碟（Shared Drive）也可以，把服務帳戶加成該雲端硬碟的成員即可。

### 3. 找出資料夾 ID

打開那個資料夾，網址列長這樣：

```
https://drive.google.com/drive/folders/1A2b3C4dEfGhIjKlMnOpQrStUvWxYz
                                       └──────── 這一段就是 ID ────────┘
```

多個資料夾用逗號分隔，不要有空白：

```ini
GDRIVE_FOLDER_IDS=1A2b3C4dEfGhIjKlMnOpQrStUvWxYz,1ZzYy9Xx8Ww7Vv6Uu5Tt4Ss
```

子資料夾會自動一起掃，不用逐一列出。清空這個參數就停用 Google Drive 同步。

### 4. 確認

啟動時會印 `GDrive 同步: ON`（兩個參數都有值才會 ON），
跑 `python scheduler/ingest_docs.py --once` 看 log 有沒有出現「新文件（gdrive）」。

常見問題：

| 訊息 | 原因 |
|---|---|
| `找不到 GDRIVE_SA_JSON` | 路徑錯，或匯入程式的執行帳號讀不到那個檔 |
| `403 insufficientFilePermissions` | 資料夾沒分享給服務帳戶的 email |
| `404 File not found` | 資料夾 ID 抄錯，或抄到網址其他片段 |
| `Google Drive API has not been used...` | 專案沒有啟用 Drive API |
| 同步成功但一份文件都沒有 | 資料夾裡沒有 `DOC_ALLOWED_EXT` 允許的副檔名 |

Google 文件／試算表／簡報沒有實體檔案，會自動匯出成 docx／xlsx／pptx 再解析，
檔名會補上副檔名（例如「請假辦法」→「請假辦法.docx」）。

## 七、OneDrive 的兩種模式

- **delta（預設）**：第一次回傳全部，之後只回傳異動，最省。deltaLink 存在 `IT_KB_SyncState.DeltaLink`（`delta:` 開頭）。
- **完整列表**：部分 SharePoint／OneDrive for Business 環境的子資料夾不支援 delta，偵測到就自動改用這個模式，把完整清單存起來（`full:` 開頭）下次比對。
- deltaLink 過期（Graph 回 410）會自動重新完整同步一次，不用人工處理。
- `ONEDRIVE_RECURSIVE=off` 可只同步分享資料夾的第一層。
- 權限：client credentials 流程需要 **`Files.Read.All`** 應用程式權限並完成**管理員同意**，否則 Graph 回 403。
