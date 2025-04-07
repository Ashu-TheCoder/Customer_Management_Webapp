import streamlit as st
import pandas as pd
import mysql.connector
import time
import datetime
import sqlalchemy


st.set_page_config(page_title="Customer Management System", page_icon="📊", layout="wide") # Page title, icon and layout
st.markdown("<h1 style='text-align: center; color: blue; font-family: Arial;'>Customer Managent System</h1>", 
    unsafe_allow_html=True) # h1: HTML header tag for largest title style | text-align: centers the title | color: Intended color | font-family: Intended Color

DB_Name = "Customer_MS"
Table1='Customers_registration'
current_timestamp = datetime.datetime.now()



# Function
def logout():
    if st.session_state.authenticated==True:
        st.session_state["authenticated"] = False
        st.session_state.data = pd.DataFrame()  # Clear data on logout
        st.success("Logged out successfully!")


def update_df():
    conn = st.session_state["mysql_conn"]
    mydb = st.session_state["mysql_cursor"]
    mydb.execute(f'USE {DB_Name};')
    df=pd.read_sql(f'SELECT * FROM {Table1};', conn)
    return df


import streamlit as st

def Search_Customer(s_value, s_options):
    try:
        conn = st.session_state["mysql_conn"]
        mydb = st.session_state["mysql_cursor"]

        if s_value=='':
            time.sleep(1.5)  # ✅ Add a delay before showing error message
            st.error('❌ Error | Enter a value to search')

        
        # Execute search query with wildcard for partial matching
        # conn is required because pd.read_sql() uses direct database connection.
        mydb.execute(f'USE {DB_Name};')
        dfs = pd.read_sql(f"SELECT * FROM {Table1} WHERE {s_options} = %s", conn, params=(s_value,))
        return dfs

    except mysql.connector.Error as e:
        st.error(f"❌ Error searching customer: {e}")


def Add_Customer(cm_id,fname, lname, email, phone, address,current_timestamp):
    if not fname or not lname or not email or not phone or not address:
        st.error("❌ Please fill in all fields.")
        return None
    elif not cm_id.startswith('CM'):  # ✅ Check if ID starts with 'CM'
        st.error("❌ Invalid ID format! ID should start with CM (e.g., CM0001)")
    
    else:
        try:
            conn = st.session_state["mysql_conn"]
            mydb = st.session_state["mysql_cursor"]

            # SQL Query to insert data
            mydb.execute(f'USE {DB_Name};')
            mydb.execute(f'insert into {Table1} (cm_id, fname, lname, email, phone, address,timestamp) VALUES (%s,%s,%s,%s,%s,%s,%s);',(cm_id,fname,lname,email,phone,address,current_timestamp))
            conn.commit()
            update_df()
            
            
            st.success(f"Employee added in {Table1} successfully!")
        except mysql.connector.Error as e:
            st.error(f"❌ Customer addition Error: {e}")





# Update function
def Update_Customer(cm_id,fname, lname, email, phone, address):
    if not fname or not lname or not email or not phone or not address:
        st.error("❌ Please fill in all fields.")
        return None
    else:
        try:
            conn = st.session_state["mysql_conn"]
            mydb = st.session_state["mysql_cursor"]

            # Delete database if it exists
            mydb.execute(f'USE {DB_Name};')
            mydb.execute(f'UPDATE {Table1} SET fname = %s, lname = %s, email = %s, phone = %s, address = %s WHERE cm_id = %s;', (fname, lname, email, phone, address, cm_id))
            conn.commit()
            st.success(f"Employee Udated in {Table1} successfully!")
            update_df()
            
            
            st.success(f"Employee Udated in {Table1} successfully!")
        except mysql.connector.Error as e:
            st.error(f"❌ Customer updation Error: {e}")


def Delete_Customer(cm_id):
    conn = st.session_state["mysql_conn"]
    mydb = st.session_state["mysql_cursor"]
    mydb.execute(f'USE {DB_Name};')
    mydb.execute(f'DELETE FROM {Table1} WHERE cm_id=%s',(cm_id,)) # delete the data
    conn.commit()

def Delete_Multiple(s_value, s_options):
    try:
        conn = st.session_state["mysql_conn"]
        mydb = st.session_state["mysql_cursor"]

        if s_value=='':
            st.error('❌ Error | Enter a value to search')

        
        # Execute search query with wildcard for partial matching
        mydb.execute(f'USE {DB_Name};')
        mydb.execute(f'DELETE FROM {Table1} WHERE {s_options} = %s',(s_value,))
        return None

    except mysql.connector.Error as e:
        st.error(f"❌ Error searching customer: {e}")

# Initial data
col1, col2, col3, col4, col5, col6 = st.columns(6)  # First row
col6.button("Logout", key="Logout",on_click=logout)  # Input field for password

# Restrict access to logged-in users
if "authenticated" in st.session_state and st.session_state["authenticated"]:
    st.title("Dashboard")

else:
    st.warning("Unauthorized access! Please login first.")
    st.switch_page("Login.py")  # Redirect back to login

# 

# Display the table
st.title("Interactive Table")
st.info("The search widget can be used for both operations: Searching records and deleting multiple entries at once. Hence Use carefully!") # Section title for searched data
col1,col2=st.columns(2)
s_value=col1.text_input('Search by Value',placeholder='Enter the value here') # Input field for search
s_options=col2.selectbox('Search by Column',options=['cm_id','fname','lname','email','phone','address']) # Input field for search
col1,col2,col3=st.columns(3)
col3.button('Search Customer',key='search',on_click=lambda:Search_Customer(s_value,s_options)) # Input field for search



# Create a form labeled "Add Row" to group inputs together
with st.form("Add Row"):
    cm_id=st.sidebar.text_input("ID", placeholder="Enter ID here") # Input field for ID
    fname=st.sidebar.text_input("F_Name", placeholder="Enter First Name") # Input field for Name
    lname=st.sidebar.text_input("L_Name", placeholder="Enter Last Name here") # Input field for Name
    email=st.sidebar.text_input("Email", placeholder="Enter Email ID here") # Input field for Email
    phone=st.sidebar.text_input('Phone',placeholder='Enter Phone Number here') #
    address=st.sidebar.text_input('Address',placeholder='Enter the Address here')

dfs = Search_Customer(s_value, s_options) # Call the function to search customer
if dfs.empty and s_value != '':
    pass
else:
    st.text('Searched Data') # Section title for searched data
    st.dataframe(dfs, use_container_width=True) # Display the table

st.text("Customer Registration") # Section title for customer registration
st.dataframe(update_df(), use_container_width=True) # Display the table


# Buttons for actions with Grid layout
col7, col8,col9,col10 =st.columns(4) # Second row

col7.button('Add New Customer', key='add customer',on_click=lambda:Add_Customer(cm_id,fname, lname, email, phone, address,current_timestamp)) # 
col8.button('Update Customer', key='update customer',on_click=lambda:Update_Customer(cm_id,fname, lname, email, phone, address)) # Input field for password
col9.button('Delete Customer', key='delete customer',on_click=lambda:Delete_Customer(cm_id,)) # Input field for password
col10.button('Delete Multiple Customer',key='Delete Multiple',on_click=lambda:Delete_Multiple(s_value, s_options)) # Input field for search











st.write("---")
st.markdown(f"**Developed by Ashish Bonde** <br> [LinkedIn](https://www.linkedin.com/in/ashish-bonde/)<br> [GitHub Profile](https://github.com/Ashu-TheCoder)", unsafe_allow_html=True)
