import tkinter as tk
from views.home_screen import HomeScreen
from views.inventory_view import InventoryView
from views.sales_view import SalesView

class MainController(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("POS System")
        self.geometry("840x440")
        self.resizable(width=False, height=False)

        self.frames = {}

        # Initialize Frames
        for F in (HomeScreen, InventoryView, SalesView):
            frame = F(self, self.show_frame)
            self.frames[F.__name__] = frame
            # frame.grid(row=0, column=0, sticky="nsew")
            frame.place(x=0, y=0, relwidth=1, relheight=1)

        self.show_frame("HomeScreen")

    def show_frame(self, frame_name):
        frame = self.frames.get(frame_name)
        if frame:
            frame.tkraise()
