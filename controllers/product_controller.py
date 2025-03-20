import tkinter.messagebox as messagebox
from models.cashier_model import CashierModel

class ProductController:

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
            for product in products:
                # NOTE: Create the logic to display the products
                print(product)
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
