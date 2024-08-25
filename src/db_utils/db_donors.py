import sqlite3
from datetime import datetime
from src.db_utils.image_to_blob_util import image_to_blob

database_location = "src/data/theGivingCook.db"

def connect(database_loc=database_location):
    try:
        conn = sqlite3.connect(database_loc)
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

def update_inventory_qty_individual(inventory_id, database_loc=database_location):
    try:
        conn = connect(database_loc)
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

def update_inventory_qty_ngo(inventory_id, qty, database_loc=database_location):
    try:
        conn = connect(database_loc)
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

def get_vendor_donations(vendor_id, database_loc=database_location):
    try:
        conn = connect(database_loc)
        if conn is None:
            return None
        cur = conn.cursor()

        cur.execute("""
            SELECT id, food_name, food_type, description, is_halal, is_vegetarian, 
                   expiry, date_of_entry, total_qty, qty_left_after_booking, qty_left_after_scanning, photo, qr_code
            FROM inventory
            WHERE vendor_id = ?
        """, (vendor_id,))

        donations = cur.fetchall()
        conn.close()
        return donations
    except Exception as e:
        print(f"Error retrieving vendor donations: {e}")
        return None

def get_donation_by_id(item_id, database_loc=database_location):
    try:
        conn = connect(database_loc)
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

def update_inventory_item(item_id, food_name, food_type, description, is_halal, is_vegetarian, expiry_date, 
                          total_qty, qty_left_after_booking, qty_left_after_scanning, database_loc=database_location):
    try:
        conn = connect(database_loc)
        if conn is None:
            return False
        cur = conn.cursor()

        cur.execute("""
            UPDATE inventory
            SET food_name = ?, food_type = ?, description = ?, is_halal = ?, 
                is_vegetarian = ?, expiry = ?, total_qty = ?, qty_left_after_booking = ?, qty_left_after_scanning = ?
            WHERE id = ?
        """, (food_name, food_type, description, is_halal, is_vegetarian, expiry_date, 
              total_qty, qty_left_after_booking, qty_left_after_scanning, item_id))

        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error updating inventory item: {e}")
        return False

def update_vendor(vendor_id, name, hp_number, address, cuisine, description, database_loc=database_location):
    try:
        conn = connect(database_loc)
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

def add_new_inventory_item_without_qrcode(food_name, food_type, description, is_halal, is_vegetarian,
                                          expiry_date, quantity, for_ngo, vendor_id, image, database_loc=database_location):
    try:
        conn = connect(database_loc)
        if conn is None:
            return False
        cur = conn.cursor()

        date_of_entry = datetime.now().strftime('%Y-%m-%d')
        image_blob = image_to_blob(image)

        cur.execute("""
            INSERT INTO inventory (
                food_name, food_type, description, is_halal, is_vegetarian, 
                expiry, date_of_entry, total_qty, qty_left_after_booking, 
                qty_left_after_scanning, for_ngo, vendor_id, photo
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (food_name, food_type, description, is_halal, is_vegetarian, expiry_date, 
              date_of_entry, quantity, quantity, quantity, for_ngo, vendor_id, image_blob))

        conn.commit()

        item_id = cur.lastrowid

        cur.close()
        conn.close()

        return item_id

    except Exception as e:
        print(f"An error occurred: {e}")
        return False

def update_inventory_item_with_qr_code(item_id, qr_code, database_loc=database_location):
    try:
        conn = connect(database_loc)
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
            conn.close()
        return False

def add_item_price(item_id, price, database_loc=database_location):
    try:
        conn = connect(database_loc)
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
            conn.close()
        return False

def validate_if_user_made_booking_with_inventory_id(inventory_id, user_id, database_loc=database_location):
    try:
        conn = connect(database_loc)
        if conn is None:
            return False
        cur = conn.cursor()

        cur.execute("""
            SELECT id FROM orders
            WHERE user_id = ? AND item_id = ?
        """, (user_id, inventory_id))

        booking = cur.fetchone()
        conn.close()

        return booking is not None
    except Exception as e:
        print(f"Error validating booking: {e}")
        return False
