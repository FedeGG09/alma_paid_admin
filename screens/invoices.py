# screens/invoices.py
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, ListProperty
from data.repository import SQLiteRepository
from data.models import Invoice

repo = SQLiteRepository()

class InvoicesScreen(Screen):
    rv = ObjectProperty()
    invoices = ListProperty([])

    def on_enter(self):
        self.refresh_list()

    def refresh_list(self):
        self.invoices = repo.list_invoices()
        self.rv.data = [
            {
                "dni": inv.dni,
                "total": f"{inv.total:.2f}",
                "surcharge": f"{inv.surcharge:.2f}",
                "status": inv.status
            }
            for inv in self.invoices
        ]
