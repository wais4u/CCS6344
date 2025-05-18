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