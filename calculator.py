import tkinter as tk
import math

# Global Variables
entry_var = ""
angle_mode = "DEG"  # DEG or RAD
inv_mode = False     # Inverse mode

#  Functions 
def press(key):
    global entry_var, angle_mode, inv_mode

    if key == "=":
        calculate()
    elif key == "C":
        entry_var = ""
        display_var.set(entry_var)
    elif key == "<-":
        entry_var = entry_var[:-1]
        display_var.set(entry_var)
    elif key == "π":
        entry_var += str(math.pi)
        display_var.set(entry_var)
    elif key == "e":
        entry_var += str(math.e)
        display_var.set(entry_var)
    elif key == "inv":
        toggle_inv()
    elif key == "1/x":
        try:
            entry_var = str(1 / eval(entry_var))
            display_var.set(entry_var)
        except:
            display_var.set("Error")
            entry_var = ""
    elif key == "deg":
        angle_mode = "DEG"
    elif key == "rad":
        angle_mode = "RAD"
    elif key in ["sin","cos","tan","ln","log","√"]:
        if key in ["sin","cos","tan"]:
            func = {"sin":"math.asin","cos":"math.acos","tan":"math.atan"}[key] if inv_mode else {"sin":"math.sin","cos":"math.cos","tan":"math.tan"}[key]
            if angle_mode == "DEG" and not inv_mode:
                func += "(math.radians("
            entry_var += func + "("
        else:
            if inv_mode:
                func = {"ln":"math.exp","log":"10**","√":"("}[key]
                if key == "√":
                    entry_var += "("  # Will close later with x^2
                else:
                    entry_var += func + "("
            else:
                func = {"ln":"math.log","log":"math.log10","√":"math.sqrt"}[key]
                entry_var += func + "("
        display_var.set(entry_var)
    else:
        entry_var += key
        display_var.set(entry_var)

def toggle_inv():
    global inv_mode
    inv_mode = not inv_mode
    # Update trig button labels
    btn_sin.config(text="sin⁻¹" if inv_mode else "sin")
    btn_cos.config(text="cos⁻¹" if inv_mode else "cos")
    btn_tan.config(text="tan⁻¹" if inv_mode else "tan")
    # Update ln, log, √ button labels
    btn_ln.config(text="eˣ" if inv_mode else "ln")
    btn_log.config(text="10ˣ" if inv_mode else "log")
    btn_sqrt.config(text="x²" if inv_mode else "√")

def calculate():
    global entry_var, angle_mode, inv_mode
    try:
        expr = entry_var.replace("×", "*").replace("÷", "/").replace("^", "**")
        expr = expr.replace("!", "math.factorial")
        expr = expr.replace("√", "math.sqrt")
        expr = expr.replace("ln", "math.log").replace("log", "math.log10")

        # Close parentheses for DEG mode trig
        if angle_mode == "DEG":
            expr = expr.replace("math.sin(math.radians(", "math.sin(math.radians(")
            expr = expr.replace("math.cos(math.radians(", "math.cos(math.radians(")
            expr = expr.replace("math.tan(math.radians(", "math.tan(math.radians(")
            expr += ")" * (expr.count("math.sin(math.radians(") +
                            expr.count("math.cos(math.radians(") +
                            expr.count("math.tan(math.radians("))

        # Handle x^2 for √⁻¹
        if inv_mode:
            expr = expr.replace("(", "(")  # user input inside x²
            expr = expr.replace(")", ")**2") if entry_var.endswith("(") else expr

        result = eval(expr)
        entry_var = str(result)
        display_var.set(entry_var)
    except:
        display_var.set("Error")
        entry_var = ""

# Main Window
root = tk.Tk()
root.title("Scientific Calculator")
root.geometry("500x650")
root.resizable(0,0)

#  Display 
display_var = tk.StringVar()
display = tk.Entry(root, textvariable=display_var, font=("Helvetica", 24), bd=5, relief=tk.RIDGE, justify="right")
display.pack(fill="both", ipadx=8, pady=10)

# Buttons Layout 
buttons = [
    ["C","<-","deg","rad","π","e"],
    ["sin","cos","tan","√","!","1/x"],
    ["7","8","9","÷","%","^"],
    ["4","5","6","×","(",")"],
    ["1","2","3","-","log","ln"],
    ["0","00",".","+","=","inv"]
]

#  Buttons Frame 
btn_frame = tk.Frame(root)
btn_frame.pack(expand=True, fill="both")

# Dictionary to keep track of buttons
button_objects = {}

for i, row in enumerate(buttons):
    for j, button in enumerate(row):
        btn = tk.Button(btn_frame, text=button, font=("Helvetica", 18), bd=2, relief=tk.RAISED)
        btn.grid(row=i, column=j, sticky="nsew", padx=1, pady=1)
        btn.configure(command=lambda b=button: press(b))
        if button in ["sin","cos","tan","ln","log","√"]:
            button_objects[button] = btn

# Assign buttons for toggle_inv
btn_sin = button_objects["sin"]
btn_cos = button_objects["cos"]
btn_tan = button_objects["tan"]
btn_ln = button_objects["ln"]
btn_log = button_objects["log"]
btn_sqrt = button_objects["√"]

# Make buttons responsive 
rows = len(buttons)
cols = len(buttons[0])
for i in range(rows):
    btn_frame.rowconfigure(i, weight=1)
for j in range(cols):
    btn_frame.columnconfigure(j, weight=1)

root.mainloop()
