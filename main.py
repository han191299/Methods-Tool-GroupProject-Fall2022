from multiprocessing import connection
from os import curdir
from sqlite3 import Connection, Cursor, connect
import mysql.connector
import sys

#Connects to mysql if information is correctfrom multiprocessing import connection
from os import curdir
from sqlite3 import Connection, Cursor, connect
import mysql.connector
import sys

#Connects to mysql if information is correct
try:
    db= mysql.connector.connect(
        host= "localhost",
        user= "root",
        password= "",
        database= "methodsgroupproj"
    )
    print("successful conncection!")
#if connection fails then exits
except:
    print("failed connection.")
    sys.exit()


coursor= db.cursor()

#Account class
class Account:
    
    #creates an account and adds the account info inputed
    def CreateAccount(fullname, password, email, payment, address):
        coursor.execute("INSERT INTO account (fullname, password, email, payment, address, orderHistory) VALUES (%s,%s,%s,%s,%s,%s)", (fullname, password, email, payment, address,0))
        db.commit()
        print(coursor.rowcount, "inserted items")
        return True
    
    #login by inputing an accurate email and password
    def Login(email,password):
        
        coursor.execute('SELECT * FROM account WHERE email = %s AND password = %s', (email, password,))
        
        currentAcc= coursor.fetchone()
    

        if currentAcc:
          
            return True
        else:
            return False
    
    #deletes an account with the eamil inputed
    def DeleteAccount():
        curem=str(input("please enter your email: "))
        
        coursor.execute("DELETE FROM shoppingcart")
        db.commit()


        coursor.execute('DELETE FROM account WHERE email = %s',(curem,))
        

        db.commit()
    
    #displays order history from the account email inputed
    def orderHistory():
        userEmail= str(input("enter email: "))
        
        coursor.execute('SELECT orderHistory FROM account WHERE email=%s', (userEmail,))
        ordernum= coursor.fetchone()
        print(ordernum)
        
        
    #chooses account from email inputed then allows you to update order history
    def EditOrderHistory():
        accountName=str(input("enter the email: "))
        coursor.execute('SELECT orderHistory FROM account WHERE email=%s', (accountName,))
        num= coursor.fetchone()
        num +=1
        coursor.execute('UPDATE account SET orderHistory = %s WHERE email=%s', (num,accountName,))
        db.commit() 


    def Logout():
        LogStatus= False
        return LogStatus
    
    #edits payment info from specified account
    def EditPaymentMethod(payment):
        newPayment= str(input("enter new  payment: "))
        coursor.execute('UPDATE account SET payment = %s WHERE payment=%s', (newPayment,payment))
        db.commit()

    #edits shipping address from specifed account
    def EditShippingAddress(address):
        
        newAdd= str(input("enter new shipping address: "))
        coursor.execute('UPDATE account SET address = %s WHERE address=%s', (newAdd,address))
        db.commit()
    
    #displays account info from email inputed
    def ViewAccountInformation():

        userEmail= str(input("enter email: "))
        coursor.execute('SELECT * FROM account WHERE email=%s', (userEmail,))
        info= coursor.fetchone()
        nam,pas,em,pay,add,orderh=info
        #displays all the account information
        print("Name:",nam, "Password:", pas,"Email:",em, "Payment:",pay,"Address:",add,"Order History:",orderh)

#Inventory class
class Inventory:
    #displays a book with the price and ISBN num
    def displayBooks():
        coursor.execute("SELECT * FROM Inventory")
        table= coursor.fetchall()
        print("\nTitle:  ISBN Number: Price:  Stock\n")
        for i in table:
            print(i)
            print("\n")


        #asks if you want to add anything to cart
        ans= str(input("would you like to add anything to the shopping cart (yes or no): "))
        
        #if yes then adds book to cart with the title inputed
        if ans== "yes":

            title= str(input("what is the title?: "))
            coursor.execute('INSERT INTO methodsgroupproj.shoppingcart (title,isbn,price) SELECT Title,Isbn,Price FROM Inventory WHERE Title= %s',(title,))
            print("\nsuccessfully added!")
            db.commit()
            

            
        #if no or fails goes back to start
        else:
            print("please try again")
            loggedin=True
        
#Shopping Cart class
class shoppingCart:
    #searches for and adds book to cart that was inputed
    def additems():
        #item= int(input())
        coursor.execute(('INSERT INTO methodsgroupproj.shoppingcart (title,price,isbn) SELECT Title,Price,Isbn FROM Inventory WHERE isbn= %s',(item,)))
        db.commit()
    
    #displays items in your cart
    def displayCart():

        coursor.execute("Select * FROM shoppingcart")
        res= coursor.fetchall()
        print("shopping cart \n")
        for i in res:
            print(i, "\n")
       
    #deletes book inputed from your cart
    def deleteItem():
        item= str(input("whats the item you want to delete (title): "))
        coursor.execute("DELETE FROM shoppingcart WHERE title=%s", (item,))            
        db.commit()

        return True
    
    #searches for everything in your cart, checks you out, then clears your cart
    def checkingOut():

        coursor.execute("SELECT * FROM shoppingcart")
        table=coursor.fetchall()
        currorder=0
        useremail= str(input("please enter your email: "))
        for i in table:
            
            title,isbn,price= i
            coursor.execute("SELECT * FROM Inventory WhERE Title=%s",(title,))
            currstock=coursor.fetchone()
            name,isbnnum,price,stock= currstock
            stock-=1
            coursor.execute("UPDATE Inventory SET Stock=%s WHERE Title=%s ",(stock,title,))
            db.commit()
            coursor.execute("UPDATE account SET orderHistory=%s WHERE email=%s ",(currorder+1,useremail,))
            db.commit()
        coursor.execute("DELETE FROM shoppingcart")
        db.commit()
   
#deletes shopping cart
    def deleteCart():
         coursor.execute("DELETE FROM shoppingcart")
         db.commit()
#Review class
class Review:
    #Gives you the reviews/ratings for the book selected
    def viewReviews():
        coursor.execute("SELECT * FROM Reviews")
        reviews=coursor.fetchall()
        print("\n")
        print("Aurthor, Title, Star Rating, Date:")
        print("\n")
        for i in reviews:
            
            print(i, "\n")

    #enter your name and give a book a review and rating
    def addReview():
        name=str(input("enter your name: "))
        bookTitle= str(input("enter the title of book: "))
        stars= int(input("rating? (0-5 star): "))
        date=str(input("enter the date: "))
        #adds the review given
        coursor.execute("INSERT INTO methodsgroupproj.Reviews (name,bookTitle,stars,date) VALUES (%s,%s,%s,%s)",(name,bookTitle,stars,date,))
        db.commit()
    
    #deletes a review that was given
    def deleteReview():
        name=str(input("enter your name: "))
        coursor.execute("DELETE FROM Reviews WHERE name=%s",(name,))
        db.commit()




   

# beginning main


loggedin= False
#welcomes you to store and ask what you want to do
while(True):
    while(loggedin==False):
        print("\nwelcome to the bookstore\n")
        print("what would you like to do (1,2,3)\n")
       
        # welcome menu 
        answer= int(input(" 1. Login\n 2. Create an Account.\n 3. Exit Program\n"))
        #if 1 then login with email and password
        if answer== 1:
            email= str(input("enter your email: "))
            password= str(input("enter your password: "))

            loggingIn= Account.Login(email,password)
            
            #if login is successful
            if loggingIn== True:
                print("successful login ")
                loggedin=True
            
            else:
                print("\ndid not log in. please try again.\n")
            
                loggedin==False
        #if 2 then enter need account info and creates an account
        elif answer== 2:
            print("\ncreating an account\n")

            fullname= str(input("please enter your full name: "))
            password= str(input("please enter your a password: "))
            email= str(input("please enter your email: "))
            payment= str(input("please enter your payment info: "))
            address= str(input("please enter your address: "))
            
            #creates account with info
            account= Account.CreateAccount(fullname,password,email, payment, address)
            
            #for account creation success
            if account== True:
                print("\nseccssfully created an account")
                loggingIn=True
                loggingIn==True
                loggedin==True
                loggedin=True

            elif account==False:
                print("something went wrong")                
        
        #if 3 then exits
        elif answer==3:
            print("goodbye!")
            sys.exit(1)
        
        #anything else then try another input
        else:
            print("please try again. \n")
            loggedin=False
            

    #if logged in then presents this menu
    while(loggedin==True):
        #logged in menu
        print("\n 1. View Shopping Cart\n 2. Account Info\n 3. View Items \n 4. Reviews\n 5. Exit\n")
        
        choice= int(input("please enter a choice: "))
        #if 1 then go to and view your cart
        if choice== 1:

            shoppingCart.displayCart()
            ans= str(input("would you like to remove anything from the cart? (yes/no): "))
            #if yes then deletes selected item
            if ans == "yes":
                re=shoppingCart.deleteItem()
                if re==True:
                    print("successfully deleted")
                else:
                    print("title not found")
            
            #if no then asks if you wnat to checkout
            elif ans=="no":
                 ans2= str(input("\ndo you want to checkout? (yes/no): \n"))
                 if ans2=="no":
                    loggingIn==True
                 elif ans2=="yes":
                    shoppingCart.checkingOut()
                    print("\nSuccessfully checked out. Please come back again!\n")
                    
                    loggingIn==True
                 else:
                     print("please try again. ")
                     loggingIn=True
            else:
                print("\nplease try again.\n")
                loggedin=True
               
                


                    
        #if 2 then displays account menu
        elif choice== 2:
            print("\n Account Information")
            print("\n1. Show account Info")
            print("\n2. Update Shipping Info")
            print("\n3. Update Payment Info")
            print("\n4. Delete Account")
            print("\n5. View order history")
            print("\n\nEnter Choice:")
            choice1=int(input())
            
            #if 1 then views your account info
            if(choice1==1):
                Account.ViewAccountInformation()
            #if 2 then updates shipping info
            elif(choice1==2):
           
                
                addy= str(input("enter your current address: "))
                Account.EditShippingAddress(addy)
            #if 3 then updates payment info
            elif(choice1==3):
                currpayment= str(input("enter current payment number: "))
                Account.EditPaymentMethod(currpayment)
            #if 4 deletes account
            elif(choice1==4):
                Account.DeleteAccount()
                print("\naccount deleted! \n")
                
                loggedin=False
                
                
                
            #if 5 then views order history    
            elif (choice1==5):                
                Account.orderHistory()
            else:
                 print("please try again. ")
                 loggedin=True
        
        #if 3 then displays books    
        elif choice==3:
            Inventory.displayBooks()
        
        #if 4 then review menu displays
        elif choice==4:
            reviewChoice= int(input("\nWelcome to the review page. \n Do  you want to\n 1. View Current Reviews\n 2. Add an Review\n 3. Delete your Review\n 4. Go back to Menu\n"))
            if reviewChoice==1:
                Review.viewReviews()
            elif reviewChoice==2:
                Review.addReview()
            elif reviewChoice==3:
                Review.deleteReview()
            elif reviewChoice==4:
                loggedin=True
            else:
                print("please try again. ")
                loggedin=True
        #if 5 then exits     
        elif choice==5:
            sys.exit()
        else:
            print("please try again. ")
            loggedin=True
            





try:
    db= mysql.connector.connect(
        host= "localhost",
        user= "root",
        password= "",
        database= "methodsgroupproj"
    )
    print("successful conncection!")
#if connection fails then exits
except:
    print("failed connection.")
    sys.exit()

print("made it here")
coursor= db.cursor()

#Account class
class Account:
    
    #creates an account and adds the account info inputed
    def CreateAccount(fullname, password, email, payment, address):
        coursor.execute("INSERT INTO account (fullname, password, email, payment, address, orderHistory) VALUES (%s,%s,%s,%s,%s,%s)", (fullname, password, email, payment, address,0))
        db.commit()
        print(coursor.rowcount, "inserted items")
        return True
    
    #login by inputing an accurate email and password
    def Login(email,password):
        
        coursor.execute('SELECT * FROM account WHERE email = %s AND password = %s', (email, password,))
        
        currentAcc= coursor.fetchone()
    

        if currentAcc:
          
            return True
        else:
            return False
    
    #deletes an account with the eamil inputed
    def DeleteAccount():
        curem=str(input("please enter your email: "))
        
        coursor.execute("DELETE FROM shoppingcart")
        db.commit()


        coursor.execute('DELETE FROM account WHERE email = %s',(curem,))
        

        db.commit()
    
    #displays order history from the account email inputed
    def orderHistory():
        userEmail= str(input("enter email: "))
        
        coursor.execute('SELECT orderHistory FROM account WHERE email=%s', (userEmail,))
        ordernum= coursor.fetchone()
        print(ordernum)
        
        
    #chooses account from email inputed then allows you to update order history
    def EditOrderHistory():
        accountName=str(input("enter the email: "))
        coursor.execute('SELECT orderHistory FROM account WHERE email=%s', (accountName,))
        num= coursor.fetchone()
        num +=1
        coursor.execute('UPDATE account SET orderHistory = %s WHERE email=%s', (num,accountName,))
        db.commit()  #added??


    def Logout():
        LogStatus= False
        return LogStatus
    
    #edits payment info from specified account
    def EditPaymentMethod(payment):
        newPayment= str(input("enter new  payment: "))
        coursor.execute('UPDATE account SET payment = %s WHERE payment=%s', (newPayment,payment))
        db.commit()

    #edits shipping address from specifed account
    def EditShippingAddress(address):
        
        newAdd= str(input("enter new shipping address: "))
        coursor.execute('UPDATE account SET address = %s WHERE address=%s', (newAdd,address))
        db.commit()
    
    #displays account info from email inputed
    def ViewAccountInformation():

        userEmail= str(input("enter email: "))
        coursor.execute('SELECT * FROM account WHERE email=%s', (userEmail,))
        info= coursor.fetchone()
        nam,pas,em,pay,add,orderh=info
        #displays all the account information
        print("Name:",nam, "Password:", pas,"Email:",em, "Payment:",pay,"Address:",add,"Order History:",orderh)

#Inventory class
class Inventory:
    #displays a book with the price and ISBN num
    def displayBooks():
        coursor.execute("SELECT * FROM Inventory")
        table= coursor.fetchall()
        print("\nTitle:  ISBN Number: Price:  Stock\n")
        for i in table:
            print(i)
            print("\n")


        #asks if you want to add anything to cart
        ans= str(input("would you like to add anything to the shopping cart (yes or no): "))
        
        #if yes then adds book to cart with the title inputed
        if ans== "yes":

            title= str(input("what is the title?"))
            coursor.execute('INSERT INTO methodsgroupproj.shoppingcart (title,isbn,price) SELECT Title,Isbn,Price FROM Inventory WHERE Title= %s',(title,))
           
            db.commit()
        #if no or fails goes back to start
        else:
            print("please try again")
            loggedin=True
        
#Shopping Cart class
class shoppingCart:
    #searches for and adds book to cart that was inputed
    def additems():
        #item= int(input())
        coursor.execute(('INSERT INTO methodsgroupproj.shoppingcart (title,price,isbn) SELECT Title,Price,Isbn FROM Inventory WHERE isbn= %s',(item,)))
        db.commit()
    
    #displays items in your cart
    def displayCart():

        coursor.execute("Select * FROM shoppingcart")
        res= coursor.fetchall()
        print("shopping cart ")
        for i in res:
            print(i, "\n")
       
    #deletes book inputed from your cart
    def deleteItem():
        item= str(input("whats the item you want to delete (title): "))
        coursor.execute("DELETE FROM shoppingcart WHERE title=%s", (item,))            
        db.commit()

        return True
    
    #searches for everything in your cart, checks you out, then clears your cart
    def checkingOut():

        coursor.execute("SELECT * FROM shoppingcart")
        table=coursor.fetchall()
        currorder=0
        useremail= str(input("please enter your email: "))
        for i in table:
            
            title,isbn,price= i
            coursor.execute("SELECT * FROM Inventory WhERE Title=%s",(title,))
            currstock=coursor.fetchone()
            name,isbnnum,price,stock= currstock
            stock-=1
            coursor.execute("UPDATE Inventory SET Stock=%s WHERE Title=%s ",(stock,title,))
            db.commit()
            coursor.execute("UPDATE account SET orderHistory=%s WHERE email=%s ",(currorder+1,useremail,))
            db.commit()
        coursor.execute("DELETE FROM shoppingcart")
        db.commit()
   
#deletes shopping cart
    def deleteCart():
         coursor.execute("DELETE FROM shoppingcart")
         db.commit()
#Review class
class Review:
    #Gives you the reviews/ratings for the book selected
    def viewReviews():
        coursor.execute("SELECT * FROM Reviews")
        reviews=coursor.fetchall()
        print("\n")
        print("Aurthor, Title, Star Rating, Date:")
        print("\n")
        for i in reviews:
            
            print(i, "\n")

    #enter your name and give a book a review and rating
    def addReview():
        name=str(input("enter your name: "))
        bookTitle= str(input("enter the title of book: "))
        stars= int(input("rating? (0-5 star): "))
        date=str(input("enter the date: "))
        #adds the review given
        coursor.execute("INSERT INTO methodsgroupproj.Reviews (name,bookTitle,stars,date) VALUES (%s,%s,%s,%s)",(name,bookTitle,stars,date,))
        db.commit()
    
    #deletes a review that was given
    def deleteReview():
        name=str(input("enter your name: "))
        coursor.execute("DELETE FROM Reviews WHERE name=%s",(name,))
        db.commit()




   

# beginning main


loggedin= False
#welcomes you to store and ask what you want to do
while(True):
    while(loggedin==False):
        print("welcome to the bookstore\n")
        print("what would you like to do (1,2,3)\n")
       
        # welcome menu 
        answer= int(input("1. Login\n 2. Create an Account.\n 3. Exit Program\n"))
        #if 1 then login with email and password
        if answer== 1:
            email= str(input("enter your email: "))
            password= str(input("enter your password: "))

            loggingIn= Account.Login(email,password)
            
            #if login is successful
            if loggingIn== True:
                print("successful login ")
                loggedin=True
            
            else:
                print("\ndid not log in. please try again.\n")
            
                loggedin==False
        #if 2 then enter need account info and creates an account
        elif answer== 2:
            print("\ncreating an account\n")

            fullname= str(input("please enter your full name: "))
            password= str(input("please enter your a password: "))
            email= str(input("please enter your email: "))
            payment= str(input("please enter your payment info: "))
            address= str(input("please enter your address: "))
            
            #creates account with info
            account= Account.CreateAccount(fullname,password,email, payment, address)
            
            #for account creation success
            if account== True:
                print("\nseccssfully created an account")
                loggingIn=True
                loggingIn==True
                loggedin==True
                loggedin=True

            elif account==False:
                print("something went wrong")                
        
        #if 3 then exits
        elif answer==3:
            print("goodbye!")
            sys.exit(1)
        
        #anything else then try another input
        else:
            print("please try again. \n")
            loggedin=False
            

    #if logged in then presents this menu
    while(loggedin==True):
        #logged in menu
        print("\n1. View Shopping Cart\n 2. Account Info\n 3. View Items \n4. Reviews\n 5. Exit\n")
        
        choice= int(input("please enter a choice: "))
        #if 1 then go to and view your cart
        if choice== 1:

            shoppingCart.displayCart()
            ans= str(input("would you like to remove anything from the cart? (yes/no): "))
            #if yes then deletes selected item
            if ans == "yes":
                re=shoppingCart.deleteItem()
                if re==True:
                    print("successfully deleted")
                else:
                    print("title not found")
            
            #if no then asks if you wnat to checkout
            elif ans=="no":
                 ans2= str(input("do you want to checkout? (yes/no): "))
                 if ans2=="no":
                    loggingIn==True
                 elif ans2=="yes":
                    shoppingCart.checkingOut()
                    
                    loggingIn==True
                 else:
                     print("please try again. ")
                     loggingIn=True
            else:
                print("\nplease try again.\n")
                loggedin=True
               
                


                    
        #if 2 then displays account menu
        elif choice== 2:
            print("\n Account Information")
            print("\n1. Show account Info")
            print("\n2. Update Shipping Info")
            print("\n3. Update Payment Info")
            print("\n4. Delete Account")
            print("\n5. View order history")
            print("\n\nEnter Choice:")
            choice1=int(input())
            
            #if 1 then views your account info
            if(choice1==1):
                Account.ViewAccountInformation()
            #if 2 then updates shipping info
            elif(choice1==2):
           
                
                addy= str(input("enter your current address: "))
                Account.EditShippingAddress(addy)
            #if 3 then updates payment info
            elif(choice1==3):
                currpayment= str(input("enter current payment number: "))
                Account.EditPaymentMethod(currpayment)
            #if 4 deletes account
            elif(choice1==4):
                Account.DeleteAccount()
                print("\naccount deleted! \n")
                
                loggedin=False
                
                
                
            #if 5 then views order history    
            elif (choice1==5):                
                Account.orderHistory()
            else:
                 print("please try again. ")
                 loggedin=True
        
        #if 3 then displays books    
        elif choice==3:
            Inventory.displayBooks()
        
        #if 4 then review menu displays
        elif choice==4:
            reviewChoice= int(input("Welcome to the review page. \n Do  you want to\n 1. View Current Reviews\n 2. Add an Review\n 3. Delete your Review\n 4. Go back to Menu\n"))
            if reviewChoice==1:
                Review.viewReviews()
            elif reviewChoice==2:
                Review.addReview()
            elif reviewChoice==3:
                Review.deleteReview()
            elif reviewChoice==4:
                loggedin=True
            else:
                print("please try again. ")
                loggedin=True
        #if 5 then exits     
        elif choice==5:
            sys.exit()
        else:
            print("please try again. ")
            loggedin=True
            




