import tkinter as tk
from tkinter import messagebox
import sqlite3
import datetime

def Notes(root):
    root.title("Quick Notes")
    root.geometry("420x480")

    dark_mode = {"enabled": False}

    # Improved themes
    light_theme = {
        "bg": "#ffffff", "fg": "#000000",
        "btn_bg": "#007acc", "btn_fg": "#ffffff",
        "clear_bg": "#d32f2f", "text_bg": "#f9f9f9", "text_fg": "#000000"
    }

    dark_theme = {
        "bg": "#121212", "fg": "#ffffff",
        "btn_bg": "#2196f3", "btn_fg": "#ffffff",
        "clear_bg": "#ff5252", "text_bg": "#1e1e1e", "text_fg": "#ffffff"
    }

    current_theme = light_theme

    root.rowconfigure(2, weight=1)
    root.columnconfigure(0, weight=1)

    # DB setup
    conn = sqlite3.connect("studybuddy.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS notes (content TEXT)")
    conn.commit()

    # Header
    header = tk.Label(root, text="📝 Quick Notes", font=("Segoe UI", 20, "bold"))
    header.grid(row=0, column=0, pady=(10, 2), sticky="n")

    # Time
    def update_time():
        now = datetime.datetime.now().strftime("%A, %d %B %Y %I:%M %p")
        time_label.config(text=now)
        root.after(60000, update_time)

    time_label = tk.Label(root, font=("Segoe UI", 10))
    time_label.grid(row=1, column=0, pady=(0, 5))
    update_time()

    # Text Area
    text = tk.Text(root, font=("Segoe UI", 12), wrap='word', bd=2, relief="groove")
    text.grid(row=2, column=0, sticky="nsew", padx=15, pady=10)

    # Load content
    c.execute("SELECT content FROM notes")
    result = c.fetchone()
    if result:
        text.insert(tk.END, result[0])

    # Functions
    def save_note():
        content = text.get("1.0", tk.END).strip()
        c.execute("DELETE FROM notes")
        c.execute("INSERT INTO notes VALUES (?)", (content,))
        conn.commit()
        messagebox.showinfo("Saved", "Note saved successfully!")

    def clear_note():
        text.delete("1.0", tk.END)

    def toggle_mode():
        nonlocal current_theme
        dark_mode["enabled"] = not dark_mode["enabled"]
        current_theme = dark_theme if dark_mode["enabled"] else light_theme
        apply_theme()

    def apply_theme():
        th = current_theme
        root.configure(bg=th["bg"])
        header.configure(bg=th["bg"], fg=th["fg"])
        time_label.configure(bg=th["bg"], fg=th["fg"])
        text.configure(bg=th["text_bg"], fg=th["text_fg"], insertbackground=th["fg"])
        button_frame.configure(bg=th["bg"])
        save_btn.configure(bg=th["btn_bg"], fg=th["btn_fg"], relief="raised", font=("Segoe UI", 10, "bold"))
        clear_btn.configure(bg=th["clear_bg"], fg=th["btn_fg"], relief="raised", font=("Segoe UI", 10, "bold"))
        mode_btn.configure(bg=th["bg"], fg=th["fg"], activebackground=th["text_bg"], font=("Segoe UI", 10))

    # Buttons
    button_frame = tk.Frame(root)
    button_frame.grid(row=3, column=0, pady=10)

    save_btn = tk.Button(button_frame, text="💾 Save", command=save_note, padx=12, pady=6)
    save_btn.pack(side="left", padx=8)

    clear_btn = tk.Button(button_frame, text="🧹 Clear", command=clear_note, padx=12, pady=6)
    clear_btn.pack(side="left", padx=8)

    mode_btn = tk.Button(button_frame, text="🌙 Toggle Dark Mode", command=toggle_mode, padx=12, pady=6)
    mode_btn.pack(side="left", padx=8)

    apply_theme()

# Run App
if __name__ == "__main__":
    root = tk.Tk()
    Notes(root)
    root.mainloop()
