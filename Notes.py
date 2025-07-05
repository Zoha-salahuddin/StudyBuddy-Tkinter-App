import tkinter as tk
from tkinter import messagebox
import sqlite3
import datetime

def Notes(root):
    root.title("Quick Notes")
    root.geometry("400x400")

    # --- Theme Config ---
    dark_mode = {"enabled": False}

    light_theme = {
        "bg": "#f0f8ff", "fg": "#000000",
        "btn_bg": "#4caf50", "btn_fg": "white",
        "clear_bg": "#f44336", "text_bg": "white", "text_fg": "black"
    }

    dark_theme = {
        "bg": "#1e1e1e", "fg": "#ffffff",
        "btn_bg": "#388e3c", "btn_fg": "white",
        "clear_bg": "#c62828", "text_bg": "#2e2e2e", "text_fg": "#ffffff"
    }

    current_theme = light_theme

    # --- Grid Config ---
    root.rowconfigure(2, weight=1)
    root.columnconfigure(0, weight=1)

    # Connect to DB
    conn = sqlite3.connect("studybuddy.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS notes (content TEXT)")
    conn.commit()

    # --- Header ---
    header = tk.Label(root, text="📝 Quick Notes", font=("Helvetica", 18, "bold"))
    header.grid(row=0, column=0, pady=(10, 2), sticky="n")

    # --- Time Label ---
    def update_time():
        now = datetime.datetime.now().strftime("%A, %d %B %Y %I:%M %p")
        time_label.config(text=now)
        root.after(60000, update_time)

    time_label = tk.Label(root, font=("Arial", 10))
    time_label.grid(row=1, column=0, pady=(0, 5))
    update_time()

    # --- Text Area ---
    text = tk.Text(root, font=("Arial", 12), wrap='word')
    text.grid(row=2, column=0, sticky="nsew", padx=10, pady=5)

    # Load saved content
    c.execute("SELECT content FROM notes")
    result = c.fetchone()
    if result:
        text.insert(tk.END, result[0])

    # --- Functions ---
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
        theme = current_theme
        root.configure(bg=theme["bg"])
        header.configure(bg=theme["bg"], fg=theme["fg"])
        time_label.configure(bg=theme["bg"], fg=theme["fg"])
        text.configure(bg=theme["text_bg"], fg=theme["text_fg"], insertbackground=theme["fg"])
        button_frame.configure(bg=theme["bg"])
        save_btn.configure(bg=theme["btn_bg"], fg=theme["btn_fg"])
        clear_btn.configure(bg=theme["clear_bg"], fg=theme["btn_fg"])
        mode_btn.configure(bg=theme["bg"], fg=theme["fg"], activebackground=theme["text_bg"])

    # --- Button Frame ---
    button_frame = tk.Frame(root)
    button_frame.grid(row=3, column=0, pady=10)

    save_btn = tk.Button(button_frame, text="💾 Save", command=save_note, padx=12, pady=5)
    save_btn.pack(side="left", padx=5)

    clear_btn = tk.Button(button_frame, text="🧹 Clear", command=clear_note, padx=12, pady=5)
    clear_btn.pack(side="left", padx=5)

    mode_btn = tk.Button(button_frame, text="🌙 Toggle Dark Mode", command=toggle_mode, padx=12, pady=5)
    mode_btn.pack(side="left", padx=5)

    # --- Apply Initial Theme ---
    apply_theme()

# --- Run App ---
# --- Run App ---
if __name__ == "__main__":
    root = tk.Tk()
    Notes(root)
    root.mainloop()
