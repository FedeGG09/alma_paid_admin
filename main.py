# main.py
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager

# Importa todas las pantallas que llenan tu alma_paid.kv
from screens.DashboardScreen import DashboardScreen
from screens.students import EstudiantesScreen
from screens.courses import CursosScreen        # <— aquí
from screens.enrollments import MatriculasScreen    # tu archivo enrollments.py
from screens.invoices import InvoicesScreen      # invoices.py
from screens.student_form import EstudianteFormScreen
from data.repository import SQLiteRepository      # <— import


class AlmaPaidApp(App):
    def build(self):
        # Carga el kv después de haber importado las clases
        Builder.load_file("alma_paid.kv")
        sm = ScreenManager()
        sm.add_widget(DashboardScreen(name='inicio'))
        sm.add_widget(EstudiantesScreen(name='estudiantes'))
        sm.add_widget(CursosScreen(name='talleres'))
        sm.add_widget(MatriculasScreen(name='inscripciones'))
        sm.add_widget(InvoicesScreen(name='pagos'))
        sm.add_widget(EstudianteFormScreen(name='estudiante_form'))
        return sm


if __name__ == "__main__":
    # 1) Esto cargará tu Excel en SQLite la primera vez:
    SQLiteRepository()  

    # 2) Luego arranca la app:
    AlmaPaidApp().run()