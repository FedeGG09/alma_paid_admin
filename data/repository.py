# data/repository.py

import sqlite3
import pandas as pd
import datetime
from data.models import Student, Course, Enrollment

EXCEL_PATH = "alumnos por talleres.xlsx"

class SQLiteRepository:
    def __init__(self, db_path="alma_paid.db"):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self._create_tables()
        self._load_initial_data()
        self._load_initial_fees()

    def _create_tables(self):
        c = self.conn.cursor()
        # students
        c.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id      INTEGER PRIMARY KEY AUTOINCREMENT,
                name    TEXT UNIQUE,
                email   TEXT,
                status  TEXT
            );
        """)
        # dni migration
        cols = [r[1] for r in c.execute("PRAGMA table_info(students);")]
        if "dni" not in cols:
            c.execute("ALTER TABLE students ADD COLUMN dni TEXT;")

        # courses
        c.execute("""
            CREATE TABLE IF NOT EXISTS courses (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                title        TEXT UNIQUE
            );
        """)
        # monthly_fee migration
        cols = [r[1] for r in c.execute("PRAGMA table_info(courses);")]
        if "monthly_fee" not in cols:
            c.execute("ALTER TABLE courses ADD COLUMN monthly_fee REAL DEFAULT 15000.0;")

        # enrollments
        c.execute("""
            CREATE TABLE IF NOT EXISTS enrollments (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id  INTEGER,
                course_id   INTEGER,
                status      TEXT,
                UNIQUE(student_id, course_id),
                FOREIGN KEY(student_id) REFERENCES students(id),
                FOREIGN KEY(course_id)  REFERENCES courses(id)
            );
        """)
        self.conn.commit()

    def _load_initial_data(self):
        cur = self.conn.cursor()
        cur.execute("SELECT COUNT(*) FROM courses;")
        if cur.fetchone()[0] > 0:
            return

        df = pd.read_excel(EXCEL_PATH)
        for _, row in df.iterrows():
            title = row["Taller"].strip()
            cur.execute("INSERT OR IGNORE INTO courses(title) VALUES(?);", (title,))
            cur.execute("SELECT id FROM courses WHERE title=?;", (title,))
            course_id = cur.fetchone()[0]

            alumnos = [s.strip() for s in str(row["Estudiantes"]).split(",") if s.strip()]
            for name in alumnos:
                cur.execute(
                    "INSERT OR IGNORE INTO students(name, email, status) VALUES (?, ?, ?);",
                    (name, "", "activo")
                )
                cur.execute("SELECT id FROM students WHERE name=?;", (name,))
                student_id = cur.fetchone()[0]
                cur.execute(
                    "INSERT OR IGNORE INTO enrollments(student_id, course_id, status) VALUES (?, ?, ?);",
                    (student_id, course_id, "activo")
                )
        self.conn.commit()

    def _load_initial_fees(self):
        fee_map = {
            "TANGO": 10000.0,
            "KPOP DANCE": 10000.0,
            "ZUMBA": 18000.0,
            "XP - LOAD": 18000.0,
        }
        c = self.conn.cursor()
        c.execute("SELECT id, title FROM courses;")
        for cid, title in c.fetchall():
            fee = fee_map.get(title.upper(), 15000.0)
            c.execute("UPDATE courses SET monthly_fee=? WHERE id=?;", (fee, cid))
        self.conn.commit()

    def list_students(self):
        cur = self.conn.cursor()
        cur.execute("SELECT id, name, email, dni, status FROM students;")
        return [
            Student(id=r[0], name=r[1], email=r[2], dni=r[3] or "", status=r[4])
            for r in cur.fetchall()
        ]

    def upsert_student(self, s: Student):
        cur = self.conn.cursor()
        if s.id:
            cur.execute(
                "UPDATE students SET name=?, email=?, dni=?, status=? WHERE id=?;",
                (s.name, s.email, s.dni, s.status, s.id)
            )
            last_id = s.id
        else:
            cur.execute(
                "INSERT OR IGNORE INTO students(name, email, dni, status) VALUES (?, ?, ?, ?);",
                (s.name, s.email, s.dni, s.status)
            )
            last_id = cur.lastrowid
        self.conn.commit()
        return last_id

    def list_courses(self):
        cur = self.conn.cursor()
        # ahora solo id, title, monthly_fee
        cur.execute("SELECT id, title, monthly_fee FROM courses;")
        return [
            Course(id=r[0], title=r[1], description="", monthly_fee=r[2])
            for r in cur.fetchall()
        ]

    def upsert_course(self, c: Course):
        cur = self.conn.cursor()
        if c.id:
            cur.execute(
                "UPDATE courses SET title=?, monthly_fee=? WHERE id=?;",
                (c.title, c.monthly_fee, c.id)
            )
            last_id = c.id
        else:
            cur.execute(
                "INSERT OR IGNORE INTO courses(title, monthly_fee) VALUES (?, ?);",
                (c.title, c.monthly_fee)
            )
            last_id = cur.lastrowid
        self.conn.commit()
        return last_id

    def list_enrollments(self):
        cur = self.conn.cursor()
        cur.execute("SELECT id, student_id, course_id, status FROM enrollments;")
        return [
            Enrollment(id=r[0], student_id=r[1], course_id=r[2], status=r[3])
            for r in cur.fetchall()
        ]

    def upsert_enrollment(self, e: Enrollment):
        cur = self.conn.cursor()
        if e.id:
            cur.execute(
                "UPDATE enrollments SET student_id=?, course_id=?, status=? WHERE id=?;",
                (e.student_id, e.course_id, e.status, e.id)
            )
            last_id = e.id
        else:
            cur.execute(
                "INSERT OR IGNORE INTO enrollments(student_id, course_id, status) VALUES (?, ?, ?);",
                (e.student_id, e.course_id, e.status)
            )
            last_id = cur.lastrowid
        self.conn.commit()
        return last_id

    def get_courses_by_student_id(self, student_id: int):
        cur = self.conn.cursor()
        cur.execute("""
            SELECT c.id, c.title, c.monthly_fee
            FROM courses c
            JOIN enrollments e ON e.course_id=c.id
            WHERE e.student_id=?;
        """, (student_id,))
        return [
            Course(id=r[0], title=r[1], description="", monthly_fee=r[2])
            for r in cur.fetchall()
        ]

    def calculate_due_for_student(self, dni: str):
        """
        Devuelve (subtotal, surcharge, total) para el MES ACTUAL,
        aplicando recargo si HOY > 10.
        """
        cur = self.conn.cursor()
        cur.execute("SELECT id FROM students WHERE dni=?;", (dni,))
        row = cur.fetchone()
        if not row:
            return 0.0, 0.0, 0.0
        student_id = row[0]

        # Suma de mensualidades
        cur.execute("""
            SELECT c.monthly_fee
              FROM courses c
              JOIN enrollments e ON e.course_id=c.id
             WHERE e.student_id=?;
        """, (student_id,))
        fees = [r[0] for r in cur.fetchall()]
        subtotal = sum(fees)

        # Recargo: fijo 2000 si hoy >10
        today = datetime.date.today()
        surcharge = 2000.0 if today.day > 10 else 0.0
        total = subtotal + surcharge

        return subtotal, surcharge, total

    def calculate_next_month_due_for_student(self, dni: str):
        """
        Devuelve (subtotal, surcharge, total) PARA EL PRIMER DÍA DEL
        MES SIGUIENTE. Asume que si hoy >10, el recargo aplica
        inmediatamente al arrancar el mes.
        """
        cur = self.conn.cursor()
        cur.execute("SELECT id FROM students WHERE dni=?;", (dni,))
        row = cur.fetchone()
        if not row:
            return 0.0, 0.0, 0.0
        student_id = row[0]

        # Suma de mensualidades (mismo que mes actual)
        cur.execute("""
            SELECT c.monthly_fee
              FROM courses c
              JOIN enrollments e ON e.course_id=c.id
             WHERE e.student_id=?;
        """, (student_id,))
        fees = [r[0] for r in cur.fetchall()]
        subtotal = sum(fees)

        # Determinamos recargo según fecha actual:
        # si hoy >10, recargo de 2000 al inicio del mes siguiente
        today = datetime.date.today()
        surcharge = 2000.0 if today.day > 10 else 0.0
        total = subtotal + surcharge

        return subtotal, surcharge, total

