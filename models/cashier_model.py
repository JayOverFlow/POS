from models.Database import Database

class CashierModel:
    def __init__(self):
        self.db = Database()

    # Product Management
    @staticmethod
    def add_product(name, price, stock, category):
        query = """
                    INSERT INTO products_tbl (product_name, product_price, product_stock, product_category)
                    VALUES (%s, %s, %s, %s)
                """
        try:
            conn = Database.get_connection()
            cursor = conn.cursor()
            cursor.execute(query, (name, price, stock, category))
            conn.commit()
            print("Product added successfully")
        except Exception as error:
            print(f"Error adding product: {error}")
        finally:
            cursor.close()
            conn.close()

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
    def update_product(product_id, name, price, stock, category):
        query = """
                UPDATE products_tbl
                SET product_name = %s, product_price = %s, product_stock = %s, product_category = %s
                WHERE product_id = %s
            """
        try:
            connection = Database.get_connection()
            cursor = connection.cursor()
            cursor.execute(query, (name, price, stock, category, product_id))
            connection.commit()
            print("Product updated successfully.")
        except Exception as e:
            print(f"Error updating product: {e}")
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def delete_product(product_id):
        query = "DELETE FROM products_tbl WHERE product_id = %s"
        try:
            connection = Database.get_connection()
            cursor = connection.cursor()
            cursor.execute(query, (product_id,))
            connection.commit()
            print("Product deleted successfully.")
        except Exception as e:
            print(f"Error deleting product: {e}")
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