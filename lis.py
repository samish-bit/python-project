import sqlite3
import os

# Remove old DB if exists (to reset schema)
if os.path.exists("students.db"):
    os.remove("students.db")

# Connect to database
conn = sqlite3.connect("students.db")
cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    roll INTEGER PRIMARY KEY,
    name TEXT,
    english INTEGER,
    math INTEGER,
    science INTEGER,
    social INTEGER,
    nepali INTEGER,
    total INTEGER,
    percentage REAL,
    result TEXT
)
""")
conn.commit()

# Hardcoded full marks and pass marks
subjects = {
    "English": {"full": 100, "pass": 40},
    "Math": {"full": 100, "pass": 40},
    "Science": {"full": 100, "pass": 40},
    "Social": {"full": 100, "pass": 40},
    "Nepali": {"full": 100, "pass": 40}
}

#  Function to get valid marks input
def get_valid_marks(subject):
    while True:
        try:
            mark = int(input(f"Enter marks in {subject} (0-{subjects[subject]['full']}): "))
            if 0 <= mark <= subjects[subject]["full"]:
                return mark
            else:
                print(f" Invalid! Marks must be between 0 and {subjects[subject]['full']}.")
        except ValueError:
            print(" Invalid input! Please enter a number.")

def calculate_result(marks):
    total = sum(marks.values())
    percentage = total / len(marks)
    result = "Pass" if all(m >= subjects[sub]["pass"] for sub, m in marks.items()) else "Fail"
    return total, percentage, result

def save_marksheet(roll, name, marks, total, percentage, result):
    filename = f"marksheet_{roll}.txt"
    with open(filename, "w") as f:
        f.write(f"Roll: {roll}\nName: {name}\n")
        for sub, mark in marks.items():
            f.write(f"{sub}: {mark}/{subjects[sub]['full']}\n")
        f.write(f"Total: {total}\nPercentage: {percentage:.2f}%\nResult: {result}\n")
    print(f" Marksheet saved as {filename}")

def add_student():
    try:
        roll = int(input("Enter roll number: "))
        name = input("Enter name: ")
        marks = {}
        for sub in subjects:
            marks[sub] = get_valid_marks(sub)  #  Validation used here

        total, percentage, result = calculate_result(marks)

        cursor.execute("INSERT INTO students VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                       (roll, name, marks["English"], marks["Math"], marks["Science"],
                        marks["Social"], marks["Nepali"], total, percentage, result))
        conn.commit()
        save_marksheet(roll, name, marks, total, percentage, result)
        print(" Student added successfully.")
    except Exception as e:
        print("Error:", e)

def update_student():
    try:
        roll = int(input("Enter roll number to update: "))
        cursor.execute("SELECT * FROM students WHERE roll=?", (roll,))
        student = cursor.fetchone()
        if not student:
            print(" No student found with that roll number. Update failed.")
            return

        name = input("Enter new name: ")
        marks = {}
        for sub in subjects:
            marks[sub] = get_valid_marks(sub)  # Validation used here

        total, percentage, result = calculate_result(marks)

        cursor.execute("""UPDATE students SET name=?, english=?, math=?, science=?, 
                          social=?, nepali=?, total=?, percentage=?, result=? WHERE roll=?""",
                       (name, marks["English"], marks["Math"], marks["Science"],
                        marks["Social"], marks["Nepali"], total, percentage, result, roll))
        conn.commit()
        save_marksheet(roll, name, marks, total, percentage, result)
        print(" Student updated successfully.")
    except Exception as e:
        print("Error:", e)


def delete_student():
    try:
        roll = int(input("Enter roll number to delete: "))
        cursor.execute("SELECT * FROM students WHERE roll=?", (roll,))
        student = cursor.fetchone()
        if not student:
            print(" No student found with that roll number. Delete failed.")
            return

        cursor.execute("DELETE FROM students WHERE roll=?", (roll,))
        conn.commit()
        print(" Student deleted successfully.")
    except Exception as e:
        print("Error:", e)



def view_students():
    cursor.execute("SELECT * FROM students")
    for row in cursor.fetchall():
        print(row)

def generate_marksheet_by_roll():
    try:
        roll = int(input("Enter roll number: "))
        cursor.execute("SELECT * FROM students WHERE roll=?", (roll,))
        student = cursor.fetchone()
        if student:
            marks = {
                "English": student[2],
                "Math": student[3],
                "Science": student[4],
                "Social": student[5],
                "Nepali": student[6]
            }
            save_marksheet(student[0], student[1], marks, student[7], student[8], student[9])
        else:
            print(" No student found with that roll number.")
    except Exception as e:
        print("Error:", e)

def main():
    while True:
        print("\n===== Student Marksheet System =====")
        print("1. Add Student")
        print("2. Update Student")
        print("3. Delete Student")
        print("4. View Students")
        print("5. Exit")
        print("6. Generate Marksheet by Roll Number")
        choice = input("Enter choice: ")

        if choice == "1":
            add_student()
        elif choice == "2":
            update_student()
        elif choice == "3":
            delete_student()
        elif choice == "4":
            view_students()
        elif choice == "5":
            break
        elif choice == "6":
            generate_marksheet_by_roll()
        else:
            print(" Invalid choice.")

main()
conn.close()
