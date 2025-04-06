import mysql.connector

# Establish connection to MySQL
conn = mysql.connector.connect(host='localhost',user='root',password='My@SQL123')

# Create a cursor object to execute queries
cursor = conn.cursor()

# Create a new database
cursor.execute("CREATE DATABASE IF NOT EXISTS my_database")

# Connect to the newly created database
conn.database = "my_database"

# Create a sample table inside the database
cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL,
        age INT
    )
""")

print("✅ Database and table created successfully!")

conn.commit()  # Commit the changes





# Copy pasted Database.py code

import streamlit as st
import random
import mysql.connector
import datetime

if "S_Key_Auth" in st.session_state and st.session_state["S_Key_Auth"]:
    st.title("Welcome to Database Creator!")
else:
    st.warning("Unauthorized access! Please login first.")
    st.switch_page("Login.py")  # Redirect back to login
DB_Name = "Customer_MS"
# Initialize session state correctly
for key in ["Host", "User", "Password"]:
    if key not in st.session_state:
        st.session_state[key] = ""  # Use empty string instead of None

# st.header()  

# Create columns for input fields
col1, col2, col3 = st.columns(3)

# Pre-fill inputs with previous session state values
Host = col1.text_input("Enter Host Name", value=st.session_state["Host"])
User = col2.text_input("Enter User Name", value=st.session_state["User"])
Password = col3.text_input("Enter Password", type="password", value=st.session_state["Password"])

# Only update session state if non-empty values are entered
if Host: st.session_state["Host"] = Host
if User: st.session_state["User"] = User
if Password: st.session_state["Password"] = Password





def db_connector(Host, User, Password, DB_Name):
    if not Host or not User or not Password:
        st.error("❌ Please fill in all fields.")
        return None, None
        
    else:
        try:
            conn = mysql.connector.connect(host=Host, user=User, password=Password, database=DB_Name)
            mydb = conn.cursor()

            # Store connection & cursor in session state
            st.session_state["mysql_conn"] = conn
            st.session_state["mysql_cursor"] = mydb

            st.success(f"✅ Connected to '{DB_Name}' successfully!")

            # ✅ Returning session state variables properly
            return st.session_state["mysql_conn"], st.session_state["mysql_cursor"]

        except mysql.connector.Error as e:
            st.error(f"❌ Database Connection Error: {e}")
            return None, None
        except Exception as e:
            st.error("❌ Unexpected Error")
            return None, None




st.sidebar.button('Connect to Database', key='Connect_to_DB_key', on_click=lambda:db_connector(Host=st.session_state["Host"],
        User=st.session_state["User"],
        Password=st.session_state["Password"],
        DB_Name=DB_Name))  # Button to go back to database creation






 
    

st.sidebar.button('Back to Login page', key='Back_to_Login_key', on_click=lambda: st.session_state.update({"S_Key_Auth": False, "authenticated": False}))  # Button to go back to login
col1, col2, col3 = st.columns(3)  # First row
create_db=col1.button('Create Database', key='create_db_key')  # Button to create database
delete_db=col2.button('Delete Database', key='delete_db_key')  # Button to delete database
clear_table=col3.button('Clear the Table', key='clear_table_key')  # Button to update database



