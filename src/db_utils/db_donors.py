import sqlite3

class DatabaseConnector:
    def __init__(self):
        self.database_location = "src/data/theGivingCook.db"

    def connect(self):
        try:
            conn = sqlite3.connect(self.database_location)
            return conn
        except Exception as e:
            print(f"Error connecting to database: {e}")
            return None