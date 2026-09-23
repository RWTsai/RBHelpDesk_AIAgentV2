/* ============================================================
   RBIT 改版 V2（To-Be）新增資料表
   - 文件 GraphRAG：SourceDoc / Chunk / Entity / Relation / EntityChunk
   - 雲端同步進度：SyncState
   - Agent 執行紀錄：AgentTrace
   既有 IT_KB_Document / IT_KB_Graph / IT_KB_UserMemory 不動。
   可重複執行（已存在的表會略過）。
   ============================================================ */

-- 1) 文件來源
IF OBJECT_ID('dbo.IT_KB_SourceDoc', 'U') IS NULL
BEGIN
    CREATE TABLE dbo.IT_KB_SourceDoc (
        DocumentID   BIGINT IDENTITY(1,1) PRIMARY KEY,
        FileName     NVARCHAR(500)  NOT NULL,
        SourceType   NVARCHAR(20)   NOT NULL,          -- upload / folder / gdrive / onedrive
        SourceRef    NVARCHAR(1000) NULL,              -- 資料夾相對路徑 / Drive fileId / OneDrive driveId:itemId
        SourceUrl    NVARCHAR(2000) NULL,              -- 雲端檔案網頁連結（回覆引用用）
        FileContent  VARBINARY(MAX) NULL,              -- 後台上傳的原檔（其他來源不存）
        FileHash     NVARCHAR(128)  NULL,
        Status       NVARCHAR(20)   NOT NULL DEFAULT 'Pending',  -- Pending / Processing / Done / Failed / Deleting
        ErrorMsg     NVARCHAR(MAX)  NULL,
        ChunkCount   INT            NOT NULL DEFAULT 0,
        UploadedBy   NVARCHAR(200)  NULL,
        CreatedAt    DATETIME2(7)   NOT NULL DEFAULT SYSUTCDATETIME(),
        UpdatedAt    DATETIME2(7)   NOT NULL DEFAULT SYSUTCDATETIME()
    );
    CREATE INDEX IX_KB_SourceDoc_Status ON dbo.IT_KB_SourceDoc(Status);
    CREATE INDEX IX_KB_SourceDoc_Source ON dbo.IT_KB_SourceDoc(SourceType) INCLUDE (SourceRef);
END
GO

-- 2) 文件分塊
IF OBJECT_ID('dbo.IT_KB_Chunk', 'U') IS NULL
BEGIN
    CREATE TABLE dbo.IT_KB_Chunk (
        ChunkID      BIGINT IDENTITY(1,1) PRIMARY KEY,
        DocumentID   BIGINT         NOT NULL,
        Seq          INT            NOT NULL,
        SectionPath  NVARCHAR(1000) NULL,              -- 標題階層 / 頁碼 / 工作表名
        ChunkText    NVARCHAR(MAX)  NOT NULL,
        Embedding    VARBINARY(MAX) NULL,              -- float32[]，與 IT_KB_Graph 相同格式
        TokenCount   INT            NULL,
        CreatedAt    DATETIME2(7)   NOT NULL DEFAULT SYSUTCDATETIME(),
        CONSTRAINT FK_KB_Chunk_Doc FOREIGN KEY (DocumentID) REFERENCES dbo.IT_KB_SourceDoc(DocumentID)
    );
    CREATE INDEX IX_KB_Chunk_Doc ON dbo.IT_KB_Chunk(DocumentID);
END
GO

-- 3) 實體（跨文件共用，以 NormName 合併）
IF OBJECT_ID('dbo.IT_KB_Entity', 'U') IS NULL
BEGIN
    CREATE TABLE dbo.IT_KB_Entity (
        EntityID     BIGINT IDENTITY(1,1) PRIMARY KEY,
        Name         NVARCHAR(400)  NOT NULL,
        NormName     NVARCHAR(400)  NOT NULL,
        EntityType   NVARCHAR(50)   NULL,
        Description  NVARCHAR(MAX)  NULL,
        Embedding    VARBINARY(MAX) NULL,
        UpdatedAt    DATETIME2(7)   NOT NULL DEFAULT SYSUTCDATETIME()
    );
    CREATE UNIQUE INDEX UX_KB_Entity_NormName ON dbo.IT_KB_Entity(NormName);
END
GO

-- 4) 關係（屬於某份文件的某個 chunk）
IF OBJECT_ID('dbo.IT_KB_Relation', 'U') IS NULL
BEGIN
    CREATE TABLE dbo.IT_KB_Relation (
        RelationID   BIGINT IDENTITY(1,1) PRIMARY KEY,
        SrcEntityID  BIGINT         NOT NULL,
        DstEntityID  BIGINT         NOT NULL,
        Relation     NVARCHAR(200)  NOT NULL,
        Description  NVARCHAR(1000) NULL,
        Weight       FLOAT          NOT NULL DEFAULT 1,
        ChunkID      BIGINT         NULL,
        DocumentID   BIGINT         NOT NULL
    );
    CREATE INDEX IX_KB_Relation_Src ON dbo.IT_KB_Relation(SrcEntityID);
    CREATE INDEX IX_KB_Relation_Dst ON dbo.IT_KB_Relation(DstEntityID);
    CREATE INDEX IX_KB_Relation_Doc ON dbo.IT_KB_Relation(DocumentID);
END
GO

-- 5) 實體出現在哪些 chunk
IF OBJECT_ID('dbo.IT_KB_EntityChunk', 'U') IS NULL
BEGIN
    CREATE TABLE dbo.IT_KB_EntityChunk (
        EntityID     BIGINT NOT NULL,
        ChunkID      BIGINT NOT NULL,
        DocumentID   BIGINT NOT NULL,
        CONSTRAINT PK_KB_EntityChunk PRIMARY KEY (EntityID, ChunkID)
    );
    CREATE INDEX IX_KB_EntityChunk_Doc ON dbo.IT_KB_EntityChunk(DocumentID);
    CREATE INDEX IX_KB_EntityChunk_Chunk ON dbo.IT_KB_EntityChunk(ChunkID);
END
GO

-- 6) 雲端來源同步進度（OneDrive deltaLink、GDrive 最後同步時間）
IF OBJECT_ID('dbo.IT_KB_SyncState', 'U') IS NULL
BEGIN
    CREATE TABLE dbo.IT_KB_SyncState (
        SourceKey    NVARCHAR(200)  NOT NULL PRIMARY KEY,   -- onedrive:<hash> / gdrive:<folderId>
        DeltaLink    NVARCHAR(MAX)  NULL,
        LastSyncAt   DATETIME2(7)   NULL,
        LastError    NVARCHAR(MAX)  NULL
    );
END
GO

-- 7) Agent 執行紀錄
IF OBJECT_ID('dbo.IT_KB_AgentTrace', 'U') IS NULL
BEGIN
    CREATE TABLE dbo.IT_KB_AgentTrace (
        TraceID      BIGINT IDENTITY(1,1) PRIMARY KEY,
        UserID       NVARCHAR(100)  NULL,
        Question     NVARCHAR(MAX)  NULL,
        StepsJson    NVARCHAR(MAX)  NULL,   -- 每個階段：類型、工具、參數、結果摘要、耗時
        Verdict      NVARCHAR(30)   NULL,   -- fast_path / pass / pass_skip / needs_more / fail / error
        Answer       NVARCHAR(MAX)  NULL,
        LatencyMs    INT            NULL,
        CreatedAt    DATETIME2(7)   NOT NULL DEFAULT SYSUTCDATETIME()
    );
    CREATE INDEX IX_KB_AgentTrace_Created ON dbo.IT_KB_AgentTrace(CreatedAt);
END
GO

/* ------------------------------------------------------------
   唯讀帳號範例（請 DBA 依實際白名單調整，並與 .env 的 SQL_ALLOWED_TABLES 一致）
   ------------------------------------------------------------
CREATE LOGIN rbit_agent_ro WITH PASSWORD = '請改成強密碼';
CREATE USER  rbit_agent_ro FOR LOGIN rbit_agent_ro;
GRANT SELECT ON dbo.<允許查詢的表或檢視> TO rbit_agent_ro;
-- 不要加入 db_datareader，只逐表授權
------------------------------------------------------------ */
