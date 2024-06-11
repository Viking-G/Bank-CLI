import json
import uuid
from datetime import datetime

# File paths
SAVING_ACCOUNT_FILE = "saving_accounts.txt"
CURRENT_ACCOUNT_FILE = "current_accounts.txt"
CUSTOMER_FILE = "customers.txt"
TRANSACTION_FILE = "transactions.txt"

class Account:
    def __init__(self, account_number, balance, customer):
        self.account_number = account_number
        self.balance = balance
        self.customer = customer

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if self.balance >= amount:
            self.balance -= amount
        else:
            print("Insufficient balance")

    def check_balance(self):
        return self.balance

class SavingAccount(Account):
    interest_rate = 0.02  # Example interest rate

    def add_monthly_interest(self):
        self.balance += self.balance * SavingAccount.interest_rate

class CurrentAccount(Account):
    def __init__(self, account_number, balance, customer, overdraw_limit):
        super().__init__(account_number, balance, customer)
        self.overdraw_limit = overdraw_limit

class Customer:
    def __init__(self, name, address, contact_details):
        self.name = name
        self.address = address
        self.contact_details = contact_details
        self.accounts = []

    def add_account(self, account):
        self.accounts.append(account)

class Transaction:
    def __init__(self, account, transaction_type, amount):
        self.transaction_id = uuid.uuid4()
        self.timestamp = datetime.now()
        self.account = account
        self.transaction_type = transaction_type
        self.amount = amount

# File handling functions
def load_data():
    try:
        with open(SAVING_ACCOUNT_FILE, 'r') as file:
            saving_accounts_data = json.load(file)
    except FileNotFoundError:
        saving_accounts_data = {}

    try:
        with open(CURRENT_ACCOUNT_FILE, 'r') as file:
            current_accounts_data = json.load(file)
    except FileNotFoundError:
        current_accounts_data = {}

    try:
        with open(CUSTOMER_FILE, 'r') as file:
            customers_data = json.load(file)
    except FileNotFoundError:
        customers_data = {}

    try:
        with open(TRANSACTION_FILE, 'r') as file:
            transactions_data = json.load(file)
    except FileNotFoundError:
        transactions_data = []

    return saving_accounts_data, current_accounts_data, customers_data, transactions_data

def save_data(saving_accounts_data, current_accounts_data, customers_data, transactions_data):
    with open(SAVING_ACCOUNT_FILE, 'w') as file:
        json.dump(saving_accounts_data, file)

    with open(CURRENT_ACCOUNT_FILE, 'w') as file:
        json.dump(current_accounts_data, file)

    with open(CUSTOMER_FILE, 'w') as file:
        json.dump(customers_data, file)

    with open(TRANSACTION_FILE, 'w') as file:
        json.dump(transactions_data, file)

# CLI functions
def create_customer():
    name = input("Enter customer name: ")
    address = input("Enter customer address: ")
    contact_details = input("Enter customer contact details: ")
    return Customer(name, address, contact_details)

def create_account(customer):
    account_type = input("Enter account type (Saving/Current): ").lower()
    account_number = input("Enter account number: ")
    balance = float(input("Enter initial balance: "))
    if account_type == "saving":
        account = SavingAccount(account_number, balance, customer)
    elif account_type == "current":
        overdraw_limit = float(input("Enter overdraw limit: "))
        account = CurrentAccount(account_number, balance, customer, overdraw_limit)
    else:
        print("Invalid account type")
        return None
    customer.add_account(account)
    return account

def make_transaction(account):
    transaction_type = input("Enter transaction type (Deposit/Withdrawal): ").lower()
    amount = float(input("Enter transaction amount: "))
    if transaction_type == "deposit":
        account.deposit(amount)
    elif transaction_type == "withdrawal":
        account.withdraw(amount)
    else:
        print("Invalid transaction type")

def check_balance(account):
    print("Current balance:", account.check_balance())

def view_transaction_history(transactions_data):
    for transaction in transactions_data:
        print("Transaction ID:", transaction["transaction_id"])
        print("Timestamp:", transaction["timestamp"])
        print("Account:", transaction["account"])
        print("Transaction Type:", transaction["transaction_type"])
        print("Amount:", transaction["amount"])
        print("-----------------------")

def main():
    # Load data from files
    saving_accounts_data, current_accounts_data, customers_data, transactions_data = load_data()
    
    print("\nAayush Shrestha")
    print("MIT231370")
    print("Melbourne Institute of Technology")
    
    # Main loop
    while True:
        print("\n1. Create Customer")
        print("2. Create Account")
        print("3. Make Transaction")
        print("4. Check Balance")
        print("5. View Transaction History")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            customer = create_customer()
            customers_data[customer.name] = {
                "address": customer.address,
                "contact_details": customer.contact_details,
                "accounts": [account.account_number for account in customer.accounts]
            }
            save_data(saving_accounts_data, current_accounts_data, customers_data, transactions_data)
       
        elif choice == "2":
            customer_name = input("Enter customer name: ")
            if customer_name in customers_data:
                customer = Customer(customer_name, customers_data[customer_name]["address"], customers_data[customer_name]["contact_details"])
                account = create_account(customer)
                if account:
                    if isinstance(account, SavingAccount):
                        saving_accounts_data[account.account_number] = {
                            "balance": account.balance,
                            "customer": customer.name
                        }
                    elif isinstance(account, CurrentAccount):
                        current_accounts_data[account.account_number] = {
                            "balance": account.balance,
                            "customer": customer.name,
                            "overdraw_limit": account.overdraw_limit
                        }
                    customers_data[customer_name]["accounts"].append(account.account_number)
                    save_data(saving_accounts_data, current_accounts_data, customers_data, transactions_data)
            else:
                print("Customer not found")
        
        elif choice == "3":
            account_number = input("Enter account number: ")
            if account_number in saving_accounts_data:
                account = SavingAccount(account_number, saving_accounts_data[account_number]["balance"], None)
            elif account_number in current_accounts_data:
                account = CurrentAccount(account_number, current_accounts_data[account_number]["balance"], None, current_accounts_data[account_number]["overdraw_limit"])
            else:
                print("Account not found")
                continue
    
            transaction_type = input("Enter transaction type (Deposit/Withdrawal): ").lower()
            amount = float(input("Enter transaction amount: "))  # Define amount here
            if transaction_type == "deposit":
                account.deposit(amount)
                saving_accounts_data[account_number]["balance"]= account.balance
            elif transaction_type == "withdrawal":
                if account_number in saving_accounts_data:
                    account = SavingAccount(account_number, saving_accounts_data[account_number]["balance"], None)
                elif account_number in current_accounts_data:
                    account = CurrentAccount(account_number, current_accounts_data[account_number]["balance"], None, current_accounts_data[account_number]["overdraw_limit"])
            else:
                print("Invalid transaction type")
                continue;
            
            account.withdraw(amount);
            
            if account_number in saving_accounts_data:
                saving_accounts_data[account_number]["balance"]= account.balance
            elif account_number in current_accounts_data:
                current_accounts_data[account_number]["balance"]= account.balance
    
            transactions_data.append({
                "transaction_id": str(uuid.uuid4()),
                "timestamp": str(datetime.now()),
                "account": account_number,
                "transaction_type": transaction_type,  # Use the entered transaction type
                "amount": amount
            })
            save_data(saving_accounts_data, current_accounts_data, customers_data, transactions_data)
        
        elif choice == "4":
            account_number = input("Enter account number: ")
            if account_number in saving_accounts_data:
                print("Current balance:", saving_accounts_data[account_number]["balance"])
                
        
        elif choice == "5":
            view_transaction_history(transactions_data)
        elif choice == "6":
            # Save data to files
            save_data(saving_accounts_data, current_accounts_data, customers_data, transactions_data)
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()
