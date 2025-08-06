from customtkinter import *
from PIL import Image
from tkinter import messagebox

def login():
    if usernameEntry.get() == '' or passwordEntry.get() == '':
        messagebox.showerror("Error", "All fields are required")
    elif usernameEntry.get() == 'Divija' and passwordEntry.get() == '1234':
        messagebox.showinfo("Success", "Login Successful")
        root.destroy()
        import main  
    else:
        messagebox.showerror("Error", "Invalid credentials")

# ========== MAIN WINDOW ==========
root = CTk()
root.geometry('930x478')
root.resizable(0, 0)
root.title("Login Page")

# ========== FULL BACKGROUND IMAGE ==========
bg_image = CTkImage(Image.open("cover_page.jpg"), size=(930, 478))
bg_label = CTkLabel(root, image=bg_image, text="")
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# ========== LOGIN FRAME (NAVY BLUE BOX, CENTERED, ROUNDED) ==========
login_frame = CTkFrame(
    master=root,
    width=280,
    height=300,
    fg_color="#02173B",     # Dark navy blue
    
    corner_radius=25
)
login_frame.place(x=700, y=200, anchor="center")

# ========== "Login" Heading ==========
heading = CTkLabel(
    login_frame,
    text="  Employement Portal Login  ",
    font=("Goudy Old Style", 22, "bold"),
    text_color="white"
)
heading.pack(pady=(25, 20))

# ========== USERNAME FIELD ==========
usernameEntry = CTkEntry(
    login_frame,
    placeholder_text="Enter Your Username",
    font=("Goudy Old Style", 16),
    width=280,
    corner_radius=15,
    text_color="black",              # Text typed by user
    placeholder_text_color="gray",  # Placeholder text
    fg_color="white"                # Background color of entry
)
usernameEntry.pack(pady=10)

passwordEntry = CTkEntry(
    login_frame,
    placeholder_text="Enter Your Password",
    show="*",
    font=("Goudy Old Style", 16),
    width=280,
    corner_radius=15,
    text_color="black",
    placeholder_text_color="gray",
    fg_color="white"
)
passwordEntry.pack(pady=10)


# ========== LOGIN BUTTON ==========
loginButton = CTkButton(
    login_frame,
    text="Login",
    font=("Goudy Old Style", 14, "bold"),
    width=120,
    height=35,
    corner_radius=10,
    fg_color="#2C73D2",    # Blue
    hover_color="#1A5CA2",
    command=login
)
loginButton.pack(pady=20)

# ========== MAINLOOP ==========
root.mainloop()
