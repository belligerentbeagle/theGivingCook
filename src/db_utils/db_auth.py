import sqlite3
import streamlit_authenticator as stauth
import streamlit as st

# Database utility functions
def query_db(query, params=None):
    with sqlite3.connect("src/data/theGivingCook.db") as conn:
        cur = conn.cursor()
        cur.execute(query, params or ())
        return cur.fetchall()
    
# Adjust the registration functions to insert users into the database
def register_user(params):
    # Step 1: Insert into the credits table and retrieve the new credit_id, if needed
    if "credit_value" in params:
        credit_query = "INSERT INTO credits (credit_value) VALUES (:credit_value)"
        query_db(credit_query, {"credit_value": params["credit_value"]})
        
        # Retrieve the last inserted credit_id
        params["credit_id"] = query_db("SELECT last_insert_rowid()")[0][0]

    # Hash the password
    params["password"] = stauth.Hasher([params["password"]]).generate()[0]
    
    # Step 2: Determine the role (now the table name) and construct the appropriate query
    if params["role"] == "vendor":
        query = """
        INSERT INTO vendor (name, username, hp_number, address, cuisine, description, password)
        VALUES (:name, :username, :hp_number, :address, :cuisine, :description, :password)
        """
    
    elif params["role"] == "ngo":
        query = """
        INSERT INTO ngo (name, username, hp_number, address, number_of_ppl, credit_id, password)
        VALUES (:name, :username, :hp_number, :address, :number_of_ppl, :credit_id, :password)
        """
    
    elif params["role"] == "user":
        query = """
        INSERT INTO user (first_name, last_name, username, hp_number, age, sex, credit_id, password)
        VALUES (:first_name, :last_name, :username, :hp_number, :age, :sex, :credit_id, :password)
        """
    
    # Step 3: Execute the query with the params dictionary
    query_db(query, params)
