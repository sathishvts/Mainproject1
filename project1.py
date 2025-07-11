import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import sqlite3
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os

# DATABASE SETUP 
conn = sqlite3.connect("invoices.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS invoices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client TEXT,
    product TEXT,
    quantity INTEGER,
    unit_price REAL,
    subtotal REAL,
    tax REAL,
    total REAL,
    date TEXT
)
""")
conn.commit()

# MAIN APP
class InvoiceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Invoice Generator")

        # Variables
        self.client = tk.StringVar()
        self.product = tk.StringVar()
        self.quantity = tk.IntVar(value=1)
        self.unit_price = tk.DoubleVar(value=0.0)
        self.subtotal = tk.DoubleVar()
        self.tax = tk.DoubleVar()
        self.total = tk.DoubleVar()

        # Form
        self.create_form()

        # Buttons
        self.create_buttons()

    def create_form(self):
        frame = tk.Frame(self.root, padx=10, pady=10)
        frame.pack()

        tk.Label(frame, text="Client Name:").grid(row=0, column=0, sticky='e')
        tk.Entry(frame, textvariable=self.client).grid(row=0, column=1)

        tk.Label(frame, text="Product/Service:").grid(row=1, column=0, sticky='e')
        tk.Entry(frame, textvariable=self.product).grid(row=1, column=1)

        tk.Label(frame, text="Quantity:").grid(row=2, column=0, sticky='e')
        tk.Entry(frame, textvariable=self.quantity).grid(row=2, column=1)

        tk.Label(frame, text="Unit Price:").grid(row=3, column=0, sticky='e')
        tk.Entry(frame, textvariable=self.unit_price).grid(row=3, column=1)

        tk.Label(frame, text="Subtotal:").grid(row=4, column=0, sticky='e')
        tk.Label(frame, textvariable=self.subtotal).grid(row=4, column=1)

        tk.Label(frame, text="Tax (18%):").grid(row=5, column=0, sticky='e')
        tk.Label(frame, textvariable=self.tax).grid(row=5, column=1)

        tk.Label(frame, text="Total:").grid(row=6, column=0, sticky='e')
        tk.Label(frame, textvariable=self.total).grid(row=6, column=1)

    def create_buttons(self):
        frame = tk.Frame(self.root, pady=10)
        frame.pack()

        tk.Button(frame, text="Calculate", command=self.calculate).grid(row=0, column=0, padx=5)
        tk.Button(frame, text="Save Invoice", command=self.save_invoice).grid(row=0, column=1, padx=5)
        tk.Button(frame, text="View Invoices", command=self.view_invoices).grid(row=0, column=2, padx=5)

    def calculate(self):
        qty = self.quantity.get()
        price = self.unit_price.get()
        subtotal = qty * price
        tax = subtotal * 0.18
        total = subtotal + tax

        self.subtotal.set(round(subtotal, 2))
        self.tax.set(round(tax, 2))
        self.total.set(round(total, 2))

    def save_invoice(self):
        self.calculate()
        data = (
            self.client.get(), self.product.get(), self.quantity.get(),
            self.unit_price.get(), self.subtotal.get(), self.tax.get(),
            self.total.get(), datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        cursor.execute("""
            INSERT INTO invoices (client, product, quantity, unit_price, subtotal, tax, total, date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, data)
        conn.commit()

        invoice_id = cursor.lastrowid
        self.generate_pdf(invoice_id)
        messagebox.showinfo("Saved", f"Invoice #{invoice_id} saved and PDF generated!")

    def generate_pdf(self, invoice_id):
        cursor.execute("SELECT * FROM invoices WHERE id=?", (invoice_id,))
        inv = cursor.fetchone()

        file_path = f"Invoice_{invoice_id}.pdf"
        c = canvas.Canvas(file_path, pagesize=A4)
        width, height = A4

        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, height - 50, f"Invoice #{inv[0]}")
        c.setFont("Helvetica", 12)

        c.drawString(50, height - 100, f"Date: {inv[8]}")
        c.drawString(50, height - 130, f"Client Name: {inv[1]}")
        c.drawString(50, height - 160, f"Product/Service: {inv[2]}")
        c.drawString(50, height - 190, f"Quantity: {inv[3]}")
        c.drawString(50, height - 220, f"Unit Price: ₹{inv[4]:.2f}")
        c.drawString(50, height - 250, f"Subtotal: ₹{inv[5]:.2f}")
        c.drawString(50, height - 280, f"Tax (18%): ₹{inv[6]:.2f}")
        c.drawString(50, height - 310, f"Total: ₹{inv[7]:.2f}")

        c.showPage()
        c.save()

        # Print support (Windows only)
        if os.name == "nt":
            os.startfile(file_path, "print")

    def view_invoices(self):
        win = tk.Toplevel(self.root)
        win.title("Invoice Records")

        # Filters
        filter_frame = tk.Frame(win)
        filter_frame.pack(pady=5)
        search_client = tk.StringVar()
        tk.Entry(filter_frame, textvariable=search_client, width=20).pack(side='left')
        tk.Button(filter_frame, text="Search", command=lambda: load_data(search_client.get())).pack(side='left')

        # Treeview
        tree = ttk.Treeview(win, columns=("ID", "Client", "Date", "Total"), show='headings')
        tree.heading("ID", text="ID")
        tree.heading("Client", text="Client")
        tree.heading("Date", text="Date")
        tree.heading("Total", text="Total ₹")
        tree.pack(padx=10, pady=10)

        def load_data(filter_text=""):
            tree.delete(*tree.get_children())
            if filter_text:
                cursor.execute("SELECT id, client, date, total FROM invoices WHERE client LIKE ?", (f'%{filter_text}%',))
            else:
                cursor.execute("SELECT id, client, date, total FROM invoices ORDER BY date DESC")
            for row in cursor.fetchall():
                tree.insert('', 'end', values=row)

        load_data()

# RUN APP 
root = tk.Tk()
app = InvoiceApp(root)
root.mainloop()
