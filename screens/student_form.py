from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

from data.models import Student
from data.repository import SQLiteRepository

repo = SQLiteRepository()

class EstudianteFormScreen(Screen):
    def on_enter(self):
        self.clear_widgets()

        layout = BoxLayout(orientation="vertical", padding=10, spacing=10)
        self.name_input = TextInput(hint_text="Nombre")
        self.email_input = TextInput(hint_text="Email")
        self.dni_input = TextInput(hint_text="DNI")
        self.status_input = TextInput(hint_text="Estado")

        layout.add_widget(Label(text="Agregar Nuevo Estudiante"))
        layout.add_widget(self.name_input)
        layout.add_widget(self.email_input)
        layout.add_widget(self.dni_input)
        layout.add_widget(self.status_input)

        save_btn = Button(text="Guardar", on_press=self.save_student)
        layout.add_widget(save_btn)

        self.add_widget(layout)

    def save_student(self, instance):
        student = Student(
            id=None,
            name=self.name_input.text,
            email=self.email_input.text,
            dni=self.dni_input.text,
            status=self.status_input.text
        )
        repo.upsert_student(student)
        self.manager.current = "estudiantes"

