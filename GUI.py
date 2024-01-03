import tkinter as tk
from tkinter import ttk

def greet():
    print("Hello")
    

root = tk.Tk()

green_button = ttk.Button(root, text="Greet", command=greet)
green_button.pack()

root.mainloop()