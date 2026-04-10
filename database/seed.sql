-- =====================================================
-- Clinify - Sample Data
-- =====================================================

\c clinic_management;

INSERT INTO "USER" (First_Name, Last_Name, Email, Phone, Password_Hash, Role) VALUES
('Alex',     'Johnson',  'alex.johnson@email.com',  '4031111111', 'hash1', 'patient'),
('Sarah',    'Lee',      'sarah.lee@email.com',     '4032222222', 'hash2', 'patient'),
('Michael',  'Brown',    'michael.brown@email.com', '4033333333', 'hash3', 'patient'),
('Rose',     'Smith',    'rose.smith@email.com',    '4034444444', 'hash4', 'doctor'),
('James',    'Wilson',   'james.wilson@email.com',  '4035555555', 'hash5', 'doctor'),
('Sara',     'Admin',    'sara.admin@email.com',    '4036666666', 'hash6', 'admin');

INSERT INTO PATIENT (Patient_ID, Date_Of_Birth, Gender, Address, Emergency_Contact_Name, Emergency_Contact_Phone) VALUES
(1, '1995-03-10', 'Male',   '123 Main St, Calgary',   'Mary Johnson', '4039991111'),
(2, '1988-07-22', 'Female', '456 Oak Ave, Calgary',   'Tom Lee',      '4039992222'),
(3, '2000-11-05', 'Male',   '789 Pine Rd, Calgary',   'Lisa Brown',   '4039993333');

INSERT INTO DOCTOR (Doctor_ID, Specialty, License_Number) VALUES
(4, 'Family Medicine', 'LIC10001'),
(5, 'Cardiology',      'LIC10002');

INSERT INTO ADMIN (Admin_ID) VALUES (6);

INSERT INTO MEDICAL_RECORD (Patient_ID, Record_Number) VALUES
(1, 1),
(2, 1),
(3, 1);

INSERT INTO AVAILABILITY (Doctor_ID, Day_Of_Week, Start_Time, End_Time) VALUES
(4, 'Monday',    '09:00:00', '12:00:00'),
(4, 'Wednesday', '13:00:00', '17:00:00'),
(4, 'Friday',    '09:00:00', '12:00:00'),
(5, 'Tuesday',   '10:00:00', '14:00:00'),
(5, 'Thursday',  '13:00:00', '17:00:00');

INSERT INTO APPOINTMENT (Appointment_Date, Appointment_Time, Status, Reason, Patient_ID, Doctor_ID, Admin_ID) VALUES
('2026-04-14', '09:00:00', 'Scheduled',  'Routine checkup',    1, 4, 6),
('2026-04-14', '10:00:00', 'Scheduled',  'Chest pain',         2, 5, 6),
('2026-03-20', '09:30:00', 'Completed',  'Flu symptoms',       3, 4, 6),
('2026-03-15', '11:00:00', 'Cancelled',  'Back pain',          1, 5, 6);

INSERT INTO VISIT (Appointment_ID, Patient_ID, Record_Number, Diagnosis, Vitals, Visit_Notes, Visit_Date) VALUES
(3, 3, 1, 'Influenza', 'BP 118/76, Temp 38.5C', 'Prescribed rest and fluids.', '2026-03-20');

INSERT INTO MEDICATION (Medication_Name, Description, Dosage_Form) VALUES
('Acetaminophen', 'Pain reliever and fever reducer', '500mg tablet'),
('Amoxicillin',   'Antibiotic for bacterial infections', '250mg capsule'),
('Cough Syrup',   'Relief for cough symptoms', '50ml syrup'),
('Ibuprofen',     'Anti-inflammatory pain reliever', '400mg tablet');

INSERT INTO PRESCRIPTION (Visit_ID, Doctor_ID, Issue_Date) VALUES
(3, 4, '2026-03-20');

INSERT INTO CONTAINS (Prescription_ID, Medication_ID, Frequency, Duration) VALUES
(1, 1, 'Twice daily', '5 days'),
(1, 3, 'Once daily',  '3 days');