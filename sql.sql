CREATE DATABASE ApartmentManagement;
USE ApartmentManagement;

CREATE TABLE RentAlerts (
    AlertID INT AUTO_INCREMENT PRIMARY KEY,
    ApartmentID INT,
    TotalDueAmount DECIMAL(10,2),
    AlertDate DATE,
    FOREIGN KEY (ApartmentID) REFERENCES Apartments(ApartmentID)
);

CREATE TABLE Rent (
    RentID INT AUTO_INCREMENT PRIMARY KEY,
    Amount DECIMAL(10, 2) NOT NULL,
    DueDate DATE NOT NULL,
    Status ENUM('Paid', 'Due') NOT NULL,
    ApartmentID INT,
    TenantID INT,
    FOREIGN KEY (ApartmentID) REFERENCES Apartments(ApartmentID),
    FOREIGN KEY (TenantID) REFERENCES Tenants(TenantID)
    );

CREATE TABLE MaintenanceRequests (
    RequestID INT PRIMARY KEY AUTO_INCREMENT,
    ApartmentID INT,
    RequestDescription TEXT,
    RequestDate DATE,
    Status ENUM('Pending', 'Completed') DEFAULT 'Pending',
    -- Add other columns as needed
    FOREIGN KEY (ApartmentID) REFERENCES Apartments(ApartmentID)
);

Create Trigger_Log table
CREATE TABLE IF NOT EXISTS Trigger_Log (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    log_message VARCHAR(255),
    log_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

DELIMITER //

CREATE TRIGGER update_tenants_after_apartment_update
AFTER UPDATE ON Apartments
FOR EACH ROW
BEGIN
    -- Add logging for Apartments
    INSERT INTO Trigger_Log (log_message) VALUES ('Trigger executed for updating Apartments');

    -- Update Tenants based on the changes in Apartments
    UPDATE Tenants
    SET ApartmentID = NEW.ApartmentID
    WHERE TenantID = NEW.TenantID;

    -- Add logging for Owners
    INSERT INTO Trigger_Log (log_message) VALUES ('Trigger executed for updating Owners');

    -- Update Owners based on the changes in Apartments
    UPDATE Owners
    SET ApartmentID = NEW.ApartmentID
    WHERE OwnerID = NEW.OwnerID;
END //

DELIMITER ;

ALTER TABLE Tenants
ADD CONSTRAINT tenants_ibfk_1
FOREIGN KEY (ApartmentID)
REFERENCES Apartments(ApartmentID)
ON DELETE SET NULL
ON UPDATE CASCADE;
ALTER TABLE Owners
ADD CONSTRAINT owners_ibfk_1
FOREIGN KEY (ApartmentID)
REFERENCES Apartments(ApartmentID)
ON DELETE SET NULL
ON UPDATE CASCADE;
DELIMITER //

CREATE TRIGGER delete_apartment_trigger
AFTER DELETE ON Apartments
FOR EACH ROW
BEGIN
    -- Add logging
    INSERT INTO Trigger_Log (log_message) VALUES ('Apartment deleted');

    -- Update Tenant's ApartmentID to NULL
    UPDATE Tenants
    SET ApartmentID = NULL
    WHERE TenantID = OLD.TenantID;

    -- Update Owner's ApartmentID to NULL
    UPDATE Owners
    SET ApartmentID = NULL
    WHERE OwnerID = OLD.OwnerID;

    -- You can add more logic based on your requirements

END //

DELIMITER ;

CREATE TABLE IF NOT EXISTS Users (
         UserID INT AUTO_INCREMENT PRIMARY KEY,
         Username VARCHAR(255) UNIQUE NOT NULL,
         PasswordHash CHAR(64) NOT NULL, -- SHA-256 hash produces a 64-character string
         Email VARCHAR(255),
         Role VARCHAR(50), -- Example of a column for user roles if needed
         CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
     );

INSERT INTO Tenants (FirstName, LastName, MovingDate, ContactInfo)
     VALUES ('Emily', 'Davis', '2023-03-10', 'emily@example.com'),
            ('Michael', 'Brown', '2023-04-15', 'michael@example.com');

INSERT INTO LeaseRent (LeaseStartDate, LeaseEndDate, Rent, ApartmentID)
     VALUES ('2023-01-01', '2023-12-31', 1200.00, 1),
            ('2023-02-01', '2023-11-30', 1100.00, 2);

INSERT INTO Owners (FirstName, LastName, ContactInfo)
     VALUES ('Jane', 'Smith', 'jane@example.com');
INSERT INTO Apartments (ApartmentNumber, RentAmount, NumberOfRooms) VALUES ('101', 1000.00, 2);
INSERT INTO Apartments (ApartmentNumber, BuildingID, RentAmount, NumberOfRooms)
     VALUES
         ('101', 1, 1000.00, 2),
         ('102', 1, 1200.00, 3),
         ('201', 2, 800.00, 1);

INSERT INTO MaintenanceRequest (Description, StaffID, ApartmentID, Status)
	VALUES
         ('Leaky faucet', 1, 1, 'Open'),
         ('Broken window', 2, 2, 'Open');

 INSERT INTO MaintenanceStaff (FirstName, LastName, ContactInfo)
     VALUES
         ('Mark', 'Anderson', 'mark@example.com'),
         ('Emily', 'Davis', 'emily@example.com');

INSERT INTO Buildings (OwnerID, TotalFloors, Address)
     VALUES (1, 5, '123 Main St');
INSERT INTO Owners (FirstName, LastName, ContactInfo)
     VALUES ('John', 'Doe', 'john.doe@example.com');

CREATE TABLE IF NOT EXISTS LeaseRent (
         TenantID INT,
         OwnerID INT,
         LeaseStartDate DATE,
         LeaseEndDate DATE,
         Rent DECIMAL(10, 2),
         ApartmentID INT,
         PRIMARY KEY (TenantID, ApartmentID),
         FOREIGN KEY (TenantID) REFERENCES Tenants(TenantID),
         FOREIGN KEY (OwnerID) REFERENCES Owners(OwnerID),
         FOREIGN KEY (ApartmentID) REFERENCES Apartments(ApartmentID)
     );

 CREATE TABLE IF NOT EXISTS MaintenanceRequest (
         RequestID INT AUTO_INCREMENT PRIMARY KEY,
         Description VARCHAR(255),
         StaffID INT,
         ApartmentID INT,
         Status VARCHAR(50),
         FOREIGN KEY (StaffID) REFERENCES MaintenanceStaff(StaffID),
         FOREIGN KEY (ApartmentID) REFERENCES Apartments(ApartmentID)
     );

Create the MaintenanceRequest table with auto-incremented RequestID
Query OK, 0 rows affected (0.00 sec)
CREATE TABLE IF NOT EXISTS MaintenanceStaff (
         StaffID INT AUTO_INCREMENT PRIMARY KEY,
         FirstName VARCHAR(255),
         LastName VARCHAR(255),
         ContactInfo VARCHAR(255)
     );

 CREATE TABLE IF NOT EXISTS Tenants (
         TenantID INT AUTO_INCREMENT PRIMARY KEY,
         FirstName VARCHAR(255),
         LastName VARCHAR(255),
         MovingDate DATE,
         ContactInfo VARCHAR(255)
     );

CREATE TABLE IF NOT EXISTS Apartments (
         ApartmentID INT AUTO_INCREMENT PRIMARY KEY,
         ApartmentNumber VARCHAR(50),
         OwnerID INT, -- Owner of the apartment
         BuildingID INT, -- Building in which the apartment is located
         RentAmount DECIMAL(10, 2),
         NumberOfRooms INT,
         FOREIGN KEY (OwnerID) REFERENCES Owners(OwnerID),
         FOREIGN KEY (BuildingID) REFERENCES Buildings(BuildingID)
     );


CREATE TABLE IF NOT EXISTS Buildings (
         BuildingID INT AUTO_INCREMENT PRIMARY KEY,
         TotalFloors INT,
         Address VARCHAR(255)
     );


CREATE TABLE IF NOT EXISTS Owners (
         OwnerID INT AUTO_INCREMENT PRIMARY KEY,
         FirstName VARCHAR(255),
         LastName VARCHAR(255),
         ContactInfo VARCHAR(255)
     );






