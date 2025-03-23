import tkinter as tk
from tkinter import ttk
from tkinter import font, messagebox
from pathlib import Path
import ctypes
from decimal import Decimal
from datetime import datetime

# Controllers
from controllers.product_controller import ProductController
from controllers.sales_controller import SalesController

class HomeScreen(tk.Frame):
    def __init__(self, master, show_frame):
        super().__init__(master, bg="#FFFFFF")
        self.master = master
        self.show_frame = show_frame
        self.current_category = 'All'
        self.product_controller = ProductController(self)
        self.sales_controller = SalesController(self)
        self.cart_items = {}

        # Canvas
        self.canvas = tk.Canvas(self, bg="#FFFFFF")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Heading
        self.canvas.create_text(350, 40, text="Cravings")

        self.create_navigation_buttons()
        self.create_product_section()
        # self.create_cart()

    # ---------------- Navigation Buttons ----------------
    def create_navigation_buttons(self):
        nav_frame = tk.Frame(self, bg="#FFFFFF", width=400, height=50)
        nav_frame.place(x=10, y=60)

        ttk.Button(nav_frame, text="Home", command=self.create_product_section).pack(side=tk.LEFT, padx=10)
        ttk.Button(nav_frame, text="Inventory", command=self.create_add_product_frame).pack(side=tk.LEFT, padx=10)
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

        self.create_cart()
        self.display_products("All")

    # ---------------- Display Products ----------------
    def display_products(self, category):
        self.current_category = category
        products = self.product_controller.get_all_products()

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

            # Bind Click Event for Product Management
            if self.current_category == "Inventory":
                card.bind("<Button-1>", lambda e, p=product: self.create_update_product_frame(p))
            else:
                card.bind("<Button-1>", lambda e, p=product: self.on_product_click(p))

        # Update Scroll Region
        self.product_frame.update_idletasks()
        self.canvas_frame.config(scrollregion=self.canvas_frame.bbox("all"))

    # ---------------- Handle Product Click ----------------
    def on_product_click(self, product):
        if hasattr(self, 'add_product_frame') and self.add_product_frame.winfo_ismapped():
            # Inventory Mode: Show Update Frame
            self.show_update_product_frame(product)
        else:
            # Cart Mode: Add to Cart
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
        self.cart_tree = ttk.Treeview(self.cart_frame, columns=("Order", "-", "Quantity", "+", "Price", "Remove"),
                                      show="headings", height=5)
        self.cart_tree.heading("Order", text="Order")
        self.cart_tree.heading("-", text="")
        self.cart_tree.heading("Quantity", text="Quantity")
        self.cart_tree.heading("+", text="")
        self.cart_tree.heading("Price", text="Price")
        self.cart_tree.heading("Remove", text="")
        self.cart_tree.pack(fill=tk.BOTH, expand=True)

        self.cart_tree.column("Order", width=100, anchor=tk.CENTER)
        self.cart_tree.column("-", width=10, anchor=tk.CENTER)
        self.cart_tree.column("Quantity", width=60, anchor=tk.CENTER)
        self.cart_tree.column("+", width=10, anchor=tk.CENTER)
        self.cart_tree.column("Price", width=80, anchor=tk.CENTER)
        self.cart_tree.column("Remove", width=20, anchor=tk.CENTER)

        self.cart_tree.bind('<Button-1>', self.handle_cart_action)

        # Mode of Payment Dropdown
        self.payment_frame = tk.Frame(self.cart_frame, bg="#F4F4F4")
        self.payment_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=(10, 5))

        tk.Label(self.payment_frame, text="Mode of Payment:", bg="#F4F4F4").pack(side=tk.LEFT)
        self.payment_var = tk.StringVar(value="Cash or GCash")
        self.payment_dropdown = ttk.Combobox(self.payment_frame, textvariable=self.payment_var,
                                             values=["Cash", "Gcash"], state="readonly")
        self.payment_dropdown.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)

        # Discount Entry
        self.discount_frame = tk.Frame(self.cart_frame, bg="#F4F4F4")
        self.discount_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=(0, 10))

        tk.Label(self.discount_frame, text="Discount:", bg="#F4F4F4").pack(side=tk.LEFT)
        self.discount_var = tk.StringVar(value="Apply Discount")
        self.discount_entry = ttk.Entry(self.discount_frame, textvariable=self.discount_var)
        self.discount_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)

        def validate_discount_input(new_value):
            if new_value == "" or new_value.replace(".", "", 1).isdigit():
                return True
            return False

        validate_command = self.register(validate_discount_input)
        self.discount_entry.config(validate="key", validatecommand=(validate_command, "%P"))

        def clear_placeholder(event):
            if self.discount_var.get() == "Apply Discount":
                self.discount_var.set("")

        def restore_placeholder(event):
            if not self.discount_var.get():
                self.discount_var.set("Apply Discount")

        self.discount_entry.bind("<FocusIn>", clear_placeholder)
        self.discount_entry.bind("<FocusOut>", restore_placeholder)
        # Summary Frame
        self.summary_frame = tk.Frame(self.cart_frame, bg="#F4F4F4")
        self.summary_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        self.subtotal_label = tk.Label(self.summary_frame, text="Subtotal: ₱0.00", bg="#F4F4F4", font=("Arial", 10))
        self.subtotal_label.pack(anchor="w")

        self.discount_applied_label = tk.Label(self.summary_frame, text="Discount Applied: ₱0.00", bg="#F4F4F4",
                                               font=("Arial", 10))
        self.discount_applied_label.pack(anchor="w")

        self.total_payment_label = tk.Label(self.summary_frame, text="Total Payment: ₱0.00", bg="#F4F4F4",
                                            font=("Arial", 12, "bold"))
        self.total_payment_label.pack(anchor="w")

        self.discount_entry.bind("<KeyRelease>", lambda e: self.update_summary())
        self.cart_tree.bind("<<TreeviewSelect>>", lambda e: self.update_summary())

        # Buttons
        self.button_frame = tk.Frame(self.cart_frame, bg="#F4F4F4")
        self.button_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

        tk.Button(self.button_frame, text="Clear", command=self.clear_cart).pack(side=tk.LEFT, expand=True,
                                                                                 fill=tk.BOTH, padx=5)
        tk.Button(self.button_frame, text="Proceed", command=self.proceed_checkout).pack(side=tk.RIGHT, expand=True,
                                                                                         fill=tk.BOTH, padx=5)

    def clear_cart(self):
        self.cart_items.clear()
        self.update_cart_view()

    # ---------------- Proceed Checkout ----------------
    def proceed_checkout(self):
        if self.payment_var.get() == "Cash or GCash":
            messagebox.showwarning("Warning", "Please select a mode of payment before proceeding.")
            return

        if not self.cart_items:
            messagebox.showwarning("Warning", "Your cart is empty. Please add items before proceeding.")
            return

        if not self.cart_items:
            tk.messagebox.showwarning("Empty Cart", "Your cart is empty. Please add products before proceeding.")
            return

        # Create Receipt Frame
        self.receipt_frame = tk.Frame(self, bg="#FFFFFF", width=310, height=380)
        self.receipt_frame.place(x=520, y=10)
        self.receipt_frame.pack_propagate(False)

        # Date and Time
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        tk.Label(self.receipt_frame, text=f"Date & Time: {now}", bg="#FFFFFF").pack(anchor="w")

        # Receipt Treeview
        receipt_tree = ttk.Treeview(self.receipt_frame, columns=("Unit", "Product Name", "Quantity", "Price"), show="headings", height=5)
        receipt_tree.heading("Unit", text="Unit")
        receipt_tree.heading("Product Name", text="Product Name")
        receipt_tree.heading("Quantity", text="Quantity")
        receipt_tree.heading("Price", text="Price")
        receipt_tree.pack(fill=tk.BOTH, expand=True)

        receipt_tree.column("Unit", width=30, anchor=tk.CENTER)
        receipt_tree.column("Product Name", width=60, anchor=tk.CENTER)
        receipt_tree.column("Quantity", width=30, anchor=tk.CENTER)
        receipt_tree.column("Price", width=60, anchor=tk.CENTER)

        # Populate Treeview
        unit_count = 0
        subtotal = Decimal(0)
        for product_name, data in self.cart_items.items():
            unit_count += 1
            price = Decimal(data['product']['product_price']) * Decimal(data['quantity'])
            subtotal += price
            receipt_tree.insert('', 'end', values=(unit_count, product_name, data['quantity'], f"₱{price:.2f}"))

        # Discount and Total Calculation
        try:
            discount_percentage = Decimal(self.discount_var.get()) if self.discount_var.get().replace('.', '',
                                                                                                      1).isdigit() else Decimal(
                0)
            if discount_percentage > 100 or discount_percentage < 0:
                raise ValueError("Invalid discount percentage")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid discount percentage (0-100).")
            return

        # Calculate the discount amount and total payment
        discount_value = (subtotal * discount_percentage) / 100
        total_payment = max(subtotal - discount_value, Decimal(0))

        # Display Summary
        tk.Label(self.receipt_frame, text=f"Subtotal: ₱{subtotal:.2f}", bg="#FFFFFF").pack(anchor="w")
        tk.Label(self.receipt_frame,
                 text=f"Discount Applied: {discount_percentage:.2f}% (₱{discount_value:.2f})",
                 bg="#FFFFFF").pack(anchor="w")
        tk.Label(self.receipt_frame, text=f"Total Payment: ₱{total_payment:.2f}", bg="#FFFFFF",
                 font=("Arial", 12, "bold")).pack(anchor="w")

        # Continue Button
        tk.Button(self.receipt_frame, text="Continue", command=self.finalize_transaction).pack(side=tk.BOTTOM)

    # ---------------- Finalize Transaction ----------------
    def finalize_transaction(self):
        payment_method = self.payment_var.get()
        self.product_controller.finalize_transaction(payment_method, self.cart_items)

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
        # Ensure cart_tree exists before attempting to update it
        if not hasattr(self, 'cart_tree') or not self.cart_tree.winfo_exists():
            return

        for item in self.cart_tree.get_children():
            self.cart_tree.delete(item)

        for product_name, data in self.cart_items.items():
            product = data['product']
            quantity = data['quantity']
            price = product['product_price'] * quantity
            self.cart_tree.insert('', 'end', values=(product_name, "-", quantity, "+", f"₱{price:.2f}", "🗑️"))

        self.update_summary()

    def update_summary(self):
        subtotal = sum(
            Decimal(str(data['product']['product_price'])) * data['quantity'] for data in self.cart_items.values())
        try:
            discount_percentage = Decimal(
                str(self.discount_var.get())) if self.discount_var.get() and self.discount_var.get() != "Apply Discount" else Decimal(
                "0.0")
            if discount_percentage < 0 or discount_percentage > 100:
                raise ValueError("Invalid discount percentage")
        except (ValueError, ArithmeticError):
            discount_percentage = Decimal("0.0")

        discount_value = (subtotal * discount_percentage) / Decimal("100.0")
        total_payment = max(subtotal - discount_value, Decimal("0.0"))

        self.subtotal_label.config(text=f"Subtotal: ₱{subtotal:.2f}")
        self.discount_applied_label.config(text=f"Discount Applied: {discount_percentage:.2f}% (₱{discount_value:.2f})")
        self.total_payment_label.config(text=f"Total Payment: ₱{total_payment:.2f}")

    def create_add_product_frame(self):
        # Destroy Cart Frame if it exists
        if hasattr(self, 'cart_frame'):
            self.cart_frame.destroy()

        # Create Inventory Frame
        self.add_product_frame = tk.Frame(self, bg="#F4F4F4", width=310, height=185)
        self.add_product_frame.place(x=520, y=205)
        self.add_product_frame.pack_propagate(False)
        self.add_product_frame.grid_propagate(False)

        # Labels and Entry Widgets
        tk.Label(self.add_product_frame, text="Product Name:", bg="#F4F4F4").grid(row=0, column=0, padx=5, pady=5)
        self.product_name_entry = ttk.Entry(self.add_product_frame)
        self.product_name_entry.grid(row=1, column=0, padx=5, pady=5)

        tk.Label(self.add_product_frame, text="Price:", bg="#F4F4F4").grid(row=0, column=1, padx=5, pady=5)
        self.product_price_entry = ttk.Entry(self.add_product_frame)
        self.product_price_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.add_product_frame, text="Category:", bg="#F4F4F4").grid(row=2, column=0, padx=5, pady=5)
        self.category_var = tk.StringVar(value="Choose Category")
        self.category_dropdown = ttk.Combobox(self.add_product_frame, textvariable=self.category_var,
                                                  values=["Donuts", "Bread", "Cakes", "Sandwiches"], state="readonly")
        self.category_dropdown.grid(row=3, column=0, padx=5, pady=5)

        tk.Label(self.add_product_frame, text="Stock:", bg="#F4F4F4").grid(row=2, column=1, padx=5, pady=5)
        self.product_stock_entry = ttk.Entry(self.add_product_frame)
        self.product_stock_entry.grid(row=3, column=1, padx=5, pady=5)

        # Add Product Button
        tk.Button(self.add_product_frame, text="Add Product", command=self.add_product_to_database).grid(row=4,
                                                                                                           column=0,
                                                                                                           columnspan=2,
                                                                                                           pady=10)

    def add_product_to_database(self):
        name = self.product_name_entry.get().strip()
        price = self.product_price_entry.get().strip()
        category = self.category_var.get().strip()
        stock = self.product_stock_entry.get().strip()

        if not name or not price or not stock or category == "Choose Category":
            messagebox.showwarning("Invalid Input", "All fields are required.")
            return

        try:
            price = Decimal(price)
            stock = int(stock)
            if price <= 0 or stock < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Input", "Enter a valid price and stock.")
            return

        # Call the ProductController to add product
        if self.product_controller.add_product(name, price, category, stock):
            messagebox.showinfo("Success", "Product added successfully!")
            self.product_name_entry.delete(0, tk.END)
            self.product_price_entry.delete(0, tk.END)
            self.product_stock_entry.delete(0, tk.END)
            self.category_var.set("Choose Category")
        else:
            messagebox.showerror("Error", "Failed to add product.")

    def show_update_product_frame(self, product):
        # Destroy any existing update frame to prevent duplicates
        if hasattr(self, 'update_product_frame'):
            self.update_product_frame.destroy()

        # Create Update Product Frame
        self.update_product_frame = tk.Frame(self, bg="#F8F8F8", width=310, height=185)
        self.update_product_frame.place(x=520, y=10)
        self.update_product_frame.pack_propagate(False)
        self.update_product_frame.grid_propagate(False)

        # Product Details
        tk.Label(self.update_product_frame, text=product['product_name'], bg="#F8F8F8").grid(row=0, column=0, columnspan=2, pady=2)

        # New Name Entry
        tk.Label(self.update_product_frame, text="New Product Name:", bg="#F8F8F8").grid(row=1, column=0, padx=5, pady=5)
        self.new_name_entry = ttk.Entry(self.update_product_frame)
        self.new_name_entry.insert(0, product['product_name'])
        self.new_name_entry.grid(row=2, column=0, padx=5, pady=5)

        # Category Dropdown
        tk.Label(self.update_product_frame, text="Category:", bg="#F8F8F8").grid(row=1, column=1, padx=5, pady=5)
        self.update_category_var = tk.StringVar(value=product['product_category'].capitalize())
        self.update_category_dropdown = ttk.Combobox(self.update_product_frame, textvariable=self.update_category_var,
                                                     values=["Donuts", "Bread", "Cakes", "Sandwiches"],
                                                     state="readonly")
        self.update_category_dropdown.grid(row=2, column=1, padx=5, pady=5)

        # Stock Entry
        tk.Label(self.update_product_frame, text="Stock:", bg="#F8F8F8").grid(row=3, column=0, padx=5, pady=5)
        self.update_stock_entry = ttk.Entry(self.update_product_frame)
        self.update_stock_entry.insert(0, str(product['product_stock']))
        self.update_stock_entry.grid(row=4, column=0, padx=5, pady=5)

        # Price Entry
        tk.Label(self.update_product_frame, text="Price:", bg="#F8F8F8").grid(row=3, column=1, padx=5, pady=5)
        self.update_price_entry = ttk.Entry(self.update_product_frame)
        self.update_price_entry.insert(0, str(product['product_price']))
        self.update_price_entry.grid(row=4, column=1, padx=5, pady=5)

        # Buttons
        button_frame = tk.Frame(self.update_product_frame, bg="#F8F8F8")
        button_frame.grid(row=5, column=0, columnspan=2, pady=5)

        tk.Button(button_frame, text="Toss to Bin",
                  command=lambda: self.product_controller.delete_product(product['product_id'])).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Revise",
                  command=lambda p=product: self.product_controller.update_product(
                      p['product_id'],
                      self.new_name_entry.get().strip(),
                      self.update_category_var.get().strip(),
                      self.update_stock_entry.get().strip(),
                      self.update_price_entry.get().strip()
                  )).pack(side=tk.RIGHT, padx=10)



