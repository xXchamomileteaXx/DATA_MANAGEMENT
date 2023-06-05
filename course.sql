DROP database hospital;
CREATE DATABASE IF NOT EXISTS hospital;
USE hospital; 


FLUSH PRIVILEGES;

CREATE TABLE IF NOT EXISTS `Patient` (
  `PatientID` INT NOT NULL AUTO_INCREMENT,
  `Name` TEXT(50) NOT NULL,
  `Gender` ENUM('Мужской', 'Женский') NULL,
  `Address` TEXT(100) NULL,
  `Phone_number` TEXT(15) NULL,
  PRIMARY KEY (`PatientID`)
);

CREATE TABLE IF NOT EXISTS `Doctor` (
  `DoctorID` INT NOT NULL AUTO_INCREMENT,
  `Name` TEXT(50) NULL,
  `Specialty` TEXT(50) NULL,
  PRIMARY KEY (`DoctorID`)
);

CREATE TABLE IF NOT EXISTS `Medicine` (
  `MedicineID` INT NOT NULL AUTO_INCREMENT,
  `Name` TEXT(50) NULL,
  `Method_of_reception` TEXT(100) NULL,
  `Description` TEXT(100) NULL,
  `Side_effects` TEXT(100) NULL,
  PRIMARY KEY (`MedicineID`)
);

CREATE TABLE IF NOT EXISTS `Inspection` (
  `InspectionID` INT NOT NULL AUTO_INCREMENT,
  `Date` DATE NOT NULL,
  `Location` TEXT(50) NULL,
  `Symptoms` TEXT(100) NULL,
  `Diagnosis` TEXT(100) NULL,
  `Prescriptions` TEXT(100) NULL,
  `PatientID` INT NOT NULL,
  `DoctorID` INT NOT NULL,
  `MedicineID` INT NOT NULL,
  PRIMARY KEY (`InspectionID`),
  FOREIGN KEY (`PatientID`) REFERENCES `Patient`(`PatientID`),
  FOREIGN KEY (`DoctorID`) REFERENCES `Doctor`(`DoctorID`),
  FOREIGN KEY (`MedicineID`) REFERENCES `Medicine`(`MedicineID`)
);


CREATE TABLE IF NOT EXISTS `Patient_has_Medicine` (
  `PatientID` INT NOT NULL,
  `MedicineID` INT NOT NULL,
  `DoctorID` INT NOT NULL,
  PRIMARY KEY (`PatientID`, `MedicineID`, `DoctorID`),
  FOREIGN KEY (`MedicineID`) REFERENCES `Medicine`(`MedicineID`),
  FOREIGN KEY (`DoctorID`) REFERENCES `Doctor`(`DoctorID`),
   FOREIGN KEY (`PatientID`) REFERENCES `Patient`(`PatientID`)
);

-- Заполнение таблицы "Patient"
INSERT INTO `Patient` (`Name`, `Gender`, `Address`, `Phone_number`)
VALUES
('Иванов Иван', 'Мужской', 'ул. Ленина, д. 10', '555-12-34'),
('Петрова Александра', 'Женский', 'ул. Кирова, д. 5', '555-55-55'),
('Сидоров Василий', 'Мужской', 'ул. Пушкина, д. 15', '555-12-34'),
('Егорова Ольга', 'Женский', 'ул. Парковая, д. 20', '555-55-55'),
('Кузнецов Виктор', 'Мужской', 'ул. Молодежная, д. 30', '555-98-76');

-- Заполнение таблицы "Doctor"
INSERT INTO `Doctor` (`Name`, `Specialty`)
VALUES
('Денисова Екатерина', 'Кардиолог'),
('Смирнов Артем', 'Невролог'),
('Калинина Анастасия', 'Педиатр'),
('Шевченко Людмила', 'Дерматолог'),
('Лебедев Игорь', 'Офтальмолог'),
('Позов Максим', 'Хирург'),
('Бронзова Кристина', 'Эндокринолог'),
('Олова Надежда', 'Терапевт');

-- Заполнение таблицы "Medicine"
INSERT INTO `Medicine` (`Name`, `Method_of_reception`, `Description`, `Side_effects`)
VALUES
('Аспирин', 'Пероральный', 'Снижает температуру и уменьшает боль', 'Опасность возникновения язвы'),
('Парацетамол', 'Пероральный', 'Устраняет болезненные ощущения и снижает температуру', 'Возможно нарушение работы печени'),
('Амоксициллин', 'Пероральный', 'Лечение бактериальных инфекций', 'Диарея, сыпь'),
('Тетрациклин', 'Пероральный', 'Лечение бактериальных инфекций', 'Изменение цвета зубов'),
('Омепразол', 'Пероральный', 'Снижение кислотности желудка и предотвращение язв', 'Головная боль, диарея');

-- Заполнение таблицы "Inspection"
INSERT INTO `Inspection` (`Date`, `Location`, `Symptoms`, `Diagnosis`, `MedicineID`, `PatientID`, `DoctorID`, `Prescriptions`)
VALUES
('2021-01-01', 'Кабинет 123', 'Высокая температура, кашель', 'Грипп', 1, 1, 1, 'Принимать 2 таблетки каждые 4 часа'),
('2021-02-03', 'Кабинет 102', 'Головная боль, головокружение', 'Мигрень', 2, 2, 2, 'Принимать по 1 таблетке каждые 6 часов'),
('2021-03-05', 'Кабинет 212', 'Боль в горле, температура', 'Ангина', 3, 3, 3, 'Принимать по 1 таблетке каждые 8 часов'),
('2021-04-07', 'Кабинет 109', 'Сыпь, зуд', 'Экзема', 4, 4, 4, 'Наносить крем на пораженные участки 2 раза в день'),
('2021-05-09', 'Кабинет 105', 'Смазанный зрения', 'Миопия', 5, 5, 5, 'Принимать по 1 таблетке перед сном');

-- Заполнение таблицы "Patient_has_Medicine"
INSERT INTO `Patient_has_Medicine` (`PatientID`, `MedicineID`, `DoctorID`)
VALUES
(1, 1, 1),
(2, 2, 2),
(3, 3, 3),
(4, 5, 4),
(5, 4, 5);

-- Создание пользователя "HeadDoctor" с правами администратора
CREATE USER 'HeadDoctor'@'localhost' IDENTIFIED BY
'fgsDSF76DS';
GRANT ALL PRIVILEGES ON hospital.* TO 'HeadDoctor'@'localhost';


-- Создание пользователя "Doctor" с ограниченными правами
CREATE USER Doctor@'localhost' IDENTIFIED BY'RF565FV' ;
GRANT SELECT, INSERT, UPDATE ON hospital.* TO 'Doctor'@'localhost';

COMMIT


