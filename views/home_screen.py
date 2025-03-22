import tkinter as tk
from tkinter import ttk
from controllers.product_controller import ProductController

class HomeScreen(tk.Frame):
    def __init__(self, master, show_frame):
        super().__init__(master, bg="red")
        self.master = master
        self.show_frame = show_frame
        self.current_category = 'All'
        self.controller = ProductController(self)
        self.cart_items = {}

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
        nav_frame.place(x=10, y=60)

        ttk.Button(nav_frame, text="Home", command=lambda: self.show_frame("HomeScreen")).pack(side=tk.LEFT, padx=10)
        ttk.Button(nav_frame, text="Inventory", command=lambda: self.show_frame("InventoryView")).pack(side=tk.LEFT, padx=10)
        ttk.Button(nav_frame, text="Sales", command=lambda: self.show_frame("SalesView")).pack(side=tk.LEFT, padx=10)

    # ---------------- Product Section ----------------
    def create_product_section(self):
        self.product_section = tk.Frame(self, bg="#F4F4F4", width=500, height=300)
        self.product_section.place(x=10, y=90)
        self.product_section.pack_propagate(False)

        # Create Category Buttons
        categories = ["All", "Donuts", "Bread", "Cakes", "Sandwiches"]
        self.category_frame = tk.Frame(self.product_section, bg="#F4F4F4", width=500, height=40)
        self.category_frame.place(x=0, y=0)

        for category in categories:
            tk.Button(self.category_frame, text=category, command=lambda c=category: self.display_products(c), bg="white").pack(side=tk.LEFT, padx=5)

        # Create Scrollable Product Area
        self.canvas_frame = tk.Canvas(self.product_section, bg="#F4F4F4", width=490, height=250, highlightthickness=0)
        self.canvas_frame.place(x=5, y=50)

        self.scrollbar = tk.Scrollbar(self.product_section, orient="vertical", command=self.canvas_frame.yview)
        self.scrollbar.place(x=495, y=50, height=250)
        self.canvas_frame.configure(yscrollcommand=self.scrollbar.set)

        self.product_frame = tk.Frame(self.canvas_frame, bg="#F4F4F4")
        self.canvas_frame.create_window((0, 0), window=self.product_frame, anchor="nw")

        self.display_products("All")

    # ---------------- Display Products ----------------
    def display_products(self, category):
        self.current_category = category
        products = self.controller.get_all_products()

        # Filter Products by Category
        if category != "All":
            products = [p for p in products if p['product_category'].lower() == category.lower()]

        # Clear previous product display
        for widget in self.product_frame.winfo_children():
            widget.destroy()

        # Display Products in Grid
        columns = 4
        card_width = 100
        card_height = 100

        for index, product in enumerate(products):
            row = index // columns
            col = index % columns

            # Create Product Card
            card = tk.Frame(self.product_frame, bg="white", relief="raised", bd=2, width=card_width, height=card_height)
            card.grid(row=row, column=col, padx=10, pady=10)
            card.pack_propagate(False)

            # Product Info
            tk.Label(card, text=product['product_name'], font=("Arial", 12), bg="white").pack(pady=5)
            tk.Label(card, text=f"₱{product['product_price']}", font=("Arial", 10), bg="white").pack()

            # Bind Click Event
            card.bind("<Button-1>", lambda e, p=product: self.on_product_click(p))

        # Update Scroll Region
        self.product_frame.update_idletasks()
        self.canvas_frame.config(scrollregion=self.canvas_frame.bbox("all"))

    # ---------------- Handle Product Click ----------------
    def on_product_click(self, product):
        product_name = product['product_name']
        if product_name in self.cart_items:
            self.cart_items[product_name]['quantity'] += 1
        else:
            self.cart_items[product_name] = {'product': product, 'quantity': 1}
        self.update_cart_view()

    # ---------------- Create Cart ----------------
    def create_cart(self):
        self.cart_frame = tk.Frame(self, bg="#F4F4F4", width=310, height=380)
        self.cart_frame.place(x=520, y=10)
        self.cart_frame.pack_propagate(False)

        self.lbl = tk.Label(self.cart_frame, text="CART")
        self.lbl.pack(side=tk.TOP)

        # Treeview for Cart
        self.cart_tree = ttk.Treeview(self.cart_frame, columns=("Order", "-", "Quantity", "+", "Price", "Remove"), show="headings", height=10)
        self.cart_tree.heading("Order", text="Order")
        self.cart_tree.heading("-", text="-")
        self.cart_tree.heading("Quantity", text="Quantity")
        self.cart_tree.heading("+", text="+")
        self.cart_tree.heading("Price", text="Price")
        self.cart_tree.heading("Remove", text="")
        self.cart_tree.pack(fill=tk.BOTH, expand=True)

        self.cart_tree.column("Order", width=80, anchor=tk.CENTER)
        self.cart_tree.column("-", width=30, anchor=tk.CENTER)
        self.cart_tree.column("Quantity", width=60, anchor=tk.CENTER)
        self.cart_tree.column("+", width=30, anchor=tk.CENTER)
        self.cart_tree.column("Price", width=80, anchor=tk.CENTER)
        self.cart_tree.column("Remove", width=20, anchor=tk.CENTER)

        self.cart_tree.bind('<Button-1>', self.handle_cart_action)

    # ---------------- Handle Cart Action ----------------
    def handle_cart_action(self, event):
        region = self.cart_tree.identify_region(event.x, event.y)
        item = self.cart_tree.identify_row(event.y)
        column = self.cart_tree.identify_column(event.x)

        if not item:
            return

        product_name = self.cart_tree.item(item, 'values')[0]

        if column == '#2':  # Decrement
            if self.cart_items[product_name]['quantity'] > 1:
                self.cart_items[product_name]['quantity'] -= 1
        elif column == '#4':  # Increment
            self.cart_items[product_name]['quantity'] += 1
        elif column == '#6':  # Remove
            del self.cart_items[product_name]

        self.update_cart_view()

    # ---------------- Update Cart View ----------------
    def update_cart_view(self):
        for item in self.cart_tree.get_children():
            self.cart_tree.delete(item)

        for product_name, data in self.cart_items.items():
            product = data['product']
            quantity = data['quantity']
            price = product['product_price'] * quantity
            self.cart_tree.insert('', 'end', values=(product_name, "-", quantity, "+", f"₱{price}", "🗑️"))
