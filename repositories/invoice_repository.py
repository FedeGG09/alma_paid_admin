class InvoiceRepository:
    def __init__(self):
        self.invoices = {}

    def get_all_invoices(self):
        return list(self.invoices.values())

    def upsert_invoice(self, invoice):
        self.invoices[invoice.dni] = invoice
