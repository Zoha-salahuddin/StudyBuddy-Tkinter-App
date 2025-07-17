import tkinter as tk

def Timer(root):
    # Make the window fullscreen or maximized
    root.title("📚 Study Timer")
    root.geometry("600x400")  # You can also use root.attributes("-fullscreen", True)
    root.configure(bg="#e3f2fd")
    root.resizable(True, True)

    time_left = [1500]  # 25 minutes in seconds
    paused = [False]
    timer_running = [False]

    # Title Label
    title_label = tk.Label(root, text="📚 Study Timer", font=("Helvetica", 28, "bold"), bg="#e3f2fd", fg="#0d47a1")
    title_label.pack(pady=(30, 20))

    # Timer Label
    timer_label = tk.Label(root, text="25:00", font=("Helvetica", 64, "bold"), bg="#e3f2fd", fg="#212121")
    timer_label.pack(pady=30)

    # Countdown Function
    def countdown():
        if not paused[0] and time_left[0] > 0:
            time_left[0] -= 1
            mins, secs = divmod(time_left[0], 60)
            timer_label.config(text=f"{mins:02}:{secs:02}")
            root.after(1000, countdown)
        elif time_left[0] == 0:
            timer_label.config(text="🎉 Done!")

    # Button Functions
    def start_timer():
        if not timer_running[0]:
            timer_running[0] = True
            countdown()

    def pause_timer():
        paused[0] = not paused[0]
        if not paused[0]:
            countdown()

    def reset_timer():
        time_left[0] = 1500
        timer_label.config(text="25:00")
        paused[0] = False
        timer_running[0] = False

    def short_break():
        time_left[0] = 300
        timer_label.config(text="05:00")
        paused[0] = False
        countdown()

    # Stylish Button Factory
    def create_button(text, command, bg="#64b5f6", fg="white", hover_bg="#42a5f5"):
        btn = tk.Button(root, text=text, font=("Arial", 14, "bold"), bg=bg, fg=fg, activebackground=hover_bg,
                        width=18, height=2, bd=0, relief="ridge", command=command, cursor="hand2")
        btn.bind("<Enter>", lambda e: btn.config(bg=hover_bg))
        btn.bind("<Leave>", lambda e: btn.config(bg=bg))
        return btn

    # Buttons
    start_button = create_button("▶ Start", start_timer)
    pause_button = create_button("⏸ Pause / Resume", pause_timer, bg="#4db6ac", hover_bg="#26a69a")
    reset_button = create_button("🔁 Reset", reset_timer, bg="#ff8a65", hover_bg="#ff7043")
    break_button = create_button("☕ Short Break", short_break, bg="#9575cd", hover_bg="#7e57c2")

    # Pack buttons
    start_button.pack(pady=8)
    pause_button.pack(pady=8)
    reset_button.pack(pady=8)
    break_button.pack(pady=8)

# Run app
if __name__ == "__main__":
    root = tk.Tk()
    Timer(root)
    root.mainloop()
