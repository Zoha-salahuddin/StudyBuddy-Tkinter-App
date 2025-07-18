import tkinter as tk
from tkinter import messagebox, Toplevel, Label
import sqlite3
import datetime

def Notes(root):
    root.title("Quick Notes")

    # Set full screen
    try:
        root.state("zoomed")  # Works on Windows
    except:
        root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}")

    dark_mode = {"enabled": False}

    # Themes
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
        if messagebox.askyesno("Confirm", "Clear all notes?"):
            text.delete("1.0", tk.END)

    def toggle_mode():
        nonlocal current_theme
        dark_mode["enabled"] = not dark_mode["enabled"]
        current_theme = dark_theme if dark_mode["enabled"] else light_theme
        apply_theme()

    # Tooltip function
    def create_tooltip(widget, text):
        tooltip = Toplevel(widget)
        tooltip.withdraw()
        tooltip.overrideredirect(True)
        tooltip_label = Label(tooltip, text=text, background="#333", foreground="white", padx=5, pady=2, font=("Segoe UI", 9))
        tooltip_label.pack()

        def enter(event):
            x = event.x_root + 10
            y = event.y_root + 10
            tooltip.geometry(f"+{x}+{y}")
            tooltip.deiconify()

        def leave(event):
            tooltip.withdraw()

        widget.bind("<Enter>", enter)
        widget.bind("<Leave>", leave)

    # Buttons
    button_frame = tk.Frame(root)
    button_frame.grid(row=3, column=0, pady=10)

    save_btn = tk.Button(button_frame, text="💾 Save", command=save_note, padx=12, pady=6)
    save_btn.pack(side="left", padx=8)

    clear_btn = tk.Button(button_frame, text="🧹 Clear", command=clear_note, padx=12, pady=6)
    clear_btn.pack(side="left", padx=8)

    mode_btn = tk.Button(button_frame, text="🌙 Toggle Dark Mode", command=toggle_mode, padx=12, pady=6)
    mode_btn.pack(side="left", padx=8)
    create_tooltip(mode_btn, "Switch between Light and Dark mode")

    # Theme function
    def apply_theme():
        th = current_theme
        root.configure(bg=th["bg"])
        header.configure(bg=th["bg"], fg=th["fg"])
        time_label.configure(bg=th["bg"], fg=th["fg"])
        text.configure(bg=th["text_bg"], fg=th["text_fg"], insertbackground=th["fg"])
        button_frame.configure(bg=th["bg"])
        save_btn.configure(bg=th["btn_bg"], fg=th["btn_fg"], relief="raised", font=("Segoe UI", 10, "bold"))
        clear_btn.configure(bg=th["clear_bg"], fg=th["btn_fg"], relief="raised", font=("Segoe UI", 10, "bold"))

        # 🔄 Updated toggle dark mode button style
        toggle_bg = "#555555" if not dark_mode["enabled"] else "#dddddd"
        toggle_fg = "#ffffff" if not dark_mode["enabled"] else "#000000"
        mode_btn.configure(bg=toggle_bg, fg=toggle_fg, activebackground=th["text_bg"], font=("Segoe UI", 10))

    apply_theme()

    def on_closing():
        conn.close()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)

# Run App
if __name__ == "__main__":
    root = tk.Tk()
    Notes(root)
    root.mainloop()
