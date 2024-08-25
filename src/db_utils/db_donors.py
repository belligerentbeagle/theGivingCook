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
    
    def get_vendor_donations(self, vendor_id):
        try:
            conn = self.connect()
            if conn is None:
                return False
            cur = conn.cursor()

            cur.execute("""
                SELECT id, food_name, food_type, description, is_halal, is_vegetarian, expiry, date_of_entry, total_qty, curr_qty, qr_code
                FROM inventory
                WHERE vendor_id = ?
            """, (vendor_id,))

            donations = cur.fetchall()

            conn.close()

            return donations
        except Exception as e:
            print(f"Error retrieving vendor donations: {e}")
            return None
    
    def get_donation_by_id(self, item_id):
        try:
            conn = self.connect()
            if conn is None:
                return None
            cur = conn.cursor()

            cur.execute("""
                SELECT id, food_name, food_type, description, is_halal, is_vegetarian, 
                       expiry, date_of_entry, total_qty, curr_qty, qr_code
                FROM inventory
                WHERE id = ?
            """, (item_id,))

            donation = cur.fetchone()
            conn.close()
            return donation
        except Exception as e:
            print(f"Error retrieving donation: {e}")
            return None

    def update_inventory_item(self, item_id, food_name, food_type, description, is_halal, is_vegetarian, expiry_date, total_qty, curr_qty):
        try:
            conn = self.connect()
            if conn is None:
                return False
            cur = conn.cursor()

            cur.execute("""
                UPDATE inventory
                SET food_name = ?, food_type = ?, description = ?, is_halal = ?, 
                    is_vegetarian = ?, expiry = ?, total_qty = ?, curr_qty = ?
                WHERE id = ?
            """, (food_name, food_type, description, is_halal, is_vegetarian, expiry_date, total_qty, curr_qty, item_id))

            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error updating inventory item: {e}")
            return False