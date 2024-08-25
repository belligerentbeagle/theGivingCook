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


def updateNgo(ngo_id, name, hp_number, address, number_of_ppl, database_loc="theGivingCook.db"):
    try:
        conn = sqlite3.connect(database_loc)
        cur = conn.cursor()
        cur.execute("""
            UPDATE ngo
            SET name = ?, hp_number = ?, address = ?, number_of_ppl = ?
            WHERE id = ?
        """, (name, hp_number, address, number_of_ppl, ngo_id))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return False


def updateUser(user_id, first_name, last_name, hp_number, age, sex, database_loc="theGivingCook.db"):
    try:
        conn = sqlite3.connect(database_loc)
        cur = conn.cursor()
        cur.execute("""
            UPDATE user
            SET first_name = ?, last_name = ?, hp_number = ?, age = ?, sex = ?
            WHERE id = ?
        """, (first_name, last_name, hp_number, age, sex, user_id))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
