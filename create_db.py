import mysql.connector

con = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Divi@9010"  # change this to your MySQL password
)

cursor = con.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS employee_db")
cursor.execute("USE employee_db")

cursor.execute("""
CREATE TABLE IF NOT EXISTS employees (
    id INT PRIMARY KEY,
    name VARCHAR(100),
    phone VARCHAR(15),
    role VARCHAR(50),
    gender VARCHAR(10),
    salary FLOAT
)
""")

con.commit()
cursor.close()
con.close()
print("Database and table created successfully.")
