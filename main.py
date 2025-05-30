# main.py

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager

# Importa todas las pantallas antes de cargar el KV
from screens.DashboardScreen import DashboardScreen
from screens.students import EstudiantesScreen
from screens.courses import CursosScreen
from screens.enrollments import MatriculasScreen
from screens.invoices import DueScreen            # Clase renombrada a DueScreen
from screens.student_form import EstudianteFormScreen

# No hace falta guardar esta instancia, solo inicializa la base
from data.repository import SQLiteRepository      

class AlmaPaidApp(App):
    def build(self):
        # 1) Carga el archivo .kv con todas las reglas de UI
        Builder.load_file("alma_paid.kv")

        # 2) Construye el ScreenManager y registra cada pantalla
        sm = ScreenManager()
        sm.add_widget(DashboardScreen(name='inicio'))
        sm.add_widget(EstudiantesScreen(name='estudiantes'))
        sm.add_widget(CursosScreen(name='talleres'))
        sm.add_widget(MatriculasScreen(name='inscripciones'))
        sm.add_widget(DueScreen(name='pagos'))
        sm.add_widget(EstudianteFormScreen(name='estudiante_form'))
        return sm

if __name__ == "__main__":
    # Inicializa la base de datos (carga Excel, tablas, migraciones, etc.)
    SQLiteRepository()

    # Ejecuta la app Kivy
    AlmaPaidApp().run()
