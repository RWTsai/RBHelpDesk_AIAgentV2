USE [RBDev]
GO

/****** Object:  Table [dbo].[IT_KB_Document]    Script Date: 2025/11/17 ¤W¤È 11:18:37 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[IT_KB_Document](
	[DocID] [bigint] IDENTITY(1,1) NOT NULL,
	[Instruction] [nvarchar](max) NOT NULL,
	[InputText] [nvarchar](max) NULL,
	[OutputText] [nvarchar](max) NOT NULL,
	[SourceKey] [nvarchar](200) NULL,
	[CreatedAt] [datetime2](7) NULL,
	[UpdatedAt] [datetime2](7) NULL,
PRIMARY KEY CLUSTERED 
(
	[DocID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO

ALTER TABLE [dbo].[IT_KB_Document] ADD  DEFAULT (sysutcdatetime()) FOR [CreatedAt]
GO


