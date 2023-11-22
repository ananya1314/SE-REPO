from hashlib import sha256
import streamlit as st
import mysql.connector
import datetime

from mysql.connector import Error

#Define the custom CSS style for the gradient background
gradient_style = f"""
    <style>
    .stApp {{
        background: linear-gradient(to bottom, #E0F4FF, #87C4FF);
        color: #000080; /* Dark blue text color (#000080 is dark blue in hexadecimal) */
    }}
    </style>
"""

# Apply the custom CSS style using st.markdown
st.markdown(gradient_style, unsafe_allow_html=True)


# Establishes a connection to the database
def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='biryani1403',
            database='ApartmentManagement'
        )
        st.success("Connection to MySQL DB successful")
    except Error as e:
        st.error(f"The error '{e}' occurred")
        return None
    return connection

# Creates a new user in the database
def create_user(connection, username, password):
    try:
        cursor = connection.cursor()
        hashed_password = sha256(password.encode()).hexdigest()
        cursor.execute(
            "INSERT INTO Users (Username, PasswordHash) VALUES (%s, %s)",
            (username, hashed_password),
        )
        connection.commit()
        cursor.close()
        return True
    except Error as e:
        st.error(f"Failed to create user: {e}")
        return False

# Verifies the user's login credentials
def verify_login(connection, username, password):
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT PasswordHash FROM Users WHERE Username = %s", (username,))
        user_record = cursor.fetchone()
        cursor.close()
        if user_record and sha256(password.encode()).hexdigest() == user_record['PasswordHash']:
            return True
        else:
            return False
    except Error as e:
        st.error(f"Database error: {e}")
        return False

# UI for the login form
def login_ui():
    st.subheader("Login")
    with st.form("Login Form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button("Login")

        if submit_button:
            connection = create_connection()
            if connection and verify_login(connection, username, password):
                st.session_state['logged_in'] = True
                st.success("Logged in successfully!")
            else:
                st.error("Invalid username or password")
            connection.close()

# UI for the sign-up form
def signup_ui():
    st.subheader("Sign Up")
    with st.form("Sign Up Form"):
        username = st.text_input("Choose a Username")
        password = st.text_input("Choose a Password", type="password")
        password_confirm = st.text_input("Confirm Password", type="password")
        submit_button = st.form_submit_button("Create Account")

        if submit_button:
            if password == password_confirm:
                connection = create_connection()
                if connection and create_user(connection, username, password):
                    st.success("Account created successfully!")
                connection.close()
            else:
                st.error("Passwords do not match")

# Fetches all owner records from the database
def fetch_owners(connection):
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Owners")
        owner_records = cursor.fetchall()
        cursor.close()
        return owner_records
    except Error as e:
        st.error(f"Failed to fetch owners: {e}")
        return []

# Displays owner records in the Streamlit UI
def display_owners_ui(owners):
    st.subheader("Owners")
    for owner in owners:
        apartment_id = owner.get('ApartmentID', 'N/A')
        st.text(f"ID: {owner['OwnerID']}, Name: {owner['FirstName']} {owner['LastName']}, Contact: {owner['ContactInfo']}, Apartment ID: {apartment_id}")

# Add CRUD operations for Owners

# Adds a new owner to the database
def add_owner(connection, first_name, last_name, contact_info, apartment_number):
    try:
        cursor = connection.cursor()
        # Fetch ApartmentID based on ApartmentNumber
        cursor.execute("SELECT ApartmentID FROM Apartments WHERE ApartmentNumber = %s", (apartment_number,))
        result = cursor.fetchone()
        apartment_id = result['ApartmentID'] if result else None
        # Insert owner with ApartmentID
        cursor.execute(
            "INSERT INTO Owners (FirstName, LastName, ContactInfo, ApartmentID) VALUES (%s, %s, %s, %s)",
            (first_name, last_name, contact_info, apartment_id),
        )
        connection.commit()
        cursor.close()
        st.success("Owner added successfully!")
    except Error as e:
        st.error(f"Failed to add owner: {e}")

def update_owner(connection, owner_id, first_name, last_name, contact_info):
    try:
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE Owners SET FirstName = %s, LastName = %s, ContactInfo = %s WHERE OwnerID = %s",
            (first_name, last_name, contact_info, owner_id),
        )
        connection.commit()
        cursor.close()
        st.success("Owner updated successfully!")
    except Error as e:
        st.error(f"Failed to update owner: {e}")

# Deletes an owner from the database
def delete_owner(connection, owner_id):
    try:
        cursor = connection.cursor()
        cursor.execute(
            "DELETE FROM Owners WHERE OwnerID = %s", (owner_id,)
        )
        connection.commit()
        cursor.close()
        st.success("Owner deleted successfully!")
    except Error as e:
        st.error(f"Failed to delete owner: {e}")

# Fetches all tenant records from the database
def fetch_tenants(connection):
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Tenants")
        tenant_records = cursor.fetchall()
        cursor.close()
        return tenant_records
    except Error as e:
        st.error(f"Failed to fetch tenants: {e}")

# Display tenants records in the Streamlit UI
def display_tenants_ui(tenants):
    st.subheader("Tenants")
    for tenant in tenants:
        apartment_id = tenant.get('ApartmentID', 'N/A')
        st.text(f"ID: {tenant['TenantID']}, Name: {tenant['FirstName']} {tenant['LastName']}, Moving Date: {tenant['MovingDate']}, Contact: {tenant['ContactInfo']},Apartment ID: {apartment_id}")

# Add CRUD operations for Tenants

# Adds a new tenant to the database
def add_tenant(connection, first_name, last_name, moving_date, contact_info, apartment_number):
    try:
        cursor = connection.cursor()
        # Fetch ApartmentID based on ApartmentNumber
        cursor.execute("SELECT ApartmentID FROM Apartments WHERE ApartmentNumber = %s", (apartment_number,))
        result = cursor.fetchone()
        apartment_id = result['ApartmentID'] if result else None
        # Insert tenant with ApartmentID
        cursor.execute(
            "INSERT INTO Tenants (FirstName, LastName, MovingDate, ContactInfo, ApartmentID) VALUES (%s, %s, %s, %s, %s)",
            (first_name, last_name, moving_date, contact_info, apartment_id),
        )
        connection.commit()
        cursor.close()
        st.success("Tenant added successfully!")
    except Error as e:
        st.error(f"Failed to add tenant: {e}")

# Updates a tenant's details in the database
def update_tenant(connection, tenant_id, first_name, last_name, moving_date, contact_info):
    try:
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE Tenants SET FirstName = %s, LastName = %s, MovingDate = %s, ContactInfo = %s WHERE TenantID = %s",
            (first_name, last_name, moving_date, contact_info, tenant_id),
        )
        connection.commit()
        cursor.close()
        st.success("Tenant updated successfully!")
    except Error as e:
        st.error(f"Failed to update tenant: {e}")

# Deletes a tenant from the database
def delete_tenant(connection, tenant_id):
    try:
        cursor = connection.cursor()
        cursor.execute(
            "DELETE FROM Tenants WHERE TenantID = %s", (tenant_id,)
        )
        connection.commit()
        cursor.close()
        st.success("Tenant deleted successfully!")
    except Error as e:
        st.error(f"Failed to delete tenant: {e}")

# Fetches all apartment records from the database
def fetch_apartments(connection):
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Apartments")
        apartment_records = cursor.fetchall()
        cursor.close()
        return apartment_records
    except Error as e:
        st.error(f"Failed to fetch apartments: {e}")
        return[]

# Displays apartment records in the Streamlit UI
def display_apartments_ui(apartments):
    st.subheader("Apartments")
    for apartment in apartments:
        apartment_number = apartment.get('ApartmentNumber', 'N/A')
        apartment_id = apartment.get('ApartmentID', 'N/A')
        owner_id = apartment.get('OwnerID', 'N/A')
        tenant_id = apartment.get('TenantID', 'N/A')
        st.text(f"Apartment ID: {apartment_id}, Apartment Number: {apartment_number}, Owner ID: {owner_id}, Tenant ID: {tenant_id}")

# Add CRUD operations for Apartments

# Adds a new apartment to the database
def add_apartment(connection, apartment_number, owner_id, tenant_id):
    try:
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO Apartments (ApartmentNumber, OwnerID, TenantID) VALUES (%s, %s, %s)",
            (apartment_number, owner_id, tenant_id) #if tenant_id is not None else (apartment_number, owner_id, None),
        )
        connection.commit()
        cursor.close()
        st.success("Apartment added successfully!")
    except Error as e:
        st.error(f"Failed to add apartment: {e}")



# Update Apartment function with an additional call to update_apartment_owners
def update_apartment(connection, apartment_id, owner_id, tenant_id):
    try:
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE Apartments SET OwnerID = %s, TenantID = %s WHERE ApartmentID = %s",
            (owner_id, tenant_id, apartment_id),
        )
        connection.commit()
        cursor.close()
        st.success("Apartment updated successfully!")
        # Call the function to update Owners
       # update_apartment_owners(connection, apartment_id, owner_id)
    except Error as e:
        st.error(f"Failed to update apartment: {e}")

# Deletes an apartment from the database
def delete_apartment(connection, apartment_id):
    try:
        cursor = connection.cursor()
        cursor.execute(
            "DELETE FROM Apartments WHERE ApartmentID = %s", (apartment_id,)
        )
        connection.commit()
        cursor.close()
        st.success("Apartment deleted successfully!")
    except Error as e:
        st.error(f"Failed to delete apartment: {e}")

def manage_apartments_ui(connection):
    st.subheader("Apartments")
    apartments = fetch_apartments(connection)
   
    display_apartments_ui(apartments)
    
    st.subheader("Manage Apartments")
    operation_choice = st.selectbox("Select operation", ["Add Apartment", "Update Apartment", "Delete Apartment"])
    
    if operation_choice == "Add Apartment":
        with st.form("Add Apartment Form"):
            apartment_number = st.number_input("Apartment Number")
            owner_id = st.number_input("Owner ID")
            tenant_id = st.number_input("Tenant ID")
            submit_button = st.form_submit_button("Add Apartment")
            if submit_button:
                add_apartment(connection, apartment_number, owner_id, tenant_id)
    elif operation_choice == "Update Apartment":
        with st.form("Update Apartment Form"):
            apartment_id = st.number_input("Apartment ID")
            owner_id = st.number_input("Owner ID")
            tenant_id = st.number_input("Tenant ID")
            submit_button = st.form_submit_button("Update Apartment")
            if submit_button:
                update_apartment(connection, apartment_id, owner_id, tenant_id)
    elif operation_choice == "Delete Apartment":
        with st.form("Delete Apartment Form"):
            apartment_id = st.number_input("Apartment ID")
            submit_button = st.form_submit_button("Delete Apartment")
            if submit_button:
                delete_apartment(connection, apartment_id)
def fetch_rents(connection):
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Rent")
        rent_records = cursor.fetchall()
        cursor.close()
        return rent_records
    except Error as e:
        st.error(f"Failed to fetch rent entries: {e}")
        
# Function to display total rent due for each tenant
def display_total_rent_due_for_each_tenant(connection):
    st.subheader("Total Rent Due for Each Tenant")
    
    cursor = connection.cursor(dictionary=True)
    cursor.execute(
        """
        SELECT TenantID, SUM(Amount) AS TotalRentDue
        FROM Rent
        WHERE Status = 'Due'
        GROUP BY TenantID
        """
    )
    
    rent_due_info = cursor.fetchall()
    cursor.close()
    
    for info in rent_due_info:
        tenant_id = info['TenantID']
        total_rent_due = info['TotalRentDue']
        
        st.write(f"Tenant ID: {tenant_id}, Total Rent Due: Rs{total_rent_due:.2f}")


def display_rents_ui(rents):
    st.subheader("Rent Entries")
    for rent in rents:
        st.text(f"Rent ID: {rent['RentID']}, Amount: {rent['Amount']}, Due Date: {rent['DueDate']}, Status: {rent['Status']}, Apartment ID: {rent['ApartmentID']}, Tenant ID: {rent['TenantID']}")

def add_rent(connection, amount, due_date, status, apartment_id, tenant_id):
    try:
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO Rent (Amount, DueDate, Status, ApartmentID, TenantID) VALUES (%s, %s, %s, %s, %s)",
            (amount, due_date, status, apartment_id, tenant_id),
        )
        connection.commit()
        cursor.close()
        st.success("Rent entry added successfully!")
    except Error as e:
        st.error(f"Failed to add rent entry: {e}")

def update_rent(connection, rent_id, amount, due_date, status, apartment_id, tenant_id):
    try:
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE Rent SET Amount = %s, DueDate = %s, Status = %s, ApartmentID = %s, TenantID = %s WHERE RentID = %s",
            (amount, due_date, status, apartment_id, tenant_id, rent_id),
        )
        connection.commit()
        cursor.close()
        st.success("Rent entry updated successfully!")
    except Error as e:
        st.error(f"Failed to update rent entry: {e}")

def delete_rent(connection, rent_id):
    try:
        cursor = connection.cursor()
        cursor.execute(
            "DELETE FROM Rent WHERE RentID = %s", (rent_id,)
        )
        connection.commit()
        cursor.close()
        st.success("Rent entry deleted successfully!")
    except Error as e:
        st.error(f"Failed to delete rent entry: {e}")

def manage_rents_ui(connection):
    st.subheader("Rent Management")
    rents = fetch_rents(connection)
    
    display_rents_ui(rents)
    
    st.subheader("Manage Rent Entries")
    operation_choice = st.selectbox("Select operation", ["Add Rent Entry", "Update Rent Entry", "Delete Rent Entry"])
    
    if operation_choice == "Add Rent Entry":
        with st.form("Add Rent Entry Form"):
            amount = st.number_input("Amount")
            due_date = st.date_input("Due Date")
            status = st.selectbox("Status", ["Paid", "Due"])
            apartment_id = st.number_input("Apartment ID")
            tenant_id = st.number_input("Tenant ID")
            submit_button = st.form_submit_button("Add Rent Entry")
            if submit_button:
                add_rent(connection, amount, due_date, status, apartment_id, tenant_id)
    elif operation_choice == "Update Rent Entry":
        with st.form("Update Rent Entry Form"):
            rent_id = st.number_input("Rent Entry ID")
            amount = st.number_input("Amount")
            due_date = st.date_input("Due Date")
            status = st.selectbox("Status", ["Paid", "Due"])
            apartment_id = st.number_input("Apartment ID")
            tenant_id = st.number_input("Tenant ID")
            submit_button = st.form_submit_button("Update Rent Entry")
            if submit_button:
                update_rent(connection, rent_id, amount, due_date, status, apartment_id, tenant_id)
    elif operation_choice == "Delete Rent Entry":
        with st.form("Delete Rent Entry Form"):
            rent_id = st.number_input("Rent Entry ID")
            submit_button = st.form_submit_button("Delete Rent Entry")
            if submit_button:
                delete_rent(connection, rent_id)

def fetch_maintenance_requests(connection):
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM MaintenanceRequests")
        maintenance_requests = cursor.fetchall()
        cursor.close()
        return maintenance_requests
    except Error as e:
        st.error(f"Failed to fetch maintenance requests: {e}")
    

# Add a global variable to store the generated alerts
generated_alerts = []

def generate_rent_alerts(connection, threshold_amount):
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT ApartmentID, SUM(Amount) AS TotalDueAmount
            FROM Rent
            WHERE Status = 'Due'
            GROUP BY ApartmentID
            HAVING TotalDueAmount > %s
            """,
            (threshold_amount,)
        )
        alert_records = cursor.fetchall()

        inserted_alerts = []  # New variable to store inserted alerts

        for alert in alert_records:
            apartment_id = alert['ApartmentID']
            total_due_amount = alert['TotalDueAmount']

            cursor.execute(
                """
                INSERT INTO RentAlerts (ApartmentID, TotalDueAmount, AlertDate)
                VALUES (%s, %s, CURDATE())
                """,
                (apartment_id, total_due_amount)
            )

            inserted_alerts.append({
                'ApartmentID': apartment_id,
                'TotalDueAmount': total_due_amount,
                'AlertDate': datetime.date.today(),
            })

        connection.commit()
        cursor.close()
       

        return inserted_alerts  # Return the inserted alerts
    except Error as e:
        st.error(f"Failed to generate rent alerts: {e}")

# Call generate_rent_alerts before main to initialize the variable
generated_alerts = generate_rent_alerts(create_connection(), 1000.00)



# Displays maintenance requests in the Streamlit UI
def display_maintenance_requests_ui(maintenance_requests):
    st.subheader("Maintenance Requests")
    for request in maintenance_requests:
        st.text(f"ID: {request['RequestID']}, Apartment ID: {request['ApartmentID']}, Status: {request['Status']}, Description: {request['RequestDescription']}, Date: {request['RequestDate']}")


# Adds a maintenance request to the database
def add_maintenance_request(connection, request_description, apartment_id, status):
    try:
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO MaintenanceRequests (ApartmentID, RequestDescription, Status) VALUES (%s, %s, %s)",
            (apartment_id, request_description, status),
        )
        connection.commit()
        cursor.close()
        st.success("Maintenance request added successfully!")
    except Error as e:
        st.error(f"Failed to add maintenance request: {e}")

# UI for submitting maintenance requests
def maintenance_request_ui(connection):
    st.subheader("Maintenance Requests")
    maintenance_requests = fetch_maintenance_requests(connection)
    display_maintenance_requests_ui(maintenance_requests)

    st.subheader("Manage Maintenance Requests")
    operation_choice = st.selectbox("Select operation", ["Add Request", "Update Request"])

    if operation_choice == "Add Request":
        with st.form("Add Maintenance Request Form"):
            description = st.text_input("Description")
            # Ensure that the input is converted to an integer
            apartment_id = int(st.number_input("Apartment ID"))
            status = st.selectbox("Status", ["Pending", "Completed"])
            submit_button = st.form_submit_button("Add Request")
            if submit_button:
                add_maintenance_request(connection, description, apartment_id, status)
    elif operation_choice == "Update Request":
        with st.form("Update Maintenance Request Form"):
            request_id = st.number_input("Request ID")
            status = st.selectbox("Status", ["Pending", "Completed"])
            submit_button = st.form_submit_button("Update Request")
            if submit_button:
                update_maintenance_request(connection, request_id, status)
   

# Add this function to handle updating maintenance requests
def update_maintenance_request(connection, request_id, status):
    try:
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE MaintenanceRequests SET Status = %s WHERE RequestID = %s",
            (status, request_id),
        )
        connection.commit()
        cursor.close()
        st.success("Maintenance Request updated successfully!")
    except Error as e:
        st.error(f"Failed to update maintenance request: {e}")



def main():
    # st.title("Apartment Management System")
    st.title("Mulberry Woods")

    # Initialize session state
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    # User is logged in
    if st.session_state['logged_in']:
        st.sidebar.subheader("Navigation")
        choice = st.sidebar.selectbox("Choose option", ["Home", "Owners", "Tenants", "Apartments", "Rent", "Maintenance Requests", "Logout"])

        connection = create_connection()
        if not connection:
            return  # If connection fails, don't proceed

        if choice == "Home":
            st.subheader("Welcome to Mulberry Woods Community")
            st.write("Select an option from the sidebar to get started.")
        elif choice == "Owners":
            st.subheader("Owners")
            owners = fetch_owners(connection)
            display_owners_ui(owners)

            st.subheader("Manage Owners")
            operation_choice = st.selectbox("Select operation", ["Add Owner", "Update Owner", "Delete Owner"])

            if operation_choice == "Add Owner":
                with st.form("Add Owner Form"):
                    first_name = st.text_input("First Name")
                    last_name = st.text_input("Last Name")
                    contact_info = st.text_input("Contact Info")
                    apartment_number = st.number_input("Apartment Number")  # New field
                    submit_button = st.form_submit_button("Add Owner")
                    if submit_button:
                        add_owner(connection, first_name, last_name, contact_info, apartment_number)
            elif operation_choice == "Update Owner":
                with st.form("Update Owner Form"):
                    owner_id = st.number_input("Owner ID")
                    first_name = st.text_input("First Name")
                    last_name = st.text_input("Last Name")
                    contact_info = st.text_input("Contact Info")
                    submit_button = st.form_submit_button("Update Owner")
                    if submit_button:
                        update_owner(connection, owner_id, first_name, last_name, contact_info)
            elif operation_choice == "Delete Owner":
                with st.form("Delete Owner Form"):
                    owner_id = st.number_input("Owner ID")
                    submit_button = st.form_submit_button("Delete Owner")
                    if submit_button:
                        delete_owner(connection, owner_id)
        elif choice == "Tenants":
            st.subheader("Tenants")
            tenants = fetch_tenants(connection)
            display_tenants_ui(tenants)

            st.subheader("Manage Tenants")
            operation_choice = st.selectbox("Select operation", ["Add Tenant", "Update Tenant", "Delete Tenant"])

            if operation_choice == "Add Tenant":
                with st.form("Add Tenant Form"):
                    first_name = st.text_input("First Name")
                    last_name = st.text_input("Last Name")
                    moving_date = st.date_input("Moving Date")
                    contact_info = st.text_input("Contact Info")
                    apartment_number = st.number_input("Apartment Number")  # New field
                    submit_button = st.form_submit_button("Add Tenant")
                    if submit_button:
                        add_tenant(connection, first_name, last_name, moving_date, contact_info, apartment_number)
            elif operation_choice == "Update Tenant":
                with st.form("Update Tenant Form"):
                    tenant_id = st.number_input("Tenant ID")
                    first_name = st.text_input("First Name")
                    last_name = st.text_input("Last Name")
                    moving_date = st.date_input("Moving Date")
                    contact_info = st.text_input("Contact Info")
                    submit_button = st.form_submit_button("Update Tenant")
                    if submit_button:
                        update_tenant(connection, tenant_id, first_name, last_name, moving_date, contact_info)
            elif operation_choice == "Delete Tenant":
                with st.form("Delete Tenant Form"):
                    tenant_id = st.number_input("Tenant ID")
                    submit_button = st.form_submit_button("Delete Tenant")
                    if submit_button:
                        delete_tenant(connection, tenant_id)
        elif choice == "Apartments":
                manage_apartments_ui(connection)
        elif choice == "Rent":
                manage_rents_ui(connection)
                display_total_rent_due_for_each_tenant(connection)


                st.subheader("Rent Alerts")
                with st.form("Generate Rent Alerts"):
                    threshold_amount = st.number_input("Set Threshold Amount", min_value=0.0)

                    submit_button = st.form_submit_button("Generate Rent Alerts")
                    if submit_button:
                     alerts = generate_rent_alerts(connection, threshold_amount)
                     if alerts:  # If there are alerts
                          st.subheader("Generated Rent Alerts:")
                          for alert in alerts:
                             st.write(f"Apartment ID: {alert['ApartmentID']}, Amount: {alert['TotalDueAmount']}, Alert Date: {alert['AlertDate']}")
                     else: 
                            st.info("No rent alerts to display. All rents are below the threshold.")

                     
        elif choice == "Maintenance Requests":
            maintenance_request_ui(connection)
        elif choice == "Logout":
            st.session_state['logged_in'] = False
            st.experimental_rerun()

        connection.close()
    else:
        # User is not logged in
        choice = st.sidebar.selectbox("Menu", ["Login", "Sign Up"])
        if choice == "Login":
            login_ui()
        elif choice == "Sign Up":
            signup_ui()

if __name__ == "__main__":
    main()
