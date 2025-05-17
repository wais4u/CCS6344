# Current setup of the database USING SSMS QUERY

'''

CREATE DATABASE diary_app;
GO

USE diary_app;
GO

CREATE TABLE Users (
	User_ID INT IDENTITY(1,1) PRIMARY KEY,
	Username VARCHAR(50) NOT NULL UNIQUE,
	Email VARCHAR(50) NOT NULL UNIQUE,
	Password VARCHAR(255) NOT NULL,
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
CREATE LOGIN diaryblockuser WITH PASSWORD = 'D1aryBlock01';

-- In your target database
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