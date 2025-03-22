import tkinter.messagebox as messagebox
from models.cashier_model import CashierModel

class ProductController:
    def __init__(self, view):
        self.view = view

    @staticmethod
    def display_products(self):
        # Fetch all the products
        products = CashierModel.get_all_products()

        # Categorize products using a dictionary
        categorized_products = {"All": products}
        for product in products:
            category = product["category"].capitalize()
            if category not in categorized_products:
                categorized_products[category] = []
            categorized_products[category].append(product)

        self.view.display_all_products(categorized_products)

    @staticmethod
    def add_product(name, price, stock, category):
        if not name or price <= 0 or stock < 0:
            print("Invalid product data. Please check the inputs.")
            return False
        CashierModel.add_product(name, price, stock, category)
        return True

    @staticmethod
    def get_all_products():
        products = CashierModel.get_all_products()
        if products:
            print("Products fetched")
        else:
            print("No products available.")
        return products

    @staticmethod
    def update_product(product_id, name, price, stock, category):
        if not name or price <= 0 or stock < 0:
            print("Invalid product data. Please check the inputs.")
            return False
        CashierModel.update_product(product_id, name, price, stock, category)
        return True

    @staticmethod
    def delete_product(product_id):
        confirmation = messagebox.askyesno("Delete Product", f"Are you sure you want to delete product ID {product_id}?")
        if confirmation:
            CashierModel.delete_product(product_id)
            print("Product deleted.")
            return True
        print("Operation canceled.")
        return False
