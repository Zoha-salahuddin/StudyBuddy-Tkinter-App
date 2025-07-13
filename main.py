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
root.geometry("320x280")  # 🎯 Slightly bigger 
root.configure(bg="#f0f4f7")  # 🎨 Soft background color

# Interface
tk.Label(root, text="📚 Welcome to StudyBuddy!", font=("Helvetica", 16, "bold"), bg="#f0f4f7").pack(pady=20)

# 🟦 Updated Buttons with wider layout and padding
button_style = {"width": 20, "font": ("Arial", 12), "padx": 5, "pady": 5}
tk.Button(root, text="✅ Task Manager", command=lambda: open_window(TaskManager), **button_style).pack(pady=5)
tk.Button(root, text="⏱️ Study Timer", command=lambda: open_window(Timer), **button_style).pack(pady=5)
tk.Button(root, text="📝 Quick Notes", command=lambda: open_window(Notes), **button_style).pack(pady=5)

# Start the GUI event loop
root.mainloop()
