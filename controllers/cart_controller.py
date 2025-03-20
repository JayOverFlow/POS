import tkinter.messagebox as messagebox

class CartController:
    def __init__(self):
        self.cart_items = []

    # Add product into cart
    def add_to_cart(self, product_id, product_name, price):
        # Check if the product already exists in the cart
        for item in self.cart_items:
            if item['product_id'] == product_id:
                item['quantity'] += 1
                item['subtotal'] = item['quantity'] * price
                break
        else:
            subtotal = price
            self.cart_items.append({
                'product_id': product_id,
                'product_name': product_name,
                'price': price,
                'quantity': 1,
                'subtotal': subtotal
            })
        messagebox.showinfo("Success", f"{product_name} added to cart.")

    # Add product quantity
    def increment_quantity(self, product_id):
        for item in self.cart_items:
            if item['product_id'] == product_id:
                item['quantity'] += 1
                item['subtotal'] = item['quantity'] * item['price']
                messagebox.showinfo("Success", f"Increased quantity of {item['product_name']} to {item['quantity']}.")
                return
        messagebox.showerror("Error", "Product not found in cart.")

    # Subtract product quantity
    def decrement_quantity(self, product_id):
        for item in self.cart_items:
            if item['product_id'] == product_id:
                if item['quantity'] > 1:
                    item['quantity'] -= 1
                    item['subtotal'] = item['quantity'] * item['price']
                    messagebox.showinfo("Success", f"Decreased quantity of {item['product_name']} to {item['quantity']}.")
                else:
                    self.remove_from_cart(product_id)
                return
        messagebox.showerror("Error", "Product not found in cart.")

    # Remove product from cart
    def remove_from_cart(self, product_id):
        self.cart_items = [item for item in self.cart_items if item['product_id'] != product_id]
        messagebox.showinfo("Success", "Product removed from cart.")

    # Calculate the total price
    def calculate_total(self, discount=0, tax_rate=0.12):
        subtotal = sum(item['subtotal'] for item in self.cart_items)
        discount_amount = subtotal * (discount / 100)
        tax_amount = (subtotal - discount_amount) * tax_rate
        total = (subtotal - discount_amount) + tax_amount
        return {
            'subtotal': subtotal,
            'discount_amount': discount_amount,
            'tax_amount': tax_amount,
            'total': total
        }
