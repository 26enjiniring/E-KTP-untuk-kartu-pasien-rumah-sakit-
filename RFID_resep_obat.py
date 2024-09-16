

import pyrebase
import tkinter as tk
from tkinter.constants import END
from tkinter import CENTER, LEFT, W, messagebox
from datetime import datetime
from ttkwidgets.autocomplete import *
from database import *
from tkinter import filedialog as fd
import time

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
x = ""
master = tk.Tk()
master.geometry("600x200")
master.title("Resep Obat")
db.child("Farmasi").child("send").child("UID").set("")

def done():
  now = datetime.now()
  dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
  data1 = e3.get()
  data2 = e2.get()
  data3 = dt_string
  data4 = e4.get()
  data5 = e5.get()
  data6 = clicked1.get()
  data7 = e7.get()
  data8 = clicked2.get()
  data9 = e9.get()
  data10 = clicked3.get()
  if bool(e1.get()) & bool(e2.get()) & bool(data1) & bool(data2) & bool(data3) & bool(data4) & bool(data5) & bool(data6) & bool(data7) & bool(data8) & bool(data9) & bool(data10)== True:
    owner = db.child("Data Pasien").order_by_child("UID").equal_to(x).get()
    for Owner in owner.each():
      text ="""
      Nama Pemeriksa : {}
      Poli Pemeriksa : {} 
      tanggal pemberian : {}
      ========================RESEP===========================

          {} {}{}
            {} {}
            @{}{}

  

      ========================================================
  
      Pro : {}
      Alamat : {}
  
      """.format(data1, data2, data3, data4, data5, data6, data7,data8,data9,data10,Owner.val()["Nama"],Owner.val()["Alamat"])
      print(text)
      db.child("Data Pasien").child(e1.get()).child("Resep").set(text)
      e1.delete(0,END)
      e2.delete(0,END)
      e3.delete(0,END)
      e4.delete(0,END)
      e5.delete(0,END)
      e7.delete(0,END)
      e9.delete(0,END)
      db.child("Farmasi").child("send").child("UID").set("")
      messagebox.showinfo("INGFO","Resep obat berhasil disimpan ke dalam database")


  else :
    messagebox.showerror("error","data tidak boleh kosong")

"""
def done():
  data3 = e3.get()
  data2 = e4.get("1.0","end-1c")
  data1 = e2.get()
  print(bool(data1))

  if bool(e1.get()) & bool(e3.get()) & bool(e2.get()) & bool(e4.get("1.0","end-1c"))== True:
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    db.child("Farmasi").child("Resep").child(e1.get()).child("Resep").set(data2)
    db.child("Farmasi").child("Resep").child(e1.get()).child("Pemeriksa").set(data1)
    db.child("Farmasi").child("Resep").child(e1.get()).child("tgl pemberian").set(dt_string)
    # db.child

  else :
    messagebox.showerror("error","data tidak boleh kosong")
    print(e2.get())
  # time.sleep(3)
  # x = db.child('test').get()
  # for i in x.each():
  #   print(i.val())
"""
  
def save():
  now = datetime.now()
  dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
  data1 = e3.get()
  data2 = e2.get()
  data3 = dt_string
  data4 = e4.get()
  data5 = e5.get()
  data6 = clicked1.get()
  data7 = e7.get()
  data8 = clicked2.get()
  data9 = e9.get()
  data10 = clicked3.get()
  if bool(e1.get()) & bool(e2.get()) & bool(data1) & bool(data2) & bool(data3) & bool(data4) & bool(data5) & bool(data6) & bool(data7) & bool(data8) & bool(data9) & bool(data10)== True:
    owner = db.child("Data Pasien").order_by_child("UID").equal_to(x).get()
    for Owner in owner.each():
      text ="""
      Nama Pemeriksa : {}
      Poli Pemeriksa : {} 
      tanggal pemberian : {}
      ========================RESEP===========================

          {} {}{}
            {} {}
            @{}{}

  

      ========================================================
  
      Pro : {}
      Alamat : {}
  
      """.format(data1, data2, data3, data4, data5, data6, data7,data8,data9,data10,Owner.val()["Nama"],Owner.val()["Alamat"])
      print(text)
      location = fd.asksaveasfilename(defaultextension=".txt")
      file = open(location,'w')
      file.write(text)
      time.sleep(5)
      for Owner in owner.each():
        print(Owner.val()["Resep"])


  else :
    messagebox.showerror("error","data tidak boleh kosong")
  
def clear():
  e1.delete(0,END)
  e2.delete(0,END)
  e3.delete(0,END)
  e4.delete(0,END)
  e5.delete(0,END)
  e7.delete(0,END)
  e9.delete(0,END)
  db.child("Farmasi").child("send").child("UID").set("")
  


def keluar():
  res = messagebox.askyesno("EXIT","anda yakin ingin keluar ?")
  if res == True :
   master.destroy()
  elif res == False :
    pass
  
def loop():
 global x
 dp = db.child("Data Pasien").get()
 for Id in dp.each():
   data.append(Id.val()["UID"])
 
 e1.delete(0, END)
 send = db.child("Farmasi").child('send').get()
 for uid in send.each():
    x = uid.val()
    if bool(x) == True:
      print(x)
      if x in data :
        print("UID :",uid.val())
        e1.insert(0, uid.val())
       
      else:
        messagebox.showerror("error","Kartu tidak terdaftar")
        db.child("Farmasi").child("send").child("UID").set("")

 e1.after(400,loop)

poli = ["POLIKLINIK UMUM","POLIKLINIK ANAK","UNIT GAWAT DARURAT","POLIKLINIK THT"]
opsi1 = ["Mg","Ml","Tablet"]
opsi2 = ["Sesudah Makan","Sebelum Makan"]
Obat = obat

clicked1 = tk.StringVar() # untuk opsi 1
clicked1.set( "Mg" )

clicked2 = tk.StringVar() # untuk opsi 2
clicked2.set( "Sebelum Makan" )

clicked3 = tk.StringVar() # untuk opsi 2
clicked3.set( "Mg" )


lt = tk.Label(master, text="INPUT RESEP OBAT", pady=10, padx=10)
f1 = tk.Frame(master)
f2 = tk.Frame(master)
f3 = tk.Frame(master)
lt.pack(anchor=CENTER)
f1.pack(anchor=W)
f2.pack(anchor=CENTER)
f3.pack(anchor=CENTER)


l1 = tk.Label(f1, text="UID :")
l2 = tk.Label(f1, text="Poli Pemeriksa :")
l3 = tk.Label(f1, text="Nama Pemeriksa :")
l4 = tk.Label(f1, text="Obat Yang Diresepkan :")
l5 = tk.Label(f1, text="Jumlah :")
l6 = tk.Label(f1, text="Dosis pemakaian :")
l7 = tk.Label(f1, text="@")


e1 = tk.Entry(f1) #UID
e2 = AutocompleteCombobox(f1, completevalues=poli) #poli
e3 = tk.Entry(f1) #Pemeriksa
e4 = AutocompleteCombobox(f1,completevalues=Obat) #nama obat
e5 = tk.Entry(f1,width=10) #jumlah
e6 = tk.OptionMenu(f1, clicked1, *opsi1) #mg/ml/tablet
e7 = tk.Entry(f1, width=20) #dosis
e8 = tk.OptionMenu(f1, clicked2, *opsi2) #sesudah/sebelum
e9 = tk.Entry(f1, width=10) #takaran
e10 = tk.OptionMenu(f1, clicked3, *opsi1) #mg/ml/tablet

l1.grid(row=0, column=0)
e1.grid(row=0, column=1)
l2.grid(row=1, column=0)
e2.grid(row=1, column=1)
l3.grid(row=2, column=0)
e3.grid(row=2, column=1)
l4.grid(row=3,column=0)
e4.grid(row=3,column=1)
l5.grid(row=3,column=2)
e5.grid(row=3,column=3)
e6.grid(row=3, column=4)
l6.grid(row=4,column=0)
e7.grid(row=4, column=1)
e8.grid(row=4, column=2)
l7.grid(row=4,column=3)
e9.grid(row=4, column=4)
e10.grid(row=4, column=5)

b1 = tk.Button(f3, text="Done", command=done)
b2 = tk.Button(f3, text="Save", command=save)
b3 = tk.Button(f3, text="Clear", command=clear)
b4 = tk.Button(f3, text="Exit", command=keluar)
b1.grid(row=0, column=0)
b2.grid(row=0, column=1)
b3.grid(row=0, column=2)
b3.grid(row=0, column=3)

loop()
master.mainloop()