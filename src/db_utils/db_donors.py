import sqlite3
from datetime import datetime

from src.db_utils.image_to_blob_util import image_to_blob


class DatabaseConnector:
    def __init__(self, database_location="src/data/theGivingCook.db"):  # might need to set to ../data/theGivingCook.db
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

    def update_inventory_item(self, item_id, food_name, food_type, description, is_halal, is_vegetarian, expiry_date,
                              total_qty, qty_left_after_booking, qty_left_after_scanning, ):
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
            """, (
            food_name, food_type, description, is_halal, is_vegetarian, expiry_date, total_qty, qty_left_after_booking,
            qty_left_after_scanning, item_id))

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
                                              expiry_date, quantity, for_ngo, vendor_id, image):
        try:
            conn = self.connect()
            if conn is None:
                return False
            cur = conn.cursor()

            date_of_entry = datetime.now().strftime('%Y-%m-%d')
            image_blob = image_to_blob(image)

            cur.execute("""
                INSERT INTO inventory (
                    food_name,
                    food_type,
                    description,
                    is_halal,
                    is_vegetarian,
                    expiry,
                    date_of_entry,
                    total_qty,
                    qty_left_after_booking,
                    qty_left_after_scanning,
                    for_ngo,
                    vendor_id,
                    photo
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                food_name, food_type, description, is_halal, is_vegetarian, expiry_date, date_of_entry,
                quantity, quantity, quantity, for_ngo, vendor_id, image_blob))

            conn.commit()

            item_id = cur.lastrowid

            cur.close()
            conn.close()

            return item_id

        except Exception as e:
            print(f"An error occurred: {e}")
            return False

    def update_inventory_item_with_qr_code(self, item_id, qr_code):
        try:
            conn = self.connect()
            if conn is None:
                return False
            cur = conn.cursor()

            image_blob = image_to_blob(qr_code)

            cur.execute("""
                UPDATE inventory
                SET qr_code = ?
                WHERE id = ?
            """, (image_blob, item_id))

            conn.commit()

            cur.close()
            conn.close()

            return True

        except Exception as e:
            print(f"An error occurred: {e}")
            if conn:
                conn.close()  # Ensure the connection is closed even if an error occurs
            return False

    def add_item_price(self, item_id, price):
        try:
            conn = self.connect()
            if conn is None:
                return False
            cur = conn.cursor()

            cur.execute("""
                INSERT INTO price_inventory (
                    food_id,
                    price
                )
                VALUES (?, ?)
            """, (item_id, price))

            conn.commit()

            cur.close()
            conn.close()

            return True

        except Exception as e:
            print(f"An error occurred: {e}")
            if conn:
                conn.close()  # Ensure the connection is closed even if an error occurs
            return False

def validateIfUserMadeBookingWithInventoryId(self, inventory_id, user_id):
    try:
        conn = self.connect()
        if conn is None:
            return False
        cur = conn.cursor()

        # Query to check if the user has made a booking for the specified inventory_id
        cur.execute("""
            SELECT id FROM orders
            WHERE user_id = ? AND item_id = ?
        """, (user_id, inventory_id))

        booking = cur.fetchone()
        conn.close()

        # Return True if a booking is found, otherwise False
        return booking is not None
    except Exception as e:
        print(f"Error validating booking: {e}")
        return False
