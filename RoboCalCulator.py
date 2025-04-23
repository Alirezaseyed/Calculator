import tkinter as tk
from tkinter import ttk, messagebox
import sympy as sp
import math
import matplotlib.pyplot as plt
import numpy as np
import json
import os
from playsound import playsound
import uuid

class ProCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Pro Calculator")
        self.memory = 0
        self.history = []
        self.language = "en"
        self.sound_enabled = True
        self.decimal_places = 4
        self.mode = "standard"
        self.setup_ui()
        self.bind_keys()

    def setup_ui(self):
        self.style = ttk.Style()
        self.set_theme("light")

        # Notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Frames for tabs
        self.standard_frame = ttk.Frame(self.notebook)
        self.scientific_frame = ttk.Frame(self.notebook)
        self.unit_frame = ttk.Frame(self.notebook)
        self.programmer_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.standard_frame, text="Standard")
        self.notebook.add(self.scientific_frame, text="Scientific")
        self.notebook.add(self.unit_frame, text="Unit Converter")
        self.notebook.add(self.programmer_frame, text="Programmer")

        # Settings and menu
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)
        self.settings_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Settings", menu=self.settings_menu)
        self.settings_menu.add_command(label="Toggle Sound", command=self.toggle_sound)
        self.settings_menu.add_command(label="Change Language (EN/FA)", command=self.toggle_language)
        self.settings_menu.add_command(label="Set Decimal Places", command=self.set_decimal_places)
        self.settings_menu.add_command(label="Save History", command=self.save_history)
        self.settings_menu.add_command(label="Load History", command=self.load_history)
        self.settings_menu.add_command(label="Toggle Fullscreen", command=self.toggle_fullscreen)

        # Standard tab
        self.setup_standard_tab()
        self.setup_scientific_tab()
        self.setup_unit_converter_tab()
        self.setup_programmer_tab()

        # Window settings
        self.root.geometry("800x900")
        self.root.resizable(True, True)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

    def set_theme(self, theme):
        self.theme = theme
        if theme == "light":
            self.style.configure("TButton", font=("Helvetica", 16), background="#f0f0f0", foreground="#000000")
            self.style.configure("TFrame", background="#ffffff")
        else:
            self.style.configure("TButton", font=("Helvetica", 16), background="#333333", foreground="#ffffff")
            self.style.configure("TFrame", background="#1a1a1a")

    def toggle_sound(self):
        self.sound_enabled = not self.sound_enabled
        messagebox.showinfo("Sound", "Sound is now " + ("ON" if self.sound_enabled else "OFF"))

    def toggle_language(self):
        self.language = "fa" if self.language == "en" else "en"
        self.update_ui_texts()

    def set_decimal_places(self):
        places = tk.simpledialog.askinteger("Decimal Places", "Enter number of decimal places (0-10):", minvalue=0, maxvalue=10)
        if places is not None:
            self.decimal_places = places

    def toggle_fullscreen(self):
        self.root.attributes("-fullscreen", not self.root.attributes("-fullscreen"))

    def update_ui_texts(self):
        tabs = ["Standard", "Scientific", "Unit Converter", "Programmer"]
        if self.language == "fa":
            tabs = ["استاندارد", "علمی", "مبدل واحد", "برنامه‌نویسی"]
        for i, tab in enumerate(tabs):
            self.notebook.tab(i, text=tab)

    def setup_standard_tab(self):
        self.result_var = tk.StringVar()
        self.result_entry = ttk.Entry(self.standard_frame, textvariable=self.result_var, font=("Helvetica", 24), justify="right")
        self.result_entry.grid(row=0, column=0, columnspan=5, sticky="nsew", pady=10)

        self.history_var = tk.StringVar(value="History:\n")
        self.history_label = ttk.Label(self.standard_frame, textvariable=self.history_var, font=("Helvetica", 12), anchor="nw", relief="sunken", padding=5)
        self.history_label.grid(row=1, column=0, columnspan=5, sticky="nsew", pady=5)

        buttons = [
            ("C", 2, 0), ("(", 2, 1), (")", 2, 2), ("÷", 2, 3), ("%", 2, 4),
            ("7", 3, 0), ("8", 3, 1), ("9", 3, 2), ("×", 3, 3), ("±", 3, 4),
            ("4", 4, 0), ("5", 4, 1), ("6", 4, 2), ("-", 4, 3), ("M+", 4, 4),
            ("1", 5, 0), ("2", 5, 1), ("3", 5, 2), ("+", 5, 3), ("M-", 5, 4),
            ("0", 6, 0, 2), (".", 6, 2), ("=", 6, 3), ("MR", 6, 4),
            ("MC", 7, 0), ("Theme", 7, 1, 4)
        ]

        for button_info in buttons:
            button_text, row, col = button_info[:3]
            colspan = button_info[3] if len(button_info) > 3 else 1
            button = ttk.Button(self.standard_frame, text=button_text, command=lambda text=button_text: self.handle_button_click(text), style="TButton")
            button.grid(row=row, column=col, columnspan=colspan, sticky="nsew", padx=5, pady=5)

        for i in range(8):
            self.standard_frame.grid_rowconfigure(i, weight=1)
        for i in range(5):
            self.standard_frame.grid_columnconfigure(i, weight=1)

    def setup_scientific_tab(self):
        self.sci_result_var = tk.StringVar()
        ttk.Entry(self.scientific_frame, textvariable=self.sci_result_var, font=("Helvetica", 24), justify="right").grid(row=0, column=0, columnspan=6, sticky="nsew", pady=10)

        buttons = [
            ("C", 2, 0), ("(", 2, 1), (")", 2, 2), ("÷", 2, 3), ("√", 2, 4), ("^", 2, 5),
            ("7", 3, 0), ("8", 3, 1), ("9", 3, 2), ("×", 3, 3), ("sin", 3, 4), ("cos", 3, 5),
            ("4", 4, 0), ("5", 4, 1), ("6", 4, 2), ("-", 4, 3), ("tan", 4, 4), ("log", 4, 5),
            ("1", 5, 0), ("2", 5, 1), ("3", 5, 2), ("+", 5, 3), ("π", 5, 4), ("e", 5, 5),
            ("0", 6, 0, 2), (".", 6, 2), ("=", 6, 3), ("Graph", 6, 4, 2)
        ]

        for button_info in buttons:
            button_text, row, col = button_info[:3]
            colspan = button_info[3] if len(button_info) > 3 else 1
            button = ttk.Button(self.scientific_frame, text=button_text, command=lambda text=button_text: self.handle_button_click(text, "scientific"), style="TButton")
            button.grid(row=row, column=col, columnspan=colspan, sticky="nsew", padx=5, pady=5)

        for i in range(7):
            self.scientific_frame.grid_rowconfigure(i, weight=1)
        for i in range(6):
            self.scientific_frame.grid_columnconfigure(i, weight=1)

    def setup_unit_converter_tab(self):
        self.unit_var = tk.StringVar()
        ttk.Entry(self.unit_frame, textvariable=self.unit_var, font=("Helvetica", 24), justify="right").grid(row=0, column=0, columnspan=4, sticky="nsew", pady=10)

        self.unit_type = tk.StringVar(value="length")
        ttk.Combobox(self.unit_frame, textvariable=self.unit_type, values=["length", "weight", "temperature", "time"]).grid(row=1, column=0, columnspan=4, sticky="nsew")

        self.from_unit = tk.StringVar()
        self.to_unit = tk.StringVar()
        ttk.Combobox(self.unit_frame, textvariable=self.from_unit, values=["m", "km", "cm"]).grid(row=2, column=0, columnspan=2, sticky="nsew")
        ttk.Combobox(self.unit_frame, textvariable=self.to_unit, values=["m", "km", "cm"]).grid(row=2, column=2, columnspan=2, sticky="nsew")

        ttk.Button(self.unit_frame, text="Convert", command=self.convert_unit).grid(row=3, column=0, columnspan=4, sticky="nsew")

        for i in range(4):
            self.unit_frame.grid_rowconfigure(i, weight=1)
        for i in range(4):
            self.unit_frame.grid_columnconfigure(i, weight=1)

    def setup_programmer_tab(self):
        self.prog_result_var = tk.StringVar()
        ttk.Entry(self.programmer_frame, textvariable=self.prog_result_var, font=("Helvetica", 24), justify="right").grid(row=0, column=0, columnspan=5, sticky="nsew", pady=10)

        buttons = [
            ("C", 2, 0), ("AND", 2, 1), ("OR", 2, 2), ("XOR", 2, 3), ("NOT", 2, 4),
            ("7", 3, 0), ("8", 3, 1), ("9", 3, 2), ("Bin", 3, 3), ("Hex", 3, 4),
            ("4", 4, 0), ("5", 4, 1), ("6", 4, 2), ("Dec", 4, 3), ("Oct", 4, 4),
            ("1", 5, 0), ("2", 5, 1), ("3", 5, 2), ("=", 5, 3), ("Shift", 5, 4),
            ("0", 6, 0, 2), (".", 6, 2), ("±", 6, 3), ("%", 6, 4)
        ]

        for button_info in buttons:
            button_text, row, col = button_info[:3]
            colspan = button_info[3] if len(button_info) > 3 else 1
            button = ttk.Button(self.programmer_frame, text=button_text, command=lambda text=button_text: self.handle_button_click(text, "programmer"), style="TButton")
            button.grid(row=row, column=col, columnspan=colspan, sticky="nsew", padx=5, pady=5)

        for i in range(7):
            self.programmer_frame.grid_rowconfigure(i, weight=1)
        for i in range(5):
            self.programmer_frame.grid_columnconfigure(i, weight=1)

    def bind_keys(self):
        self.root.bind("<Return>", lambda event: self.handle_button_click("=", self.mode))
        self.root.bind("<BackSpace>", lambda event: self.handle_button_click("C", self.mode))
        self.root.bind("<Delete>", lambda event: self.handle_button_click("C", self.mode))
        for key in "0123456789.+-*/()":
            self.root.bind(key, lambda event, k=key: self.handle_button_click(k, self.mode))

    def handle_button_click(self, clicked_button_text, mode="standard"):
        if self.sound_enabled:
            try:
                playsound("click.wav", block=False)
            except:
                pass

        current_text = self.result_var.get() if mode == "standard" else self.sci_result_var.get() if mode == "scientific" else self.prog_result_var.get()
        result_var = self.result_var if mode == "standard" else self.sci_result_var if mode == "scientific" else self.prog_result_var

        if clicked_button_text == "=":
            try:
                expression = current_text.replace("÷", "/").replace("×", "*").replace("^", "**").replace("π", str(math.pi)).replace("e", str(math.e))
                result = sp.sympify(expression, evaluate=True)
                result = float(result)
                formatted_result = round(result, self.decimal_places)
                if formatted_result.is_integer():
                    formatted_result = int(formatted_result)
                result_var.set(formatted_result)
                self.history.append(f"{current_text} = {formatted_result}")
                self.update_history()
            except Exception:
                result_var.set("Error")
        elif clicked_button_text == "C":
            result_var.set("")
        elif clicked_button_text == "%":
            try:
                current_number = float(current_text)
                result_var.set(current_number / 100)
            except ValueError:
                result_var.set("Error")
        elif clicked_button_text == "±":
            try:
                current_number = float(current_text)
                result_var.set(-current_number)
            except ValueError:
                result_var.set("Error")
        elif clicked_button_text == "√":
            try:
                current_number = float(current_text)
                if current_number >= 0:
                    result_var.set(math.sqrt(current_number))
                else:
                    result_var.set("Error")
            except ValueError:
                result_var.set("Error")
        elif clicked_button_text in ["sin", "cos", "tan"]:
            try:
                current_number = float(current_text)
                rad = math.radians(current_number)
                if clicked_button_text == "sin":
                    result_var.set(math.sin(rad))
                elif clicked_button_text == "cos":
                    result_var.set(math.cos(rad))
                else:
                    result_var.set(math.tan(rad))
            except ValueError:
                result_var.set("Error")
        elif clicked_button_text == "log":
            try:
                current_number = float(current_text)
                if current_number > 0:
                    result_var.set(math.log10(current_number))
                else:
                    result_var.set("Error")
            except ValueError:
                result_var.set("Error")
        elif clicked_button_text == "Graph":
            self.plot_graph(current_text)
        elif clicked_button_text in ["M+", "M-", "MR", "MC"]:
            try:
                if clicked_button_text == "M+":
                    self.memory += float(current_text)
                elif clicked_button_text == "M-":
                    self.memory -= float(current_text)
                elif clicked_button_text == "MR":
                    result_var.set(self.memory)
                elif clicked_button_text == "MC":
                    self.memory = 0
            except ValueError:
                result_var.set("Error")
        elif clicked_button_text == "Theme":
            self.set_theme("dark" if self.theme == "light" else "light")
        elif clicked_button_text in ["Bin", "Hex", "Dec", "Oct"]:
            try:
                num = int(current_text)
                if clicked_button_text == "Bin":
                    result_var.set(bin(num)[2:])
                elif clicked_button_text == "Hex":
                    result_var.set(hex(num)[2:].upper())
                elif clicked_button_text == "Dec":
                    result_var.set(num)
                elif clicked_button_text == "Oct":
                    result_var.set(oct(num)[2:])
            except ValueError:
                result_var.set("Error")
        elif clicked_button_text in ["AND", "OR", "XOR", "NOT"]:
            try:
                num = int(current_text)
                if clicked_button_text == "NOT":
                    result_var.set(~num)
                else:
                    second_num = tk.simpledialog.askinteger("Input", "Enter second number:")
                    if second_num is not None:
                        if clicked_button_text == "AND":
                            result_var.set(num & second_num)
                        elif clicked_button_text == "OR":
                            result_var.set(num | second_num)
                        elif clicked_button_text == "XOR":
                            result_var.set(num ^ second_num)
            except ValueError:
                result_var.set("Error")
        else:
            result_var.set(current_text + clicked_button_text)

    def convert_unit(self):
        try:
            value = float(self.unit_var.get())
            unit_type = self.unit_type.get()
            from_unit = self.from_unit.get()
            to_unit = self.to_unit.get()

            if unit_type == "length":
                units = {"m": 1, "km": 1000, "cm": 0.01}
                result = value * units[from_unit] / units[to_unit]
            elif unit_type == "weight":
                units = {"kg": 1, "g": 0.001, "lb": 0.453592}
                result = value * units[from_unit] / units[to_unit]
            elif unit_type == "temperature":
                if from_unit == "C" and to_unit == "F":
                    result = (value * 9/5) + 32
                elif from_unit == "F" and to_unit == "C":
                    result = (value - 32) * 5/9
                else:
                    result = value
            elif unit_type == "time":
                units = {"s": 1, "min": 60, "h": 3600}
                result = value * units[from_unit] / units[to_unit]

            self.unit_var.set(round(result, self.decimal_places))
        except Exception:
            self.unit_var.set("Error")

    def plot_graph(self, expression):
        try:
            x = np.linspace(-10, 10, 400)
            expr = expression.replace("×", "*").replace("÷", "/").replace("^", "**").replace("π", str(math.pi)).replace("e", str(math.e))
            y = [sp.sympify(expr, locals={"x": xi}).evalf() for xi in x]

            plt.figure(figsize=(8, 6))
            plt.plot(x, y, label=expression)
            plt.title(f"Graph of {expression}")
            plt.xlabel("x")
            plt.ylabel("y")
            plt.grid(True)
            plt.legend()
            plt.savefig("graph.png")
            plt.close()
            messagebox.showinfo("Graph", "Graph saved as graph.png")
        except Exception:
            messagebox.showerror("Error", "Invalid function for graphing")

    def save_history(self):
        with open("calculator_history.json", "w") as f:
            json.dump(self.history, f)
        messagebox.showinfo("History", "History saved successfully")

    def load_history(self):
        if os.path.exists("calculator_history.json"):
            with open("calculator_history.json", "r") as f:
                self.history = json.load(f)
            self.update_history()
            messagebox.showinfo("History", "History loaded successfully")
        else:
            messagebox.showerror("Error", "No history file found")

    def update_history(self):
        history_text = "History:\n" + "\n".join(self.history[-5:])
        self.history_var.set(history_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = ProCalculator(root)
    root.mainloop()
