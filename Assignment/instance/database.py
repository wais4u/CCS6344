# Current setup of the database USING SSMS QUERY

'''

CREATE DATABASE diary_app;
GO

USE diary_app;
GO

CREATE TABLE Users (
    username NVARCHAR(50) NOT NULL UNIQUE,
    password NVARCHAR(50) NOT NULL
)

'''