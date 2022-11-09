from multiprocessing import connection
from os import curdir
from sqlite3 import Connection, Cursor, connect
import mysql.connector
import sys

try:
    db= mysql.connector.connect(
        host= "localhost",
        user= "root",
        password= "",
        database= "methods group project"
    )
    print("successful conncection!")

except:
    print("failed connection.")
    sys.exit()

print("made it here")

coursor= db.cursor()


class Account:
    
    def CreateAccount(fullname, password, email, payment, address, orderHistory):
        coursor.execute("INSERT INTO account (fullname, password, email, payment, address, orderHistory) VALUES (%s,%s,%s,%s,%s,%s)", (fullname, password, email, payment, address,0))
        db.commit

        print(coursor.rowcount, "inserted items")

    def Login(email,password):
        
        coursor.execute('SELECT * FROM account WHERE UserID = %s AND Password = %s', (email, password,))
        
        currentAcc= coursor.fetchone

        if currentAcc:
           
            return True
        else:
            return False
        
    def DeleteAccount(email):

        coursor.execute('DELETE FROM account WHERE email = %s',(email,))
        db.commit

    def EditAccount(fullname, password, email, payment, address):
        pass
        

    def EditOrderHistory():
        accountName=str(input("enter the email"))
        coursor.execute('SELECT orderHistory FROM account WHERE email=%s', (accountName,))
        num= coursor.fetchone()
        num +=1
        coursor.execute('UPDATE account SET orderHistory = %s WHERE email=%s', (num,accountName,))
        db.commit  #added??


    def Logout():
        LogStatus= False
        return LogStatus

    def EditPaymentMethod(email):
        newPayment= str(input("enter new shipping payment"))
        coursor.execute('UPDATE account SET payment = %s WHERE email=%s', (newPayment,email))
        db.commit


    def EditShippingAddress(email):

        newAdd= str(input("enter new shipping address"))
        coursor.execute('UPDATE account SET address = %s WHERE email=%s', (newAdd,email))
        db.commit

    def ViewAccountInformation():

        userEmail= str(input("enter email"))
        coursor.execute('SELECT * FROM account WHERE email=%s', (userEmail,))
        info= coursor.fetchone
        print(info)


class Inventory:

    def displayBooks():
        coursor.execute("SELECT * FROM Inventory")
        table= coursor

        for i in table:
            print(i)
            print("\n")

            ans= str(input("would you like to add anything to the shopping cart (yes or no"))

            if ans== "yes":
                itemid= int(input("what is the isbn number?"))
                coursor.execute('INSERT INTO shopping cart (title,price,quantity,isbn) SELECT title,Price,Stock,isbn FROM Inventory WHERE isbn= %s',(itemid,))

class shoppingCart:

    def additems():
        item= int(input())
        coursor.execute(('INSERT INTO shopping cart (title,price,quantity,isbn) SELECT title,price,stock,isbn FROM Inventory WHERE isbn= %s',(item,)))
        db.commit

    def displayCart():

        coursor.execute("Select * FROM shopping cart")
        res= coursor.fetchall
        print("shopping cart ")
        for i in res:
            print(i, "\n")

    def totalPrice():
        res=coursor.execute("SELECT SUM(price) FROM shopping cart")
        print(res)
    
    def deleteItem():
        item= int(input("whats the item you want to delete (isbn number"))
        coursor.execute("delete FROM shopping cart WHERE isbn=%s", (item,))
    
    def checkingOut():
        coursor.execute("'delete FROM ShoppingCart'")

# begging main

loggedin= False

while(True):
    while(loggedin==False):
        print("welcome to the bookstore\n")
        print("what would you like to do\n")
        print("1. Login\n 2. Create an Account.\n 3. Exit Program")

        answer= int(input())

        if answer== 1:
            email= str(input("enter your email"))
            password= str(input("enter your password"))

            loggingIn= Account.Login(email,password)

            if loggingIn== True:
                print("successful login ")
        
            elif loggingIn==False:
                print("not logged in")
            else:
                print("line 153")
            
                exit()

        elif answer== 2:
            print("creating an account")

            fullname= str(input("please enter your full name"))
            password= str(input("please enter your a password"))
            email= str(input("please enter your email"))
            payment= str(input("please enter your payment info"))
            address= str(input("please enter your address"))
            
            account= Account.CreateAccount(fullname,password,email, payment, address,0)

            if account== True:
                print("seccssfully created an account")

            elif account==False:
                print("something went wrong")
            else:
                print("line 174")
            
                exit()

        elif answer==3:
            print("goodbye!")
            sys.exit(1)


    while(loggedin==True):

        print("1. Shopping Cart\n 2. Account Info\n 3. View Items 4. Logout\n 5. Exit\n")
        
        choice= int(input("please enter a choice"))

        if choice== 1:
            pass





