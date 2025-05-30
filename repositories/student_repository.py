class StudentRepository:
    def __init__(self):
        self.students = {}

    def get_all_students(self):
        return list(self.students.values())

    def upsert_student(self, student):
        self.students[student.dni] = student
