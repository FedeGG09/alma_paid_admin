import sqlite3

def create_tables():
    conn = sqlite3.connect("alma_paid.db")
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS student_courses (
            student_id INTEGER,
            course_id INTEGER,
            PRIMARY KEY (student_id, course_id),
            FOREIGN KEY (student_id) REFERENCES students(id),
            FOREIGN KEY (course_id) REFERENCES courses(id)
        );
    """)

    conn.commit()
    conn.close()

create_tables()

courses_data = {
    "FUNCIONAL KIDS / PAMELA PAEZ": ["Martín", "Santino", "Isabella", "Iana", "Yanara", "Aaron"],
    "TANGO INTERMEDIO AVANZADO": ["Rocío Scaglioni", "Sol", "Josho Mugas", "Stiven Yanaje", "Victor Ramirez", "Macarena Waidat", "Camila Herrera"],
    "YOGA / MONICA SÁNCHEZ": ["Gabriela 9 hs", "Mirtha 9 hs", "Martha Núñez", "Juanita Casiva", "Lucía Vega", "Marina", "Cynthia Riquelme", "Mabel Ruarte"],
    "DANCE COVER KPOP": ["Ornella", "Viky"],
    "KPOP FITNESS": ["Enea Gómez", "Natalia Cerezo", "Sol", "Pia Juncos", "Vicky Sabanes", "Maria"],
    "CONTEMPORÁNEA ADULTOS + 30": ["María José Loyola", "Lore Lovento", "Marina", "Caro Ticar", "Cristina", "Doli", "Susana", "Gonzalo", "Karen"],
    "RUMBA TERAPIA": ["Sandra González", "Fernanda Carmona", "Lore Lovento", "Ruth", "María José Loyola", "Mariela Canderolo", "Nacho", "Gonzalo"],
    "LA CAJA DE PANDORA": ["Victoria López", "Alejo Chanampe"],
    "TEATRIN TRIN TRIN": ["Bety", "Ramiro", "Ofelia", "Ley", "Bety Vega", "Yamila Ormeño"],
    "YOGA / MAÑANA": ["Gabriela", "Rebecca", "Alejandra Gordillo", "Ivanna García"],
    "YOGA / TARDE": ["Betty Andrada", "Patri Castro", "Cori Corea", "Natalia", "Fabián"],
    "DANZA CLÁSICA 3 A 6 AÑOS / ROCIO": ["Sofía Ríos", "Olivia", "Catalina", "Constanza Moretta", "Lucía Casiva", "Alfonsina Vichi", "Marquesina"],
    "DANZA CLÁSICA 7 A 12 AÑOS / ROCIO": ["Anya Torres"],
    "DANZA CONTEMPORÁNEA 7 A 12 AÑOS / ROCIO": ["Antonella Gareis", "Octavia", "Constanza Moretta"],
    "FOLKLORE ESTILIZADO / ROCIO": ["Rocío", "Leandro Benítez", "Carla", "Iocco", "Vale", "Antonella López", "Fernanda Tejada", "Ariana Papiche"],
    "TALLERES / ROCIO": ["Belkys Bazán", "Sol Guardia", "Jesica Pérez", "Carina Luna", "Alfonsina Nader", "María Quaglia", "Ana María Bordón"],
    "RITMOS / LUCIA ZIMMERMAN": ["Kiara Poblete", "Salma González", "Paola Barrionuevo", "Agustina Ambrosini", "Romina", "Clelia Ibarra"],
    "ACROTELA ADULTO / KAREN NAZAR": ["Jocelyn", "Ely", "Agostina Cobo", "Felipe Palacios", "Gonzalo", "Pilar", "Melina", "Patricia", "Luciana"],
    "DANZA FOLKLÓRICA / DAMIAN SÁNCHEZ": ["María Quaglia", "Ómar Latif", "Sardina y Sra", "Patricia", "Deisy", "Lorena", "Daiana Herrera", "Rocío"],
    "XP LOAND / AGUSTINA MORETA": ["Paola Travesani", "Ana Iglesias", "Yamila", "José", "Gabriela", "Roxana Velázquez", "Nadia Herrera", "Ruth Suárez"],
    "ZUMBA + LOCALIZADA / AGUSTINA MORETA": ["Norma Arias", "Alvear", "Elizondo", "Ruth Suárez", "Fanny", "Ruth Arias", "Nancy Flores", "Yamila"]
}
def insert_courses_and_students(data):
    conn = sqlite3.connect("alma_paid.db")
    cur = conn.cursor()

    for course_title, student_names in data.items():
        # Insertar el curso
        cur.execute("INSERT INTO courses (title) VALUES (?)", (course_title,))
        course_id = cur.lastrowid

        for student_name in student_names:
            # Verificar si el estudiante ya existe
            cur.execute("SELECT id FROM students WHERE name = ?", (student_name,))
            result = cur.fetchone()
            if result:
                student_id = result[0]
            else:
                cur.execute("INSERT INTO students (name) VALUES (?)", (student_name,))
                student_id = cur.lastrowid

            # Relación
            cur.execute("INSERT OR IGNORE INTO student_courses (student_id, course_id) VALUES (?, ?)",
                        (student_id, course_id))

    conn.commit()
    conn.close()

insert_courses_and_students(courses_data)


