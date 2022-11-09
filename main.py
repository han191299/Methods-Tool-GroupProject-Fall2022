import mysql.connector
import sys

try:
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="methods"
    )

    print("Successful connection.")

except:
    print("Failed connection.")
    sys.exit()



coursor = connection.cursor()

class Account:
    
    def CreateAccount(fullname, password, email, payment, address, orderHistory):
        coursor.execute("INSERT INTO account (fullname, password, email, payment, address, orderHistory) VALUES (%s,%s,%s,%s,%s,%s)", (fullname, password, email, payment, address,0))
        db.commit

        print(coursor.rowcount, "inserted items")

    def Login(email,password):
        pass
        
    def DeleteAccount(email):

        coursor.execute('DELETE FROM account WHERE email = %s',(email,))
        db.commit

    def EditAccount():
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
    def Show_laptops_inventory():
        coursor.execute('SELECT * FROM Inventory WHERE Name = 1')
        result = coursor.fetchall()
  
        for row in result:
          print(row,"\n")
        productname=str(input("\nwhich laptop would you like to add to your cart? (Y/N)"))

        coursor.execute('INSERT INTO methodsnew.ShoppingCart (Itemid,Cost,Name) SELECT Itemid,Cost,Stock FROM methodsnew.Inventory WHERE Name= %s',(productname,))


    
    def editstock():
        product=int(input("\n Which product would you like to edit the stock of?:"))
        stockamount=int(input("\n How many of these products are in stock?"))
        coursor.execute('UPDATE Inventory SET Stock = %s WHERE Itemid=%s', (stockamount,product,))
        db.commit() # # we commit(save) the records to the table

        for row in result:
          print(row,"\n")
        productname=str(input("\nwhich laptop would you like to add to your cart? (Y/N)"))

        coursor.execute('INSERT INTO methodsnew.ShoppingCart (Itemid,Cost,Name) SELECT Itemid,Cost,Stock FROM methodsnew.Inventory WHERE Itemid= %s',(productname,))


