# screens/invoices.py

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.metrics import dp
from kivy.graphics import Color, Rectangle

from data.repository import SQLiteRepository

repo = SQLiteRepository()

class DueScreen(Screen):
    def on_enter(self):
        container = self.ids.container
        container.clear_widgets()
        repo = SQLiteRepository()

        for s in repo.list_students():
            # Mes en curso
            sub, rec, tot = repo.calculate_due_for_student(s.dni)
            # Mes siguiente
            next_sub, next_rec, next_tot = repo.calculate_next_month_due_for_student(s.dni)

            # Mostrar ambas líneas o combinarlas como prefieras:
            info = (
                f"{s.name} — Hoy: ${tot:.2f} "
                f"(base ${sub:.2f} + rec ${rec:.2f})\n"
                f"1/Próx: ${next_tot:.2f} "
                f"(base ${next_sub:.2f} + rec ${next_rec:.2f})"
            )

            
            row = Label(text=info, size_hint_y=None, height=60, color=(0,0,0,1))
            with row.canvas.before:
                Color(1,1,1,1)
                rect = Rectangle(pos=row.pos, size=row.size)
            row.bind(pos=lambda i, v, r=rect: setattr(r, 'pos', v),
                     size=lambda i, v, r=rect: setattr(r, 'size', v))
            container.add_widget(row)