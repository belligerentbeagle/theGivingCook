import sqlite3


def createTables(cur):
    # Create Vendor table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS vendor(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            name TEXT NOT NULL,
            hp_number TEXT NOT NULL,
            address TEXT NOT NULL,
            cuisine TEXT NOT NULL,
            description TEXT,
            password TEXT NOT NULL
        )
    """)

    # Create User table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS user(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            hp_number TEXT NOT NULL,
            age INTEGER NOT NULL,
            sex TEXT NOT NULL,
            credit_id INTEGER,
            password TEXT NOT NULL,
            FOREIGN KEY (credit_id) REFERENCES credits(id)
        )
    """)

    # Create NGO table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS ngo(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            name TEXT NOT NULL,
            hp_number TEXT NOT NULL,
            address TEXT NOT NULL,
            number_of_ppl INTEGER NOT NULL,
            credit_id INTEGER,
            password TEXT NOT NULL,
            FOREIGN KEY (credit_id) REFERENCES credits(id)
        )
    """)

    # Create Credits table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS credits(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            credit_value REAL NOT NULL
        )
    """)

    # Create Price Inventory table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS price_inventory(
            food_id INTEGER NOT NULL,
            price REAL NOT NULL,
            FOREIGN KEY (food_id) REFERENCES inventory(id)
        )
    """)

    # Create Inventory table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS inventory(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            food_name TEXT NOT NULL,
            food_type TEXT NOT NULL,
            description TEXT NOT NULL,
            is_halal BOOLEAN NOT NULL,
            is_vegetarian BOOLEAN NOT NULL,
            expiry DATE NOT NULL,
            date_of_entry DATE NOT NULL,
            total_qty INTEGER NOT NULL,
            qty_left_after_booking INTEGER NOT NULL,
            qty_left_after_scanning INTEGER NOT NULL, 
            for_ngo BOOLEAN NOT NULL,
            vendor_id INTEGER NOT NULL,
            photo BLOB NOT NULL,  
            qr_code BLOB,
            FOREIGN KEY (vendor_id) REFERENCES vendor(id)
        )
    """)

    # UserPref table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS user_pref(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            restrictions TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )""")

    cur.execute("""
        CREATE TABLE IF NOT EXISTS vendor_reports(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vendor_id INTEGER NOT NULL, 
            description TEXT NOT NULL,
            time TIMESTAMP NOT NULL,
            FOREIGN KEY (vendor_id) REFERENCES vendor(id)
        )""")

    cur.execute("""
            CREATE TABLE IF NOT EXISTS orders(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                qty INTEGER NOT NULL,
                credits_spent REAL NOT NULL,
                is_complete BOOLEAN NOT NULL,
                FOREIGN KEY (item_id) REFERENCES inventory(id),
                FOREIGN KEY (user_id) REFERENCES user(id)
            )
        """)


def insertDummyData(cur):
    # Insert dummy data into vendor table
    cur.execute("""
        INSERT INTO vendor (username, name, hp_number, address, cuisine, description, password) VALUES
        ('mcdonald', 'McDonalds', '+65 91234567', '5 Tampines Street 32, #01-01 Tampines Mart, Singapore 529284', 'Italian', 'A cozy place with homemade pasta', 'password'),
        ('kfc', 'KFC', '+65 98765432', '4 Tampines Central 5, #01-47 Tampines Mall, Singapore 529510', 'American', 'Gourmet burgers and fries', 'password'),
        ('fourfingers', 'Four Fingers', '+65 82345678', '277 Orchard Road, Gateway, #01-04/05 Orchard, 238858', 'Japanese', 'Fresh sushi and sashimi', 'password'),
        ('subway', 'Subway', '+65 91258765', '5 Tampines Street 32, #01-21 Tampines Mart, Singapore 529284', 'Chinese', 'Traditional dim sum and tea', 'password'),
        ('tajmahal', 'Taj Mahal', '+65 93458765', '820 Tampines Street 81, Singapore 520820', 'Indian', 'Authentic North Indian cuisine', 'password'),
        ('lafiesta', 'La Fiesta', '+65 90254875', '3 Kaki Bukit Rd 2, #01-05B Eunos Warehouse, Singapore 417837', 'Mexican', 'Spicy tacos and fresh guacamole', 'password'),
        ('patisvalerie', 'Patisserie Valerie', '+65 94752865', '61 Ubi Avenue 2, #01-13 Automobile Megamart, 408898', 'French', 'Elegant pastries and desserts', 'password'),
        ('cairogrill', 'Cairo Grill', '+65 86578439', '10 Kaki Bukit Ave 4, #03-60, Singapore 415874', 'Middle Eastern', 'Kebabs and meze platter', 'password'),
        ('seoulfood', 'Seoul Food', '+65 96547832', '739A Bedok Reservoir Rd, #01-01, Singapore 471739', 'Korean', 'BBQ and kimchi specials', 'password'),
        ('bangkokbites', 'Bangkok Bites', '+65 81345672', '901 Bedok Reservoir Rd, Singapore 479266', 'Thai', 'Tom Yum Goong and Pad Thai', 'password')
    """)

    # Insert dummy data into user table with credit_id
    cur.execute("""
        INSERT INTO user (username, first_name, last_name, hp_number, age, sex, credit_id, password) VALUES
            ('jsmith@gmail.com', 'John', 'Doe', '+65 91234567', 30, 'M', 4, 'password'),
            ('janesmith@gmail.com', 'Jane', 'Smith', '+65 92345678', 25, 'F', 5, 'password'),
            ('atan@gmail.com', 'Alice', 'Tan', '+65 93456789', 28, 'F', 6, 'password')
    """)

    # Insert dummy data into ngo table with credit_id
    cur.execute("""
        INSERT INTO ngo (username, name, hp_number, address, number_of_ppl, credit_id, password) VALUES
            ('feedthehungry', 'Feed the Hungry', '+65 92345678', '789 Oak St', 100, 1, 'password'),
            ('helpinghands', 'Helping Hands', '+65 93456789', '321 Pine St', 50, 2, 'password'),
            ('caringhearts', 'Caring Hearts', '+65 94567890', '567 Cedar Ave', 200, 3, 'password')
    """)

    # Insert dummy data into credits table
    cur.execute("""
        INSERT INTO credits (credit_value) VALUES
            (20000),
            (10000),
            (40000),
            (200),
            (200),
            (200)
    """)

    # Insert dummy data into price_inventory table
    cur.execute("""
        INSERT INTO price_inventory (food_id, price) VALUES
            (1, 3.5),
            (2, 1),
            (3, 2),
            (4, 3),
            (5, 3)
    """)

    # Read actual image files in binary mode
    with open("../data/assets/pasta.jpeg", "rb") as file:
        pasta = file.read()

    with open("../data/assets/ketchup.png", "rb") as file:
        tomatosauce = file.read()

    with open("../data/assets/milo.jpeg", "rb") as file:
        milo = file.read()

    with open("../data/assets/xiumai.png", "rb") as file:
        xiumai = file.read()

    with open("../data/assets/naanbread.png", "rb") as file:
        naan = file.read()

    with open("../data/assets/qrcode.png", "rb") as file:
        qr = file.read()

    # Insert dummy data into inventory table with real image data
    cur.execute("""
    INSERT INTO inventory (food_name, food_type, description, is_halal, is_vegetarian, expiry, date_of_entry, total_qty, 
        qty_left_after_booking, qty_left_after_scanning, for_ngo, vendor_id, photo, qr_code) VALUES
            (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, ('Pasta', 'cooked', 'yummy', 1, 0, '2024-12-01', '2024-08-20', 1, 1, 1, 1, 1, pasta, qr))

    cur.execute("""
        INSERT INTO inventory (food_name, food_type, description, is_halal, is_vegetarian, expiry, date_of_entry, total_qty, 
        qty_left_after_booking, qty_left_after_scanning, for_ngo, vendor_id, photo, qr_code) VALUES
            (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, ('Tomato Sauce', 'packaged', 'Delicious tomato sauce', 1, 0, '2025-01-15', '2024-08-21', 3, 3, 3, 0, 1, tomatosauce, qr))

    cur.execute("""
        INSERT INTO inventory (food_name, food_type, description, is_halal, is_vegetarian, expiry, date_of_entry, total_qty, 
        qty_left_after_booking, qty_left_after_scanning, for_ngo, vendor_id, photo, qr_code) VALUES
            (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, ('Milo Packet', 'packaged', 'good for health', 1, 0, '2024-09-10', '2024-08-22', 2, 2, 2, 0, 2, milo, qr))

    cur.execute("""
        INSERT INTO inventory (food_name, food_type, description, is_halal, is_vegetarian, expiry, date_of_entry, total_qty, 
        qty_left_after_booking, qty_left_after_scanning, for_ngo, vendor_id, photo, qr_code) VALUES
            (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, ('Xiu Mai', 'cooked', 'just xiu mai', 0, 0, '2024-10-05', '2024-08-23', 2, 2, 2, 1, 3, xiumai, qr))

    cur.execute("""
        INSERT INTO inventory (food_name, food_type, description, is_halal, is_vegetarian, expiry, date_of_entry, total_qty, 
        qty_left_after_booking, qty_left_after_scanning, for_ngo, vendor_id, photo, qr_code) VALUES
            (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, ('Naan Bread', 'cooked', 'Soft naan bread', 1, 1, '2024-08-30', '2024-08-24', 4, 4, 4, 1, 4, naan, qr))

    # Insert dummy data into user_pref table
    cur.execute("""
        INSERT INTO user_pref (user_id, restrictions) VALUES
            (1, 'No shellfish'),
            (2, 'Halal'),
            (2, 'Vegetarian'),
            (3, 'Halal'),
            (3, 'Vegetarian'),
            (3, 'No dairy'),
            (3, 'Gluten-free'),
            (3, 'Vegan'),
            (3, 'No nuts'),
            (3, 'Kosher')
    """)

    # Insert dummy data into vendor_reports table
    cur.execute("""
        INSERT INTO vendor_reports (vendor_id, description, time) VALUES
            (1, 'got diarrhoea', '2024-08-24 14:30:00'),
            (2, 'food is not good', '2024-08-23 13:20:00'),
            (3, 'Needs improvement in hygiene', '2024-08-22 12:10:00'),
            (3, 'got stomachache', '2024-08-21 11:00:00')
    """)

    cur.execute("""
        INSERT INTO orders (item_id, user_id, qty, credits_spent, is_complete) VALUES
            (1, 4, 1, 3.5, 0),
            (2, 5, 2, 2, 0),
            (3, 1, 1, 2, 0)
    """)


def setupDB():
    con = sqlite3.connect("../data/theGivingCook.db")
    cur = con.cursor()

    # Drop tables if they exist
    cur.execute("DROP TABLE IF EXISTS vendor")
    cur.execute("DROP TABLE IF EXISTS ngo")
    cur.execute("DROP TABLE IF EXISTS user")
    cur.execute("DROP TABLE IF EXISTS user_pref")
    cur.execute("DROP TABLE IF EXISTS vendor_reports")
    cur.execute("DROP TABLE IF EXISTS credits")
    cur.execute("DROP TABLE IF EXISTS price_inventory")
    cur.execute("DROP TABLE IF EXISTS inventory")
    cur.execute("DROP TABLE IF EXISTS orders")

    # Create tables
    createTables(cur)

    # Insert dummy data
    insertDummyData(cur)

    con.commit()
    con.close()


if __name__ == "__main__":
    setupDB()
