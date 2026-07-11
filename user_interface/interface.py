import customtkinter as tk
from customtkinter import filedialog
import os
import sys

class ConsoleSelect(tk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(0, weight=1, uniform="systems")
        self.grid_columnconfigure(1, weight=1, uniform="systems")
        self.grid_columnconfigure(2, weight=1, uniform="systems")
        self.grid_columnconfigure(3, weight=1, uniform="systems")

        nintendo_frame = tk.CTkFrame(self)
        nintendo_frame.grid_columnconfigure(1, weight=1, uniform="nintendo")
        nintendo_frame.grid_columnconfigure(2, weight=1, uniform="nintendo")
        nintendo_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=10)

        nintendo_label = tk.CTkLabel(nintendo_frame, text="Nintendo", font=("Arial", 20))
        nintendo_label.grid(row=0, column=1, pady=20, columnspan=2, sticky="ew")

        nintendo_consoles = ["NES", "SNES", "N64", "GameCube", "Wii", "Wii U", "Switch",
                             "GB", "GBC", "GBA", "NDS", "3DS"]
        count = 1
        column_position = 1
        for index, console in enumerate(nintendo_consoles):
            if count == 7:
                count = 1
                column_position += 1
            checkbox = tk.CTkCheckBox(nintendo_frame, text=console, onvalue="on", offvalue="off")
            checkbox.grid(row=count, column=column_position, padx=30, pady=3, sticky="w")
            count += 1

        sony_frame = tk.CTkFrame(self)
        sony_frame.grid_columnconfigure(1, weight=1, uniform="sony")
        sony_frame.grid_columnconfigure(2, weight=1, uniform="sony")
        sony_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=10)

        sony_label = tk.CTkLabel(sony_frame, text="Sony") 
        sony_label.grid(row=0, column=1, pady=20, columnspan=2, sticky="ew")

        sony_consoles = ["PS1", "PS2", "PS3", "PSP"]
        count = 1
        column_position = 1
        for index, console in enumerate(sony_consoles):
            if count == 7:
                count = 1
                column_position += 1
            checkbox = tk.CTkCheckBox(sony_frame, text=console, onvalue="on", offvalue="off")
            checkbox.grid(row=count, column=column_position, padx=30, pady=3, sticky="w")

        sega_frame = tk.CTkFrame(self)
        sega_frame.grid(row=0, column=2, sticky="nsew", padx=20, pady=10)

        sega_label = tk.CTkLabel(sega_frame, text="Sega") 
        sega_label.grid(row=0, column=2, pady=20)

        sega_consoles = ["SG-1000", "Master System", "Genesis/Mega Drive", "CD", "32X", "Saturn", "Dreamcast"]
        for index, console in enumerate(sega_consoles):
            checkbox = tk.CTkCheckBox(sega_frame, text=console, onvalue="on", offvalue="off")
            checkbox.grid(row=index + 1, column=2, padx=10, pady=3, sticky="w")

        xbox_frame = tk.CTkFrame(self)
        xbox_frame.grid(row=0, column=3, sticky="nsew", padx=20, pady=10)

        xbox_label = tk.CTkLabel(xbox_frame, text="Xbox")
        xbox_label.grid(row=0, column=3, pady=20)



class App(tk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Steam ROM Scraper")
        self.geometry("1500x900-1720+300")

        self.bind("<\\>", self.reload_window)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.console_select = ConsoleSelect(master=self)
        self.console_select.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

    def select_file():
        filename = filedialog.askopenfilename()
        print(filename)

    def reload_window(self, event=None):
        os.execv(sys.executable, [sys.executable] + sys.argv)

app = App()
app.mainloop()