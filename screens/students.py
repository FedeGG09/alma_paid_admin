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
        back = Button(
            text="< Volver al inicio",
            size_hint_y=None, height=50,
            background_color=(0.8,0.8,0.8,1),
            color=(0,0,0,1)
        )
        back.bind(on_press=lambda *_: setattr(self.manager, 'current', 'inicio'))
        layout.add_widget(back)

        for student in repo.list_students():
            courses = repo.get_courses_by_student_id(student.id)
            text_courses = ", ".join(c.title for c in courses) or "Sin cursos"

            row = BoxLayout(
                orientation='horizontal',
                size_hint_y=None,
                height=60,
                spacing=10,
                padding=5
            )
            # fondo blanco
            from kivy.graphics import Color, Rectangle
            with row.canvas.before:
                Color(1,1,1,1)
                rect = Rectangle(pos=row.pos, size=row.size)
            row.bind(
                pos=lambda inst, val, r=rect: setattr(r, 'pos', val),
                size=lambda inst, val, r=rect: setattr(r, 'size', val)
            )

            info = f"{student.id} | {student.name} | {student.email} | {student.dni} | {student.status}\nCursos: {text_courses}"
            row.add_widget(Label(text=info, color=(0,0,0,1)))

            edit = Button(text="Editar", size_hint_x=0.15,
                          background_color=(0.7,0.7,0.7,1),
                          color=(0,0,0,1))
            edit.bind(on_press=lambda inst, s=student: self.edit_student(s))
            row.add_widget(edit)

            delete = Button(text="Eliminar", size_hint_x=0.15,
                            background_color=(0.7,0.7,0.7,1),
                            color=(0,0,0,1))
            delete.bind(on_press=lambda inst, s=student: self.delete_student(s))
            row.add_widget(delete)

            layout.add_widget(row)

    def edit_student(self, student):
        print("Editar:", student)

    def delete_student(self, student):
        print("Eliminar:", student)

