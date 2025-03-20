from models.cashier_model import CashierModel
import tkinter.messagebox as messagebox


class SalesController:

    @staticmethod
    def process_sale(cart_items, total_amount, payment_method):
        # NOTE: cart_items structure:
        # cart_items = [
        #     {
        #         "product_id": 1,
        #         "product_name": "Milk",
        #         "quantity": 2,
        #         "subtotal": 160.00  # price * quantity
        #     },
        #     {
        #         "product_id": 2,
        #         "product_name": "Bread",
        #         "quantity": 1,
        #         "subtotal": 60.00
        #     }
        # ]

        if not cart_items:
            messagebox.showerror("Error", "Cart is empty. Please add items before processing the sale.")
            return False

        if total_amount <= 0:
            messagebox.showerror("Error", "Invalid total amount.")
            return False

        # Insert sale into the database
        sale_id = CashierModel.add_sale(total_amount, payment_method)

        if not sale_id:
            messagebox.showerror("Error", "Failed to record sale.")
            return False

        # Insert sale items into sales_items table
        for item in cart_items:
            product_id = item['product_id']
            quantity = item['quantity']
            subtotal = item['subtotal']
            CashierModel.add_sale_item(sale_id, product_id, quantity, subtotal)

        messagebox.showinfo("Success", "Sale processed successfully!")
        return True

    @staticmethod
    def generate_receipt(sale_id, cart_items, total_amount, payment_method):
        receipt_text = f"Receipt - Sale ID: {sale_id}\nPayment Method: {payment_method}\n\n"
        receipt_text += "Item\tQuantity\tSubtotal\n"
        for item in cart_items:
            receipt_text += f"{item['product_name']}\t{item['quantity']}\t₱{item['subtotal']:.2f}\n"
        receipt_text += f"\nTotal: ₱{total_amount:.2f}"

        # Display or print the receipt (can be extended to save as file)
        # NOTE: Create a logic for display the receipt on the UI
        print(receipt_text)
        return receipt_text
