import tkinter as tk
from tkinter import ttk
import sqlite3
from tkinter import messagebox

def create_tables():
    connection = sqlite3.connect("interview1.db")
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS invoiceDetails (lineNo INTEGER PRIMARY KEY, productName TEXT, UnitNo INTEGER, price REAL, quantity REAL, total REAL, expiryDate TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS unit (unitNo INTEGER PRIMARY KEY, unitName TEXT)")
    connection.commit()
    connection.close()

def insert_invoice(line_no, product_name, unit_no, price, quantity, total, expiry_date):
    connection = sqlite3.connect("interview1.db")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO invoiceDetails (lineNo, productName, UnitNo, price, quantity, total, expiryDate) VALUES (?, ?, ?, ?, ?, ?, ?)",
                   (line_no, product_name, unit_no, price, quantity, total, expiry_date))
    connection.commit()
    connection.close()
    messagebox.showinfo("Success", "Invoice inserted successfully")

def update_invoice(line_no, product_name, unit_no, price, quantity, total, expiry_date):
    connection = sqlite3.connect("interview1.db")
    cursor = connection.cursor()
    cursor.execute("UPDATE invoiceDetails SET productName=?, UnitNo=?, price=?, quantity=?, total=?, expiryDate=? WHERE lineNo=?",
                   (product_name, unit_no, price, quantity, total, expiry_date, line_no))
    connection.commit()
    connection.close()
    messagebox.showinfo("Success", "Invoice updated successfully")

def display_invoices(filter_criteria=""):
    connection = sqlite3.connect("interview1.db")
    cursor = connection.cursor()
    query = """
        SELECT invoiceDetails.lineNo, invoiceDetails.productName, unit.unitName, invoiceDetails.price, 
               invoiceDetails.quantity, invoiceDetails.total, invoiceDetails.expiryDate
        FROM invoiceDetails
        JOIN unit ON invoiceDetails.UnitNo = unit.unitNo
    """
    if filter_criteria:
        query += f" WHERE productName LIKE '%{filter_criteria}%'"
    cursor.execute(query)
    records = cursor.fetchall()
    connection.close()

    display_window = tk.Toplevel(root)
    display_window.title("Invoice Details")
    display_window.configure(bg=gradient_color)

    tree = ttk.Treeview(display_window, columns=("lineNo", "productName", "unitName", "price", "quantity", "total", "expiryDate"), show="headings")
    tree.heading("lineNo", text="Line No")
    tree.heading("productName", text="Product Name")
    tree.heading("unitName", text="Unit Name")
    tree.heading("price", text="Price")
    tree.heading("quantity", text="Quantity")
    tree.heading("total", text="Total")
    tree.heading("expiryDate", text="Expiry Date")

    for record in records:
        tree.insert("", "end", values=record)

    tree.pack(expand=True, fill=tk.BOTH)

    filter_frame = tk.Frame(display_window, bg=gradient_color)
    filter_frame.pack(fill=tk.X, pady=10)

    tk.Label(filter_frame, text="Filter by Product Name:", bg=gradient_color).pack(side=tk.LEFT, padx=5)
    filter_entry = tk.Entry(filter_frame)
    filter_entry.pack(side=tk.LEFT, padx=5)
    filter_button = tk.Button(filter_frame, text="Filter", command=lambda: display_invoices(filter_entry.get()))
    filter_button.pack(side=tk.LEFT, padx=5)

def display_units():
    connection = sqlite3.connect("interview1.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM unit")
    records = cursor.fetchall()
    connection.close()

    display_window = tk.Toplevel(root)
    display_window.title("Unit Details")
    display_window.configure(bg=gradient_color)

    tree = ttk.Treeview(display_window, columns=("unitNo", "unitName"), show="headings")
    tree.heading("unitNo", text="Unit No")
    tree.heading("unitName", text="Unit Name")

    for record in records:
        tree.insert("", "end", values=record)

    tree.pack(expand=True, fill=tk.BOTH)

def show_frame(frame):
    frame.tkraise()

def open_invoice_window():
    invoice_window = tk.Toplevel(root)
    invoice_window.title("Add/Update Invoice")
    invoice_window.configure(bg=gradient_color)

    frame = tk.Frame(invoice_window, bg=gradient_color)
    frame.pack(pady=10)

    tk.Label(frame, text="Line No:", bg=gradient_color).grid(row=0, column=0, pady=2, padx=5, sticky='w')
    line_no_entry = tk.Entry(frame)
    line_no_entry.grid(row=0, column=1, pady=2, padx=5)

    tk.Label(frame, text="Product Name:", bg=gradient_color).grid(row=1, column=0, pady=2, padx=5, sticky='w')
    product_name_entry = tk.Entry(frame)
    product_name_entry.grid(row=1, column=1, pady=2, padx=5)

    tk.Label(frame, text="Unit No:", bg=gradient_color).grid(row=2, column=0, pady=2, padx=5, sticky='w')
    unit_no_entry = tk.Entry(frame)
    unit_no_entry.grid(row=2, column=1, pady=2, padx=5)

    tk.Label(frame, text="Price:", bg=gradient_color).grid(row=3, column=0, pady=2, padx=5, sticky='w')
    price_entry = tk.Entry(frame)
    price_entry.grid(row=3, column=1, pady=2, padx=5)

    tk.Label(frame, text="Quantity:", bg=gradient_color).grid(row=4, column=0, pady=2, padx=5, sticky='w')
    quantity_entry = tk.Entry(frame)
    quantity_entry.grid(row=4, column=1, pady=2, padx=5)

    tk.Label(frame, text="Total:", bg=gradient_color).grid(row=5, column=0, pady=2, padx=5, sticky='w')
    total_entry = tk.Entry(frame)
    total_entry.grid(row=5, column=1, pady=2, padx=5)

    tk.Label(frame, text="Expiry Date (YYYY-MM-DD):", bg=gradient_color).grid(row=6, column=0, pady=2, padx=5, sticky='w')
    expiry_date_entry = tk.Entry(frame)
    expiry_date_entry.grid(row=6, column=1, pady=2, padx=5)

    def insert_callback():
        if not all([line_no_entry.get(), product_name_entry.get(), unit_no_entry.get(), price_entry.get(), quantity_entry.get(), total_entry.get(), expiry_date_entry.get()]):
            messagebox.showwarning("Warning", "All fields must be filled")
        else:
            insert_invoice(line_no_entry.get(), product_name_entry.get(), unit_no_entry.get(), price_entry.get(), quantity_entry.get(), total_entry.get(), expiry_date_entry.get())

    def update_callback():
        if not all([line_no_entry.get(), product_name_entry.get(), unit_no_entry.get(), price_entry.get(), quantity_entry.get(), total_entry.get(), expiry_date_entry.get()]):
            messagebox.showwarning("Warning", "All fields must be filled")
        else:
            update_invoice(line_no_entry.get(), product_name_entry.get(), unit_no_entry.get(), price_entry.get(), quantity_entry.get(), total_entry.get(), expiry_date_entry.get())

    button_frame = tk.Frame(invoice_window, bg=gradient_color)
    button_frame.pack(pady=10)

    insert_button = tk.Button(button_frame, text="Insert Invoice", command=insert_callback)
    update_button = tk.Button(button_frame, text="Update Invoice", command=update_callback)
    insert_button.pack(side=tk.LEFT, padx=5, ipadx=10, ipady=10)
    update_button.pack(side=tk.LEFT, padx=5, ipadx=10, ipady=10)

root = tk.Tk()
root.title("Interview GUI")
root.geometry("230x400")

gradient_color ="#FBF4F4"  # Light blue color for gradient background

root.configure(bg=gradient_color)

create_tables()

# Create frames for each page
home_frame = tk.Frame(root, bg=gradient_color)
invoice_frame = tk.Frame(root, bg=gradient_color)

for frame in (home_frame, invoice_frame):
    frame.grid(row=0, column=0, sticky='nsew')

# Home Page
home_button = tk.Button(home_frame, text="Home Page", command=lambda: show_frame(home_frame), bg="blue", fg="white", font=("Helvetica", 14, "bold"))
invoice_list_button = tk.Button(home_frame, text="Invoice List", command=lambda: display_invoices(), bg="lightblue", font=("Helvetica", 12))
add_invoice_button = tk.Button(home_frame, text="Add/Update Invoice", command=open_invoice_window, bg="lightblue", font=("Helvetica", 12))
unit_details_button = tk.Button(home_frame, text="Unit Details", command=display_units, bg="lightblue", font=("Helvetica", 12))

home_button.pack(pady=10, ipadx=10, ipady=10)
invoice_list_button.pack(pady=10, ipadx=10, ipady=10)
add_invoice_button.pack(pady=10, ipadx=10, ipady=10)
unit_details_button.pack(pady=10, ipadx=10, ipady=10)

# Signature Label
signature_label = tk.Label(root, text="Ahmed Einshouka", bg=gradient_color, fg="black", font=("Helvetica", 10))
signature_label.place(relx=1.0, rely=1.0, anchor='se', x=-10, y=-10)

show_frame(home_frame)  # Start with the home page

root.mainloop()
