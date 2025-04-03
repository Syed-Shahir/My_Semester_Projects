import mysql.connector as connector

#Bank Database
class Bank_DB:
    def __init__(self):
        self.conn=connector.connect(host='',user='',password='',port='',database='Bank_Management_System')
        
    def create_portal_log_in(self,user_name,password,verification_code):
        
        query = "INSERT INTO Registered_Accounts(User_Name, User_Password, Verification_Code) VALUES (%s, %s, %s)"
        cur = self.conn.cursor()
        cur.execute(query, (user_name, password, verification_code))
        self.conn.commit()
        print("Account created successfully")
        return 1
        
    def log_in(self, user_name, password):
        # Check if the username exists
        query_username = "SELECT User_Name FROM Registered_Accounts WHERE User_Name = %s"
        cur = self.conn.cursor()
        cur.execute(query_username, (user_name,))
        result_username = cur.fetchone()

        if result_username:
            # If the username exists, check the password
            query_password = "SELECT User_Password FROM Registered_Accounts WHERE User_Name = %s"
            cur.execute(query_password, (user_name,))
            stored_password = cur.fetchone()[0]

            if stored_password == password:
                print("Login successful!")
                return 1
            else:
                print("Incorrect password. Please try again.")
        else:
            print("Username does not exist.")
        return 0

    def delete_account(self, user_name):
        Customer_ID = self.get_customer_id(user_name)
        query = "DELETE FROM Account_Info WHERE Customer_ID = %s"
        cur = self.conn.cursor()
        cur.execute(query, (Customer_ID,))
        self.conn.commit()
        print("Account deleted successfully.")
        
    def update_personal_info(self, user_name):
        query_select = "SELECT * FROM Customer_Personal_Info WHERE User_name = %s"
        query_update = """
            UPDATE Customer_Personal_Info 
            SET Customer_Name = %s, Guardian_Name = %s,
                Secondary_Address = %s, Postal_Code = %s, Email_ID = %s
            WHERE User_name = %s
        """


        cur = self.conn.cursor()
        cur.execute(query_select, (user_name,))
        existing_data = cur.fetchone()

        if existing_data:
            print("Enter new personal details:")
            Customer_Name = input("enter customer Name = ").capitalize()
            Guardian_Name = input("enter Guardian Name = ")
            Secondary_Address = input("enter Secondary Address = ")
            Postal_Code = input("enter Postal Code = ")
            Email_ID = input("enter Email Address = ")
        # Execute the SQL query to update data in the database
            cur.execute(query_update, ( Customer_Name, Guardian_Name,
                                        Secondary_Address, Postal_Code,
                                    Email_ID,user_name))
            self.conn.commit()
            print("Personal details updated successfully.")
        else:
            print("User not found.")
    
    def insert_personal_details(self,User_name):
        Customer_Name = input("enter customer Name = ").capitalize()
        Date_Of_Birth = input("enter DOB {YYYY-MM-DD} = ")
        Guardian_Name = input("enter Guardian Name = ")
        Permanent_Address = input("enter your Permenant Address = ")
        Secondary_Address = input("enter Secondary Address = ")
        Postal_Code = input("enter Postal Code = ")
        Email_ID = input("enter Email Address = ")
        Gender = input("enter your gender male/female = ")
        CNIC_Number = input("enter CNIC {XXXXX-XXXXXXX-X} = ")
        
        query = "INSERT INTO Customer_Personal_Info(Customer_Name,Date_Of_Birth,Guardian_Name,Permanent_Address,Secondary_Address,Postal_Code,Email_ID,Gender,CNIC_Number,User_Name)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cur = self.conn.cursor()
        cur.execute(query,(Customer_Name,Date_Of_Birth,Guardian_Name,Permanent_Address,Secondary_Address,Postal_Code,Email_ID,Gender,CNIC_Number,User_name))
        self.conn.commit()
        print("data entered successfully")
        
    def print_personal_details(self, user_name):
        query = "SELECT * FROM Customer_Personal_Info WHERE User_name = %s"
        cur = self.conn.cursor()
        cur.execute(query, (user_name,))
        
        # Fetching the details of the user
        user_details = cur.fetchone()

        if user_details:  # If the user is found
            print("User Details:")
            print(f"Customer ID: {user_details[0]}")
            print(f"User Name: {user_details[1]}")
            print(f"Customer Name: {user_details[2]}")
            print(f"Guardian Name : {user_details[4]}")
            print(f"Email address : {user_details[8]} ")
            print(f"Postal Code : {user_details[7]}")
            # Include other details similarly
       
       
    def get_customer_id(self, user_name):
        query = "SELECT Customer_ID FROM Customer_Personal_Info WHERE User_name = %s"
        cur = self.conn.cursor()
        cur.execute(query, (user_name,))
        result = cur.fetchone()

        if result:
            return result[0]  # Return the Customer_ID if found
        else:
            print("Username does not exist.")
            return None  # Return None if username doesn't exist
        
        
    def create_account(self,user_name):
        Customer_ID = self.get_customer_id(user_name)
        if Customer_ID: 
            print("enter account details ") 
            Account_Type = input("enter account type = ").lower()
            Registration_Date = input("enter registeration date {YYYY-MM-DD} = ")
            Activation_Date = input("enter Activation date {YYYY-MM-DD} = ")
            Initial_Deposit = int(input("enter initial deposit = "))
            Current_Balance = Initial_Deposit

            # Execute the SQL query to insert data into the database
            query = "insert into Account_Info(Customer_ID,Account_Type,Registration_Date,Activation_Date,Initial_Deposit,Current_Balance)values(%s,%s,%s,%s,%s,%s)"
            cur = self.conn.cursor()
            cur.execute(query,(Customer_ID,Account_Type,Registration_Date,Activation_Date,Initial_Deposit,Current_Balance))
            self.conn.commit()
            print("account details entered successfully")
        
    def print_account_details(self,user_name):
        Customer_ID = self.get_customer_id(user_name)
        query = "SELECT * from Account_Info WHERE Customer_ID = %s"
        cur = self.conn.cursor()
        cur.execute(query,(Customer_ID,))
        user_details = cur.fetchone()
        if user_details:
            print(f"account number = {user_details[0]}")
            print(f"account type = {user_details[2]} ")
            print(f"current balance = {user_details[6]}")
        else:
            print("account does not exist")
    
    def deposit_cash(self, user_name):
        customer_id = self.get_customer_id(user_name)
        if customer_id:
            deposit_amount = int(input("Enter the amount to deposit: "))
            
            # Assuming the account number is already known or fetched
            # Update the Current_Balance in Account_Info table
            query = "UPDATE Account_Info SET Current_Balance = Current_Balance + %s WHERE Customer_ID = %s"
            cur = self.conn.cursor()
            cur.execute(query, (deposit_amount,customer_id))
            self.conn.commit()

            print(f"Deposit of {deposit_amount} made successfully.")
        else:
            print("Unable to find the customer ID for the given username.")
    
    def withdraw_cash(self, user_name):
        customer_id = self.get_customer_id(user_name)
        if customer_id:
            query = "SELECT Current_Balance FROM Account_Info WHERE Customer_ID = %s"
            cur = self.conn.cursor()
            cur.execute(query, (customer_id,))
            check_current = cur.fetchone()

            if check_current:
                current_balance = check_current[0]
                amount = int(input("Enter amount to withdraw: "))

                if amount <= current_balance:
                    query = "UPDATE Account_Info SET Current_Balance = Current_Balance - %s WHERE Customer_ID = %s"
                    cur.execute(query, (amount, customer_id))
                    self.conn.commit()
                    print(f"Withdrawal of {amount} made successfully.")
                else:
                    print("Insufficient funds.")
            else:
                print("Failed to retrieve current balance.")
        else:
            print("Customer ID not found for the given username.")

bank1 = Bank_DB()
switch = True

while(switch):
    print("*****************WELCOME TO AL-SYED BANK*************")
    print("*****************************************************")
    print("*****************ENTER YOUR OPTION*******************")
    print("*****************************************************")
    print("press 1 to logIN ")
    print("press 2 for Registeration ")
    print("press 0 to exit ")
    choice = int(input("your choice = "))
    if(choice == 1):
        #login function
        user_name = input("Enter username: ")
        password = input("Enter your password: ")
        if(bank1.log_in(user_name,password) == 1):
            login_switch = True
            while(login_switch):
                print("press 1 for personal details ")
                print("press 2 for account details ")
                print("press 3 deposit cash in account ")
                print("press 4 to withdraw cash from account ")
                print("press 5 for deleting your account")
                print("press 6 for update personal information your account")
                print("press 0 to exit ")
                login_choice = int(input("***enter your choice*** = "))
                if(login_choice == 1):
                    bank1.print_personal_details(user_name)
                elif(login_choice == 2):
                    bank1.print_account_details(user_name)
                elif(login_choice == 3):
                    #cash deposit
                    bank1.deposit_cash(user_name)
                elif(login_choice == 4):
                    #cash with draw
                    bank1.withdraw_cash(user_name)
                elif(login_choice==5):
                    bank1.delete_account(user_name)
                elif(login_choice==6):
                    bank1.update_personal_info(user_name)
                elif(login_choice == 0):
                    login_switch = False
                else:
                    print("invalid input")
            bank1.print_personal_details(user_name)
        else:
            print("Access Denied")
    elif(choice == 2):
        #registeration function
        registeration_switch = True
        while(registeration_switch):
            print("press 1 for new user")
            print("press 2 for account creation")
            print("press 0 to exit ")
            registeration_choice = int(input("enter your choice = "))
            if(registeration_choice == 1):
                user_name = input("Enter the username: ")
                password = input("Enter the password: ")
                verification_code = input("Enter the code received: ")
                bank1.create_portal_log_in(user_name,password,verification_code)
                print("enter the personal details :")
                bank1.insert_personal_details(user_name)
            elif(registeration_choice == 2):
                user_name = input("Enter username: ")
                password = input("Enter your password: ")
                if(bank1.log_in(user_name,password) == 1):
                    bank1.create_account(user_name)
                else:
                    print("account do not exist")
            elif(registeration_choice == 0):
                    registeration_switch = False
            else:
                print("invalid input!!!")
    elif(choice == 0):
        switch = False
    else:
        print("invalid input")

print("****You exited From Bank System****")

