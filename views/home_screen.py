import tkinter as tk
from tkinter import ttk

class HomeScreen(tk.Frame):
    def __init__(self, master, show_frame):
        super().__init__(master, bg="red")
        self.master = master
        self.show_frame = show_frame
        self.current_category = 'All'

        # Canvas
        self.canvas = tk.Canvas(self, bg="#FFFFFF")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Heading
        self.canvas.create_text(350, 40, text="Cravings", font=("Arial", 16, "bold"))

        self.create_navigation_buttons()
        self.create_product_section()
        self.create_cart()

    # ---------------- Navigation Buttons ----------------
    def create_navigation_buttons(self):
        nav_frame = tk.Frame(self, bg="#FFFFFF", width=400, height=50)
        # nav_frame.pack(side=tk.TOP, fill=tk.X)
        nav_frame.place(x=10, y=60)

        ttk.Button(nav_frame, text="Home", command=lambda: self.show_frame("HomeScreen")).pack(side=tk.LEFT, padx=10)
        ttk.Button(nav_frame, text="Inventory", command=lambda: self.show_frame("InventoryView")).pack(side=tk.LEFT, padx=10)
        ttk.Button(nav_frame, text="Sales", command=lambda: self.show_frame("SalesView")).pack(side=tk.LEFT, padx=10)

    # ---------------- Product Section ----------------
    def create_product_section(self):
        self.product_section = tk.Frame(self, bg="#F4F4F4", width= 500, height=300)
        self.product_section.place(x=10, y=90)
        self.product_section.pack_propagate(False)

        # Create Category Buttons at the top of Product Section
        categories = ["All", "Donuts", "Bread", "Cakes", "Sandwiches"]
        self.category_frame = tk.Frame(self.product_section, bg="#F4F4F4", width=200, height=100)
        self.category_frame.place(x=0, y=0)

        for category in categories:
            tk.Button(self.category_frame, text=category, command=lambda c=category: self.display_products(c), bg="white").pack(side=tk.LEFT, padx=5)

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

        self.lbl = tk.Label(self.cart_frame, text="CART")
        self.lbl.pack(side=tk.TOP)

