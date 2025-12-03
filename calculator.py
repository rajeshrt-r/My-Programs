import tkinter as tk
from tkinter import font

class StylishCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Stylish Calculator")
        self.root.geometry("400x600")
        self.root.resizable(False, False)
        self.root.configure(bg="#1e1e2e")
        
        self.expression = ""
        self.result_var = tk.StringVar()
        self.result_var.set("0")
        
        self.create_widgets()
    
    def create_widgets(self):
        # Display frame
        display_frame = tk.Frame(self.root, bg="#1e1e2e", height=150)
        display_frame.pack(fill="both", padx=20, pady=20)
        
        # Result display
        result_font = font.Font(family="Segoe UI", size=36, weight="bold")
        result_display = tk.Label(
            display_frame, 
            textvariable=self.result_var,
            font=result_font,
            bg="#1e1e2e",
            fg="#cdd6f4",
            anchor="e",
            padx=10,
            pady=20
        )
        result_display.pack(fill="both", expand=True)
        
        # Expression display
        self.expr_var = tk.StringVar()
        expr_font = font.Font(family="Segoe UI", size=14)
        expr_display = tk.Label(
            display_frame,
            textvariable=self.expr_var,
            font=expr_font,
            bg="#1e1e2e",
            fg="#9399b2",
            anchor="e",
            padx=10
        )
        expr_display.pack(fill="x")
        
        # Buttons frame
        buttons_frame = tk.Frame(self.root, bg="#1e1e2e")
        buttons_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Button layout
        buttons = [
            ['C', '⌫', '%', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['0', '.', '=']
        ]
        
        button_font = font.Font(family="Segoe UI", size=18, weight="bold")
        
        for i, row in enumerate(buttons):
            for j, btn_text in enumerate(row):
                # Determine button styling
                if btn_text == '=':
                    bg_color = "#89b4fa"
                    fg_color = "#1e1e2e"
                    colspan = 2
                elif btn_text in ['C', '⌫', '%', '/', '*', '-', '+']:
                    bg_color = "#313244"
                    fg_color = "#cdd6f4"
                    colspan = 1
                else:
                    bg_color = "#45475a"
                    fg_color = "#cdd6f4"
                    colspan = 1
                
                btn = tk.Button(
                    buttons_frame,
                    text=btn_text,
                    font=button_font,
                    bg=bg_color,
                    fg=fg_color,
                    activebackground="#585b70",
                    activeforeground="#cdd6f4",
                    bd=0,
                    cursor="hand2",
                    command=lambda x=btn_text: self.on_button_click(x)
                )
                
                btn.grid(
                    row=i, 
                    column=j, 
                    columnspan=colspan,
                    sticky="nsew",
                    padx=5,
                    pady=5
                )
        
        # Configure grid weights
        for i in range(5):
            buttons_frame.grid_rowconfigure(i, weight=1)
        for j in range(4):
            buttons_frame.grid_columnconfigure(j, weight=1)
    
    def on_button_click(self, char):
        if char == 'C':
            self.expression = ""
            self.result_var.set("0")
            self.expr_var.set("")
        
        elif char == '⌫':
            self.expression = self.expression[:-1]
            self.expr_var.set(self.expression)
            if not self.expression:
                self.result_var.set("0")
        
        elif char == '=':
            try:
                result = eval(self.expression)
                self.result_var.set(str(result))
                self.expression = str(result)
                self.expr_var.set("")
            except:
                self.result_var.set("Error")
                self.expression = ""
        
        else:
            self.expression += str(char)
            self.expr_var.set(self.expression)
            try:
                preview = eval(self.expression)
                self.result_var.set(str(preview))
            except:
                pass

if __name__ == "__main__":
    root = tk.Tk()
    calculator = StylishCalculator(root)
    root.mainloop()