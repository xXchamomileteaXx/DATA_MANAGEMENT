import mysql.connector
from datetime import date
import datetime
from datetime import datetime


class Hospital:
    def __init__(self, us, passw):
        self.conn = mysql.connector.connect(
            user=us,
            password=passw,
            host='localhost',
            database='hospital'
        )
        self.cursor = self.conn.cursor()

    from datetime import datetime

    def get_inspection_count(self):

        date = input("Введите дату (в формате YYYY-MM-DD): ")

        try:
            date = datetime.strptime(date, '%Y-%m-%d').date()
        except ValueError:
            print("Некорректный формат даты. Используйте формат YYYY-MM-DD")
            return False

        self.cursor.execute("""
            SELECT DISTINCT DoctorID
            FROM Inspection 
            WHERE DATE(Date) = %s
            """, (date,))

        result = self.cursor.fetchall()
        print("\nКоличество осмотров в указанную дату:")
        for row in result:
            print(row[0])

        doctor_id = result[0][0]
        self.cursor.execute("""
            SELECT Name FROM Doctor WHERE DoctorID = %s
        """, (doctor_id,))
        result = self.cursor.fetchone()
        if result is not None:
            doctor_name = result[0]
            print("\nВ указанную дату осмотр проводил врач:")
            print(doctor_name)
        else:
            print("Доктор с таким ID не найден.")

    def get_side_effects(self):
        print("\nЛекарства,которы используют для лечения в клинике:")

        self.cursor.execute("""
            SELECT GROUP_CONCAT(Name SEPARATOR ',') 
            AS All_Medicines FROM Medicine;""")
        res = hospital.cursor.fetchall()
        for row in res:
            print(row)

        print("Введите название лекарства:")
        medicine_name = input()
        self.cursor.execute("""
            SELECT Side_effects FROM 
            Medicine WHERE Name = %s""", (medicine_name,))
        result = self.cursor.fetchone()
        if result:
            print(f"Побочные эффекты лекарства {medicine_name}: {result[0]}")
            return result[0]
        else:
            print(f"Лекарство {medicine_name} не найдено в базе данных")
            return None

    def show_all_medicine(self):
        self.cursor.execute("""
            SELECT DISTINCT Name,Description
            FROM Medicine""")
        result = self.cursor.fetchall()
        for row in result:
            print("Лекарство:", row[0], "|", "Описание:", row[1])

    def add_medicine(self):
        print("\nЛекарства,которы используют для лечения в клинике:")
        self.cursor.execute("""
            SELECT GROUP_CONCAT(Name SEPARATOR ',') 
            AS All_Medicines FROM Medicine;""")
        res = hospital.cursor.fetchall()
        for row in res:
            print(row)

        name = input("\nВведите название лекарства,которое нужно добавить: ")
        self.cursor.execute("""
            SELECT * FROM 
            Medicine WHERE Name = %s""",
            (name,))
        if self.cursor.fetchone():
            print(f"Лекарство {name} уже существует в базе данных")
            return False

        description = input("Введите описание: ")
        side_effects = input("Введите побочные эффекты: ")
        method_of_reception = input("Введите способ применения: ")
        self.cursor.execute("""
            INSERT INTO Medicine 
            (Name,Method_of_reception, Description, Side_effects) 
            VALUES (%s, %s, %s, %s)""",
                            (name, method_of_reception, description, side_effects))

        self.conn.commit()
        print(f"Лекарство {name} успешно добавлено в базу клиники")
        return True

    def delete_medicine(self):
        self.cursor.execute("SELECT MedicineID, Name FROM Medicine")
        medicines = self.cursor.fetchall()
        for i, medicine in enumerate(medicines):
            print("- {}: {}".format(i + 1, medicine[1]))
        medicine_index = int(input("Выберите препарат: "))
        medicine_id = medicines[medicine_index - 1][0]

        self.cursor.execute("""
            DELETE FROM Patient_has_Medicine WHERE MedicineID = %s
            """, (medicine_id,))
        self.cursor.execute("""
            DELETE FROM Inspection WHERE MedicineID = %s
            """, (medicine_id,))
        self.cursor.execute("""
            DELETE FROM Medicine WHERE MedicineID = %s
             """, (medicine_id,))
        self.conn.commit()
        print("Препарат успешно удален\n")

    def get_inspection_report(self):
        print("Введите диапазон дат для отчета о проведенных осмотрах.")
        start_date = input("Начальная дата (в формате YYYY-MM-DD): ")
        end_date = input("Конечная дата (в формате YYYY-MM-DD): ")

        try:
            start_date = date.fromisoformat(start_date)
            end_date = date.fromisoformat(end_date)
        except ValueError:
            print("Некорректный формат даты. Используйте формат YYYY-MM-DD")
            return False

        inspection_report = {}

        self.cursor.execute("""
            SELECT Doctor.Name, COUNT(*) AS NumInspections
            FROM Inspection
            JOIN Doctor ON Inspection.DoctorID = Doctor.DoctorID
            WHERE Inspection.Date BETWEEN %s AND %s 
            GROUP BY Doctor.DoctorID""",
                            (start_date, end_date))

        rows = self.cursor.fetchall()
        for row in rows:
            inspection_report[row[0]] = row[1]

        if not inspection_report:
            print("За выбранный период нет проведенных осмотров")
            return False

        print("\nОтчет о проведенных осмотрах за период:")
        print(f"С {start_date} по {end_date}")
        for doctor, num_inspections in inspection_report.items():
            print(f"{doctor}: {num_inspections} проведенных осмотров")

        return True

    def generate_personal_report(self):
        self.cursor.execute("""
            SELECT PatientID, Name
            FROM Patient""")

        patients = self.cursor.fetchall()
        for patient in patients:
            print("ID пациента: {}, имя: {}".format(patient[0], patient[1]))
        cnt = 0

        self.cursor.execute("SELECT PatientID,Name FROM Patient")
        patients = self.cursor.fetchall()
        if not patients:
            print("Список пациентов пуст")
            return False

        patient_index = int(input("Введите номер пациента: "))
        print("\n")
        patient_id = patients[patient_index - 1][0]
        self.cursor.execute("""
            SELECT Patient.Name AS PatientName, Doctor.Name AS DoctorName, Inspection.Date, 
            Inspection.Location, Inspection.Symptoms, Inspection.Diagnosis, 
            Inspection.Prescriptions, Medicine.Name AS MedicineName, 
            Medicine.Method_of_reception, Medicine.Side_effects
            FROM Inspection
            INNER JOIN Patient ON Inspection.PatientID = Patient.PatientID
            INNER JOIN Doctor ON Inspection.DoctorID = Doctor.DoctorID
            INNER JOIN Medicine ON Inspection.MedicineID = Medicine.MedicineID
            WHERE Inspection.PatientID = %s
            ORDER BY Inspection.Date DESC;
            """, (patient_id,))

        result = self.cursor.fetchall()
        if not result:
            print("Не найдено ни одного осмотра для данного пациента и даты")
        c = 1
        for r in result:
            print(f"Отчет об осмотре №{c}")
            print("Дата: {}".format(r[2]))
            print("Место: {}".format(r[3]))
            print("Симптомы: {}".format(r[4]))
            print("Диагноз: {}".format(r[5]))
            print("Назначения: {}".format(r[6]))
            print("Пациент: {}".format(r[0]))
            print("Врач: {}".format(r[1]))
            print("Лекарство: {} (способ применения: {}, побочные эффекты: {})".format(r[7], r[8], r[9]))
            print("\n")
            c = c + 1

    def show_all_doctors(self):
        self.cursor.execute("SELECT DISTINCT Name, Specialty FROM Doctor")
        result = self.cursor.fetchall()
        print("\nВрачи,которые работают в клинике: \n")
        for row in result:
            print(row[0], "-", row[1])

    def add_doctor(self):

        name = input("\nВведите имя и фамилмю врача: ")

        self.cursor.execute("""
            SELECT * FROM 
            Doctor WHERE Name = %s""",
                            (name,))
        if self.cursor.fetchone():
            print(f"Врач {name} уже существует в базе клиники")
            return False

        specialty = input("Введите специализацию: ")
        self.cursor.execute("""
            SELECT * FROM 
            Doctor WHERE Specialty = %s""",
                            (specialty,))
        if self.cursor.fetchone():
            print(f"Врач со специализацией {specialty} уже существует в базе клиники")
            return False

        self.cursor.execute("""
            INSERT INTO Doctor 
            (Name, Specialty) 
            VALUES (%s, %s)""",
                            (name, specialty))

        self.conn.commit()
        print(f"Врач {name} успешно добавлен в базу клиники")
        return True

    def add_patient(self):
        name = input("Введите ФИО пациента: ")
        gender = input("Введите пол пациента ('Мужской' или 'Женский'): ")
        address = input("Введите адрес пациента: ")
        phone_number = input("Введите номер телефона пациента: ")

        self.cursor.execute("""
             INSERT INTO Patient (Name, Gender, Address, Phone_number) 
             VALUES (%s, %s, %s, %s)""",
                            (name, gender, address, phone_number))
        self.conn.commit()

        print("Пациент {} успешно добавлен в базу клиники".format(name))

    def show_all_patients(self):
        self.cursor.execute("SELECT DISTINCT Name, Address FROM Patient")
        result = self.cursor.fetchall()
        for row in result:
            print(row[0], "-", row[1])

    def add_Inspection(self):

        date = input("Введите дату осмотра (гггг-мм-дд): ")
        location = input("Введите место осмотра: ")
        symptoms = input("Введите симптомы: ")
        diagnosis = input("Введите диагноз: ")

        ch = int(input("Если нужно добавить новое лекарство нажмите 1,если хотите выбрать из базы нажмите 2: "))
        if ch == 1:
            self.add_medicine()
            self.cursor.execute("""
                                   SELECT MedicineID, Name
                                   FROM Medicine""")
            medicines = self.cursor.fetchall()
            for medicine in medicines:
                print("ID лекарства: {}, название: {}".format(medicine[0], medicine[1]))
            medicine_id = int(input("Введите ID лекарства: "))
        if ch == 2:
            self.cursor.execute("""
                       SELECT MedicineID, Name
                       FROM Medicine""")
            medicines = self.cursor.fetchall()
            for medicine in medicines:
                print("ID лекарства: {}, название: {}".format(medicine[0], medicine[1]))
            medicine_id = int(input("Введите ID лекарства: "))

        self.cursor.execute("""
                                   SELECT PatientID, Name
                                   FROM Patient
                                   """)
        patients = self.cursor.fetchall()
        for patient in patients:
            print("ID пациента: {}, имя: {}".format(patient[0], patient[1]))
        patient_id = input("Введите ID пациента: ")

        self.cursor.execute("SELECT DoctorID, Name FROM Doctor")
        doctors = self.cursor.fetchall()
        for doctor in doctors:
            print("ID Доктора: {}, имя: {}".format(doctor[0], doctor[1]))
        doctor_id = input("Введите ID врача: ")

        prescriptions = input("Введите назначения: ")

        self.cursor.execute(
            "INSERT INTO Patient_has_Medicine (MedicineID, PatientID, DoctorID) VALUES (%s, %s, %s)",
            (medicine_id, patient_id, doctor_id))
        sql = """INSERT INTO Inspection 
              (Date, Location, Symptoms, Diagnosis, Prescriptions,MedicineID, PatientID, DoctorID) 
              VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
        val = (date, location, symptoms, diagnosis, prescriptions, medicine_id, patient_id, doctor_id)

        self.cursor.execute(sql, val)
        self.conn.commit()

        print(self.cursor.rowcount, "осмотр добавлен в базу клиники")

    def close_connection(self):
        self.conn.close()


if __name__ == '__main__':
    user = input("Введите логин: ")
    password = input("Введите пароль: ")
    hospital = Hospital(user, password)

    while True:
        print("\n\n1. Добавить врача в клинику")
        print("2. Посмотреть врачей,которые работают в клинике")
        print("3. Добавить лекарство в базу клиники")
        print("4. Удалить лекарство из базы клиники")
        print("5. Посмотреть все лекарства,которые могут прописать врачи")
        print("6. Посмотреть,сколько вызовов было в определенную дату")
        print("7. Посмотреть побочные эффекты лекарства")
        print("8. Показать отчет о количестве осмотров за перод")
        print("9. Показать отчет об осмотре определенного пациента")
        print("10.Добавить новый осмотр")
        print("11.Добавить нового пациента")
        print("12.Показать всех пациентов клиники")
        print("0. Выйти\n\n")

        choice = input("Выберите опцию: ")

        if choice == "1":
            hospital.add_doctor()
        elif choice == "2":
            hospital.show_all_doctors()
        elif choice == "3":
            hospital.add_medicine()
        elif choice == "4":
            hospital.delete_medicine()
        elif choice == "5":
            hospital.show_all_medicine()
        elif choice == "6":
            hospital.get_inspection_count()
        elif choice == "7":
            hospital.get_side_effects()
        elif choice == "8":
            hospital.get_inspection_report()
        elif choice == "9":
            hospital.generate_personal_report()
        elif choice == "10":
            hospital.add_Inspection()
        elif choice == "11":
            hospital.add_patient()
        elif choice == "12":
            hospital.show_all_patients()
        elif choice == "0":
            break
        else:
            print("Неверный выбор. Пожалуйста, попробуйте еще раз.")

    db.close_connection()


