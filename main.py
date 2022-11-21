from multiprocessing import connection
from os import curdir
from sqlite3 import Connection, Cursor, connect
import mysql.connector
import sys

#Connects python code to mysql database
try:
    db= mysql.connector.connect(
        host= "localhost",
        user= "root",
        password= "",
        database= "methods group project"
    )
    print("successful conncection!")

    #if fail to connect to database then exits
except:
    print("failed connection.")
    sys.exit()

print("made it here")

coursor= db.cursor()

#Account class
class Account:
    #Creates your account with personal info then adds it to the database
    def CreateAccount(fullname, password, email, payment, address, orderHistory):
        coursor.execute("INSERT INTO account (fullname, password, email, payment, address, orderHistory) VALUES (%s,%s,%s,%s,%s,%s)", (fullname, password, email, payment, address,0))
        db.commit

        print(coursor.rowcount, "inserted items")

        #Login Function
    def Login(email,password):
        #searches for account with the email and password
        coursor.execute('SELECT * FROM account WHERE UserID = %s AND Password = %s', (email, password,))
        
        currentAcc= coursor.fetchone

        if currentAcc:
           
            return True
        else:
            return False
        
    def DeleteAccount(email):
        #Deletes account with the email inputed
        coursor.execute('DELETE FROM account WHERE email = %s',(email,))
        db.commit
    
    #Edit your account information
    def EditAccount(fullname, password, email, payment, address):
        pass
        
    #Edits order history    
    def EditOrderHistory():
        #Searches order history on the account by email
        accountName=str(input("enter the email"))
        coursor.execute('SELECT orderHistory FROM account WHERE email=%s', (accountName,))
        num= coursor.fetchone()
        num +=1
        #Updates with new changes
        coursor.execute('UPDATE account SET orderHistory = %s WHERE email=%s', (num,accountName,))
        db.commit  #added??


    def Logout():
        LogStatus= False
        return LogStatus

    #Changes payment method on the specified email
    def EditPaymentMethod(email):
        newPayment= str(input("enter new shipping payment"))
        coursor.execute('UPDATE account SET payment = %s WHERE email=%s', (newPayment,email))
        db.commit

    #Changes shipping address on the specified email
    def EditShippingAddress(email):

        newAdd= str(input("enter new shipping address"))
        coursor.execute('UPDATE account SET address = %s WHERE email=%s', (newAdd,email))
        db.commit
    
    #Views account info on account with specified email
    def ViewAccountInformation():

        userEmail= str(input("enter email"))
        coursor.execute('SELECT * FROM account WHERE email=%s', (userEmail,))
        info= coursor.fetchone
        print(info)

#Inventory Class
class Inventory:

    def displayBooks():
        #Finds a book and displays it
        coursor.execute("SELECT * FROM Inventory")
        table= coursor

        for i in table:
            print(i)
            print("\n")
            
            #Asks if you would like to add the book to cart
            ans= str(input("would you like to add anything to the shopping cart (yes or no"))

            if ans== "yes":
                itemid= int(input("what is the isbn number?"))
                coursor.execute('INSERT INTO shopping cart (title,price,quantity,isbn) SELECT title,Price,Stock,isbn FROM Inventory WHERE isbn= %s',(itemid,))

class shoppingCart:
    #adds specified items to shopping cart
    def additems():
        item= int(input())
        coursor.execute(('INSERT INTO shopping cart (title,price,quantity,isbn) SELECT title,price,stock,isbn FROM Inventory WHERE isbn= %s',(item,)))
        db.commit

    def displayCart():
        #displays specified items form user shopping cart
        coursor.execute("Select * FROM shopping cart")
        res= coursor.fetchall
        print("shopping cart ")
        for i in res:
            print(i, "\n")
    
    #displays the sum of shopping cart prices
    def totalPrice():
        res=coursor.execute("SELECT SUM(price) FROM shopping cart")
        print(res)
    
    #deletes specified item from shopping cart
    def deleteItem():
        item= int(input("whats the item you want to delete (isbn number"))
        coursor.execute("delete FROM shopping cart WHERE isbn=%s", (item,))
    
    #if checking out then it clears the shopping cart
    def checkingOut():
        coursor.execute("'delete FROM ShoppingCart'")

# beginning of main

loggedin= False

while(True):
    while(loggedin==False):
        #Opening menu for bookstore
        print("welcome to the bookstore\n")
        print("what would you like to do\n")
        print("1. Login\n 2. Create an Account.\n 3. Exit Program")

        answer= int(input())
        #if 1 then login to your account
        if answer== 1:
            email= str(input("enter your email"))
            password= str(input("enter your password"))

            loggingIn= Account.Login(email,password)
            #for a login successful login
            if loggingIn== True:
                print("successful login ")
            #for a failed login
            elif loggingIn==False:
                print("not logged in")
            else:
                print("line 153")
            
                exit()
        #if 2 then create an account
        elif answer== 2:
            print("creating an account")
            
            #input all the required account information 
            fullname= str(input("please enter your full name"))
            password= str(input("please enter your a password"))
            email= str(input("please enter your email"))
            payment= str(input("please enter your payment info"))
            address= str(input("please enter your address"))
            
            account= Account.CreateAccount(fullname,password,email, payment, address,0)
            #for successful account creation
            if account== True:
                print("seccssfully created an account")
            
            #for a failed account creation
            elif account==False:
                print("something went wrong")
            else:
                print("line 174")
            
                exit()
        #exits if 3 is inputed
        elif answer==3:
            print("goodbye!")
            sys.exit(1)

    #next menu after successful login
    while(loggedin==True):

        print("1. Shopping Cart\n 2. Account Info\n 3. View Items 4. Logout\n 5. Exit\n")
        
        choice= int(input("Please enter a choice"))
        #if 1 then go to your shopping cart
        if choice== 1:
            print("\nShopping Cart")
            print("\n1. Add items to cart")
            print("\n2. View cart")
            print("\n3. Total price of cart")
            print("\n4. Remove item from cat")
            print("\n5. Check out")

            Cart_choice = int(input("\n What would you like to do:"))
            
            #if 1 then find books to add to cart
            if (Cart_choice == 1):
                Inventory.displayBooks()
                print("put in the item ID of the book you want:")
                shoppingCart.additems()
            
            #if 2 then display your cart items
            if (Cart_choice == 2):
                print("Here is the contents of your cart.")
                shoppingCart.displayCart()
            
            #if 3 then display shopping cart price total
            if (Cart_choice == 3):
                print("This is the total price of the itmes in your cart.")
                shoppingCart.totalPrice()
            
            #if 4 then find books to remove from cart
            if (Cart_choice == 4):
                Inventory.displayBooks()
                print("put in the item ID of the book you wish to remove:")
                shoppingCart.deleteItem()
            
            #if 5 then checkout
            if (Cart_choice == 5):
                shoppingCart.checkingOut()
               

        





