import streamlit as st
import random
import mysql.connector
import datetime

# Check if the serial key is valid and allow access
if "S_Key_Auth" in st.session_state and st.session_state["S_Key_Auth"]: # Session state for serial key initialized and validated in Login.py
    st.title("Welcome to Database Creator!")
else:
    st.warning("Unauthorized access! Please login first.")
    st.switch_page("Login.py")  # Redirect back to login when unauthorized

# Database and table names
DB_Name = "Customer_MS" # Specifing the database name
Table1='Customers_registration' # Specifing the table name



def create_database():
    try:
    
        conn = st.session_state["mysql_conn"]
        mydb = st.session_state["mysql_cursor"]

        # Create database if it doesn't exist
        mydb.execute(f"CREATE DATABASE IF NOT EXISTS {DB_Name};")
        mydb.execute(f"USE {DB_Name};")
    # Ensure your MySQL cursor object (`mydb`) is created first
        mydb.execute('''CREATE TABLE IF NOT EXISTS Customers_registration (
                cm_id  VARCHAR(50) PRIMARY KEY,
                fname VARCHAR(100) NOT NULL,
                lname VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                phone VARCHAR(15) DEFAULT 'Unknown',
                address TEXT,
                timestamp VARCHAR(100),
                INDEX idx_email (email));''')

        conn.commit()
        st.success(f"✅ Database '{DB_Name}' created successfully!")
    except mysql.connector.Error as e: 
        st.error(f"❌ Database Creation Error: {e}")


def delete_database():
    try:
        conn = st.session_state["mysql_conn"]
        mydb = st.session_state["mysql_cursor"]

        # Delete database if it exists
        mydb.execute(f"DROP DATABASE IF EXISTS {DB_Name};")
        conn.commit()
        st.success(f"✅ Database '{DB_Name}' deleted successfully!")
    except mysql.connector.Error as e:
        st.error(f"❌ Database Deletion Error: {e}")


def clear_table():
    try:
        conn = st.session_state["mysql_conn"]
        mydb = st.session_state["mysql_cursor"]

        # Clear table if it exists
        mydb.execute(f"USE {DB_Name};")
        mydb.execute(f"DELETE FROM {Table1};")
        conn.commit()
        st.success(f"✅ Table in '{DB_Name}' cleared successfully!")
    except mysql.connector.Error as e:
        st.error(f"❌ Table Clearing Error: {e}")




 
    
#  Buttons and layout
st.sidebar.button('Back to Login page', key='Back_to_Login_key', on_click=lambda: st.session_state.update({"S_Key_Auth": False, "authenticated": False}))  # Button to go back to login
col1, col2, col3 = st.columns(3)  # First row
create_db=col1.button('Create Database', key='create_db_key',on_click=create_database)  # Button to create database
delete_db=col2.button('Delete Database', key='delete_db_key',on_click=delete_database)  # Button to delete database
clear_table=col3.button('Clear the Table', key='clear_table_key',on_click=clear_table)  # Button to update database


# Footer
st.write("---")
st.markdown(f"""**👨‍💻 Developed by Ashish Bonde** <br> 💬 **Interested in the Customer Management WebApp?** <br> 📲 Connect with me on :<br>[LinkedIn](https://www.linkedin.com/in/ashish-bonde/)<br>[GitHub Profile](https://github.com/Ashu-TheCoder)<br>[WhatsApp](https://api.whatsapp.com/send?phone=918484864084&text=Hi%20Ashish!%20I'm%20interested%20in%20learning%20more%20about%20your%20Customer%20Management%20WebApp.%20Let's%20connect!
)""", unsafe_allow_html=True)
