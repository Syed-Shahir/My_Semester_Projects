-- Create the Bank_Management_System database
CREATE DATABASE IF NOT EXISTS Bank_Management_System;
USE Bank_Management_System;

-- Table for Registered Accounts
CREATE TABLE Registered_Accounts(
    User_Name CHAR(25) UNIQUE NOT NULL PRIMARY KEY,
    User_Password VARCHAR(25) NOT NULL,
    Verification_Code VARCHAR(10) NOT NULL
);

-- Table for Customer Personal Information
CREATE TABLE Customer_Personal_Info(
    Customer_ID INT AUTO_INCREMENT PRIMARY KEY,
    User_Name VARCHAR(25) UNIQUE NOT NULL, -- Unique username for each customer
    Customer_Name VARCHAR(25) NOT NULL, -- Customer's name
    Date_Of_Birth DATE, -- Date of birth (format: yyyy-mm-dd)
    Guardian_Name VARCHAR(25) NOT NULL, -- Guardian's name
    Permanent_Address VARCHAR(50) NOT NULL, -- Permanent address
    Secondary_Address VARCHAR(50), -- Secondary address (optional)
    Postal_Code VARCHAR(8), -- Postal code
    Email_ID VARCHAR(50) UNIQUE, -- Email address (format validation)
    Gender CHAR(6), -- Gender
    CNIC_Number VARCHAR(15) UNIQUE, -- CNIC number (format: 12345-1234567-1)
    CHECK (Customer_Name REGEXP '^[A-Za-z]+$'), -- Validates Customer_Name contains only alphabetic characters
    CHECK (Guardian_Name REGEXP '^[A-Za-z]+$'), -- Validates Guardian_Name contains only alphabetic characters
    CHECK (Email_ID REGEXP '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$'), -- Validates Email_ID format
    CHECK (CNIC_Number REGEXP '^[0-9]{5}-[0-9]{7}-[0-9]$'), -- Validates CNIC_Number format (12345-1234567-1)
    CHECK (Date_Of_Birth REGEXP '^[0-9]{4}-[0-9]{2}-[0-9]{2}$'), -- Validates Date_Of_Birth format (yyyy-mm-dd)
    FOREIGN KEY (User_Name) REFERENCES Registered_Accounts(User_Name) -- Foreign key reference to Registered_Accounts table
);

CREATE TABLE Account_Info(
    Account_No INT AUTO_INCREMENT PRIMARY KEY, -- Unique account number
    Customer_ID INT NOT NULL, -- Associated customer's ID
    Account_Type VARCHAR(10), -- Type of account
    Registration_Date DATE, -- Date of registration
    Activation_Date DATE, -- Date of activation
    Initial_Deposit BIGINT(10), -- Initial deposit amount
    Current_Balance BIGINT(20), -- Current balance
    CHECK (Activation_Date >= Registration_Date), -- Validates Activation_Date not earlier than Registration_Date
    FOREIGN KEY(Customer_ID) REFERENCES Customer_Personal_Info(Customer_ID) -- Foreign key reference to Customer_Personal_Info table
);
