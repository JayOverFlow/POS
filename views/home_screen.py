import tkinter as tk
from tkinter import ttk
from tkinter import font, messagebox
from pathlib import Path
import customtkinter as ctk
import ctypes



class HomeScreen(tk.Frame):
    def __init__(self, master, show_frame):
        super().__init__(master, bg="red")
        self.master = master
        self.show_frame = show_frame
        self.current_category = 'All'

        BASE_DIR = Path(__file__).resolve().parent.parent
        FONT_DIR = BASE_DIR / "static/fonts"
        FONT_PATH = FONT_DIR / "instrumentserif-regular.ttf"

        self.font1 = font.Font(family="Instrument Serif", size=40)
        self.font2 = font.Font(family="Instrument Serif", size=30)
        self.font3 = ctk.CTkFont(family="Instrument Serif", size=20)

        try:
            ctypes.windll.gdi32.AddFontResourceW(str(FONT_PATH))
        except Exception as e:
            print(f"Error loading font: {e}")

        # Canvas
        self.canvas = tk.Canvas(self, bg="#FFFFFF")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Heading
        self.canvas.create_text(350, 30, text="Cravings", font=self.font1)

        self.create_navigation_buttons()
        self.create_product_section()
        self.create_cart()

    # ---------------- Navigation Buttons ----------------
    def create_navigation_buttons(self):
        # Create a navigation frame with a white background
        nav_frame = tk.Frame(self, bg="#FFFFFF", width=400, height=50)
        nav_frame.place(x=10, y=60)

        # Button Configuration
        buttons = [
            ("Home", "HomeScreen"),
            ("Inventory", "InventoryView"),
            ("Sales", "SalesView")
        ]

        # Create CTkButtons with pink background
        for text, frame in buttons:
            button = ctk.CTkButton(nav_frame,
                                   text=text,
                                   command=lambda f=frame: self.show_frame(f),
                                   fg_color="#FFB2B3",  # Background color
                                   text_color="black",  # Button text color
                                   width=80, height=25)  # Button size
            button.pack(side="left", padx=10)

    # ---------------- Product Section ----------------
    def create_product_section(self):
        # Product Section Container
        self.product_section = tk.Frame(self, bg="#F4F4F4", width=500, height=300)
        self.product_section.place(x=10, y=90)
        self.product_section.pack_propagate(False)

        # Category Buttons at the Top of Product Section
        categories = ["All", "Donuts", "Bread", "Cakes", "Sandwiches"]
        self.category_frame = tk.Frame(self.product_section, bg="#F4F4F4", width=200, height=100)
        self.category_frame.place(x=0, y=0)

        for category in categories:
            # Apply underline using Unicode
            underlined_text = ''.join(char + '\u0332' for char in category)

            # Create a styled and smaller button with custom font
            button = ctk.CTkButton(self.category_frame,
                                   text=underlined_text,
                                   command=lambda c=category: self.display_products(c),
                                   fg_color="#F4F4F4",  # Transparent-like background
                                   text_color="black",  # Text color
                                   corner_radius=0,  # Square style
                                   hover=False,  # Disable hover effect
                                   width=80, height=30,  # Button size
                                   font=self.font3)  # Use the custom CTkFont
            button.pack(side="left", padx=10)  # Align horizontally with spacing

        # Product Display Area
        self.product_frame = tk.Frame(self.product_section, bg="#F4F4F4", width=490, height=270)
        self.product_frame.place(x=5, y=25)
        self.product_frame.pack_propagate(False)
        self.display_products("All")

    # ---------------- Display Products ----------------
    def display_products(self, category):
        self.current_category = category

        # Clear previous product display
        for widget in self.product_frame.winfo_children():
            widget.destroy()

        tk.Label(self.product_frame, text=f"Displaying {category} Products", font=("Arial", 16), bg="#F4F4F4").pack(pady=20)

    def create_cart(self):
        self.cart_frame = tk.Frame(self, bg="#F4F4F4", width=270, height=380)
        self.cart_frame.place(x=520, y=10)
        self.cart_frame.pack_propagate(False)

        self.lbl = tk.Label(self.cart_frame, text="Basket",font=self.font2)
        self.lbl.pack(side=tk.TOP)

