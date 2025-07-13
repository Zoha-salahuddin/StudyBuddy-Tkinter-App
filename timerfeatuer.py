import tkinter as tk

def Timer(root):
    root.title("Study Timer")
    root.geometry("260x220")
    root.configure(bg="#f0f4f7")

    time_left = [1500]  # 25 minutes in seconds

    # Label to display the timer
    timer_label = tk.Label(root, text="25:00", font=("Helvetica", 32), bg="#f0f4f7", fg="#333")
    timer_label.pack(pady=30)

    # Countdown logic
    def countdown():
        if time_left[0] > 0:
            time_left[0] -= 1
            mins, secs = divmod(time_left[0], 60)
            timer_label.config(text=f"{mins:02}:{secs:02}")
            root.after(1000, countdown)

    # Start button
    start_button = tk.Button(
        root,
        text="▶ Start",
        font=("Arial", 12),
        bg="#ffffff",
        width=12,
        relief="raised",
        command=countdown
    )
    start_button.pack(pady=10)
