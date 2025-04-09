from tkinter import *
from tkinter import messagebox
import sqlite3 as sql

def add_task():
    task_string = task_field.get().strip()
    if not task_string:
        messagebox.showwarning('Error', 'Task field is empty.')
        return

    if task_string in tasks:
        messagebox.showinfo('Duplicate', 'Task already exists.')
        return

    tasks.append(task_string)
    the_cursor.execute('INSERT INTO tasks (title) VALUES (?)', (task_string,))
    task_field.delete(0, END)
    list_update()

def list_update():
    clear_list()
    for task in tasks:
        task_listbox.insert(END, task)

def delete_task():
    try:
        selected_task = task_listbox.get(task_listbox.curselection())
        if selected_task in tasks:
            tasks.remove(selected_task)
            the_cursor.execute('DELETE FROM tasks WHERE title = ?', (selected_task,))
            list_update()
    except:
        messagebox.showerror('Error', 'No task selected.')

def delete_all_tasks():
    if messagebox.askyesno('Confirm', 'Delete all tasks?'):
        tasks.clear()
        the_cursor.execute('DELETE FROM tasks')
        list_update()

def clear_list():
    task_listbox.delete(0, END)

def close():
    if messagebox.askokcancel("Exit", "Do you really want to exit?"):
        the_connection.commit()
        the_cursor.close()
        guiWindow.destroy()

def retrieve_database():
    tasks.clear()
    for row in the_cursor.execute('SELECT title FROM tasks'):
        tasks.append(row[0])

if __name__ == "__main__":
    guiWindow = Tk()
    guiWindow.title("To-Do List")
    guiWindow.geometry("720x450+500+200")
    guiWindow.resizable(False, False)
    guiWindow.configure(bg="#F6F5F2")  # Soft background

    # Database setup
    the_connection = sql.connect('listOfTasks.db')
    the_cursor = the_connection.cursor()
    the_cursor.execute('CREATE TABLE IF NOT EXISTS tasks (title TEXT)')

    tasks = []

    # Frames & Layout
    functions_frame = Frame(guiWindow, bg="#FFFFFF", bd=2, relief="groove")
    functions_frame.pack(padx=20, pady=20, fill="both", expand=True)

    task_label = Label(
        functions_frame,
        text="TO-DO LIST",
        font=("Helvetica", 20, "bold"),
        bg="#FFFFFF",
        fg="#5D3FD3"
    )
    task_label.pack(pady=(10, 5))

    sub_label = Label(
        functions_frame,
        text="Enter a task below:",
        font=("Arial", 12),
        bg="#FFFFFF",
        fg="#555555"
    )
    sub_label.pack()

    task_field = Entry(
        functions_frame,
        font=("Arial", 14),
        width=40,
        bd=2,
        relief="solid",
        fg="#333333",
        bg="#FAFAFA"
    )
    task_field.pack(pady=10)

    button_frame = Frame(functions_frame, bg="#FFFFFF")
    button_frame.pack(pady=10)

    def styled_btn(text, cmd):
        return Button(
            button_frame,
            text=text,
            width=14,
            font=("Arial", 12, "bold"),
            bg="#5D3FD3",
            fg="white",
            activebackground="#7B68EE",
            activeforeground="white",
            relief="flat",
            command=cmd,
            cursor="hand2"
        )

    styled_btn("Add Task", add_task).grid(row=0, column=0, padx=5, pady=5)
    styled_btn("Remove Task", delete_task).grid(row=0, column=1, padx=5, pady=5)
    styled_btn("Delete All", delete_all_tasks).grid(row=0, column=2, padx=5, pady=5)

    task_listbox = Listbox(
        functions_frame,
        width=60,
        height=10,
        font=("Arial", 12),
        selectmode=SINGLE,
        bd=2,
        relief="ridge",
        bg="#FAFAFA",
        fg="#333333",
        selectbackground="#DDA0DD",
        selectforeground="black"
    )
    task_listbox.pack(pady=(10, 15))

    exit_button = Button(
        functions_frame,
        text="Exit / Close",
        width=42,
        font=("Arial", 12, "bold"),
        bg="#FF6F61",
        fg="white",
        activebackground="#FF826C",
        relief="flat",
        command=close
    )
    exit_button.pack(pady=(0, 10))

    # Load data
    retrieve_database()
    list_update()

    guiWindow.protocol("WM_DELETE_WINDOW", close)
    guiWindow.mainloop()
