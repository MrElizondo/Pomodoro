import tkinter as tk
import winsound
import sys
import os

icon_path = os.path.join(getattr(sys, '_MEIPASS', 'resources'), 'Tomato.ico')
background_file = os.path.join(getattr(sys, '_MEIPASS', 'resources'), 'Tomato.png')
ding_file = os.path.join(getattr(sys, '_MEIPASS', 'resources'), 'ding.wav')


# Pomodoro timer class
class PomodoroTimer:
    def __init__(self, master):
        self.master = master
        icon_path = os.path.join(getattr(sys, '_MEIPASS', os.path.abspath('resources')), "Tomato.ico")
        self.master.iconbitmap(icon_path)
        self.master.title('Pomodoro Timer')
        self.master.geometry('500x500')

        # Set default values
        self.is_break = False
        self.POMODORO_DURATION = 30
        self.BREAK_DURATION = 5
        self.minutes = self.POMODORO_DURATION
        self.seconds = 0
        self.is_running = False

        # Background image
        self.tomato_img = tk.PhotoImage(file=background_file) # Replace "tomato.png" with the actual path of the image file
        self.tomato_label = tk.Label(self.master, image=self.tomato_img)
        self.tomato_label.place(x=0, y=0, relwidth=1, relheight=1)

        # TODO: add label to show if it's on Pomodoro or break
        # Timer label
        self.timer_label = tk.Label(self.master, font=('Helvetica', 50), text=self.get_timer())
        height = 0.5
        self.timer_label.place(relx=0.5, rely=height, anchor='center')

        # Create buttons
        diff1 = 0.06
        height += diff1
        diff = 0.07
        self.start_button = tk.Button(self.master, text='START POMODORO', command=self.start_pomodoro)
        height += diff
        self.start_button.place(relx=0.5, rely=height, anchor='center')

        self.distracted_button = tk.Button(self.master, text='UPS, I GOT DISTRACTED', command=self.distracted)
        height += diff
        self.distracted_button.place(relx=0.5, rely=height, anchor='center')

        self.stop_button = tk.Button(self.master, text='STOP', command=self.restart_and_stop)
        height += diff
        self.stop_button.place(relx=0.5, rely=height, anchor='center')

        self.break_button = tk.Button(self.master, text='START BREAK', command=self.start_break)
        height += diff
        self.break_button.place(relx=0.5, rely=height, anchor='center')

        # TODO: add buttons or text field to change pomodoro time
        # Start the clock
        self.start()

    def get_timer(self):
        return f'{self.minutes:02d}:{self.seconds:02d}'

    # Update the timer display
    def start(self):
        if self.is_running:
            self.timer_label.config(text=self.get_timer())
            if self.seconds > 0:
                self.seconds -= 1
            else:
                if self.minutes > 0:
                    self.minutes -= 1
                    self.seconds = 59
                else:
                    # FIXME: se reproduce el sonido incorrecto
                    winsound.PlaySound('ding.wav', winsound.SND_FILENAME)
                    if not self.is_break:
                        self.start_break()
                    else:
                        self.stop()
        self.master.after(1000, self.start)

    # Restart the timer
    def restart_and_stop(self):
        self.minutes = self.POMODORO_DURATION
        self.seconds = 0
        self.timer_label.config(text=self.get_timer())
        self.stop()

    # Stop the timer
    def stop(self):
        self.is_running = False
        self.is_break = False
        if hasattr(self, 'start_button') and hasattr(self, 'break_button'):
            self.start_button.config(state=tk.NORMAL)
            self.break_button.config(state=tk.NORMAL)
            self.distracted_button.config(state=tk.NORMAL)

    # Start a pomodoro timer
    def start_pomodoro(self):
        self.stop()
        self.is_running = True
        self.is_break = False
        self.minutes = self.POMODORO_DURATION
        self.seconds = 0
        self.start_button.config(state=tk.DISABLED)
        self.break_button.config(state=tk.NORMAL)
        self.distracted_button.config(state=tk.NORMAL)

    # Handle distraction
    def distracted(self):
        self.stop()
        self.start_pomodoro()

    # Take a break
    def start_break(self):
        self.stop()
        self.is_running = True
        self.is_break = True
        self.minutes = self.BREAK_DURATION
        self.seconds = 0
        self.start_button.config(state=tk.NORMAL)
        self.break_button.config(state=tk.DISABLED)
        self.distracted_button.config(state=tk.DISABLED)


# Create the app window and run the app
root = tk.Tk()
timer = PomodoroTimer(root)
root.mainloop()
