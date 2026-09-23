/****** Object:  Table [dbo].[IT_KB_Graph]  ******/

CREATE TABLE [dbo].[IT_KB_Graph](
    [RowID] BIGINT IDENTITY(1,1) PRIMARY KEY,

    -- 來源文件：對應 IT_KB_Document.DocID
    [DocID] BIGINT NOT NULL,

    -- 文本分段後的 chunk 編號
    [ChunkID] INT NOT NULL,

    -- chunk 原文：GraphRAG 回答一定需要
    [ChunkText] NVARCHAR(MAX) NOT NULL,

    -- Embedding：該 chunk 的向量（float32[] → VARBINARY）
    -- 若為三元組 row，此欄位為 NULL
    [Embedding] VARBINARY(MAX) NULL,

    -- 三元組（若為 embedding row，則皆為 NULL）
    [Entity1] NVARCHAR(400) NULL,
    [Relation] NVARCHAR(200) NULL,
    [Entity2] NVARCHAR(400) NULL,

    -- 三元組信心值（可選）
    [Confidence] FLOAT NULL,

    [CreatedAt] DATETIME2(7) NOT NULL DEFAULT SYSUTCDATETIME(),

    CONSTRAINT [FK_KB_Graph_Doc]
        FOREIGN KEY ([DocID]) REFERENCES [dbo].[IT_KB_Document]([DocID])
);
GO

-- 查詢用索引
CREATE INDEX [IX_KB_Graph_DocID]
ON [dbo].[IT_KB_Graph]([DocID]);

CREATE INDEX [IX_KB_Graph_ChunkID]
ON [dbo].[IT_KB_Graph]([ChunkID]);

-- GraphRAG 三元組搜尋常用索引
CREATE INDEX [IX_KB_Graph_Entity1]
ON [dbo].[IT_KB_Graph]([Entity1]);

CREATE INDEX [IX_KB_Graph_Entity2]
ON [dbo].[IT_KB_Graph]([Entity2]);

CREATE INDEX [IX_KB_Graph_Relation]
ON [dbo].[IT_KB_Graph]([Relation]);
GO
--commit