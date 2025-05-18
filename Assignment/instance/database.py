# Current setup of the database USING SSMS QUERY

'''

CREATE DATABASE diary_app;
GO

USE diary_app;
GO

CREATE TABLE Users (
	User_ID INT IDENTITY(1,1) PRIMARY KEY,
	Username NVARCHAR(50) NOT NULL UNIQUE,
	Email NVARCHAR(50) NOT NULL UNIQUE,
	Password NVARCHAR(255) NOT NULL,
	Created_At DATETIME DEFAULT GETDATE()
);

CREATE TABLE Entries (
	Entry_ID INT IDENTITY(1,1) PRIMARY KEY,
	User_ID INT NOT NULL,
	Content TEXT NOT NULL,
	Created_At DATETIME DEFAULT GETDATE(),

	CONSTRAINT FK_UserEntries FOREIGN KEY (User_ID)
		REFERENCES Users(User_ID)
		ON DELETE CASCADE
);

'''



# Diaryblock role user creation 

'''
-- At server level
USE master;
CREATE LOGIN diaryblockuser WITH PASSWORD = 'D1aryBl0ck01';

-- In the diary_app database
USE diary_app;
CREATE USER diaryblockuser FOR LOGIN diaryblockuser;

-- Create role and grant permissions
CREATE ROLE diaryblockwriter;
GRANT SELECT, INSERT, UPDATE, DELETE ON Users TO diaryblockwriter;
GRANT SELECT, INSERT, UPDATE, DELETE ON Entries TO diaryblockwriter;

-- Add user to role
EXEC sp_addrolemember 'diaryblockwriter', 'diaryblockuser';

'''



# Creating audit logs for CRUD operations done 
'''
CREATE SERVER AUDIT DiaryBlockAudit
TO FILE (
    FILEPATH = 'C:\auditfiles\audit',
    MAXSIZE = 10 MB,
    MAX_FILES = 100,
    RESERVE_DISK_SPACE = OFF
)
WITH (
    QUEUE_DELAY = 1000,
    ON_FAILURE = CONTINUE
);

ALTER SERVER AUDIT DiaryBlockAudit
WITH (STATE = ON);

USE diary_app;
GO

CREATE DATABASE AUDIT SPECIFICATION AuditDiaryBlockActivity
FOR SERVER AUDIT DiaryBlockAudit
ADD (SELECT, INSERT, DELETE, UPDATE ON DATABASE::[diary_app] BY [diaryblockuser])
WITH (STATE = ON);

'''



# View the logs for CRUD operations done 
'''
SELECT *
FROM sys.fn_get_audit_file('C:\auditfiles\audit\*.sqlaudit', DEFAULT, DEFAULT);

'''



# Stop auditing the logs 
'''
ALTER DATABASE AUDIT SPECIFICATION AuditDiaryBlockActivity WITH (STATE = OFF);
ALTER SERVER AUDIT DiaryBlockAudit WITH (STATE = OFF);

'''



# Drop the audits when wanna reset
'''
DROP DATABASE AUDIT SPECIFICATION AuditDiaryBlockActivity;
DROP SERVER AUDIT DiaryBlockAudit;

'''



# Drop tables when wanna reset 

'''
DROP Table diary_app.dbo.Entries
DROP Table diary_app.dbo.Users

'''



# Drop diary_app db user and roles when wanna reset 

'''
USE diary_app;
GO

DROP USER diaryblockuser;

DROP ROLE diaryblockwriter;
'''