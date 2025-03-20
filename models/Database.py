import mysql.connector
from mysql.connector import pooling

class Database:
    _connection_pool = None

    @classmethod
    def initialize(cls, db_config):
        try:
            cls._connection_pool = pooling.MySQLConnectionPool(
                pool_name="pos_pool",
                pool_size=10,
                **db_config
            )
            print("Database connection pool initialized.")
        except mysql.connector.Error as e:
            print(f"Error initializing database connection pool: {e}")

    @classmethod
    def get_connection(cls):
        try:
            return cls._connection_pool.get_connection()
        except mysql.connector.Error as e:
            print(f"Error getting database connection: {e}")
            return None
