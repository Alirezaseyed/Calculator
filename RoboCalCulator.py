import tkinter as tk
from tkinter import ttk
import sympy as sp
import math

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Calculator")
        self.memory = 0
        self.history = []
        self.theme = "light"
        self.setup_ui()
        self.bind_keys()

    def setup_ui(self):
        # Theme configuration
        self.style = ttk.Style()
        self.set_theme("light")

        # Main frame
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Result entry
        self.result_var = tk.StringVar()
        self.result_entry = ttk.Entry(self.main_frame, textvariable=self.result_var, font=("Helvetica", 24), justify="right")
        self.result_entry.grid(row=0, column=0, columnspan=5, sticky="nsew", pady=10)

        # History panel
        self.history_var = tk.StringVar(value="History:\n")
        self.history_label = ttk.Label(self.main_frame, textvariable=self.history_var, font=("Helvetica", 12), anchor="nw", relief="sunken", padding=5)
        self.history_label.grid(row=1, column=0, columnspan=5, sticky="nsew", pady=5)

        # Button layout
        buttons = [
            ("C", 2, 0), ("(", 2, 1), (")", 2, 2), ("÷", 2, 3), ("√", 2, 4),
            ("7", 3, 0), ("8", 3, 1), ("9", 3, 2), ("×", 3, 3), ("sin", 3, 4),
            ("4", 4, 0), ("5", 4, 1), ("6", 4, 2), ("-", 4, 3), ("cos", 4, 4),
            ("1", 5, 0), ("2", 5, 1), ("3", 5, 2), ("+", 5, 3), ("tan", 5, 4),
            ("0", 6, 0, 2), (".", 6, 2), ("=", 6, 3), ("log", 6, 4),
            ("M+", 7, 0), ("M-", 7, 1), ("MR", 7, 2), ("MC", 7, 3), ("±", 7, 4),
            ("% ", 8, 0), ("^", 8, 1), ("Theme", 8, 2, 3)
        ]

        for button_info in buttons:
            button_text, row, col = button_info[:3]
            colspan = button_info[3] if len(button_info) > 3 else 1
            button = ttk.Button(self.main_frame, text=button_text, command=lambda text=button_text: self.handle_button_click(text), style="TButton")
            button.grid(row=row, column=col, columnspan=colspan, sticky="nsew", padx=5, pady=5)

        # Configure grid weights
        for i in range(9):
            self.main_frame.grid_rowconfigure(i, weight=1)
        for i in range(5):
            self.main_frame.grid_columnconfigure(i, weight=1)

        # Window settings
        self.root.geometry("600x800")
        self.root.resizable(True, True)

    def set_theme(self, theme):
        self.theme = theme
        if theme == "light":
            self.style.configure("TButton", font=("Helvetica", 16), background="#f0f0f0", foreground="#000000")
            self.style.configure("TFrame", background="#ffffff")
            self.result_entry.configure(background="#ffffff", foreground="#000000")
            self.history_label.configure(background="#f0f0f0", foreground="#000000")
        else:
            self.style.configure("TButton", font=("Helvetica", 16), background="#333333", foreground="#ffffff")
            self.style.configure("TFrame", background="#1a1a1a")
            self.result_entry.configure(background="#1a1a1a", foreground="#ffffff")
            self.history_label.configure(background="#333333", foreground="#ffffff")

    def bind_keys(self):
        self.root.bind("<Return>", lambda event: self.handle_button_click("="))
        self.root.bind("<BackSpace>", lambda event: self.handle_button_click("C"))
        self.root.bind("<Delete>", lambda event: self.handle_button_click("C"))
        for key in "0123456789.+-*/()":
            self.root.bind(key, lambda event, k=key: self.handle_button_click(k))

    def handle_button_click(self, clicked_button_text):
        current_text = self.result_var.get()

        if clicked_button_text == "=":
            try:
                # Replace symbols for sympy
                expression = current_text.replace("÷", "/").replace("×", "*").replace("^", "**")
                result = sp.sympify(expression, evaluate=True)
                result = float(result)

                if result.is_integer():
                    result = int(result)

                self.result_var.set(result)
                self.history.append(f"{current_text} = {result}")
                self.update_history()
            except Exception:
                self.result_var.set("Error")
        elif clicked_button_text == "C":
            self.result_var.set("")
        elif clicked_button_text == "%":
            try:
                current_number = float(current_text)
                self.result_var.set(current_number / 100)
            except ValueError:
                self.result_var.set("Error")
        elif clicked_button_text == "±":
            try:
                current_number = float(current_text)
                self.result_var.set(-current_number)
            except ValueError:
                self.result_var.set("Error")
        elif clicked_button_text == "√":
            try:
                current_number = float(current_text)
                if current_number >= 0:
                    self.result_var.set(math.sqrt(current_number))
                else:
                    self.result_var.set("Error")
            except ValueError:
                self.result_var.set("Error")
        elif clicked_button_text in ["sin", "cos", "tan"]:
            try:
                current_number = float(current_text)
                rad = math.radians(current_number)
                if clicked_button_text == "sin":
                    self.result_var.set(math.sin(rad))
                elif clicked_button_text == "cos":
                    self.result_var.set(math.cos(rad))
                else:
                    self.result_var.set(math.tan(rad))
            except ValueError:
                self.result_var.set("Error")
        elif clicked_button_text == "log":
            try:
                current_number = float(current_text)
                if current_number > 0:
                    self.result_var.set(math.log10(current_number))
                else:
                    self.result_var.set("Error")
            except ValueError:
                self.result_var.set("Error")
        elif clicked_button_text == "M+":
            try:
                self.memory += float(current_text)
            except ValueError:
                self.result_var.set("Error")
        elif clicked_button_text == "M-":
            try:
                self.memory -= float(current_text)
            except ValueError:
                self.result_var.set("Error")
        elif clicked_button_text == "MR":
            self.result_var.set(self.memory)
        elif clicked_button_text == "MC":
            self.memory = 0
        elif clicked_button_text == "Theme":
            self.set_theme("dark" if self.theme == "light" else "light")
        else:
            self.result_var.set(current_text + clicked_button_text)

    def update_history(self):
        history_text = "History:\n" + "\n".join(self.history[-5:])  # Show last 5 entries
        self.history_var.set(history_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = Calculator(root)
    root.mainloop()
