
from tkinter import E, INSERT, Toplevel, font, messagebox
import tkinter
from tkinter.font import BOLD
from numpy import quantile, save
import pyrebase
import tkinter as tk
from tkinter import ttk
from tkinter.constants import CENTER, END, W
import csv
from tkinter import filedialog as fd

from soupsieve import select

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

no = 0

firebase = pyrebase.initialize_app(firebaseConfig)

db = firebase.database()

root = tk.Tk()
root.title("Data Pasien")
f1 = tk.Frame(root)
f2 = tk.Frame(root)
f3 = tk.Frame(root)

f1.pack(anchor=tk.CENTER)
f2.pack(anchor=tk.CENTER)
f3.pack(anchor=tk.CENTER)

tk.Label(f1, text="DATA PASIEN").pack(anchor=tk.CENTER, pady=5)

my_tree = ttk.Treeview(f2)
my_tree["columns"]=("Nama","Gender","TTL","Golongan Darah","SUHU","STATUS","DT")

#format columns
my_tree.column("#0", width= 50, minwidth= 25)
my_tree.column("Nama",anchor=tk.W, width= 200, minwidth= 25)
my_tree.column("Gender",anchor=CENTER, width= 100, minwidth= 25)
my_tree.column("TTL",anchor=CENTER, width= 150, minwidth= 25)
my_tree.column("Golongan Darah",anchor=CENTER, width= 100, minwidth= 25)
my_tree.column("SUHU",anchor=CENTER, width= 100, minwidth= 25)
my_tree.column("STATUS",anchor=CENTER, width= 100, minwidth= 25)
my_tree.column("DT",anchor=CENTER, width= 150, minwidth= 25)

#format heading
my_tree.heading("#0",text="No", anchor=tk.W)
my_tree.heading("Nama",text="Nama",anchor=tk.W)
my_tree.heading("Gender",text="Gender",anchor=CENTER)
my_tree.heading("TTL",text="TTL",anchor=CENTER)
my_tree.heading("Golongan Darah",text="Golongan Darah",anchor=CENTER)
my_tree.heading("SUHU",text="SUHU",anchor=CENTER)
my_tree.heading("STATUS",text="STATUS",anchor=CENTER)
my_tree.heading("DT",text="Checking at",anchor=CENTER)

dpasien = db.child("Data Pasien").get()
for pasien in dpasien.each():
  no += 1
  my_tree.insert(parent="", index="end", iid=no, text=no,values=(pasien.val()["Nama"],pasien.val()["Kelamin"],
                                                                  pasien.val()["TTL"],pasien.val()["GOL"],pasien.val()["SUHU"],pasien.val()["STATUS"],pasien.val()["DT"]))
  my_tree.pack(anchor=tk.CENTER, pady=20)

def clear():
    for record in my_tree.get_children():
        my_tree.delete(record)

def insert():
  no = 0
  clear()
  dpasien = db.child("Data Pasien").get()
  for pasien in dpasien.each():
    no += 1
    # print(pasien.val())
    my_tree.insert(parent="", index="end", iid=no, text=no,values=(pasien.val()["Nama"],pasien.val()["Kelamin"],
                                                                    pasien.val()["TTL"],pasien.val()["GOL"],pasien.val()["SUHU"],pasien.val()["STATUS"],pasien.val()["DT"]))
    my_tree.pack(anchor=tk.CENTER, pady=20)
  my_tree.after(400,insert)

def Exit():
  
  res  = messagebox.askyesno("Exit","anda yakin ingin keluar?")
  if res == True :
    root.destroy()
  elif res == False :
    pass

def hapus():
    dp = db.child("Data Pasien").get()
    data = []
    for Id in dp.each():
      data.append(Id.val()["UID"])
    for i in range(0,len(data)):
      db.child("Data Pasien").child(data[i]).child("SUHU").set("")
      db.child("Data Pasien").child(data[i]).child("STATUS").set("")
      db.child("Data Pasien").child(data[i]).child("DT").set("")
      db.child("Data Pasien").child(data[i]).child("").set("")
      db.child("Data Pasien").child(data[i]).child("DT").set("")

def Save():
  data = {}
  key = ["Nama","TTL","Kelamin","UID"]
  location = fd.asksaveasfilename(defaultextension=".csv")
  with open(location, "w", newline='') as myfile:
    csvwriter = csv.writer(myfile, delimiter="|")
    for child in my_tree.get_children():
      value = my_tree.item(child)['values']
      csvwriter.writerow(value)

def displayselected1(a):
  selectedItem = my_tree.selection()[0]
  for i in range(0,7):
    print(my_tree.item(selectedItem)['values'][i])
  
  master2 = Toplevel(root)
  # master2.geometry("600x600")

  nama = my_tree.item(selectedItem)['values'][0]
  gender = my_tree.item(selectedItem)['values'][1]
  Ttl = my_tree.item(selectedItem)['values'][2]
  Goldar = my_tree.item(selectedItem)['values'][3]
  Suhu = my_tree.item(selectedItem)['values'][4]

  f1 = tk.Frame(master2)
  f2 = tk.Frame(master2)
  f3 = tk.Frame(master2)
  f4 = tk.Frame(master2)
  f5 = tk.Frame(master2)
  f6 = tk.Frame(master2)
  f61 = tk.Frame(f6)
  f62 = tk.Frame(f6)
  f7 = tk.Frame(master2)
  
  l11 = tk.Label(f1, text="Nama          :")
  l21 = tk.Label(f2, text="Jenis Kelamin :")
  l31 = tk.Label(f3, text="TTL           :")
  l41 = tk.Label(f4, text="Golongan Darah:")
  l51 = tk.Label(f5, text="Suhu          :")
  l61 = tk.Label(f61, text="Diagnosa      :")
  l71 = tk.Label(f61, text="Tindakan      :")
 
  
  l12 = tk.Label(f1,text=nama)
  l22 = tk.Label(f2,text=gender)
  l32 = tk.Label(f3,text=Ttl)
  l42 = tk.Label(f4,text=Goldar)
  l52 = tk.Label(f5,text=Suhu)
  e62 = tk.Text(f62,height=10,width=50)
  e72 = tk.Text(f62,height=10,width=50)

  f1.pack(anchor=tk.W)
  f2.pack(anchor=tk.W)
  f3.pack(anchor=tk.W)
  f4.pack(anchor=tk.W)
  f5.pack(anchor=tk.W)
  f6.pack(anchor=tk.W)
  f61.grid(row=0,column=0)
  f62.grid(row=0,column=1)
  f7.pack(anchor=tk.W)

  l11.grid(row=0,column=0)
  l21.grid(row=0,column=0)
  l31.grid(row=0,column=0)
  l41.grid(row=0,column=0)
  l51.grid(row=0,column=0)
  l61.grid(row=0,column=0,pady=75)
  l71.grid(row=1,column=0,pady=75)

  l12.grid(row=0,column=1)
  l22.grid(row=0,column=1)
  l32.grid(row=0,column=1)
  l42.grid(row=0,column=1)
  l52.grid(row=0,column=1)
  e62.grid(row=0,column=0,pady=5)
  e72.grid(row=1,column=0,pady=5)

  def save():
    diagnosa = e62.get("1.0","end-1c")
    tindakan = e72.get("1.0","end-1c")

    x = my_tree.item(selectedItem)['values'][0]
    owner = db.child("Data Pasien").order_by_child("Nama").equal_to(x).get()
    for Owner in owner.each():
      id = Owner.val()["UID"]
      db.child("Data Pasien").child(id).child("Diagnosa").set(diagnosa)
      db.child("Data Pasien").child(id).child("Tindakan").set(tindakan)
      messagebox.showinfo("done","data berhasil disubmit")


  def close():
    master2.destroy()

  b1 = tk.Button(f7,text="Save",command=save)
  b2 = tk.Button(f7,text="Close",command=close)

  b1.grid(row=0,column=0,padx=5)
  b2.grid(row=0,column=1,padx=5)



  master2.mainloop()



def displayselected2(a):
  selectedItem = my_tree.selection()[0]
  for i in range(0,7):
    print(my_tree.item(selectedItem)['values'][i])
  
  master2 = Toplevel(root)
  # master2.geometry("600x600")


  x = my_tree.item(selectedItem)['values'][0]
  owner = db.child("Data Pasien").order_by_child("Nama").equal_to(x).get()
  for Owner in owner.each():
    diagnosa = Owner.val()["Diagnosa"]
    tindakan = Owner.val()["Tindakan"]

    nama = my_tree.item(selectedItem)['values'][0]
    gender = my_tree.item(selectedItem)['values'][1]
    Ttl = my_tree.item(selectedItem)['values'][2]
    Goldar = my_tree.item(selectedItem)['values'][3]
    Suhu = my_tree.item(selectedItem)['values'][4]

    f1 = tk.Frame(master2)
    f2 = tk.Frame(master2)
    f3 = tk.Frame(master2)
    f4 = tk.Frame(master2)
    f5 = tk.Frame(master2)
    f6 = tk.Frame(master2)
    f61 = tk.Frame(f6)
    f62 = tk.Frame(f6)
    f7 = tk.Frame(master2)
  
    l11 = tk.Label(f1, text="Nama          :")
    l21 = tk.Label(f2, text="Jenis Kelamin :")
    l31 = tk.Label(f3, text="TTL           :")
    l41 = tk.Label(f4, text="Golongan Darah:")
    l51 = tk.Label(f5, text="Suhu          :")
    l61 = tk.Label(f61, text="Diagnosa      :")
    l71 = tk.Label(f61, text="Tindakan      :")
 
  
    l12 = tk.Label(f1,text=nama)
    l22 = tk.Label(f2,text=gender)
    l32 = tk.Label(f3,text=Ttl)
    l42 = tk.Label(f4,text=Goldar)
    l52 = tk.Label(f5,text=Suhu)
    e62 = tk.Text(f62,height=10,width=50)
    e72 = tk.Text(f62,height=10,width=50)

    e62.insert(INSERT,diagnosa)
    e72.insert(INSERT,tindakan)

  f1.pack(anchor=tk.W)
  f2.pack(anchor=tk.W)
  f3.pack(anchor=tk.W)
  f4.pack(anchor=tk.W)
  f5.pack(anchor=tk.W)
  f6.pack(anchor=tk.W)
  f7.pack(anchor=tk.W)
  f61.grid(row=0,column=0)
  f62.grid(row=0,column=1)

  l11.grid(row=0,column=0)
  l21.grid(row=0,column=0)
  l31.grid(row=0,column=0)
  l41.grid(row=0,column=0)
  l51.grid(row=0,column=0)
  l61.grid(row=0,column=0,pady=75)
  l71.grid(row=1,column=0,pady=75)

  l12.grid(row=0,column=1)
  l22.grid(row=0,column=1)
  l32.grid(row=0,column=1)
  l42.grid(row=0,column=1)
  l52.grid(row=0,column=1)
  e62.grid(row=0,column=0,pady=5)
  e72.grid(row=1,column=0,pady=5)

  def close():
    master2.destroy()

  b1 = tk.Button(f7,text="Close",command=close)
  b1.grid(row=0,column=0)
  master2.mainloop()


def write():
  my_tree.bind("<<TreeviewSelect>>",displayselected1)

def show():
  my_tree.bind("<<TreeviewSelect>>",displayselected2)



  
    
  

b1 = tk.Button(f3, text="Quit", command=Exit)
b2 = tk.Button(f3, text="Save", command=Save)
b3 = tk.Button(f3,text="Write", command=write)
b4 = tk.Button(f3,text="Show", command=show)

b1.grid(row=0, column=0, pady=5, padx=5)
b2.grid(row=0, column=1, pady=5, padx=5)
b3.grid(row=0, column=2, pady=5, padx=5)
b4.grid(row=0, column=3, pady=5, padx=5)

insert()
root.mainloop()
