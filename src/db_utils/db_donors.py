import sqlite3

class DatabaseConnector:
    def __init__(self, database_location="src/data/theGivingCook.db"):
        self.database_location = database_location

    def connect(self):
        try:
            conn = sqlite3.connect(self.database_location)
            return conn
        except Exception as e:
            print(f"Error connecting to database: {e}")
            return None
    
    def update_inventory_qty_individual(self, inventory_id):
        try:
            conn = self.connect()
            if conn is None:
                return False
            cur = conn.cursor()

            cur.execute("""
                UPDATE inventory
                SET curr_qty = curr_qty - 1
                WHERE id = ? AND curr_qty > 0
            """, (inventory_id,))

            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error updating inventory quantity: {e}")
            return False
    
    def update_inventory_qty_ngo(self, inventory_id, qty):
        try:
            conn = self.connect()
            if conn is None:
                return False
            cur = conn.cursor()

            cur.execute("""
                UPDATE inventory
                SET curr_qty = CASE
                            WHEN curr_qty > ? THEN curr_qty - ?
                            ELSE 0
                        END
                WHERE id = ?
            """, (qty, qty, inventory_id))

            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error updating inventory quantity: {e}")
            return False
    