from datetime import datetime, timedelta

class InvoiceTracker:
    def categorize_invoices(self, invoices):
        today = datetime.today().date()
        upcoming = today + timedelta(days=7)
        invoices_due = {"due_soon":[], "overdue": []}
        for invoice in invoices:
            due_date = invoice.get("due_date")
            try:
                due_date_dt = datetime.strptime(due_date, "%Y-%m-%d").date()
            except TypeError, ValueError:
                continue # Skip missing or malformed
            if due_date_dt < today:
                invoices_due["overdue"].append(invoice)
            elif today <= due_date_dt <= upcoming:
                invoices_due["due_soon"].append(invoice)
        return invoices_due


invoices = [
    {"id": "INV001", "due_date": "2025-11-10"},
    {"id": "INV002", "due_date": "2025-11-17"},
    {"id": "INV003", "due_date": "2025-11-20"},
    {"id": "INV003", "due_date": "2025-11-30"},
    {"id": "INV004", "due_date": "bad-date"},
    {"id": "INV005"},  # missing due_date
]

it = InvoiceTracker()
result = it.categorize_invoices(invoices)
print(result)