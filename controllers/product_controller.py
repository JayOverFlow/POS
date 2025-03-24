import tkinter.messagebox as messagebox
from models.cashier_model import CashierModel
from decimal import Decimal

class ProductController:
    def __init__(self, view):
        self.view = view

    def add_product(self, name, price, category, stock):
        # Call the model to add product to the database
        success = CashierModel.add_product(name, price, category, stock)
        if success:
            self.view.display_products("All")  # Refresh product display if needed
            self.view.create_add_product_frame()
            return True
        else:
            return False

    @staticmethod
    def get_all_products():
        products = CashierModel.get_all_products()
        if products:
            print("Products fetched")
        else:
            print("No products available.")
        return products


    def update_product(self, product_id, new_name, new_category, new_stock, new_price):
        # Validate Inputs
        if not new_name.strip():
            messagebox.showerror("Invalid Input", "Product name cannot be empty.")
            return

        valid_categories = ["Donuts", "Bread", "Cakes", "Sandwiches"]
        if new_category not in valid_categories:
            messagebox.showerror("Invalid Category", "Please select a valid category.")
            return

        try:
            new_stock = int(new_stock)
            if new_stock < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Input", "Stock must be a non-negative integer.")
            return

        try:
            new_price = Decimal(new_price)
            if new_price <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Input", "Price must be a positive number.")
            return

        # Perform Update
        if CashierModel.update_product(product_id, new_name, new_category, new_stock, new_price):
            messagebox.showinfo("Success", "Product updated successfully!")
            self.view.display_products("All")  # Refresh product display if needed
            self.view.create_add_product_frame()
        else:
            messagebox.showerror("Error", "Failed to update product. Please try again.")

    def delete_product(self, product_id):
        if messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this product?"):
            if CashierModel.delete_product(product_id):
                messagebox.showinfo("Success", "Product deleted successfully!")
                self.view.display_products("All")  # Refresh product display if needed
                self.view.create_add_product_frame()
            else:
                messagebox.showerror("Error", "Failed to delete the product.")