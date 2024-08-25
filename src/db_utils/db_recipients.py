# functions to interact with the database

import sqlite3

database_loc = f"../data/theGivingCook.db"


def createNewNgoUser(ngo_name, hp_number, address, number_of_ppl, credit_id):
    try:
        conn = sqlite3.connect(database_loc)
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO ngo(name, hp_number, address, number_of_ppl, credit_id)
            VALUES(?, ?, ?, ?, ?)
        """, (ngo_name, hp_number, address, number_of_ppl, credit_id))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(e)
        return False


def retrieveAllVendors():
    try:
        conn = sqlite3.connect(database_loc)
        cur = conn.cursor()
        cur.execute(
            "SELECT id, name, hp_number, address, cuisine, description FROM vendor")
        rows = cur.fetchall()
        conn.commit()
        conn.close()
        return rows
    except Exception as e:
        print(e)
        return []


def retrieveAvailableInventory(date):
    try:
        conn = sqlite3.connect(database_loc)
        cur = conn.cursor()
        cur.execute("""
            SELECT 
                inventory.id, inventory.food_name, inventory.food_type, inventory.description, 
                inventory.is_halal, inventory.is_vegetarian, inventory.expiry, 
                inventory.date_of_entry, inventory.qty, inventory.vendor_id, inventory.photo, 
                vendor.address
            FROM inventory 
            JOIN vendor ON inventory.vendor_id = vendor.id
            WHERE inventory.qty > 0 AND inventory.expiry > ?
        """, (date,))
        rows = cur.fetchall()
        conn.close()
        return rows
    except Exception as e:
        print("Failed to retrieve inventory and vendor data:", e)
        return []


def createNewVendorUser(vendor_name, hp_number, address, cuisine, description):
    try:
        conn = sqlite3.connect(database_loc)
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO vendor(name, hp_number, address, cuisine, description)
            VALUES(?, ?, ?, ?, ?)
        """, (vendor_name, hp_number, address, cuisine, description))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(e)
        return False
