import customtkinter as tk
from customtkinter import filedialog
import os
import sys

class ConsoleSelect(tk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.selected_consoles = []

        def select_checkbox(box_widget):
            if box_widget.get() == "on":
                self.selected_consoles.append(box_widget.cget('text'))
            if box_widget.get() == "off":
                self.selected_consoles.remove(box_widget.cget('text'))

        self.grid_columnconfigure(0, weight=1, uniform="systems")
        self.grid_columnconfigure(1, weight=1, uniform="systems")
        self.grid_columnconfigure(2, weight=1, uniform="systems")
        self.grid_columnconfigure(3, weight=1, uniform="systems")

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)

        publishers = {
            "Nintendo": ["NES", "SNES", "N64", "GameCube", "Wii", "Wii U", "Switch",
                        "GB", "GBC", "GBA", "NDS", "3DS"],
            "Sony": ["PS1", "PS2", "PS3", "PSP"],
            "Sega": ["SG-1000", "SMS", "Genesis", "CD", "32X", "Saturn", "Dreamcast"],
            "Xbox": ["Xbox", "Xbox 360"]
        }

        for index, publisher in enumerate(publishers):
            frame = tk.CTkFrame(self)
            frame.grid_columnconfigure(1, weight=1, uniform="uniform")
            frame.grid_columnconfigure(2, weight=1, uniform="uniform")
            frame.grid(row=1, column=index, sticky="nsew", padx=20, pady=10)

            label = tk.CTkLabel(frame, text=publisher, font=("", 20))
            label.grid(row=0, column=1, pady=20, columnspan=2)

            count = 1
            column_position = 1
            for index, console in enumerate(publishers[publisher]):
                if count == 7:
                    count = 1
                    column_position += 1
                checkbox = tk.CTkCheckBox(frame, text=console, onvalue="on", offvalue="off")
                checkbox.configure(command=lambda box=checkbox: select_checkbox(box))
                checkbox.grid(row=count, column=column_position, padx=30, pady=3, sticky="w")
                count += 1
        
        continue_btn = tk.CTkButton(self, text="Continue", height=40, command=self.next_screen)
        continue_btn.grid(row=3, column=1, columnspan=2, sticky="ew")
    
    def next_screen(self):
        self.master.next_frame(FolderSelect, selected_consoles=self.selected_consoles)

class FolderSelect(tk.CTkFrame):
    def __init__(self, master, selected_consoles, **kwargs):
        super().__init__(master, **kwargs)
        self.selected_consoles = selected_consoles

        def emulation_paths_to_get():
            emulators_to_return = []

            retroarch_consoles = [
                "NES", "SNES", "N64", "GB", "GBC", "GBA", "PS1", "PS2", "PS3", "PSP",
                "SG-1000", "SMS", "Genesis", "CD", "32X", "Saturn", "Dreamcast"
            ]

            for console in self.selected_consoles:
                if console in retroarch_consoles:
                    emulators_to_return.append("RetroArch")
            
            if "PS2" in self.selected_consoles:
                emulators_to_return.append("PCSX2")
            if "PS3" in self.selected_consoles:
                emulators_to_return.append("RPCS3")
            if "PSP" in self.selected_consoles:
                emulators_to_return.append("PPSSPP")
            if "Xbox" in self.selected_consoles:
                emulators_to_return.append("Xemu")
            if "Xbox 360" in self.selected_consoles:
                emulators_to_return.append("Xenia")
            if "GameCube" in self.selected_consoles or "Wii" in self.selected_consoles:
                emulators_to_return.append("Dolphin")
            if "Wii U" in self.selected_consoles:
                emulators_to_return.append("Cemu")
            if "Switch" in self.selected_consoles:
                emulators_to_return.append("Eden")
            

        def select_file(entry_widget):
            filename = filedialog.askopenfilename()
            if filename != "":
                filename_widget = tk.StringVar(value=filename)
                entry_widget.configure(textvariable=filename_widget)

        self.grid_columnconfigure([0, 1, 2, 3], weight=1)
        self.grid_rowconfigure([0, 1, 2, 3, 4, 5, 6], weight=1)

        folder_selection = tk.CTkFrame(self)
        folder_selection.grid_columnconfigure([0, 1, 2, 3], weight=1)
        folder_selection.grid_rowconfigure([0, 1, 2, 3, 4, 5], weight=1)

        folder_selection.grid(row=1, rowspan=3, column=1, columnspan=2, sticky="nsew")

        for index, console in enumerate(self.selected_consoles):
            label = tk.CTkLabel(folder_selection, text=console)
            label.grid(row=index, column=0, sticky="e", padx=20)

            placeholder = tk.StringVar(value=f"Select {console} emulator executable")
            path = tk.CTkEntry(folder_selection, state="disabled", height=10, textvariable=placeholder)
            path.grid(row=index, column=1, columnspan=2, sticky="ew")

            browse_btn = tk.CTkButton(folder_selection, text="Browse", width=40, command=lambda entry=path: select_file(entry))
            browse_btn.grid(row=index, column=3, sticky="w", padx=5)

        btn = tk.CTkButton(self, text="Back", command=self.prev_screen)
        btn.grid(row=4, column=1, padx=20, pady=20, sticky="se")
        btn2 = tk.CTkButton(self, text="Continue")
        btn2.grid(row=4, column=2, padx=20, pady=20, sticky="sw")
    
    def prev_screen(self):
        self.master.next_frame(ConsoleSelect)
        

class App(tk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Steam ROM Scraper")
        self.geometry("1500x900-1720+300")
        self.bind("<\\>", self.reload_window)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.current_screen = ConsoleSelect(self)
        self.current_screen.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
    
    def next_frame(self, next_frame, *args, **kwargs):
        self.current_screen.destroy()
        self.current_screen = next_frame(self, *args, **kwargs)
        self.current_screen.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

    def reload_window(self, event=None):
        os.execv(sys.executable, [sys.executable] + sys.argv)

app = App()
app.mainloop()