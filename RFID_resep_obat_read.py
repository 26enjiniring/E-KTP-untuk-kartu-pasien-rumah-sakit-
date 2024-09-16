from doctest import master
from operator import truediv
from pickle import FALSE
import pyrebase
import tkinter as tk
from tkinter.constants import END
from tkinter import CENTER, messagebox
import time
from datetime import datetime
from tkinter import filedialog as fd

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
data = []

master = tk.Tk()
master.title("Resep Obat")
db.child("Farmasi").child("read").child("UID2").set("")
def done():
  
  reply = messagebox.askyesno("Ayyoo?","Apakah anda ingin menyimpan resep ini")
  if reply == True:
    e1.delete(0,END)
    db.child("Farmasi").child("read").child("UID2").set("")
    e2.config(text="Resep obat akan ditampilkan disini")
    messagebox.showinfo("INGFO","Terimakasih")
  elif reply == False:
    reply2 = messagebox.askyesno("r u sure ?","Anda yakin ingin menghapus resep obat ?")
    if reply2 == True:
      if bool(e1.get()) == True:
        print(e1.get())
        db.child("Data Pasien").child(e1.get()).child("Resep").set("")
        db.child("Farmasi").child("read").child("UID2").set("")
        e1.delete(0,END)  
        e2.config(text="Resep obat akan ditampilkan disini")
        messagebox.showinfo("INGFO","Resep obat berhasil dihapus")
      else:
        messagebox.showerror("ERROR","ERROR")
    else:
      e1.delete(0,END)
      db.child("Farmasi").child("read").child("UID2").set("")
      e2.config(text="Resep obat akan ditampilkan disini")




  

  

def keluar():
  res = messagebox.askyesno("EXIT","anda yakin ingin keluar ?")
  if res == True :
   master.destroy()
  elif res == False :
    pass
  
def loop():
 dp = db.child("Data Pasien").get()
 for Id in dp.each():
   data.append(Id.val()["UID"])
 
 e1.delete(0, END)
 send = db.child("Farmasi").child("read").get()
 for uid in send.each():
    x = uid.val()
    if bool(x) == True:
      print(x)
      if x in data :
        print("UID :",uid.val())
        e1.insert(0, uid.val())
        owner = db.child("Data Pasien").order_by_child("UID").equal_to(x).get()
        for Owner in owner.each():
          if bool(Owner.val()["Resep"]) == False :
            messagebox.showwarning("","TIDAK ADA RESEP OBAT")
            db.child("Farmasi").child("read").child("UID2").set("")
          e2.config(text=Owner.val()["Resep"])

       
      else:
        messagebox.showerror("error","Kartu tidak terdaftar")
        db.child("Farmasi").child("read").child("UID2").set("")

 e1.after(400,loop)

def save():
  y =  e1.get()
  if bool(y) == True:
   owner = db.child("Data Pasien").order_by_child("UID").equal_to(y).get()
   for Owner in owner.each():
      text = Owner.val()["Resep"]
      location = fd.asksaveasfilename(defaultextension=".txt")
      file = open(location,'w')
      file.write(text)

  else : 
    messagebox.showwarning("","TIDAK ADA RESEP OBAT")




lt = tk.Label(master, text="BACA RESEP OBAT", pady=10, padx=10)
f1 = tk.Frame(master)
f2 = tk.Frame(master)
f3 = tk.Frame(master)
lt.pack(anchor=CENTER)
f1.pack(anchor=CENTER)
f2.pack(anchor=CENTER)
f3.pack(anchor=CENTER)

l1 = tk.Label(f1, text="UID :")
e1 = tk.Entry(f1)
l1.grid(row=0, column=0)
e1.grid(row=0, column=1)



l1 = tk.Label(f1, text="UID :")
e1 = tk.Entry(f1)
l1.grid(row=0, column=0)
e1.grid(row=0, column=1)


l2 = tk.Label(f2, text="RESEP", pady=10, padx=10)
e2 = tk.Label(f2,text="Resep obat akan ditampilkan disini",width=50, height=20)
l2.pack(anchor=CENTER)
e2.pack(anchor=CENTER)

b1 = tk.Button(f3, text="done", command=done)
b2 = tk.Button(f3, text="save", command=save)
b3 = tk.Button(f3, text="exit", command=keluar)
b1.grid(row=0, column=0)
b2.grid(row=0, column=1)
b3.grid(row=0, column=2)

loop()

master.mainloop()