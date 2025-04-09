import string
import random
from tkinter import *
from tkinter import messagebox
import sqlite3


with sqlite3.connect("users.db") as db:
    cursor = db.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (Username TEXT NOT NULL, GeneratedPassword TEXT NOT NULL);")
    db.commit()


class PasswordApp:
    def __init__(self, master):
        self.master = master
        self.master.title("SecurePass Vault")
        self.master.geometry("700x420")
        self.master.configure(bg="#1A374D")
        self.master.resizable(False, False)

        self.username = StringVar()
        self.password_length = IntVar()
        self.generated_password = StringVar()

        
        Label(master, text="Secure Password Generator", font=("Helvetica", 20, "bold"), bg="#1A374D", fg="#B1D0E0").pack(pady=15)

       
        form_frame = Frame(master, bg="#406882", padx=20, pady=20, bd=5, relief=GROOVE)
        form_frame.pack(pady=10)

        
        Label(form_frame, text="Username:", font=("Arial", 14), bg="#406882", fg="white").grid(row=0, column=0, sticky=W, pady=5)
        self.username_entry = Entry(form_frame, textvariable=self.username, font=("Arial", 13), width=25)
        self.username_entry.grid(row=0, column=1, pady=5, padx=10)

        
        Label(form_frame, text="Password Length:", font=("Arial", 14), bg="#406882", fg="white").grid(row=1, column=0, sticky=W, pady=5)
        self.length_entry = Entry(form_frame, textvariable=self.password_length, font=("Arial", 13), width=25)
        self.length_entry.grid(row=1, column=1, pady=5, padx=10)

        
        Label(form_frame, text="Generated Password:", font=("Arial", 14), bg="#406882", fg="white").grid(row=2, column=0, sticky=W, pady=5)
        self.password_entry = Entry(form_frame, textvariable=self.generated_password, font=("Arial", 13), fg="#EE6C4D", width=25)
        self.password_entry.grid(row=2, column=1, pady=5, padx=10)

        
        btn_frame = Frame(master, bg="#1A374D")
        btn_frame.pack(pady=20)

        Button(btn_frame, text="Generate", font=("Verdana", 13, "bold"), bg="#B1D0E0", fg="#1A374D", width=15, command=self.generate_password).grid(row=0, column=0, padx=10)
        Button(btn_frame, text="Save", font=("Verdana", 13, "bold"), bg="#6998AB", fg="white", width=15, command=self.save_password).grid(row=0, column=1, padx=10)
        Button(btn_frame, text="Clear", font=("Verdana", 13, "bold"), bg="#F9F7F7", fg="#406882", width=15, command=self.clear_fields).grid(row=0, column=2, padx=10)

    def generate_password(self):
        user = self.username.get()
        length = self.password_length.get()

        if not user:
            messagebox.showerror("Input Error", "Username cannot be empty.")
            return

        if not user.isalpha():
            messagebox.showerror("Input Error", "Username must only contain letters.")
            return

        if length < 6:
            messagebox.showerror("Input Error", "Password length must be at least 6 characters.")
            return

        upper = list(string.ascii_uppercase)
        lower = list(string.ascii_lowercase)
        digits = list(string.digits)
        symbols = list("@#%&()!?")

        u = random.randint(1, length - 3)
        l = random.randint(1, length - 2 - u)
        s = random.randint(1, length - 1 - u - l)
        d = length - u - l - s

        password = random.sample(upper, u) + random.sample(lower, l) + random.sample(symbols, s) + random.sample(digits, d)
        random.shuffle(password)
        final_password = ''.join(password)

        self.generated_password.set(final_password)

    def save_password(self):
        user = self.username.get()
        password = self.generated_password.get()

        if not user or not password:
            messagebox.showerror("Missing Info", "Please generate a password first.")
            return

        with sqlite3.connect("users.db") as db:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM users WHERE Username=?", (user,))
            if cursor.fetchone():
                messagebox.showerror("Duplicate Entry", "Username already exists. Try another.")
                return
            cursor.execute("INSERT INTO users (Username, GeneratedPassword) VALUES (?, ?)", (user, password))
            db.commit()
            messagebox.showinfo("Saved", "Password saved successfully!")

    def clear_fields(self):
        self.username.set("")
        self.password_length.set(0)
        self.generated_password.set("")


if __name__ == "__main__":
    root = Tk()
    app = PasswordApp(root)
    root.mainloop()
