# screens/courses.py

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.metrics import dp

from data.repository import SQLiteRepository
from data.models import Student, Course, Enrollment

repo = SQLiteRepository()

class CursosScreen(Screen):
    # Lista de respaldo (si la BD está vacía)
    fallback_courses = [
        "ZUMBA",
        "XP - LOAD",
        "TEATRO ADOLESCENTES +12",
        "TEATRO ADULTOS +18",
        "DANZA FOLKLÓRICAS",
        "CONTEMPORÁNEA INFANTIL 8 a 12 años",
        "CONTEMPORÁNEA JÓVENES 13 a 30 años",
        "CONTEMPORÁNEA ADULTOS +30",
        "BALLET DANZA CONTEMPORÁNEA 12 A 30",
        "RUMBA TERAPIA",
        "--- TALLERES / INTENSIVOS ---",
        "RITMOS Y ESTILOS COMERCIALES",
        "ACROTELA ADULTOS",
        "YOGA MAÑANA",
        "YOGA TARDE",
        "DANCE COVER KPOP",
        "KPOP FITNESS",
        "YOGA",
        "LA CAJA DE PANDORA",
        "TEATRÍN TRÍN TRÍN",
        "TANGO INTERMEDIO AVANZADO",
        "TANGO INICIAL",
        "FUNCIONAL KIDS",
        "GIMNASIA PARA ADULTOS",
        "DANZA CLÁSICA BABYS",
        "DANZA CLÁSICA INFANTIL",
        "DANZA CONTEMPORÁNEA INFANTIL",
        "DANZA CONTEMPORÁNEA ADULTO",
        "FOLKORE ESTILIZADO",
        "--- TALLERES / INTENSIVOS ---",
        "ACROTELA Grupo 1 - 18:30",
        "ACROTELA Grupo 2 - 19:30",
        "ACROTELA Grupo 3 - 20:00",
        "ACROTELA ADULTOS - 20:30",
    ]

    def on_enter(self):
        """
        Se dispara cada vez que esta pantalla se vuelve current:
        carga cursos desde la BD y genera un botón por cada uno.
        """
        repo = SQLiteRepository()
        courses = repo.list_courses()
        if not courses:
            # Si la BD está vacía, usamos la lista fija sin IDs
            courses = [Course(id=None, title=name, description="") for name in self.fallback_courses]

        container = self.ids.courses_list
        container.clear_widgets()

        for c in courses:
            # Cada curso es un botón con fondo blanco y texto negro
            btn = Button(
                text=c.title,
                size_hint_y=None,
                height=dp(40),
                background_normal='',
                background_color=(1, 1, 1, 1),
                color=(0, 0, 0, 1)
            )
            # Al presionar, mostramos popup con alumnos inscritos
            btn.bind(on_release=lambda btn, course_id=c.id: self.show_students(course_id, btn.text))
            container.add_widget(btn)

    def show_students(self, course_id, course_title):
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.label import Label
        from kivy.uix.button import Button
        from kivy.uix.popup import Popup
        from kivy.metrics import dp
        from kivy.graphics import Color, Rectangle

        # Recolectar inscripciones y estudiantes
        enrollments = repo.list_enrollments()
        student_ids = [e.student_id for e in enrollments if e.course_id == course_id]
        students = [s for s in repo.list_students() if s.id in student_ids]

        # Contenedor raíz con fondo blanco
        content = BoxLayout(orientation='vertical', padding=10, spacing=5)
        with content.canvas.before:
            Color(1, 1, 1, 1)     # blanco
            self._rect = Rectangle(pos=content.pos, size=content.size)
        # Asegurar que el rectángulo siga al widget
        content.bind(pos=lambda inst, val: setattr(self._rect, 'pos', val),
                     size=lambda inst, val: setattr(self._rect, 'size', val))

        # Título
        title = Label(
            text=f"[b]Inscritos en:[/b]\n{course_title}",
            markup=True,
            size_hint_y=None,
            height=dp(40),
            color=(0,0,0,1)
        )
        content.add_widget(title)

        # Lista de estudiantes o mensaje
        if students:
            for s in students:
                lbl = Label(
                    text=f"{s.id}: {s.name}",
                    size_hint_y=None,
                    height=dp(30),
                    color=(0,0,0,1)
                )
                content.add_widget(lbl)
        else:
            content.add_widget(Label(
                text="— No hay inscritos —",
                size_hint_y=None,
                height=dp(30),
                color=(0,0,0,1)
            ))

        # Botón de cerrar, también fondo blanco y texto negro
        close_btn = Button(
            text="Cerrar",
            size_hint_y=None,
            height=dp(40),
            background_normal='',
            background_color=(1,1,1,1),
            color=(0,0,0,1)
        )
        content.add_widget(close_btn)

        popup = Popup(
            title="Estudiantes Inscritos",
            content=content,
            size_hint=(0.8, 0.8),
            background=''  # sin imagen de fondo
        )
        close_btn.bind(on_release=popup.dismiss)
        popup.open()