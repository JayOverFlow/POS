import tkinter.messagebox as messagebox
from models.cashier_model import CashierModel
from decimal import Decimal

class ProductController:

    def __init__(self, view):
        self.view = view

    @staticmethod
    def get_all_products():
        products = CashierModel.get_all_products()
        if products:
            print("Products fetched")
        else:
            print("No products available.")
        return products

    def finalize_transaction(self, payment_method, cart_items):
        total_payment = sum(
            Decimal(str(data['product']['product_price'])) * data['quantity']
            for data in cart_items.values()
        )

        # Call the CashierModel to save the transaction
        success = CashierModel.save_transaction(payment_method, total_payment, cart_items)

        if success:
            messagebox.showinfo("Success", "Transaction recorded successfully.")
        else:
            messagebox.showerror("Error", "Failed to record the transaction.")

        self.view.cart_items.clear()
        self.view.receipt_frame.destroy()
        self.view.create_cart()
        self.view.display_products("All")

