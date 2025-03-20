import tkinter as tk
from tkinter import ttk

class InventoryView(tk.Frame):
    def __init__(self, master, show_frame):
        super().__init__(master, bg="red")
        self.master = master
        self.show_frame = show_frame