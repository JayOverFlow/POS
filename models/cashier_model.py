from models.Database import Database

class CashierModel:
    def __init__(self):
        self.db = Database()

    # Product Management
    @staticmethod
    def add_product(name, price, category, stock):
        try:
            connection = Database.get_connection()
            query = """
                INSERT INTO products_tbl (product_name, product_price, product_category, product_stock)
                VALUES (%s, %s, %s, %s)
            """
            cursor = connection.cursor()
            cursor.execute(query, (name, price, category, stock))
            connection.commit()
            return True
        except Exception as e:
            print(f"Error adding product: {e}")
            return False
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def get_all_products():
        try:
            connection = Database.get_connection()
            query = "SELECT * FROM products_tbl"
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query)
            products = cursor.fetchall()
            return products
        except Exception as e:
            print(f"Error fetching products: {e}")
            return []
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def update_product(product_id, new_name, new_category, new_stock, new_price):
        try:
            connection = Database.get_connection()
            query = """
                        UPDATE products_tbl 
                        SET product_name = %s, product_category = %s, product_stock = %s, product_price = %s
                        WHERE product_id = %s
                    """
            cursor = connection.cursor()
            cursor.execute(query, (new_name, new_category, new_stock, new_price, product_id))
            connection.commit()
            return True
        except Exception as e:
            print(f"Error updating product: {e}")
            return False
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def delete_product(product_id):
        try:
            connection = Database.get_connection()
            query = "DELETE FROM products_tbl WHERE product_id = %s"
            cursor = connection.cursor()
            cursor.execute(query, (product_id,))
            connection.commit()
            return True
        except Exception as e:
            print(f"Error deleting product: {e}")
            return False
        finally:
            cursor.close()
            connection.close()

    # Sales Management
    @staticmethod
    def save_transaction(payment_method, total_payment, cart_items):
        try:
            connection = Database.get_connection()
            cursor = connection.cursor()

            # Insert into sales_tbl
            query = """
                INSERT INTO sales_tbl (sale_total, sale_payment_method)
                VALUES (%s, %s)
            """
            cursor.execute(query, (total_payment, payment_method))
            sale_id = cursor.lastrowid

            # Insert into sales_items
            query = """
                INSERT INTO sales_items (sale_id_fk, product_id_fk, sale_item_quantity, sale_item_subtotal)
                VALUES (%s, %s, %s, %s)
            """
            for product_name, data in cart_items.items():
                product_id = data['product']['product_id']
                quantity = data['quantity']
                subtotal = data['product']['product_price'] * quantity

                cursor.execute(query, (sale_id, product_id, quantity, subtotal))

            connection.commit()
            print("Transaction saved successfully")
            return True
        except Exception as e:
            print(f"Error saving transaction: {e}")
            connection.rollback()
            return False
        finally:
            cursor.close()
            connection.close()