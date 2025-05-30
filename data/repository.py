# data/repository.py

import sqlite3
import pandas as pd
from data.models import Student, Course, Enrollment

EXCEL_PATH = "alumnos por talleres.xlsx"

class SQLiteRepository:
    def __init__(self, db_path="alma_paid.db"):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self._create_tables()
        self._load_initial_data()

    def _create_tables(self):
        c = self.conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id   INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE,
                email TEXT,
                status TEXT
            );""")
        c.execute("""
            CREATE TABLE IF NOT EXISTS courses (
                id    INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT UNIQUE
            );""")
        c.execute("""
            CREATE TABLE IF NOT EXISTS enrollments (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER,
                course_id  INTEGER,
                status     TEXT,
                UNIQUE(student_id, course_id),
                FOREIGN KEY(student_id) REFERENCES students(id),
                FOREIGN KEY(course_id)  REFERENCES courses(id)
            );""")
        self.conn.commit()

    def _load_initial_data(self):
        cur = self.conn.cursor()
        cur.execute("SELECT COUNT(*) FROM courses;")
        if cur.fetchone()[0] > 0:
            return  # Ya inicializado

        # Carga el Excel
        df = pd.read_excel(EXCEL_PATH)
        for _, row in df.iterrows():
            course_title = row["Taller"].strip()
            cur.execute("INSERT OR IGNORE INTO courses(title) VALUES(?);", (course_title,))
            cur.execute("SELECT id FROM courses WHERE title=?;", (course_title,))
            course_id = cur.fetchone()[0]

            alumnos = [s.strip() for s in str(row["Estudiantes"]).split(",") if s.strip()]
            for name in alumnos:
                cur.execute("""
                    INSERT OR IGNORE INTO students(name, email, status)
                    VALUES(?, ?, ?);""", (name, "", "activo"))
                cur.execute("SELECT id FROM students WHERE name=?;", (name,))
                student_id = cur.fetchone()[0]

                cur.execute("""
                    INSERT OR IGNORE INTO enrollments(student_id, course_id, status)
                    VALUES(?, ?, ?);""", (student_id, course_id, "activo"))
        self.conn.commit()

    # --- Métodos CRUD --- #

    def list_students(self):
        cur = self.conn.cursor()
        cur.execute("SELECT id, name, email, status FROM students;")
        rows = cur.fetchall()
        return [Student(row[0], row[1], row[2], "", row[3]) for row in rows]

    def list_courses(self):
        cur = self.conn.cursor()
        cur.execute("SELECT id, title FROM courses;")
        rows = cur.fetchall()
        return [Course(row[0], row[1], "") for row in rows]

    def get_courses_by_student_id(self, student_id: int):
        cur = self.conn.cursor()
        cur.execute("""
            SELECT c.id, c.title
            FROM courses c
            JOIN enrollments e ON e.course_id = c.id
            WHERE e.student_id = ?;
        """, (student_id,))
        return [Course(id=row[0], title=row[1], description="") for row in cur.fetchall()]

    def list_enrollments(self):
        cur = self.conn.cursor()
        cur.execute("SELECT id, student_id, course_id, status FROM enrollments;")
        return [Enrollment(*row) for row in cur.fetchall()]

    def upsert_enrollment(self, e: Enrollment):
        cur = self.conn.cursor()
        if e.id:
            cur.execute("""
                UPDATE enrollments SET student_id=?, course_id=?, status=? WHERE id=?;
            """, (e.student_id, e.course_id, e.status, e.id))
        else:
            cur.execute("""
                INSERT OR REPLACE INTO enrollments(student_id, course_id, status)
                VALUES(?, ?, ?);""", (e.student_id, e.course_id, e.status))
        self.conn.commit()
        return cur.lastrowid

    def upsert_student(self, s: Student):
        cur = self.conn.cursor()
        if s.id:
            cur.execute("""
                UPDATE students SET name=?, email=?, status=? WHERE id=?;
            """, (s.name, s.email, s.status, s.id))
        else:
            cur.execute("""
                INSERT OR IGNORE INTO students(name, email, status)
                VALUES(?, ?, ?);""", (s.name, s.email, s.status))
        self.conn.commit()
        return cur.lastrowid
