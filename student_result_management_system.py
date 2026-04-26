import csv
import os

FILE_NAME = "students.csv"


class Student:
    def __init__(self, student_id, name, roll_no, python_marks, sql_marks, excel_marks):
        self.student_id = student_id
        self.name = name
        self.roll_no = roll_no
        self.python_marks = python_marks
        self.sql_marks = sql_marks
        self.excel_marks = excel_marks

        self.total = python_marks + sql_marks + excel_marks
        self.percentage = self.total / 3
        self.grade = self.calculate_grade()

    def calculate_grade(self):
        if self.percentage >= 90:
            return "A+"
        elif self.percentage >= 80:
            return "A"
        elif self.percentage >= 70:
            return "B"
        elif self.percentage >= 60:
            return "C"
        elif self.percentage >= 40:
            return "D"
        else:
            return "Fail"

    def to_list(self):
        return [
            self.student_id,
            self.name,
            self.roll_no,
            self.python_marks,
            self.sql_marks,
            self.excel_marks,
            self.total,
            f"{self.percentage:.2f}",
            self.grade
        ]


class StudentManager:
    def __init__(self):
        self.create_file_if_not_exists()

    def create_file_if_not_exists(self):
        if not os.path.exists(FILE_NAME):
            with open(FILE_NAME, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([
                    "ID", "Name", "Roll No",
                    "Python", "SQL", "Excel",
                    "Total", "Percentage", "Grade"
                ])

    def generate_student_id(self):
        with open(FILE_NAME, mode="r") as file:
            rows = list(csv.reader(file))

            if len(rows) <= 1:
                return 1

            return int(rows[-1][0]) + 1

    def get_valid_name(self):
        while True:
            name = input("Enter Student Name: ").strip()

            if not name:
                print("Name cannot be empty.")

            elif name.replace(" ", "").isalpha():
                return name

            else:
                print("Invalid Name! Only alphabets and spaces are allowed.")

    def get_valid_roll_no(self):
        while True:
            roll_no = input("Enter Roll Number: ").strip()

            if not roll_no:
                print("Roll Number cannot be empty.")

            elif roll_no.isdigit():
                return roll_no

            else:
                print("Invalid Roll Number! Only numbers are allowed.")

    def get_valid_marks(self, subject):
        while True:
            try:
                marks = int(input(f"Enter {subject} Marks (0 to 100): "))

                if 0 <= marks <= 100:
                    return marks
                else:
                    print("Marks must be between 0 and 100 only.")

            except ValueError:
                print("Invalid Input! Enter numbers only.")

    def roll_no_exists(self, roll_no):
        with open(FILE_NAME, mode="r") as file:
            reader = csv.reader(file)
            next(reader)

            for row in reader:
                if row[2] == roll_no:
                    return True

        return False

    def add_student(self):
        print("\n========== Add Student ==========")

        student_id = self.generate_student_id()
        name = self.get_valid_name()
        roll_no = self.get_valid_roll_no()

        if self.roll_no_exists(roll_no):
            print("Roll Number already exists!\n")
            return

        python_marks = self.get_valid_marks("Python")
        sql_marks = self.get_valid_marks("SQL")
        excel_marks = self.get_valid_marks("Excel")

        student = Student(
            student_id,
            name,
            roll_no,
            python_marks,
            sql_marks,
            excel_marks
        )

        with open(FILE_NAME, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(student.to_list())

        print("Student added successfully!\n")

    def view_students(self):
        print("\n========== All Students ==========")

        with open(FILE_NAME, mode="r") as file:
            reader = csv.reader(file)

            for row in reader:
                print("{:<5} {:<15} {:<10} {:<8} {:<8} {:<8} {:<8} {:<10} {:<10}".format(*row))

    def update_student(self):
        print("\n========== Update Student ==========")

        roll_no = self.get_valid_roll_no()
        rows = []
        found = False

        with open(FILE_NAME, mode="r") as file:
            reader = csv.reader(file)

            for row in reader:
                if len(row) > 2 and row[2] == roll_no:
                    found = True

                    print("\nEnter New Details:")
                    name = self.get_valid_name()

                    python_marks = self.get_valid_marks("Python")
                    sql_marks = self.get_valid_marks("SQL")
                    excel_marks = self.get_valid_marks("Excel")

                    student = Student(
                        row[0],
                        name,
                        roll_no,
                        python_marks,
                        sql_marks,
                        excel_marks
                    )

                    rows.append(student.to_list())
                else:
                    rows.append(row)

        with open(FILE_NAME, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(rows)

        if found:
            print("Student updated successfully!\n")
        else:
            print("Student not found.\n")

    def delete_student(self):
        print("\n========== Delete Student ==========")

        roll_no = self.get_valid_roll_no()
        rows = []
        found = False

        with open(FILE_NAME, mode="r") as file:
            reader = csv.reader(file)

            for row in reader:
                if len(row) > 2 and row[2] == roll_no:
                    found = True
                    continue
                rows.append(row)

        with open(FILE_NAME, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(rows)

        if found:
            print("Student deleted successfully!\n")
        else:
            print("Student not found.\n")

    def print_report(self, student, rank, title="REPORT CARD"):
        print(f"\n========== {title} ==========")
        print(f"Student ID   : {student[0]}")
        print(f"Name         : {student[1]}")
        print(f"Roll Number  : {student[2]}")
        print(f"Python Marks : {student[3]}")
        print(f"SQL Marks    : {student[4]}")
        print(f"Excel Marks  : {student[5]}")
        print(f"Total Marks  : {student[6]}")
        print(f"Percentage   : {student[7]}%")
        print(f"Grade        : {student[8]}")
        print(f"Rank         : {rank}")
        print("=================================\n")

    def topper_student(self):
        print("\n========== Topper Student ==========")

        students = []

        with open(FILE_NAME, mode="r") as file:
            reader = csv.reader(file)
            next(reader)

            for row in reader:
                students.append(row)

        if not students:
            print("No student records found.\n")
            return

        students.sort(key=lambda x: float(x[7]), reverse=True)

        topper = students[0]
        self.print_report(topper, 1, "TOPPER REPORT CARD")

    def rank_students(self):
        print("\n========== Student Ranking ==========")

        students = []

        with open(FILE_NAME, mode="r") as file:
            reader = csv.reader(file)
            next(reader)

            for row in reader:
                students.append(row)

        students.sort(key=lambda x: float(x[7]), reverse=True)

        rank = 1
        for student in students:
            print(
                f"Rank {rank} -> {student[1]} | "
                f"Percentage: {student[7]}% | "
                f"Grade: {student[8]}"
            )
            rank += 1

    def failed_students(self):
        print("\n========== Failed Students ==========")

        failed_students_list = []

        with open(FILE_NAME, mode="r") as file:
            reader = csv.reader(file)
            next(reader)

            for row in reader:
                if row[8] == "Fail":
                    failed_students_list.append(row)

        if not failed_students_list:
            print("No failed students found.\n")
            return

        for student in failed_students_list:
            print("\n========== FAILED STUDENT REPORT ==========")
            print(f"Student ID   : {student[0]}")
            print(f"Name         : {student[1]}")
            print(f"Roll Number  : {student[2]}")
            print(f"Python Marks : {student[3]}")
            print(f"SQL Marks    : {student[4]}")
            print(f"Excel Marks  : {student[5]}")
            print(f"Total Marks  : {student[6]}")
            print(f"Percentage   : {student[7]}%")
            print(f"Grade        : {student[8]}")
            print("============================================\n")
        def statistics(self):
            print("\n========== Pass/Fail Statistics ==========")

        total_students = 0
        passed = 0
        failed = 0

        with open(FILE_NAME, mode="r") as file:
            reader = csv.reader(file)
            next(reader)

            for row in reader:
                total_students += 1

                if row[8] == "Fail":
                    failed += 1
                else:
                    passed += 1

        print(f"Total Students  : {total_students}")
        print(f"Passed Students : {passed}")
        print(f"Failed Students : {failed}")

    def generate_report_card(self):
        print("\n========== Student Report Card ==========")
        print("1. Search by Roll Number")
        print("2. Search by Name")

        choice = input("Enter Choice: ").strip()

        students = []

        with open(FILE_NAME, mode="r") as file:
            reader = csv.reader(file)
            next(reader)

            for row in reader:
                students.append(row)

        students.sort(key=lambda x: float(x[7]), reverse=True)

        found = False
        rank = 1

        if choice == "1":
            search_value = input("Enter Roll Number: ").strip()

            for student in students:
                if student[2] == search_value:
                    self.print_report(student, rank)
                    found = True
                    break
                rank += 1

        elif choice == "2":
            search_value = input("Enter Student Name: ").strip().lower()

            for student in students:
                if student[1].strip().lower() == search_value:
                    self.print_report(student, rank)
                    found = True
                    break
                rank += 1

        else:
            print("Invalid Choice.")
            return

        if not found:
            print("Student not found.\n")

    def menu(self):
        while True:
            print("\n========== Student Result Management System ==========")
            print("1. Add Student")
            print("2. View All Students")
            print("3. Update Student")
            print("4. Delete Student")
            print("5. Find Topper")
            print("6. Student Ranking")
            print("7. Failed Students")
            print("8. Pass/Fail Statistics")
            print("9. Generate Report Card")
            print("10. Exit")

            choice = input("\nEnter Your Choice: ")

            if choice == "1":
                self.add_student()
            elif choice == "2":
                self.view_students()
            elif choice == "3":
                self.update_student()
            elif choice == "4":
                self.delete_student()
            elif choice == "5":
                self.topper_student()
            elif choice == "6":
                self.rank_students()
            elif choice == "7":
                self.failed_students()
            elif choice == "8":
                self.statistics()
            elif choice == "9":
                self.generate_report_card()
            elif choice == "10":
                print("\nThank You for Using the System!")
                break
            else:
                print("Invalid Choice! Please try again.")


if __name__ == "__main__":
    system = StudentManager()
    system.menu()