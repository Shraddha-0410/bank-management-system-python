import streamlit as st 
import datetime 

if "accounts" not in st.session_state:
    st.session_state.accounts = []
    
if "transaction" not in st.session_state:
    st.session_state.transaction = []

if "logged_in_account" not in st.session_state:
    st.session_state.logged_in_account = None

st.title("Bank Management System")

if st.session_state.logged_in_account == None:
    st.header("Create Account")
    name = st.text_input("Enter your name")
    age = st.number_input("Enter your age", min_value=18, step=1)
    pin = st.text_input("Set a 4-digit PIN", type="password")
    
    if st.button("Create Account"):
        if name and len(pin) == 4:
            account_id = len(st.session_state.accounts) + 1
            st.session_state.accounts.append({"AccountID": account_id, "Name": name, "Age": age, "PIN": pin, "Balance": 0})
            st.success(f"Account created! Your Account ID is {account_id}")
        else:
            st.error("Please enter valid details!")
            
    st.header("Login")
    account_id = st.number_input("Enter Account ID", min_value=1, step=1)
    pin = st.text_input("Enter your PIN", type="password")
    
    if st.button("Login"):
        for account in st.session_state.accounts:
            if account["AccountID"] == account_id and account["PIN"] == pin:
                st.session_state.logged_in_account = account
                st.success(f"Welcome, {account['Name']}!")
                break
        else:
            st.error("Invalid Account ID or PIN")
else:
    st.sidebar.title(f"Welcome, {st.session_state.logged_in_account['Name']}!")
    action = st.sidebar.radio("Choose an action", ["Deposit", "Withdraw", "View Transactions", "Logout"])

    if action == "Deposit":
        st.header("Deposit Money")
        amount = st.number_input("Enter amount to deposit", min_value=1)
        
        if amount > 0:  # Check if a valid amount is entered
            if st.button("Deposit"):
                # Access the logged-in account
                account = st.session_state.logged_in_account
                # Update balance
                account["Balance"] += amount
                # Record the transaction
                st.session_state.transaction.append({
                    "AccountID": account["AccountID"], 
                    "Date": datetime.datetime.now(), 
                    "Type": "Deposit", 
                    "Amount": amount, 
                    "Balance": account["Balance"]
                })
                st.success(f"Deposited ₹{amount}. New Balance: ₹{account['Balance']}")
        else:
            st.error("Please enter a valid amount to deposit.") 
    
    elif action == "Withdraw":
        st.header("Withdraw Money")
        amount = st.number_input("Enter amount to withdraw", min_value=1)
        
        if st.button("Withdraw"):
            account = st.session_state.logged_in_account
            
            # Check if the withdrawal amount is greater than the balance
            if amount > account["Balance"]:
                st.error("Insufficient balance!")  # Show error if insufficient balance
            else:
                # Deduct the withdrawal amount from the balance
                account["Balance"] -= amount
                
                # Record the transaction (withdrawal)
                st.session_state.transaction.append({
                    "AccountID": account["AccountID"], 
                    "Date": datetime.datetime.now(),  # Ensure datetime is imported at the top
                    "Type": "Withdraw", 
                    "Amount": amount, 
                    "Balance": account["Balance"]
                })
                
                # Show success message
                st.success(f"Withdrew ₹{amount}. New Balance: ₹{account['Balance']}")

    elif action == "View Transactions":
        st.header("Transaction History")
        
        # Get the logged-in user's AccountID
        account_id = st.session_state.logged_in_account["AccountID"]
        
        # Initialize an empty list to store the user's transactions
        transactions = []
        
        # Loop through all transactions and filter the ones that belong to the logged-in user
        for t in st.session_state.transaction:
            if t["AccountID"] == account_id:
                transactions.append(t)
        
        # If the user has any transactions, display them
        if transactions:
            for t in transactions:
                st.write(f"{t['Date']} - {t['Type']}: ₹{t['Amount']} | Balance: ₹{t['Balance']}")
        else:
            st.info("No transactions found!")

    elif action == "Logout":
        st.session_state.logged_in_account = None
        st.sidebar.info("You have been logged out.")

