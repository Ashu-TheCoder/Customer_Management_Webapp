import streamlit as st
import pandas as pd
import mysql.connector
# Initialize session state keys if they don't exist

if "DB_Field" not in st.session_state:
    st.session_state["DB_Field"] = False

if "Login_Field" not in st.session_state:
    st.session_state["Login_Field"] = False

if "DB_Conn" not in st.session_state:
    st.session_state["DB_Conn"] = False

# Initialize session state for SQL connection parameters
for key in ["Host", "User", "Password"]:
    if key not in st.session_state:
        st.session_state[key] = ""  # Use empty string instead of None
# Functions


# Login function
def login_function():
    if Username == "" or Password == "":
        st.warning("Please fill in all fields.")
    elif not st.session_state.get("DB_Conn", False):  # ✅ Check `DB_Conn` safely
        st.warning("First Connect to SQL Server to Login")
    elif Username == "admin" and Password == "admin":
        st.session_state["authenticated"] = True
        st.success("Login Successful! Redirecting...")
        # st.st.rerun()  # Refresh the page to apply redirection
    else:
        st.error("Invalid Username or Password")


def db_switch():
    if serial_key == "":
        st.warning("Please fill in all fields.")
    elif not st.session_state.get("DB_Conn", False):  # ✅ Check `DB_Conn` safely
        st.warning("First Connect to SQL Server to switch to Database page")
    elif serial_key in serial_keys:
        st.success("Serial Key is valid!")
        st.session_state["S_Key_Auth"] = True
        S_key = True
    else:
        st.error("Invalid Serial Key! Please try again.")
        S_key = False

def db_connector(Host, User, Password):
    if not Host or not User or not Password:
        st.error("❌ Please fill in all fields.")
        return None, None
        
    else:
        try:
            conn = mysql.connector.connect(host=Host, user=User, password=Password)
            mydb = conn.cursor()

            # Store connection & cursor in session state
            st.session_state["mysql_conn"] = conn
            st.session_state["mysql_cursor"] = mydb

            st.success(f"✅ Connected to MySQL successfully!")
            st.session_state["DB_Conn"] = True  # Set DB_Conn to True after successful connection

            # ✅ Returning session state variables properly
            return st.session_state["mysql_conn"], st.session_state["mysql_cursor"]

        except mysql.connector.Error as e:
            st.error(f"❌ Database Connection Error: {e}")
            return None, None
        except Exception as e:
            st.error("❌ Unexpected Error")
            return None, None
        
serial_keys = [
    "A9F2-D74C-3B1E-8G5H",
    "Z1Y6-K85M-2V4X-7C3T",
    "Q7N5-P81L-4D3X-M2C9",
    "V2B4-T76G-9X3P-K81M",
    "L8D1-X74N-5Q2C-M3B9",
    "M3P7-K84X-9T2L-D65N",
    "X9L2-P83Q-5C4T-M7B6",
    "B7T1-K92X-4N3Q-M85D",
    "G4X9-M72T-1B3P-K85C",
    "P9L3-T72X-5B4Q-M81D"
]

# Initialize session state keys if they don't exist
# Redirect to another page after login
if "authenticated" in st.session_state and st.session_state["authenticated"]:
    st.switch_page("pages/Dashboard.py")  # Redirect 

elif "S_Key_Auth" in st.session_state and st.session_state["S_Key_Auth"]:
    st.switch_page("pages/Database.py")  # Redirect to database creation page


# Initialize session state for SQL connection parameters
for key in ["Host", "User", "Password"]:
    if key not in st.session_state:
        st.session_state[key] = ""  # Use empty string instead of None

st.sidebar.title("Database Connector")  # Sidebar title
# Pre-fill inputs with previous session state values
Host = st.sidebar.text_input("Enter Host Name", value=st.session_state["Host"])
User = st.sidebar.text_input("Enter User Name", value=st.session_state["User"])
Password = st.sidebar.text_input("Enter Password", type="password", value=st.session_state["Password"])

# Only update session state if non-empty values are entered
if Host: st.session_state["Host"] = Host
if User: st.session_state["User"] = User
if Password: st.session_state["Password"] = Password


st.sidebar.button('Connect to Database', key='Connect_to_DB_key', on_click=lambda:db_connector(Host=st.session_state["Host"],
        User=st.session_state["User"],
        Password=st.session_state["Password"]))  # Button to go back to database creation

# Only update session state if non-empty values are entered
if Host: st.session_state["Host"] = Host
if User: st.session_state["User"] = User
if Password: st.session_state["Password"] = Password

# Main title
col1, col2 = st.columns(2)  # First row
col1.button('Login Field', key='Login_Field_key', on_click=lambda: st.session_state.update({"DB_Field": False, "Login_Field": True}))  # Button to go back to login
col2.button('Database Creation Field', key='DB_Field_key', on_click=lambda: st.session_state.update({"Login_Field": False, "DB_Field": True}))  # Button to go back to database creation


if st.session_state['Login_Field']:
    # Main container for login form
    with st.container():
        # Create two columns for username and password input fields
        col1, col2 = st.columns(2)  # First row
        Username=col1.text_input("Username", placeholder='Please Enter Username here')  # Input field for username
        Password=col2.text_input("Password", placeholder='Please Enter Password here',type='password')  # Input field for password

    # Login button
    st.button("Login", key="Login_key", on_click=login_function)  # Button to trigger login function

elif st.session_state['DB_Field']:
    st.text("To Create Database")  # Section title for serial key authentication
    serial_key = st.text_input("Enter Serial Key", placeholder='Please Enter Serial Key here to switch database page', type="password")  # Input field for serial key
    st.button("Database Page", key="DB_Page_key", on_click=db_switch)  # Button to trigger login function

# Footer

st.write("---")
# st.markdown(f"**Developed by Ashish Bonde** <br> [LinkedIn](https://www.linkedin.com/in/ashish-bonde/)<br> [GitHub Profile](https://github.com/Ashu-TheCoder)", unsafe_allow_html=True)
st.markdown(f"""**👨‍💻 Developed by Ashish Bonde** <br> 💬 **Interested in the Customer Management WebApp?** <br> 📲 Connect with me on :<br>🔗 [LinkedIn](https://www.linkedin.com/in/ashish-bonde/) 💼  <br> 🐙 [GitHub Profile](https://github.com/Ashu-TheCoder)** 🚀  <br> [WhatsApp](https://api.whatsapp.com/send?phone=918484864084&text=Hi%20Ashish!%20I'm%20interested%20in%20learning%20more%20about%20your%20Customer%20Management%20WebApp.%20Let's%20connect!
)""", unsafe_allow_html=True)
