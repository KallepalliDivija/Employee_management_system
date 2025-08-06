import tkinter as tk
import customtkinter
from tkinter import ttk, messagebox
import mysql.connector

# MySQL Connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Divi@9010",  # Update as needed
    database="employee_db"
)
cursor = conn.cursor()

# App setup
customtkinter.set_appearance_mode("light")
customtkinter.set_default_color_theme("blue")
app = customtkinter.CTk()
app.title("Employee Management System")
app.geometry("1100x650")
app.resizable(0, 0)

# Heading
heading = tk.Label(app, text="Employee Management System", font=("Arial", 24, "bold"), bg="#0B162D", fg="white", pady=10)
heading.pack(fill=tk.X)

# Main frames
main_frame = customtkinter.CTkFrame(app, corner_radius=20, fg_color="#0B162D", width=350)
main_frame.pack(side=tk.LEFT, fill=tk.Y)

right_frame = customtkinter.CTkFrame(app, corner_radius=20, fg_color="white")
right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# --- LEFT FORM FIELDS ---
labels = ["id", "name", "phone", "role", "gender", "salary"]
entries = {}

for i, label in enumerate(labels):
    l = customtkinter.CTkLabel(main_frame, text=label.title(), text_color="white")
    l.grid(row=i, column=0, padx=20, pady=5, sticky="w")

    if label == "role":
        entry = customtkinter.CTkComboBox(main_frame, values=["Web Developer", "Tester", "Manager", "HR", "Software Developer", "Prompt Engineer", "Data Analyst"])
    elif label == "gender":
        entry = customtkinter.CTkComboBox(main_frame, values=["Male", "Female", "Other"])
    else:
        entry = customtkinter.CTkEntry(main_frame, text_color="white", fg_color="#1E2A47", border_color="white")

    entry.grid(row=i, column=1, padx=10, pady=5, sticky="ew")
    entries[label] = entry

# --- TreeView ---
columns = ("id", "name", "phone", "role", "gender", "salary")
tree = ttk.Treeview(right_frame, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col.title())
    tree.column(col, width=100)

tree.place(x=20, y=70, width=750, height=500)

# --- CRUD Functions ---
def show_all():
    for i in tree.get_children():
        tree.delete(i)
    cursor.execute("SELECT * FROM employees")
    for row in cursor.fetchall():
        tree.insert('', tk.END, values=row)

def add_employee():
    data = [entries[field].get() for field in columns]
    if any(v.strip() == "" for v in data):
        messagebox.showerror("Error", "Please fill all fields.")
        return
    try:
        cursor.execute("INSERT INTO employees VALUES (%s, %s, %s, %s, %s, %s)", data)
        conn.commit()
        show_all()
        messagebox.showinfo("Success", "Employee added.")
    except mysql.connector.IntegrityError:
        messagebox.showerror("Error", "ID already exists.")

def update_employee():
    data = [entries[field].get() for field in columns]
    if any(v.strip() == "" for v in data):
        messagebox.showerror("Error", "Please fill all fields.")
        return
    cursor.execute("UPDATE employees SET name=%s, phone=%s, role=%s, gender=%s, salary=%s WHERE id=%s",
                   (data[1], data[2], data[3], data[4], data[5], data[0]))
    conn.commit()
    show_all()
    messagebox.showinfo("Success", "Employee updated.")

def delete_employee():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Warning", "Please select an employee to delete.")
        return

    confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this employee?")
    if not confirm:
        return

    values = tree.item(selected[0], "values")
    cursor.execute("DELETE FROM employees WHERE id=%s", (values[0],))
    conn.commit()
    show_all()
    messagebox.showinfo("Deleted", "Employee details have been deleted successfully.")


def delete_all():
    confirm = messagebox.askyesno("Confirm", "Are you sure to delete all employees?")
    if confirm:
        cursor.execute("DELETE FROM employees")
        conn.commit()
        show_all()

def clear_form():
    for entry in entries.values():
        if isinstance(entry, customtkinter.CTkComboBox):
            entry.set("")
        else:
            entry.delete(0, tk.END)

# --- Search ---
def search_employee():
    col = search_by.get()
    val = search_value.get()
    if col == "" or val.strip() == "":
        return
    for i in tree.get_children():
        tree.delete(i)
    cursor.execute(f"SELECT * FROM employees WHERE {col} LIKE %s", ('%' + val + '%',))
    for row in cursor.fetchall():
        tree.insert('', tk.END, values=row)

# --- TreeView selection to form ---
def fill_form(event):
    selected = tree.selection()
    if not selected:
        return
    values = tree.item(selected[0], "values")
    for i, field in enumerate(columns):
        if isinstance(entries[field], customtkinter.CTkComboBox):
            entries[field].set(values[i])
        else:
            entries[field].delete(0, tk.END)
            entries[field].insert(0, values[i])

tree.bind("<<TreeviewSelect>>", fill_form)

# --- Buttons ---
button_frame = customtkinter.CTkFrame(main_frame, fg_color="transparent")
button_frame.grid(row=6, columnspan=2, pady=20)

customtkinter.CTkButton(button_frame, text="New Employee", command=clear_form).grid(row=0, column=0, padx=5)
customtkinter.CTkButton(button_frame, text="Add Employee", command=add_employee).grid(row=0, column=1, padx=5)
customtkinter.CTkButton(button_frame, text="Update Employee", command=update_employee).grid(row=0, column=2, padx=5)
customtkinter.CTkButton(button_frame, text="Delete Employee", command=delete_employee).grid(row=1, column=0, padx=5, pady=5)
customtkinter.CTkButton(button_frame, text="Delete All", command=delete_all).grid(row=1, column=1, padx=5, pady=5)

# --- Search Layout ---
search_by = customtkinter.CTkComboBox(right_frame, values=list(columns), width=120)
search_by.place(x=50, y=20)

search_value = customtkinter.CTkEntry(right_frame, width=150)
search_value.place(x=180, y=20)

customtkinter.CTkButton(right_frame, text="Search", command=search_employee, width=80).place(x=340, y=20)
customtkinter.CTkButton(right_frame, text="Show All", command=show_all, width=80).place(x=430, y=20)

# --- Launch App ---
show_all()
app.mainloop()
