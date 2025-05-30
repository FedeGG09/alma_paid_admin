# screens/students.py

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from data.repository import SQLiteRepository

class EstudiantesScreen(Screen):
    def on_enter(self):
        repo = SQLiteRepository()
        layout = self.ids.students_list
        layout.clear_widgets()

        # Botón para volver al inicio
        back_button = Button(text="< Volver al inicio", size_hint_y=None, height=50, background_color=(0.8, 0.8, 0.8, 1), color=(0, 0, 0, 1))
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)

        for student in repo.list_students():
            courses = repo.get_courses_by_student_id(student.id)
            courses_text = ', '.join([c.title for c in courses]) if courses else "Sin cursos"

            row = BoxLayout(orientation='horizontal', size_hint_y=None, height=60, spacing=10, padding=5)

            info = f"{student.id} | {student.name} | {student.email} | {student.dni} | {student.status} | Cursos: {courses_text}"
            row.add_widget(Label(text=info, size_hint_x=0.7, color=(0, 0, 0, 1)))

            edit_button = Button(text="Editar", size_hint_x=0.15, background_color=(0.7, 0.7, 0.7, 1), color=(0, 0, 0, 1))
            edit_button.bind(on_press=lambda instance, s=student: self.edit_student(s))
            row.add_widget(edit_button)

            delete_button = Button(text="Eliminar", size_hint_x=0.15, background_color=(0.7, 0.7, 0.7, 1), color=(0, 0, 0, 1))
            delete_button.bind(on_press=lambda instance, s=student: self.delete_student(s))
            row.add_widget(delete_button)

            layout.add_widget(row)

    def edit_student(self, student):
        print(f"Editar estudiante: {student}")

    def delete_student(self, student):
        print(f"Eliminar estudiante: {student}")

    def go_back(self, instance):
        self.manager.current = "main"

