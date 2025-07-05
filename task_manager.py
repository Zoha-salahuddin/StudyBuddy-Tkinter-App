import tkinter as tk
import sqlite3

def TaskManager(root):
    root.title("Task Manager")
    root.geometry("300x400")

    conn = sqlite3.connect("studybuddy.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS tasks (task TEXT)")
    conn.commit()

    def add_task():
        task = entry.get()
        if task:
            c.execute("INSERT INTO tasks VALUES (?)", (task,))
            conn.commit()
            listbox.insert(tk.END, task)
            entry.delete(0, tk.END)

    def delete_task():
        selected = listbox.curselection()
        if selected:
            task = listbox.get(selected)
            c.execute("DELETE FROM tasks WHERE task=?", (task,))
            conn.commit()
            listbox.delete(selected)

    listbox = tk.Listbox(root)
    listbox.pack(pady=10)

    c.execute("SELECT task FROM tasks")
    for row in c.fetchall():
        listbox.insert(tk.END, row[0])

    entry = tk.Entry(root)
    entry.pack(pady=5)

    tk.Button(root, text="Add", command=add_task).pack(pady=5)
    tk.Button(root, text="Delete", command=delete_task).pack()


root = tk.Tk()
TaskManager(root)
root.mainloop()