from models.Database import Database

class CashierModel:

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
        query = "SELECT * FROM products_tbl"
        try:
            connection = Database.get_connection()
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
    def add_sale(total_amount, payment_method):
        query = """
                INSERT INTO sales_tbl (sale_total, sale_payment_method)
                VALUES (%s, %s)
            """
        try:
            connection = Database.get_connection()
            cursor = connection.cursor()
            cursor.execute(query, (total_amount, payment_method))
            connection.commit()
            print("Sale recorded successfully.")
            return cursor.lastrowid
        except Exception as e:
            print(f"Error recording sale: {e}")
            return None
        finally:
            cursor.close()
            connection.close()
