import sqlite3

def createTables(cur):
    # Create Restaurant table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Restaurant(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT NOT NULL,
            HP_number TEXT NOT NULL,
            Address TEXT NOT NULL,
            Cuisine TEXT NOT NULL,
            Description TEXT
        )
    """)

    # Create NGO table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS NGO(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT NOT NULL,
            HP_number TEXT NOT NULL,
            Address TEXT NOT NULL,
            Number_of_ppl INTEGER NOT NULL
        )
    """)

    # Create User table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS User(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            FirstName TEXT NOT NULL,
            LastName TEXT NOT NULL,
            HP_number TEXT NOT NULL,
            Age INTEGER NOT NULL,
            Sex TEXT NOT NULL
        )
    """)

def insertDummyData(cur):
    # Insert dummy data into Restaurant table
    cur.execute("""
        INSERT INTO Restaurant (Name, HP_number, Address, Cuisine, Description) VALUES
            ('The Fancy Fork', '123456789', '123 Main St', 'Italian', 'A cozy place with homemade pasta'),
            ('Burger Bliss', '987654321', '456 Elm St', 'American', 'Gourmet burgers and fries')
    """)

    # Insert dummy data into NGO table
    cur.execute("""
        INSERT INTO NGO (Name, HP_number, Address, Number_of_ppl) VALUES
            ('Feed the Hungry', '234567890', '789 Oak St', 100),
            ('Helping Hands', '345678901', '321 Pine St', 50)
    """)

    # Insert dummy data into User table
    cur.execute("""
        INSERT INTO User (FirstName, LastName, HP_number, Age, Sex) VALUES
            ('John', 'Doe', '456789012', 30, 'M'),
            ('Jane', 'Smith', '567890123', 25, 'F')
    """)

def setupDB():
    con = sqlite3.connect("theGivingCook.db")
    cur = con.cursor()

    # Drop tables if they exist
    cur.execute("DROP TABLE IF EXISTS Restaurant")
    cur.execute("DROP TABLE IF EXISTS NGO")
    cur.execute("DROP TABLE IF EXISTS User")

    # Create tables
    createTables(cur)

    # Insert dummy data
    insertDummyData(cur)

    con.commit()
    con.close()

setupDB()