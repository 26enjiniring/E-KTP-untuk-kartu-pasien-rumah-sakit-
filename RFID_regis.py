import pyrebase
import tkinter as tk
from tkinter.constants import END
from tkinter import messagebox
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
db.child("Register").child("regis").child("UID").set("")

data = {"SUHU":"","STATUS":"","DT":"","Resep":"","Diagnosa":"","Tindakan":""}
data2={}

def clear():
    e4.deselect()
    e5.deselect()
    db.child("Register").child("regis").child("UID").set("")


def done():
    print(  bool(e1.get()) , bool(e2.get()) , bool(Radio.get()) , bool(e3.get()) , bool(clicked.get()), bool(e6.get()))
    if bool(e1.get()) & bool(e2.get()) & bool(clicked.get()) & bool(e3.get()) & bool(Radio.get())  == False :
      messagebox.showerror("Error","Data tidak boleh kosong") 
       
    elif  bool(e1.get()) & bool(e2.get()) & bool(Radio.get()) & bool(e3.get()) & bool(clicked.get()) & bool(e6.get()) == True:
        key = ["Nama","TTL","Kelamin","UID","GOL","Alamat"]
        value = [e1.get(),e2.get(),Radio.get(),e3.get(),clicked.get(),e6.get()]
        for k,v in zip(key,value):
         data[k]=v
         data2[k]=v
        db.child("Data Pasien").child(value[3]).set(data)
        # db.child("Farmasi").child("Resep").child(value[3]).set(data2)
        print("SUCCESSFULLY ADDED")
        e1.delete(0, END)
        e2.delete(0, END)
        e6.delete(0,END)
        clicked.set( "" )
        db.child("Register").child("UID").set("")
        clear()
        messagebox.showinfo("done","Kartu berhasil terdaftar")  


master = tk.Tk()
master.title("Input Data")

options = [
    "A",
    "B",
    "AB",
    "O"
]
  

clicked = tk.StringVar()
clicked.set( "" )

f1 = tk.Frame(master)
f2 = tk.Frame(master)
f3 = tk.Frame(master)
f4 = tk.Frame(master)
f5 = tk.Frame(master)
f6 = tk.Frame(master)
f7 = tk.Frame(master)

f1.pack(anchor=tk.CENTER)
f2.pack(anchor=tk.CENTER)
f3.pack(anchor=tk.CENTER)
f4.pack(anchor=tk.CENTER)
f5.pack(anchor=tk.CENTER)
f6.pack(anchor=tk.CENTER)
f7.pack(anchor=tk.CENTER)


tk.Label(f1, 
         text="Nama",font=('bold', 16)).grid(row=0,column=0)
tk.Label(f2, 
         text="TTL",font=('bold', 16)).grid(row=0,column=0)
tk.Label(f3, 
         text="Gol.Darah",font=('bold', 16)).grid(row=0,column=0)
tk.Label(f4, 
         text="Kelamin",font=('bold', 16)).grid(row=0,column=0)
tk.Label(f5, 
         text="Alamat",font=('bold', 16)).grid(row=0,column=0)
tk.Label(f6, 
         text="UID",font=('bold', 16)).grid(row=0,column=0)

e1 = tk.Entry(f1,font=('bold', 16))
e2 = tk.Entry(f2,font=('bold', 16))
drop = tk.OptionMenu( f3 , clicked , *options )
e3 = tk.Entry(f6,font=('bold', 16))
Radio = tk.StringVar()
e4 = tk.Radiobutton(f4, text="Laki-Laki", value="Laki-Laki",font=('bold', 16),variable=Radio)
e5 = tk.Radiobutton(f4, text="Perempuan", value="Perempuan",font=('bold', 16),variable=Radio)
e6 = tk.Entry(f5,font=('bold', 16))

def loop():
 e3.delete(0, END)
 regis = db.child("Register").child('regis').get()
 for uid in regis.each():
    print("UID :",uid.val())
    e3.insert(0, uid.val())
 e3.after(400,loop)

def Exit():
  res  = messagebox.askyesno("Exit","anda yakin ingin keluar?")
  if res == True :
   master.destroy()
  elif res == False :
    pass



e1.grid(row=0,column=1)
e2.grid(row=0, column=1)
drop.grid(row=0, column=1)
e3.grid(row=0,column=1)
e4.grid(row=0,column=1)
e5.grid(row=0,column=2)
e6.grid(row=0,column=1)

tk.Button(f6, 
          text='Quit', 
          command=Exit).grid(row=5, 
                                    column=0, 
                                    sticky=tk.W, 
                                    pady=4)
tk.Button(f6, 
          text='Done', command=done).grid(row=5, 
                                                       column=1, 
                                                       sticky=tk.W, 
                                                       pady=4)

e4.deselect()
e5.deselect()
loop()
tk.mainloop()