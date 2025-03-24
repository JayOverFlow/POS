import tkinter as tk
import customtkinter as ctk
from tkinter import ttk
import tkinter.font as tkFont
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

        # Define base directories
        BASE_DIR = Path(__file__).resolve().parent.parent

        self.font1 = font.Font(family="Instrument Serif",weight="normal", size=40)
        self.font2 = font.Font(family="Instrument Serif", size=20)

        # Canvas
        self.canvas = tk.Canvas(self, bg="#FFFFFF")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Heading
        self.canvas.create_text(350, 40, text="Cravings",font=self.font1)

        self.create_navigation_buttons()
        self.create_product_section()
        self.create_cart()
    # ---------------- Navigation Buttons ----------------
    def create_navigation_buttons(self):
        nav_frame = tk.Frame(self, bg="#FFFFFF", width=400, height=50)
        nav_frame.place(x=10, y=60)

        # Home Button
        ctk.CTkButton(nav_frame,
                      text="HOME",
                      corner_radius=2,  # Rounded corners
                      fg_color="#FFB2B3",  # Button background color
                      text_color="black",  # Button text color
                      width=100,  # Reduced button width
                      height=10,  # Reduced button height
                      command=self.create_product_section and self.create_cart
                      ).pack(side=tk.LEFT, padx=5)

        # Inventory Button
        ctk.CTkButton(nav_frame,
                      text="INVENTORY",
                      corner_radius=2,  # Rounded corners
                      fg_color="#FFB2B3",  # Button background color
                      text_color="black",  # Button text color
                      width=100,  # Reduced button width
                      height=10,  # Reduced button height
                      command=self.create_add_product_frame
                      ).pack(side=tk.LEFT, padx=5)

        # Sales Button
        ctk.CTkButton(nav_frame,
                      text="SALES",
                      corner_radius=2,  # Rounded corners
                      fg_color="#FFB2B3",  # Button background color
                      text_color="black",  # Button text color
                      width=100,  # Reduced button width
                      height=10,  # Reduced button height
                      command=self.create_sales_section
                      ).pack(side=tk.LEFT, padx=5)

    # ---------------- Product Section ----------------
    def create_product_section(self):
        self.destroy_inventory_and_update_frames()
        self.product_section = tk.Frame(self, bg="#F4F4F4", width=500, height=300)
        self.product_section.place(x=10, y=90)
        self.product_section.pack_propagate(False)

        # Create Category Buttons (Transparent + Underline)
        categories = ["All", "Donuts", "Bread", "Cakes", "Sandwiches"]
        self.category_frame = ctk.CTkFrame(self.product_section, fg_color="#F4F4F4", width=500, height=40)
        self.category_frame.place(x=0, y=0)

        # Create underline font
        underline_font = ctk.CTkFont(family="Instrument Serif", size=20, underline=True)

        for category in categories:
            ctk.CTkButton(
                self.category_frame,
                text=category,
                command=lambda c=category: self.display_products(c),
                fg_color="#F4F4F4",  # True transparency
                text_color="black",  # Text color
                font=underline_font,  # Underlined font
                corner_radius=0,  # No rounded corners
                border_width=0,  # No border
                width=90,  # Smaller width
            ).pack(side=ctk.LEFT, padx=5)

        # Create Scrollable Product Area
        self.canvas_frame = ctk.CTkCanvas(self.product_section, bg="#F4F4F4", width=550, height=250,
                                          highlightthickness=0)
        self.canvas_frame.place(x=5, y=50)

        # Increased width for the scrollbar (thicker appearance)
        self.scrollbar = ctk.CTkScrollbar(self.product_section,
                                          orientation="vertical",
                                          command=self.canvas_frame.yview,
                                          height=250,
                                          width=20)  # Adjust the width for thickness
        self.scrollbar.place(x=495, y=50)

        self.canvas_frame.configure(yscrollcommand=self.scrollbar.set)

        # Product Frame inside Canvas
        self.product_frame = ctk.CTkFrame(self.canvas_frame, fg_color="#F4F4F4")
        self.canvas_frame.create_window((0, 0), window=self.product_frame, anchor="nw")

        # self.create_cart()
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
        # Ensure add_product_frame exists and is valid before checking if it is mapped
        if (hasattr(self, 'add_product_frame') and
                self.add_product_frame.winfo_exists() and
                self.add_product_frame.winfo_ismapped()):
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
        self.cart_frame = tk.Frame(self, bg="#F4F4F4", width=310, height=460)
        self.cart_frame.place(x=520, y=10)
        self.cart_frame.pack_propagate(False)

        self.lbl = tk.Label(self.cart_frame, text="CART", font=self.font2)
        self.lbl.pack(side=tk.TOP)

        heading_font = font.Font(family="Inter Light", size=10)  # Heading font
        font1 = font.Font(family="Instrument Sans SemiBold", size=10)  # Input font

        # Style Configuration
        style = ttk.Style()
        style.theme_use('default')

        # Treeview Styling
        style.configure("Cart.Treeview",
                        font=("Instrument Sans", 9),
                        rowheight=25)

        style.configure("Cart.Treeview.Heading",
                        font=heading_font,
                        background="#FFB2B3",
                        foreground="black",
                        relief="flat",
                        padding=(5, 5))

        # Treeview for Cart
        self.cart_tree = ttk.Treeview(self.cart_frame,
                                      columns=("Order", "-", "Quantity", "+", "Price", "Remove"),
                                      show="headings",
                                      style="Cart.Treeview",
                                      height=5)

        # Set Treeview Headings
        self.cart_tree.heading("Order", text="Order")
        self.cart_tree.heading("-", text="")
        self.cart_tree.heading("Quantity", text="Quantity")
        self.cart_tree.heading("+", text="")
        self.cart_tree.heading("Price", text="Price")
        self.cart_tree.heading("Remove", text="")
        self.cart_tree.pack(fill=tk.BOTH, expand=True)

        # Set Treeview Columns
        self.cart_tree.column("Order", width=100, anchor=tk.CENTER)
        self.cart_tree.column("-", width=10, anchor=tk.CENTER)
        self.cart_tree.column("Quantity", width=60, anchor=tk.CENTER)
        self.cart_tree.column("+", width=10, anchor=tk.CENTER)
        self.cart_tree.column("Price", width=80, anchor=tk.CENTER)
        self.cart_tree.column("Remove", width=20, anchor=tk.CENTER)

        self.cart_tree.bind('<Button-1>', self.handle_cart_action)

        # Payment Dropdown Styling
        style.configure("Custom.TCombobox",
                        fieldbackground="#FDE0E0",
                        background="#FDE0E0",
                        foreground="#8A8A8A",
                        borderwidth=1,
                        relief="solid",
                        padding=(10, 5))

        style.map("Custom.TCombobox",
                  fieldbackground=[("readonly", "#FDE0E0"), ("!disabled", "#FDE0E0")],
                  selectbackground=[("readonly", "#FDE0E0")],
                  selectforeground=[("readonly", "#8A8A8A")],
                  arrowcolor=[("readonly", "#F5A5A5")])

        # Payment Frame
        self.payment_frame = tk.Frame(self.cart_frame, bg="#F4F4F4")
        self.payment_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=(10, 5))

        self.payment_var = tk.StringVar(value="Mode of Payment")
        self.payment_dropdown = ttk.Combobox(self.payment_frame,
                                             textvariable=self.payment_var,
                                             values=["Cash", "Gcash"],
                                             state="readonly",
                                             style="Custom.TCombobox")
        self.payment_dropdown.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)

        # Discount Entry Styling
        style.configure("Custom.TEntry",
                        fieldbackground="#FDE0E0",
                        foreground="#8A8A8A",
                        borderwidth=1,
                        relief="solid",
                        padding=(10, 5))

        style.map("Custom.TEntry",
                  fieldbackground=[("readonly", "#FDE0E0"), ("!disabled", "#FDE0E0")],
                  selectbackground=[("readonly", "#FDE0E0")],
                  selectforeground=[("readonly", "#8A8A8A")])

        # Discount Frame
        self.discount_frame = tk.Frame(self.cart_frame, bg="#F4F4F4")
        self.discount_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=(0, 10))

        tk.Label(self.discount_frame, text="Discount:", bg="#F4F4F4").pack(side=tk.LEFT)

        self.discount_var = tk.StringVar(value="Apply Discount")
        self.discount_entry = ttk.Entry(self.discount_frame,
                                        textvariable=self.discount_var,
                                        font=font1,
                                        style="Custom.TEntry")
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

        self.subtotal_label = tk.Label(self.summary_frame, text="Subtotal: ₱0.00", bg="#F4F4F4", font=font1)
        self.subtotal_label.pack(anchor="w")

        self.discount_applied_label = tk.Label(self.summary_frame, text="Discount Applied: ₱0.00", bg="#F4F4F4",
                                               font=font1)
        self.discount_applied_label.pack(anchor="w")

        self.total_payment_label = tk.Label(self.summary_frame, text="Total Payment: ₱0.00", bg="#F4F4F4",
                                            font=font1)
        self.total_payment_label.pack(anchor="w")

        self.discount_entry.bind("<KeyRelease>", lambda e: self.update_summary())
        self.cart_tree.bind("<<TreeviewSelect>>", lambda e: self.update_summary())

        # Button Frame (For Clear and Proceed Buttons)
        self.button_frame = ctk.CTkFrame(self.cart_frame, fg_color="#F4F4F4", height=100)
        self.button_frame.pack(side=ctk.TOP, fill=ctk.X, padx=30, pady=(10, 5))  # Changed to TOP and adjusted pady
        self.button_frame.pack_propagate(False)

        # Clear Button (CTkButton)
        self.clear_button = ctk.CTkButton(self.button_frame,
                                          text="Clear",
                                          fg_color="#FFB2B3",  # Background color
                                          text_color="black",  # Text color
                                          corner_radius=2,  # Rounded corners
                                          width=100,  # Button width
                                          command=self.clear_cart)
        self.clear_button.pack(side=ctk.LEFT, padx=5)

        # Proceed Button (CTkButton)
        self.proceed_button = ctk.CTkButton(self.button_frame,
                                            text="Proceed",
                                            fg_color="#FF6F6F",  # Background color
                                            text_color="white",  # Text color
                                            corner_radius=2,  # Rounded corners
                                            width=100,  # Button width
                                            command=self.proceed_checkout)
        self.proceed_button.pack(side=ctk.RIGHT, padx=5)

    def clear_cart(self):
        self.cart_items.clear()
        self.update_cart_view()

    # ---------------- Proceed Checkout ----------------
    def proceed_checkout(self):
        selected_payment = self.payment_var.get()
        if selected_payment not in ["Cash", "Gcash"]:
            messagebox.showwarning("Warning", "Please select a valid mode of payment before proceeding.")
            return

        if not self.cart_items:
            messagebox.showwarning("Warning", "Your cart is empty. Please add items before proceeding.")
            return

        self.cart_frame.destroy()

        # Create Receipt Frame
        self.receipt_frame = tk.Frame(self, bg="#FFE9E9", width=310, height=380,bd=5,relief="groove")
        self.receipt_frame.place(x=520, y=10)
        self.receipt_frame.pack_propagate(False)

        # Fonts
        small_font = font.Font(family="Instrument Sans", size=8)  # Smaller font for product names
        heading_font = font.Font(family="Instrument Sans SemiBold", size=9)  # Heading font

        # Date and Time
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        tk.Label(self.receipt_frame, text=f"Date & Time: {now}", bg="#FFE9E9").pack(anchor="w")

        # Style Configuration
        style = ttk.Style()

        # Treeview Header Style (Transparent Border)
        style.configure("Treeview.Heading",
                        font=heading_font,  # Use the heading font
                        background="#FDE0E0",  # Light pink header background
                        foreground="black",  # Black header text
                        relief="flat",  # Removes the border (flat style)
                        borderwidth=0)  # Ensures no border

        # Treeview Body Style (Transparent Border)
        style.configure("Receipt.Treeview",
                        background="#FFE9E9",  # Light gray row background
                        foreground="black",  # Black row text
                        rowheight=30,  # Increased row height for better spacing
                        fieldbackground="white",  # Background of entry fields
                        relief="flat",  # Removes the internal Treeview border
                        borderwidth=0)  # Ensures no outer border

        # Configure selected row style (for highlighting selected rows)
        style.map("Receipt.Treeview",
                  background=[("selected", "#FDE0E0")],  # Light pink when selected
                  foreground=[("selected", "black")])  # Black text on selection

        # Receipt Treeview
        receipt_tree = ttk.Treeview(self.receipt_frame, columns=("Unit", "Product Name", "Quantity", "Price"),
                                    style="Receipt.Treeview", show="headings", height=5)
        receipt_tree.heading("Unit", text="Unit")
        receipt_tree.heading("Product Name", text="Product Name")
        receipt_tree.heading("Quantity", text="Quantity")
        receipt_tree.heading("Price", text="Price")
        receipt_tree.pack(fill=tk.BOTH, expand=True)

        # Column Configuration
        receipt_tree.column("Unit", width=30, anchor=tk.CENTER)
        receipt_tree.column("Product Name", width=80, anchor=tk.CENTER)
        receipt_tree.column("Quantity", width=30, anchor=tk.CENTER)
        receipt_tree.column("Price", width=60, anchor=tk.CENTER)

        # Apply style to the Treeview
        receipt_tree.configure(style="Receipt.Treeview")

        # Configure the small font tag
        receipt_tree.tag_configure("small_font", font=small_font)  # Apply the smaller font to product names

        # Populate Treeview
        unit_count = 0
        subtotal = Decimal(0)

        for product_name, data in self.cart_items.items():
            unit_count += 1
            price = Decimal(data['product']['product_price']) * Decimal(data['quantity'])
            subtotal += price
            # Insert with the "small_font" tag to reduce product name font size
            receipt_tree.insert('', 'end', values=(unit_count, product_name, data['quantity'], f"₱{price:.2f}"),
                                tags=("small_font",))

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

        bottom_font = font.Font(family="Instrument Sans", size=12)
        # Display Summary
        tk.Label(self.receipt_frame, text=f"Subtotal: ₱{subtotal:.2f}",font=bottom_font, bg="#FFE9E9").pack(anchor="w")
        tk.Label(self.receipt_frame, text=f"Discount Applied: {discount_percentage:.2f}% (₱{discount_value:.2f})",font=bottom_font,
                 bg="#FFE9E9").pack(anchor="w")
        tk.Label(self.receipt_frame, text=f"Total : ₱{total_payment:.2f}", bg="#FFE9E9",
                 font=bottom_font).pack(anchor="w")

        (ctk.CTkButton(self.receipt_frame,
                      text="Continue",
                      command=self.finalize_transaction,
                      fg_color="#FFB2B3",  # Button background color
                      hover_color="#FFE9E9",
                      text_color="black",  # Text color
                      corner_radius=2)
         .pack(side=tk.BOTTOM, pady=10))

    # ---------------- Finalize Transaction ----------------
    def finalize_transaction(self):
        payment_method = self.payment_var.get()
        self.sales_controller.finalize_transaction(payment_method, self.cart_items)

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

        # Define fonts for the Treeview
        cart_font = font.Font(family="Instrument Sans", weight="bold", size=10)  # General font
        small_font = font.Font(family="Instrument Sans SemiBold", size=8)  # Smaller font for product names

        # Apply the custom font to the Treeview via a style
        style = ttk.Style()
        style.configure("Cart.Treeview", font=cart_font)

        # Clear existing items in the cart
        for item in self.cart_tree.get_children():
            self.cart_tree.delete(item)

        # Configure a tag for smaller product names
        self.cart_tree.tag_configure("small_order", font=small_font)

        # Populate the cart
        for product_name, data in self.cart_items.items():
            product = data['product']
            quantity = data['quantity']
            price = product['product_price'] * quantity

            # Insert rows with the small_order tag for the "Order" column
            self.cart_tree.insert('', 'end', values=(product_name, "-", quantity, "+", f"₱{price}", "🗑️"),
                                  tags=("small_order",))

        # Adjust column widths (customize as needed)
        self.cart_tree.column("Order", width=80, anchor=tk.CENTER)  # Adjust for product names
        self.cart_tree.column("Price", width=100)  # More space for prices
        self.cart_tree.column("Remove", width=50)  # Space for delete icon

        # Apply the style to the Treeview
        self.cart_tree.configure(style="Cart.Treeview")

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

        if hasattr(self, 'sale_receipt_frame'):
            self.sale_receipt_frame.destroy()

        if hasattr(self, 'sales_tree'):
            self.sales_tree.destroy()

        self.create_product_section()

        # Create Inventory Frame
        self.add_product_frame = tk.Frame(self, bg="#F4F4F4", width=310, height=185)
        self.add_product_frame.place(x=520, y=205)
        self.add_product_frame.pack_propagate(False)
        self.add_product_frame.grid_propagate(False)
        add_product_font = font.Font(family="Instrument Sans SemiBold", size=8)
        # Style Configuration (for Colored Entry and Combobox)
        style = ttk.Style()

        # Custom Entry Style (Colored)
        style.configure("Custom.TEntry",
                        fieldbackground="#FFF3CD",  # Entry background
                        foreground="black",  # Entry text color
                        borderwidth=1,  # Border width
                        padding=(5, 3))  # Padding for size control

        # Custom Combobox Style (Colored)
        style.configure("Custom.TCombobox",
                        fieldbackground="#FDE0E0",  # Background color
                        background="#FDE0E0",  # Dropdown background
                        foreground="black",  # Text color
                        borderwidth=1,  # Border width
                        padding=(5, 3))

        # Labels and Entry Widgets
        tk.Label(self.add_product_frame, text="Name of Product:", font=add_product_font, bg="#F4F4F4").grid(row=0,
                                                                                                            column=0,
                                                                                                            padx=5,
                                                                                                            pady=5)
        self.product_name_entry = ttk.Entry(self.add_product_frame, style="Custom.TEntry")
        self.product_name_entry.grid(row=1, column=0, padx=5, pady=5)

        tk.Label(self.add_product_frame, text="Price:", font=add_product_font, bg="#F4F4F4").grid(row=0, column=1,
                                                                                                  padx=5, pady=5)
        self.product_price_entry = ttk.Entry(self.add_product_frame, style="Custom.TEntry")
        self.product_price_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.add_product_frame, text="Category:", font=add_product_font, bg="#F4F4F4").grid(row=2, column=0,
                                                                                                     padx=5, pady=5)
        self.category_var = tk.StringVar(value="Choose Category")
        self.category_dropdown = ttk.Combobox(self.add_product_frame,
                                              textvariable=self.category_var,
                                              values=["Donuts", "Bread", "Cakes", "Sandwiches"],
                                              state="readonly",
                                              style="Custom.TCombobox")
        self.category_dropdown.grid(row=3, column=0, padx=5, pady=5)

        tk.Label(self.add_product_frame, text="Stock:", font=add_product_font, bg="#F4F4F4").grid(row=2, column=1,
                                                                                                  padx=5, pady=5)
        self.product_stock_entry = ttk.Entry(self.add_product_frame, style="Custom.TEntry")
        self.product_stock_entry.grid(row=3, column=1, padx=5, pady=5)
        bake_font = ctk.CTkFont(family="Instrument Sans", size=8,weight="bold")
        ctk.CTkButton(self.add_product_frame,
                      text="Bake",
                      command=self.add_product_to_database,
                      fg_color="#FFB2B3",
                      text_color="black",  # Text Color
                      corner_radius=2   ,  # Rounded Corners
                      width=130,  # Button Width
                      height=20
                      ).grid(row=4, column=0, columnspan=2, pady=10)

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

        update_font = font.Font(family="Instrument Serif", size=15)
        new_product = font.Font(family="Instrument Sans SemiBold", size=8, weight="bold")
        # Style Configuration (for Entry Backgrounds)
        style = ttk.Style()

        # Customize Entry widgets (Reduced Size)
        style.configure("Custom.TEntry",
                        fieldbackground="#FFF3CD",  # Background color
                        background="#FFF3CD",  # Background (for older versions)
                        foreground="black",  # Text color
                        padding=(3, 1))  # (Width, Height) - Reduced size

        # Payment Dropdown Styling (Reduced Size)
        style.configure("Custom.TCombobox",
                        fieldbackground="#FDE0E0",
                        background="#FDE0E0",
                        foreground="#8A8A8A",
                        borderwidth=1,
                        relief="solid",
                        padding=(3, 1))  # Reduced size (smaller dropdown height)

        # Customize the dropdown when readonly
        style.map("Custom.TCombobox",
                  fieldbackground=[("readonly", "#FDE0E0"), ("!disabled", "#FDE0E0")],
                  selectbackground=[("readonly", "#FDE0E0")],
                  selectforeground=[("readonly", "#8A8A8A")],
                  arrowcolor=[("readonly", "#F5A5A5")])

        # Product Details
        tk.Label(self.update_product_frame, text=product['product_name'], font=update_font, bg="#F8F8F8").grid(row=0,
                                                                                                               column=0,
                                                                                                               columnspan=2,
                                                                                                               pady=2)

        # New Name Entry
        tk.Label(self.update_product_frame, text="New Product Name:", font=new_product, bg="#F8F8F8").grid(row=1,
                                                                                                           column=0,
                                                                                                           padx=5,
                                                                                                           pady=5)
        self.new_name_entry = ttk.Entry(self.update_product_frame, style="Custom.TEntry")
        self.new_name_entry.insert(0, product['product_name'])
        self.new_name_entry.grid(row=2, column=0, padx=5, pady=5)

        # Category Dropdown
        tk.Label(self.update_product_frame, text="Category:", font=new_product, bg="#F8F8F8").grid(row=1, column=1,
                                                                                                   padx=5, pady=5)
        self.update_category_var = tk.StringVar(value=product['product_category'].capitalize())
        self.update_category_dropdown = ttk.Combobox(self.update_product_frame,
                                                     textvariable=self.update_category_var,
                                                     values=["Donuts", "Bread", "Cakes", "Sandwiches"],
                                                     style="Custom.TCombobox",
                                                     state="readonly")
        self.update_category_dropdown.grid(row=2, column=1, padx=5, pady=5)

        # Stock Entry
        tk.Label(self.update_product_frame, text="Stock:", font=new_product, bg="#F8F8F8").grid(row=3, column=0, padx=5,
                                                                                                pady=5)
        self.update_stock_entry = ttk.Entry(self.update_product_frame, style="Custom.TEntry")
        self.update_stock_entry.insert(0, str(product['product_stock']))
        self.update_stock_entry.grid(row=4, column=0, padx=5, pady=5)

        # Price Entry
        tk.Label(self.update_product_frame, text="Price:", font=new_product, bg="#F8F8F8").grid(row=3, column=1, padx=5,
                                                                                                pady=5)
        self.update_price_entry = ttk.Entry(self.update_product_frame, style="Custom.TEntry")
        self.update_price_entry.insert(0, str(product['product_price']))
        self.update_price_entry.grid(row=4, column=1, padx=5, pady=5)

        # Buttons
        button_frame = tk.Frame(self.update_product_frame, bg="#F8F8F8")
        button_frame.grid(row=5, column=0, columnspan=2, pady=5)

        # Toss to Bin Button (Smaller size)
        ctk.CTkButton(button_frame,
                      text="Toss to Bin",
                      command=lambda: self.product_controller.delete_product(product['product_id']),
                      fg_color="#FDE0E0",  # Light pink background
                      hover_color="#E5533C",  # Darker red (hover effect)
                      text_color="black",  # Black text
                      corner_radius=2,  # Less rounded corners
                      width=60,  # Reduced width
                      height=15  # Reduced height
                      ).pack(side=tk.LEFT, padx=5)

        # Revise Button (Smaller size)
        ctk.CTkButton(button_frame,
                      text="Revise",
                      command=lambda p=product: self.product_controller.update_product(
                          p['product_id'],
                          self.new_name_entry.get().strip(),
                          self.update_category_var.get().strip(),
                          self.update_stock_entry.get().strip(),
                          self.update_price_entry.get().strip()
                      ),
                      fg_color="#FFB2B3",  # Light red background
                      hover_color="#36648B",  # Darker blue (hover effect)
                      text_color="black",  # Black text
                      corner_radius=2,  # Less rounded corners
                      height=15  # Reduced height
                      ).pack(side=tk.RIGHT, padx=10)

    def destroy_inventory_and_update_frames(self):
        if hasattr(self, 'add_product_frame') and self.add_product_frame.winfo_exists():
            self.add_product_frame.destroy()

        if hasattr(self, 'update_product_frame') and self.update_product_frame.winfo_exists():
            self.update_product_frame.destroy()

    def create_sales_section(self):
        # Destroy Cart Frame if it exists
        if hasattr(self, 'cart_frame'):
            self.cart_frame.destroy()
        self.destroy_inventory_and_update_frames()

        self.sales_frame = tk.Frame(self, bg="#F4F4F4", width=500, height=300)
        self.sales_frame.place(x=10, y=90)
        self.sales_frame.pack_propagate(False)

        sales_font = font.Font(family="Instrument Serif", size=10)
        sales_item_font = font.Font(family="Instrument Sans SemiBold", size=10)
        # Treeview for Sales
        style = ttk.Style()

        # Configure Treeview Header
        style.configure("Sales.Treeview.Heading",
                        font=sales_font,
                        background="#FDE0E0",  # Soft pink background
                        foreground="black",  # Black text
                        relief="flat")  # Flat header

        # Configure Treeview Rows
        style.configure("Sales.Treeview",
                        font=sales_item_font,
                        background="#F8F8F8",  # Light grey rows
                        foreground="black",  # Black text
                        rowheight=20,  # Taller rows for better appearance
                        fieldbackground="#F8F8F8")

        # Highlighted Row (when selected)
        style.map("Sales.Treeview",
                  background=[("selected", "#FAD2D2")],  # Soft red on selection
                  foreground=[("selected", "black")])

        self.sales_tree = ttk.Treeview(self.sales_frame,
                                       columns=("Sale ID", "Payment", "Amount", "Date", "Time"),
                                       show="headings",
                                       style="Sales.Treeview")

        # Set Treeview Headings
        self.sales_tree.heading("Sale ID", text="Sale ID")
        self.sales_tree.heading("Payment", text="Payment")
        self.sales_tree.heading("Amount", text="Amount")
        self.sales_tree.heading("Date", text="Date")
        self.sales_tree.heading("Time", text="Time")
        self.sales_tree.pack(fill=tk.BOTH, expand=True)

        # Set Treeview Columns
        self.sales_tree.column("Sale ID", width=100, anchor=tk.CENTER)
        self.sales_tree.column("Payment", width=100, anchor=tk.CENTER)
        self.sales_tree.column("Amount", width=100, anchor=tk.CENTER)
        self.sales_tree.column("Date", width=100, anchor=tk.CENTER)
        self.sales_tree.column("Time", width=100, anchor=tk.CENTER)

        self.display_sales()

        self.sales_tree.bind('<Button-1>', self.handle_sale_click)

    def display_sales(self):
        self.sales_controller.display_sales()

    def handle_sale_click(self, event):
        # Get the selected item
        sale_record = self.sales_tree.selection()
        if not sale_record:
            return

        sale_data = self.sales_tree.item(sale_record)['values']
        if not sale_data:
            return

        sale_id = sale_data[0]
        sale_receipt_data = self.sales_controller.display_sale_receipt(sale_id)

        if not sale_receipt_data:
            messagebox.showerror("Error", "Failed to retrieve sale details.")
            return

        # Destroy previous receipt frame if it exists
        if hasattr(self, 'sale_receipt_frame'):
            self.sale_receipt_frame.destroy()

        # Create Receipt Frame
        self.sale_receipt_frame = tk.Frame(self, bg="#FFE9E9", width=300, height=300)
        self.sale_receipt_frame.place(x=520, y=90)
        self.sale_receipt_frame.pack_propagate(False)

        # Display Date and Time (Assuming the first row contains the timestamp and total)
        sale_timestamp = sale_receipt_data[0]['sale_timestamp']
        sale_date = sale_timestamp.strftime('%m/%d/%Y')
        sale_time = sale_timestamp.strftime('%H:%M:%S')

        tk.Label(self.sale_receipt_frame, text=f"Date: {sale_date}", bg="#FFE9E9").pack(anchor="w")
        tk.Label(self.sale_receipt_frame, text=f"Time: {sale_time}", bg="#FFE9E9").pack(anchor="w")

        # Treeview for Sales Items
        self.sales_receipt_tree = ttk.Treeview(self.sale_receipt_frame,
                                               columns=("Unit", "Product", "Quantity", "Price"),
                                               show="headings")

        # Set Treeview Headings
        self.sales_receipt_tree.heading("Unit", text="Unit")
        self.sales_receipt_tree.heading("Product", text="Product")
        self.sales_receipt_tree.heading("Quantity", text="Quantity")
        self.sales_receipt_tree.heading("Price", text="Price")
        self.sales_receipt_tree.pack(fill=tk.BOTH, expand=True)

        tk.Label(
            self.sale_receipt_frame,
            text=f"Total: ₱{float(sale_data[2]):.2f}",
            bg="#FFE9E9",
            font=("Arial", 10, "bold")
        ).pack(anchor="w")


        # Set Treeview Columns
        self.sales_receipt_tree.column("Unit", width=50, anchor=tk.CENTER)
        self.sales_receipt_tree.column("Product", width=80, anchor=tk.CENTER)
        self.sales_receipt_tree.column("Quantity", width=80, anchor=tk.CENTER)
        self.sales_receipt_tree.column("Price", width=80, anchor=tk.CENTER)

        # Populate Treeview with Sales Items
        for index, row in enumerate(sale_receipt_data):
            self.sales_receipt_tree.insert('', 'end', values=(
                index + 1,
                row['product_name'],
                row['sale_item_quantity'],
                f"₱{row['product_price']:.2f}"
            ))

