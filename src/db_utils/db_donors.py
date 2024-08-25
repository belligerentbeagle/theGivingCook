import sqlite3

class DatabaseConnector:
    def __init__(self, database_location="src/data/theGivingCook.db"): # might need to set to ../data/theGivingCook.db
        self.database_location = database_location

    def connect(self):
        try:
            conn = sqlite3.connect(self.database_location)
            return conn
        except Exception as e:
            print(f"Error connecting to database: {e}")
            return None
    
    def update_inventory_qty(self, collection_type, inventory_id):
        try:
            conn = self.connect()
            if conn is None:
                return False
            cur = conn.cursor()

            if collection_type == "individual":
                cur.execute("""
                    UPDATE inventory
                    SET qty = qty - 1
                    WHERE id = ? AND qty > 0
                """, (inventory_id,))
            elif collection_type == "ngo":
                cur.execute("""
                    UPDATE inventory
                    SET qty = 0
                    WHERE id = ?
                """, (inventory_id,))

            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error updating inventory quantity: {e}")
            return False

def updateVendor(vendor_id, name, hp_number, address, cuisine, description, database_loc="theGivingCook.db"):
    try:
        conn = sqlite3.connect(database_loc)
        cur = conn.cursor()
        cur.execute("""
            UPDATE vendor
            SET name = ?, hp_number = ?, address = ?, cuisine = ?, description = ?
            WHERE id = ?
        """, (name, hp_number, address, cuisine, description, vendor_id))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return False