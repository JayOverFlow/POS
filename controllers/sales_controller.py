from models.cashier_model import CashierModel
import tkinter.messagebox as messagebox
from decimal import Decimal


class SalesController:
    def __init__(self, view):
        self.view = view

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

    def display_sales(self):
        sales = CashierModel.get_all_sales()

        if not sales:
            return None

        for sale in sales:
            sale_timestamp = sale['sale_timestamp']

            if isinstance(sale_timestamp, str):
                # If timestamp is a string, parse it to a datetime object
                sale_timestamp = datetime.strptime(sale_timestamp, '%Y-%m-%d %H:%M:%S')

            # Extract and format Date
            sale_date = sale_timestamp.strftime('%m/%d/%Y')

            # Extract and format Time
            sale_time = sale_timestamp.strftime('%H:%M:%S')

            # Insert into Treeview
            self.view.sales_tree.insert('', 'end', values=(
            sale['sale_id'], sale['sale_payment_method'], sale['sale_total'], sale_date, sale_time))

    def display_sale_receipt(self, sale_id):
        return CashierModel.get_sale_receipt(sale_id)

