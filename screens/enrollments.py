# screens/enrollments.py

from kivy.uix.screenmanager import Screen
from kivy.properties import ListProperty
from kivy.clock import Clock

from data.repository import SQLiteRepository
from data.models import Enrollment, Student, Course

repo = SQLiteRepository()

class MatriculasScreen(Screen):
    enrollments = ListProperty()
    students = ListProperty()
    courses = ListProperty()

    def on_enter(self):
        # Carga dropdowns y lista de inscripciones al entrar
        self.refresh_dropdowns()
        self.refresh_enrollments()

    def refresh_dropdowns(self):
        # Obtiene listas del repo
        students = repo.list_students()
        courses = repo.list_courses()

        # Formatea para Spinner
        self.students = [f"{s.id} - {s.name}" for s in students]
        self.courses = [f"{c.id} - {c.title}" for c in courses]

        # Actualiza widgets
        self.ids.student_spinner.values = self.students
        self.ids.student_spinner.text = "Seleccionar Estudiante"
        self.ids.course_spinner.values = self.courses
        self.ids.course_spinner.text = "Seleccionar Curso"

    def refresh_enrollments(self):
        # Toma del repo y formatea para mostrar
        ens = repo.list_enrollments()
        self.enrollments = [f"{e.id} → Est:{e.student_id} Crs:{e.course_id} ({e.status})" for e in ens]
        self.ids.enrollment_rv.data = [{"text": txt} for txt in self.enrollments]

    def save_enrollment(self):
        s_text = self.ids.student_spinner.text
        c_text = self.ids.course_spinner.text
        status = self.ids.enrollment_status.text.strip()
        if "-" not in s_text or "-" not in c_text or not status:
            print("⚠️ Falta selección o estado vacío")
            return

        # Parsea ID opcional
        eid = self.ids.enrollment_id.text.strip()
        eid = int(eid) if eid.isdigit() else None
        sid = int(s_text.split(" - ")[0])
        cid = int(c_text.split(" - ")[0])

        e = Enrollment(id=eid, student_id=sid, course_id=cid, status=status)
        repo.upsert_enrollment(e)

        # Limpia formulario y recarga vista
        self.ids.enrollment_id.text = ""
        self.ids.enrollment_status.text = ""
        self.refresh_dropdowns()
        self.refresh_enrollments()

    def add_student_popup(self):
        # Popup para crear estudiante desde aquí
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.popup import Popup
        from kivy.uix.textinput import TextInput
        from kivy.uix.button import Button
        from data.models import Student

        content = BoxLayout(orientation="vertical", padding=10, spacing=5)
        name_i = TextInput(hint_text="Nombre")
        email_i = TextInput(hint_text="Email")
        status_i = TextInput(hint_text="Estado")
        save_btn = Button(text="Guardar estudiante", size_hint_y=None, height=40)
        content.add_widget(name_i)
        content.add_widget(email_i)
        content.add_widget(status_i)
        content.add_widget(save_btn)

        popup = Popup(title="Nuevo Estudiante", content=content, size_hint=(0.8,0.7))
        save_btn.bind(on_release=lambda *_: self._save_student(name_i, email_i, status_i, popup))
        popup.open()

    def _save_student(self, name_i, email_i, status_i, popup):
        from data.models import Student
        s = Student(id=None, name=name_i.text, email=email_i.text, dni="", status=status_i.text)
        repo.upsert_student(s)
        popup.dismiss()
        self.refresh_dropdowns()
