import sqlite3
from faker import Faker
import random

conn = sqlite3.connect("college.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id              INTEGER PRIMARY KEY,
        name            TEXT,
        age             INTEGER,
        major           TEXT,
        enrollment_year INTEGER
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS courses (
        id         INTEGER PRIMARY KEY,
        title      TEXT,
        credits    INTEGER,
        department TEXT
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS grades (
        id         INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        course_id  INTEGER,
        grade      TEXT,
        semester   TEXT
    )
""")

fake = Faker('en_IN')

majors = [
    "Computer Science", "Mathematics", "Physics",
    "Electronics", "Civil Engineering", "Mechanical Engineering"
]

students_data = []
for i in range(1, 21):
    name  = fake.name()
    age   = random.randint(18, 25)
    major = random.choice(majors)
    year  = random.randint(2019, 2023)
    students_data.append((i, name, age, major, year))
    
cursor.executemany(
    "INSERT INTO students VALUES (?, ?, ?, ?, ?)",
    students_data
)

courses_data = [
    (1,  "Data Structures",       4, "Computer Science"),
    (2,  "Linear Algebra",        3, "Mathematics"),
    (3,  "Thermodynamics",        3, "Mechanical Engineering"),
    (4,  "Digital Circuits",      4, "Electronics"),
    (5,  "Database Systems",      3, "Computer Science"),
    (6,  "Calculus II",           4, "Mathematics"),
    (7,  "Structural Analysis",   3, "Civil Engineering"),
    (8,  "Operating Systems",     4, "Computer Science"),
]

cursor.executemany(
    "INSERT INTO courses VALUES (?, ?, ?, ?)",
    courses_data
)

grades_list = ["A", "A", "B", "B", "B", "C", "C", "D", "F"]

semesters = ["Fall 2021", "Spring 2022", "Fall 2022", "Spring 2023"]

grades_data = []

for student_id in range(1, 21):
    num_courses = random.randint(2, 5)
    chosen_courses = random.sample(range(1, 9), num_courses)


    for course_id in chosen_courses:
        grade    = random.choice(grades_list)
        semester = random.choice(semesters)
        grades_data.append((student_id, course_id, grade, semester))
        

cursor.executemany(
    "INSERT INTO grades (student_id, course_id, grade, semester) VALUES (?, ?, ?, ?)",
    grades_data
)
conn.commit()
conn.close()