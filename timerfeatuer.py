import tkinter as tk
def Timer(root):
    root.title("Study Timer")
    root.geometry("250x200")
    time_left = [1500]  # 25 mins
    def countdown():
        if time_left[0] > 0:
            time_left[0] -= 1
            mins, secs = divmod(time_left[0], 60)
            label.config(text=f"{mins:02}:{secs:02}")
            root.after(1000, countdown)
    label = tk.Label(root, text="25:00", font=("Helvetica", 30))
    label.pack(pady=20)
    tk.Button(root, text="Start", command=countdown).pack()