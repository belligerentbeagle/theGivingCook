## functions to interact with the database

import sqlite3

database_loc = "../data/theGivingCook.db"


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