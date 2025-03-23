from models.Database import Database
from main_controller import MainController

def main():
    # Configure your database
    db_config = {
        "host": "localhost",
        "user": "root",
        "password": "1234",
        "database": "pos"
    }

    # Initialize database connection
    Database.initialize(db_config)

    # Start the main controller (it acts as the Tkinter root)
    app = MainController()
    app.mainloop()

if __name__ == "__main__":
    main()
