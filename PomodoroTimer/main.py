from tkinter import *
import math

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0
timer = None
timer_running = False

# ---------------------------- TIMER RESET ------------------------------- #
def reset_timer():
    global reps, timer_running
    window.after_cancel(timer)
    canvas.itemconfig(time_face, text="00:00")
    time_label.config(text="Timer")
    check_label.config(text="")
    reps = 0
    timer_running = False

# ---------------------------- TIMER MECHANISM ------------------------------- #
def start_timer():
    global reps, timer_running
    if not timer_running:
        reps += 1
        timer_running = True

        work_sec = WORK_MIN * 60
        short_break_sec = SHORT_BREAK_MIN * 60
        long_break_sec = LONG_BREAK_MIN * 60

        if reps % 8 == 0:
            count_down(long_break_sec)
            time_label.config(text='Break', fg=RED)
        elif reps % 2 == 0:
            count_down(short_break_sec)
            time_label.config(text='Break', fg=PINK)
        else:
            count_down(work_sec)
            time_label.config(text='Work', fg=GREEN)

# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(count):
    global timer, timer_running

    count_min = math.floor(count / 60)
    count_sec = count % 60
    if count_sec < 10:
        count_sec = f"0{count_sec}"
    canvas.itemconfig(time_face, text=f"{count_min}:{count_sec}")
    if count > 0 and timer_running:
        timer = window.after(1000, count_down, count - 1)
        if count == 5 * 60 and reps % 2 != 0:  # 5 minutes left in a work period
            show_window("5 minutes remaining!")
    else:
        timer_running = False
        if count == 0:
            if reps % 2 == 0:  # Break ends
                show_window("Break is over! Time to work.")
            start_timer()
            marks = ""
            work_sessions = math.floor(reps / 2)
            for _ in range(work_sessions):
                marks += "✔"
            check_label.config(text=marks)

# ---------------------------- SHOW MAIN WINDOW ------------------------------- #
def show_window(message):
    window.lift()  # Bring the main window to the front
    window.attributes("-topmost", True)  # Keep it on top
    window.after_idle(window.attributes, "-topmost", False)  # Allow other windows to be on top again
    time_label.config(text=message)

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=YELLOW)

time_label = Label(text="Timer", bg=YELLOW, fg=GREEN, font=(FONT_NAME, 35, "bold"))
time_label.grid(column=1, row=0)

check_label = Label(bg=YELLOW, fg=GREEN, font=(FONT_NAME, 20, "bold"))
check_label.grid(column=1, row=3)

start_button = Button(text='START', command=start_timer)
start_button.grid(column=0, row=2)

reset_button = Button(text='RESET', command=reset_timer)
reset_button.grid(column=2, row=2)

canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
tomato_img = PhotoImage(file="tomato.png")
canvas.create_image(100, 112, image=tomato_img)
time_face = canvas.create_text(110, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(column=1, row=1)

window.mainloop()
