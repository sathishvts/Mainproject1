
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
from datetime import datetime
import csv
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import os

#  DATABASE 
conn = sqlite3.connect("inventory.db")
cur = conn.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS inventory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    sku TEXT,
    category TEXT,
    price REAL,
    quantity INTEGER,
    expiry TEXT
)
""")
conn.commit()

# ---------- MAIN CLASS ----------
class InventoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Management System")

        # --------- Variables ---------
        self.name = tk.StringVar()
        self.sku = tk.StringVar()
        self.category = tk.StringVar()
        self.price = tk.DoubleVar()
        self.quantity = tk.IntVar()
        self.expiry = tk.StringVar()

        self.low_stock_threshold = 5

        self.create_form()
        self.create_buttons()
        self.create_tree()
        self.load_data()

    def create_form(self):
        frame = tk.Frame(self.root, padx=10, pady=10)
        frame.pack()

        labels = ["Name", "SKU", "Category", "Price", "Quantity", "Expiry Date (YYYY-MM-DD)"]
        variables = [self.name, self.sku, self.category, self.price, self.quantity, self.expiry]

        for i, (label, var) in enumerate(zip(labels, variables)):
            tk.Label(frame, text=label).grid(row=i, column=0, sticky='e')
            tk.Entry(frame, textvariable=var).grid(row=i, column=1, padx=5, pady=2)

    def create_buttons(self):
        frame = tk.Frame(self.root)
        frame.pack()

        tk.Button(frame, text="Add Product", command=self.add_product).grid(row=0, column=0, padx=5)
        tk.Button(frame, text="Update Product", command=self.update_product).grid(row=0, column=1, padx=5)
        tk.Button(frame, text="Delete Product", command=self.delete_product).grid(row=0, column=2, padx=5)
        tk.Button(frame, text="Export CSV", command=self.export_csv).grid(row=0, column=3, padx=5)
        tk.Button(frame, text="Export PDF", command=self.export_pdf).grid(row=0, column=4, padx=5)

        # Search
        search_frame = tk.Frame(self.root)
        search_frame.pack(pady=5)
        self.search_var = tk.StringVar()
        tk.Entry(search_frame, textvariable=self.search_var, width=30).pack(side='left')
        tk.Button(search_frame, text="Search", command=self.search_products).pack(side='left', padx=5)
        tk.Button(search_frame, text="Clear", command=self.load_data).pack(side='left')

    def create_tree(self):
        self.tree = ttk.Treeview(self.root, columns=("ID", "Name", "SKU", "Category", "Price", "Qty", "Expiry"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)

        self.tree.pack(padx=10, pady=10, fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

    def load_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        cur.execute("SELECT * FROM inventory")
        for row in cur.fetchall():
            tag = 'low' if row[5] < self.low_stock_threshold else ''
            self.tree.insert('', 'end', values=row, tags=(tag,))

        self.tree.tag_configure('low', foreground='red')

    def on_select(self, event):
        selected = self.tree.selection()
        if selected:
            values = self.tree.item(selected[0])['values']
            self.name.set(values[1])
            self.sku.set(values[2])
            self.category.set(values[3])
            self.price.set(values[4])
            self.quantity.set(values[5])
            self.expiry.set(values[6])

    def add_product(self):
        data = (self.name.get(), self.sku.get(), self.category.get(), self.price.get(), self.quantity.get(), self.expiry.get())
        cur.execute("INSERT INTO inventory (name, sku, category, price, quantity, expiry) VALUES (?, ?, ?, ?, ?, ?)", data)
        conn.commit()
        self.load_data()
        self.clear_form()

    def update_product(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Select", "Select a product to update.")
            return
        item_id = self.tree.item(selected[0])['values'][0]
        data = (self.name.get(), self.sku.get(), self.category.get(), self.price.get(), self.quantity.get(), self.expiry.get(), item_id)
        cur.execute("UPDATE inventory SET name=?, sku=?, category=?, price=?, quantity=?, expiry=? WHERE id=?", data)
        conn.commit()
        self.load_data()
        self.clear_form()

    def delete_product(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Select", "Select a product to delete.")
            return
        item_id = self.tree.item(selected[0])['values'][0]
        cur.execute("DELETE FROM inventory WHERE id=?", (item_id,))
        conn.commit()
        self.load_data()
        self.clear_form()

    def clear_form(self):
        self.name.set("")
        self.sku.set("")
        self.category.set("")
        self.price.set(0)
        self.quantity.set(0)
        self.expiry.set("")

    def search_products(self):
        query = self.search_var.get().lower()
        for row in self.tree.get_children():
            self.tree.delete(row)
        cur.execute("SELECT * FROM inventory WHERE LOWER(name) LIKE ? OR LOWER(category) LIKE ?", (f'%{query}%', f'%{query}%'))
        for row in cur.fetchall():
            tag = 'low' if row[5] < self.low_stock_threshold else ''
            self.tree.insert('', 'end', values=row, tags=(tag,))
        self.tree.tag_configure('low', foreground='red')

    def export_csv(self):
        file = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file:
            with open(file, mode='w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["ID", "Name", "SKU", "Category", "Price", "Quantity", "Expiry"])
                cur.execute("SELECT * FROM inventory")
                for row in cur.fetchall():
                    writer.writerow(row)
            messagebox.showinfo("Exported", f"Inventory exported to {file}")

    def export_pdf(self):
        file = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if file:
            c = canvas.Canvas(file, pagesize=A4)
            width, height = A4
            y = height - 50
            c.setFont("Helvetica-Bold", 14)
            c.drawString(50, y, "Inventory Report")
            c.setFont("Helvetica", 10)
            y -= 30
            headers = ["ID", "Name", "SKU", "Category", "Price", "Qty", "Expiry"]
            for i, h in enumerate(headers):
                c.drawString(50 + i * 70, y, h)
            y -= 20

            cur.execute("SELECT * FROM inventory")
            for row in cur.fetchall():
                for i, val in enumerate(row):
                    c.drawString(50 + i * 70, y, str(val))
                y -= 20
                if y < 50:
                    c.showPage()
                    y = height - 50
            c.save()
            messagebox.showinfo("Exported", f"Inventory exported to {file}")

# -RUN 
root = tk.Tk()
app = InventoryApp(root)
root.mainloop()
