from models.cashier_model import CashierModel
import tkinter.messagebox as messagebox


class SalesController:
    def __init__(self, view):
        self.view = view

    @staticmethod
    def save_transaction(payment_method, total_payment, cart_items):
        success = CashierModel.save_transaction(payment_method, total_payment, cart_items)
        if success:
            print("Transaction recorded successfully.")
        else:
            print("Failed to record transaction.")
        return success

