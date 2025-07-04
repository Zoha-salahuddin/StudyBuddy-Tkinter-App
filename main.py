import tkinter as tk
from task_manager import TaskManager
from timer import Timer
from notes import Notes

def open_window(module_class):
    module_window = tk.Toplevel(root)
    module_instance = module_class(module_window)

# Main application window
root = tk.Tk()
root.title("StudyBuddy")
root.geometry("300x250")

# Interface
tk.Label(root, text="Welcome to StudyBuddy!", font=("Arial", 16)).pack(pady=20)
tk.Button(root, text="Task Manager", command=lambda: open_window(TaskManager)).pack(pady=5)
tk.Button(root, text="Study Timer", command=lambda: open_window(Timer)).pack(pady=5)
tk.Button(root, text="Quick Notes", command=lambda: open_window(Notes)).pack(pady=5)

# Start the GUI event loop
root.mainloop()
