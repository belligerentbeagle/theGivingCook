import sqlite3
import streamlit_authenticator as stauth

def insert_dummy_users():
    # Connect to your database
    con = sqlite3.connect("src/data/theGivingCook.db")
    cur = con.cursor()

    # Hash the passwords
    hashed_passwords = stauth.Hasher(['password1', 'password2', 'password3']).generate()

    # Insert dummy data into the user table, using the hashed passwords
    cur.execute("""
        INSERT INTO user (username, first_name, last_name, hp_number, age, sex, credit_id, password)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, ('jsmith', 'John', 'Smith', '+65 91234567', 30, 'M', 1, hashed_passwords[0]))

    cur.execute("""
        INSERT INTO user (username, first_name, last_name, hp_number, age, sex, credit_id, password)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, ('rbriggs', 'Rebecca', 'Briggs', '+65 92345678', 25, 'F', 2, hashed_passwords[1]))

    cur.execute("""
        INSERT INTO user (username, first_name, last_name, hp_number, age, sex, credit_id, password)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, ('melsby', 'Mel', 'Sby', '+65 93456789', 28, 'F', 3, hashed_passwords[2]))

    con.commit()
    con.close()

def insert_dummy_donors():
    # Connect to your database
    con = sqlite3.connect("src/data/theGivingCook.db")
    cur = con.cursor()

    # Hash the passwords
    hashed_passwords = stauth.Hasher(['donorpass1', 'donorpass2', 'donorpass3']).generate()

    # Insert dummy data into the vendor (donor) table
    cur.execute("""
        INSERT INTO vendor (username, name, hp_number, address, cuisine, description, password)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, ('mcdonald', 'McDonalds', '+65 91234567', '5 Tampines Street 32, #01-01 Tampines Mart, Singapore 529284', 'Fast Food', 'Burgers and fries', hashed_passwords[0]))

    cur.execute("""
        INSERT INTO vendor (username, name, hp_number, address, cuisine, description, password)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, ('kfc', 'KFC', '+65 98765432', '4 Tampines Central 5, #01-47 Tampines Mall, Singapore 529510', 'Fast Food', 'Fried chicken and sides', hashed_passwords[1]))

    cur.execute("""
        INSERT INTO vendor (username, name, hp_number, address, cuisine, description, password)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, ('subway', 'Subway', '+65 91258765', '5 Tampines Street 32, #01-21 Tampines Mart, Singapore 529284', 'Sandwiches', 'Healthy sandwiches', hashed_passwords[2]))

    con.commit()
    con.close()

if __name__ == "__main__":
    insert_dummy_users()
    insert_dummy_donors()