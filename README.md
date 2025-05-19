# CCS6344 Database and Cloud Security Assignment
# DiaryBlock

DiaryBlock is a simple Flask-based diary web application that is secure and user-friendly developed as part of the **Database and Cloud Security CCS6344** assignment. The project focuses on demonstrating secure practices in web development and database interactions

## Group 33
## Team Members

|Name | Student ID |
|-------------------|----|
|Uwais bin Mohamed Yusof | 1211103213 |
|Muhamad Syamil Imran Bin Mohd Mansor | 1221303708 |
|Jahed, Fahad Bin | 1201303049 |

## Lecturer
Dr. Navaneethan A/L C. Arjuman

## Submission Date
19th May 2025

## Features

- Secure user registration and login
- Password hashing with `bcrypt`
- SQL Server database integration using `pyodbc`
- Session-based authentication
- CRUD operations for diary entries
- Secure account deletion
- Protection against unauthorized access

## Tech Stack

- Python 3
- Flask
- SQL Server
- pyodbc
- bcrypt
- HTML (Jinja2 templates)

## Requirements

- Python 3.7+
- pip (Python package installer)
- Microsoft SQL 
- ODBC 18

## Installation
To run this project locally, follow these steps:

1. **Clone the repository**
   ```bash
   git clone https://github.com/wais4u/CCS6344
   cd CCS6344/Assignment
2. **Set up a virtual environment (optional but recommended)**
    ```bash
    python -3 -m venv venv
    venv\Scripts\activate
    pip install flask
3. **Install dependencies**
    ```bash
    pip install -r requirements.txt
4. **Configure your database**

    Use queries contained in this repository under CCS6344/Assignment/instance/database.py to setup your database
    Ensure you have a SQL Server instance running with the following:
    ```bash
    Database: diary_app
    Tables: 
    Users: User_ID (PK), Username, Email, Password
    Entries: Entry_ID (PK), User_ID (FK), Content, Created_At
5. **Run the application**
    ```bash
    cd diaryblock
    flask --app app run
This project is developed for educational purpose as part of CCS6344 Database and Cloud Security Assignment
