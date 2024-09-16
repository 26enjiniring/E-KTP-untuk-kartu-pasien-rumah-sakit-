
from datetime import datetime
import pyrebase
import time
from notifypy import Notify



firebaseConfig = {
  'apiKey': "AIzaSyDGLjKQTEmZPrjCtsw1sbCiK3kM1WPL9ys",
  'authDomain': "rfid-e94ef.firebaseapp.com",
  'databaseURL': "https://rfid-e94ef-default-rtdb.firebaseio.com",
  'projectId': "rfid-e94ef",
  'storageBucket': "rfid-e94ef.appspot.com",
  'messagingSenderId': "476015126382",
  'appId': "1:476015126382:web:047e7d0c728c253361037f",
  "measurementId": "G-EFNSV2E7BS"
}

firebase = pyrebase.initialize_app(firebaseConfig)

db = firebase.database()
db.child("Check").child("check").child("UID2").set("")
db.child("Check").child("logic").child("logic").set("")
db.child("Check").child("logic2").child("logic2").set("")

data = []
notification = Notify()

""""
while True:
    dp = db.child("Data Pasien").get()
    for Id in dp.each():
     data.append(Id.val()["UID"])
     

   

    check_uid = db.child("Check").child("check").get()
    
    for uid in check_uid.each():
     x = uid.val()
     if bool(x)== True: 
         print("\nCard detected")
         if x in data :
             print("Card Registered")
             owner = db.child("Data Pasien").order_by_child("UID").equal_to(x).get()
             for Owner in owner.each():
                 print("this card belongs to : \nname : {}\nID : {}\n\n".format(Owner.val()["Nama"],Owner.val()["UID"]))
                 db.child("Check").child("logic").child("logic").set(1)
                 now = datetime.now()
                 dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                 db.child("Data Pasien").child(Owner.val()["UID"]).child("DT").set(dt_string)
                 print("Checking at :", dt_string)
                 print("Get data from oximeter")
                 nilai = 0
                 while nilai == 0:
                     k = db.child("Check").child("logic2").get()
                     for wait in k.each():
                         if wait.val() == 1:
                             print(wait.val())
                             suhu = db.child("Check").child("Suhu").get()
                             stat = db.child("Check").child("Status").get()
                             for y in suhu.each():
                                 print(y.val())
                                 db.child("Data Pasien").child(Owner.val()["UID"]).child("SUHU").set(y.val())
                                 for z in stat.each():
                                     print(z.val())
                                     db.child("Data Pasien").child(Owner.val()["UID"]).child("STATUS").set(z.val())
                                     print("pushing data to firebase")
                                     nilai == 1
                                     db.child("Check").child("logic").child("logic").set(0)
                                     db.child("Check").child("logic2").child("logic2").set(0)
                                     db.child("Check").child("check").child("UID2").set("")
                                     break
                         else:
                             print("Get data from oximeter")  
                             print(wait.val())



         elif x not in data :
             print("card unregister")
             db.child("Check").child("logic").child("logic").set(0)
             db.child("Check").child("check").child("UID2").set("")
     else:
          print("waiting for card")
"""

def main():
    dp = db.child("Data Pasien").get()
    for Id in dp.each():
     data.append(Id.val()["UID"])
     
    check_uid = db.child("Check").child("check").get()
    
    for uid in check_uid.each():
     x = uid.val()
     if bool(x)== True: 
         print("\nCard detected")
         if x in data :
             print("Card Registered")
             owner = db.child("Data Pasien").order_by_child("UID").equal_to(x).get()
             for Owner in owner.each():
                 print("this card belongs to : \nname : {}\nID : {}\n\n".format(Owner.val()["Nama"],Owner.val()["UID"]))
                 db.child("Check").child("logic").child("logic").set(1)
                 now = datetime.now()
                 dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                 db.child("Data Pasien").child(Owner.val()["UID"]).child("DT").set(dt_string)
                 print("Checking at :", dt_string)
                 print("Get data from oximeter")
                 nilai = 0
                 while nilai == 0:
                     k = db.child("Check").child("logic2").get()
                     for wait in k.each():
                         if wait.val() == 1:
                             print(wait.val())
                             suhu = db.child("Check").child("Suhu").get()
                             stat = db.child("Check").child("Status").get()
                             for y in suhu.each():
                                 print(y.val())
                                 db.child("Data Pasien").child(Owner.val()["UID"]).child("SUHU").set(y.val())
                                 for z in stat.each():
                                     print(z.val())
                                     db.child("Data Pasien").child(Owner.val()["UID"]).child("STATUS").set(z.val())
                                     print("pushing data to firebase")
                                     nilai = 1
                                     text = "Pasien      : {}\nChecking at : {}".format(Owner.val()["Nama"],dt_string)
                                     notification.title = "INGFO"
                                     notification.message = text
                                     notification.send()
                                     db.child("Check").child("logic").child("logic").set(0)
                                     db.child("Check").child("logic2").child("logic2").set(0)
                                     db.child("Check").child("check").child("UID2").set("")
                                     main()
                                     print("done")
                         else:
                             print("Get data from Termometer")  
                             print(wait.val())



         elif x not in data :
             print("card unregister")
             db.child("Check").child("logic").child("logic").set(0)
             db.child("Check").child("check").child("UID2").set("")
     else:
          print("waiting for card")

while True :
    main()
