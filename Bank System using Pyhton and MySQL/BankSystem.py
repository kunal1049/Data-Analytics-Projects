# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 21:07:38 2024

@author: user
"""

import mysql.connector
from mysql.connector import Error
import csv
import hashlib
import matplotlib.pyplot as plt
import numpy as np

class BankSystem:
    def __init__(self):
        self.db = None
        self.cursor = None
        
    def connect_to_database(self,username, password):
        try:
            self.db = mysql.connector.connect(host='localhost',
                                                database='bank',
                                                user=username,
                                                password=password)
            if self.db.is_connected():
                self.cursor = self.db.cursor()
                print("Connected to MySQL database")
        except Error as e:
            print("Error while connecting to MySQL:", e)
    
    def create_tables(self):
        try:
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                                ID INT AUTO_INCREMENT PRIMARY KEY,
                                email VARCHAR(100),
                                password VARCHAR(100)
                                )''')

            self.cursor.execute('''CREATE TABLE IF NOT EXISTS accounts (
                                ID INT AUTO_INCREMENT PRIMARY KEY,
                                email VARCHAR(100),
                                balance INT
                                )''')

            self.cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (
                                ID INT AUTO_INCREMENT PRIMARY KEY,
                                email VARCHAR(100),
                                date DATE,
                                message VARCHAR(100)
                                )''')
            print("Tables created successfully")
        except Error as e:
            print("Error while creating tables:", e)
            
    def register(self):
        email = input("Enter email: ")
        password = input("Enter password: ")
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        try:
            self.cursor.execute("INSERT INTO users (email, password) VALUES (%s, %s)", (email, hashed_password))
            self.cursor.execute("INSERT INTO accounts (email, balance) VALUES (%s, 0)", (email,))
            self.db.commit()
            print("Registration successful!")
        except Error as e:
            print("Error while registering:", e)
            
    def login(self):
        attempts = 0
        while attempts < 3:
            email = input("Enter email: ")
            password = input("Enter password: ")
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            self.cursor.execute("SELECT * FROM users WHERE email=%s AND password=%s", (email, hashed_password))
            if self.cursor.fetchone():
                print("Login successful!")
                return email
            else:
                print("Invalid email or password. Please try again.")
                attempts += 1
        print("Too many login attempts. Exiting...")
        exit()
    
    def deposit(self, email):
        amt = int(input("Enter deposit amount: "))
        date = input("Enter date (YYYY-MM-DD): ")
        self.cursor.execute("SELECT balance FROM accounts WHERE email=%s", (email,))
        balance = self.cursor.fetchone()[0]
        amount =balance+amt
        self.cursor.execute("UPDATE accounts SET balance = %s WHERE email = %s", (amount, email))
        self.cursor.execute("INSERT INTO transactions (email, date, message) VALUES (%s, %s, %s)", (email, date, f"Deposit of {amt}"))
        self.db.commit()
        print("Deposit successful!")
            
    def withdraw(self, email):
        amount = int(input("Enter withdrawal amount: "))
        date = input("Enter date (YYYY-MM-DD): ")
        try:
            self.cursor.execute("SELECT balance FROM accounts WHERE email=%s", (email,))
            balance = self.cursor.fetchone()[0]
            if balance >= amount:
                self.cursor.execute("UPDATE accounts SET balance = balance - %s WHERE email = %s", (amount, email))
                self.cursor.execute("INSERT INTO transactions (email, date, message) VALUES (%s, %s, %s)", (email, date, f"Withdrawal of {amount}"))
                self.db.commit()
                print("Withdrawal successful!")
            else:
                print("Insufficient balance!")
        except Error as e:
            print("Error while withdrawing:", e)

    def show_balance(self, email):
        try:
            self.cursor.execute("SELECT balance FROM accounts WHERE email=%s", (email,))
            balance = self.cursor.fetchone()[0]
            print(f"Your account balance is: {balance}")
        except Error as e:
            print("Error while fetching balance:", e)

    def show_transactions(self, email):
        try:
            self.cursor.execute("SELECT * FROM transactions WHERE email=%s", (email,))
            transactions = self.cursor.fetchall()
            transactions = reversed(transactions)
            for transaction in transactions:
                print(transaction)
        except Error as e:
            print("Error while fetching transactions:", e)

    def export_transactions(self, email):
        try:
            self.cursor.execute("SELECT * FROM transactions WHERE email=%s", (email,))
            transactions = self.cursor.fetchall()
            with open('transactions.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['ID', 'Email', 'Date', 'Message'])
                writer.writerows(reversed(transactions))
            print("Transactions exported to transactions.csv")
        except Error as e:
            print("Error while exporting transactions:", e)
            
    def display_chart(self,email):
        self.cursor.execute("SELECT email,balance FROM accounts WHERE email=%s", (email,))
        #result = self.cursor.fetchall
        
        balance = []
        
        for i in self.cursor:
            balance.append(i)
        
        x = np.array(balance)
        y = x*2
        plt.plot(x,y)
        plt.ylim(0, 5)
        plt.xlabel("Name of Students")
        plt.ylabel("Marks of Students")
        plt.show()
            
    def main(self):
        self.connect_to_database('root','root')
        self.create_tables()

        while True:
            print("\n1: Login\n2: Register\n0: Quit")
            choice = input("Enter your choice: ")
            match choice:
                case '1':
                    user_email = self.login()
                    while True:
                        print("\n1: Deposit\n2: Withdraw\n3: Show Balance\n4: Show all Transactions\n5: Export Transactions\n6: Display Chart\n0: Logout")
                        choice = input("Enter your choice: ")
                        match choice:
                            case '1':
                                self.deposit(user_email)
                            case '2':
                                self.withdraw(user_email)
                            case '3':
                                self.show_balance(user_email)
                            case '4':
                                self.show_transactions(user_email)
                            case '5':
                                self.export_transactions(user_email)
                            case '6':
                                self.display_chart(user_email)
                            case '0':
                                print("Logged Out")
                                break
                            case _:
                                print("Invalid choice")
                case '2':
                    self.register()
                case '0':
                    print("Quit")
                    break
                case _:
                    print("Invalid Input")
        if self.db.is_connected():
            self.cursor.close()
            self.db.close()
            
if __name__ == "__main__":
    bank_system = BankSystem()
    bank_system.main()