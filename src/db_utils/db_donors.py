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
    
    def update_inventory_qty_individual(self, inventory_id):
        try:
            conn = self.connect()
            if conn is None:
                return False
            cur = conn.cursor()

            cur.execute("""
                UPDATE inventory
                SET qty_left_after_scanning = qty_left_after_scanning - 1
                WHERE id = ? AND qty_left_after_scanning > 0
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
                SET qty_left_after_scanning = CASE
                            WHEN qty_left_after_scanning > ? THEN qty_left_after_scanning - ?
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
                SELECT id, food_name, food_type, description, is_halal, is_vegetarian, expiry, date_of_entry, total_qty, qty_left_after_booking, qty_left_after_scanning, qr_code
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
                       expiry, date_of_entry, total_qty, qty_left_after_booking, qty_left_after_scanning, qr_code
                FROM inventory
                WHERE id = ?
            """, (item_id,))

            donation = cur.fetchone()
            conn.close()
            return donation
        except Exception as e:
            print(f"Error retrieving donation: {e}")
            return None

    def update_inventory_item(self, item_id, food_name, food_type, description, is_halal, is_vegetarian, expiry_date, total_qty, qty_left_after_booking, qty_left_after_scanning,):
        try:
            conn = self.connect()
            if conn is None:
                return False
            cur = conn.cursor()

            cur.execute("""
                UPDATE inventory
                SET food_name = ?, food_type = ?, description = ?, is_halal = ?, 
                    is_vegetarian = ?, expiry = ?, total_qty = ?, qty_left_after_booking = ?, qty_left_after_scanning = ?
                WHERE id = ?
            """, (food_name, food_type, description, is_halal, is_vegetarian, expiry_date, total_qty, qty_left_after_booking, qty_left_after_scanning, item_id))

            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error updating inventory item: {e}")
            return False


    def updateVendor(self, vendor_id, name, hp_number, address, cuisine, description):
        try:
            conn = self.connect()
            if conn is None:
                return False
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

    def add_new_inventory_item_without_qrcode(self, food_name, food_type, description, is_halal, is_vegetarian,
                                                            expiry_date, quantity, vendor_id, image):
        try:
            conn = self.connect()
            if conn is None:
                return False
            cur = conn.cursor()

        except Exception as e:
            print(f"An error occurred: {e}")
            return False