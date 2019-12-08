from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import Menubutton

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

funktsioonid=[]

def fun1():
    funktsioonid.append("f1")
    menüü.menu.entryconfig(1, label="")
    menüü2.menu.entryconfig(1, label="")
    menüü3.menu.entryconfig(1, label="")
def fun2():
    funktsioonid.append("f2")
    menüü.menu.entryconfig(2, label="")
    menüü2.menu.entryconfig(2, label="")
    menüü3.menu.entryconfig(2, label="")
def fun3():
    funktsioonid.append("f3")
    menüü.menu.entryconfig(3, label="")
    menüü2.menu.entryconfig(3, label="")
    menüü3.menu.entryconfig(3, label="")
def fun4():
    funktsioonid.append("f4")
    menüü.menu.entryconfig(4, label="")
    menüü2.menu.entryconfig(4, label="")
    menüü3.menu.entryconfig(4, label="")
def fun5():
    funktsioonid.append("f5")
    menüü.menu.entryconfig(5, label="")
    menüü2.menu.entryconfig(5, label="")
    menüü3.menu.entryconfig(5, label="")
    
def menüülist(menüü):
    menüü.menu.add_command(label="Paneb helitugevuse maksimumile",command=fun1, activebackground="gray30", activeforeground="snow2")
    menüü.menu.add_command(label="Paneb helitugevuse miinimumile",command=fun2, activebackground="gray30", activeforeground="snow2")
    menüü.menu.add_command(label="Funktsioon 3",command=fun3, activebackground="gray30", activeforeground="snow2")
    menüü.menu.add_command(label="Funktsioon 4",command=fun4, activebackground="gray30", activeforeground="snow2")
    menüü.menu.add_command(label="Funktsioon 5",command=fun5, activebackground="gray30", activeforeground="snow2")

raam = Tk()
raam.title("Kasutajaliides")

pealkiri=ttk.Label(raam, text="Palun vali igale liigutusele vastav funktsioon (esimene valik loeb): ")
pealkiri.grid(column=1, row=0, padx=10, pady=10, sticky=(N,S,W,E))

silt1 = ttk.Label(raam, text="Rusikas")
silt1.grid(column=1, row=1, padx=10, pady=10, sticky=(E))
silt2 = ttk.Label(raam, text="Kõik sõrmed püsti")
silt2.grid(column=1, row=2, padx=10, pady=10, sticky=(E))
silt3 = ttk.Label(raam, text="Üks sõrm püsti")
silt3.grid(column=1, row=3, padx=10, pady=10, sticky=(E))

menüü=Menubutton(raam, text="Vali funktsioon", textvariable="Funktsioon 1", bg="gray60", activebackground="gray30", activeforeground="snow2")
menüü.menu = Menu(menüü)  
menüü["menu"]=menüü.menu
menüülist(menüü)

menüü2=Menubutton(raam, text="Vali funktsioon", bg="gray60", activebackground="gray30", activeforeground="snow2")
menüü2.menu = Menu(menüü2)  
menüü2["menu"]=menüü2.menu
menüülist(menüü2) 

menüü3=Menubutton(raam, text="Vali funktsioon", bg="gray60", activebackground="gray30", activeforeground="snow2")
menüü3.menu = Menu(menüü3)  
menüü3["menu"]=menüü3.menu
menüülist(menüü3)

menüü.grid(column=2, row=1, padx=10, pady=10, sticky=(W))
menüü2.grid(column=2, row=2, padx=10, pady=10, sticky=(W))
menüü3.grid(column=2, row=3, padx=10, pady=10, sticky=(W))

def suleaken():
    raam.destroy()

lõpeta=ttk.Button(raam, text="Salvesta", command=suleaken)
lõpeta.grid(column=2, row=4, padx=10, pady=10, sticky=(N,S,W,E))

raam.columnconfigure(2,weight=1)
raam.rowconfigure(2,weight=1)

raam.mainloop()


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))


if funktsioonid[0]=="f1":
    print("Rusika tuvastamisel paneb helitugevuse maksimumile")
    #if rusikas:
        #volume.SetMasterVolumeLevel(-0.0, None) 
elif funktsioonid[0]=="f2":
    print("Rusika tuvastamisel paneb helitugevuse miinimumile")
    #if rusikas:
        #volume.SetMasterVolumeLevel(-80.0, None) 
elif funktsioonid[0]=="f3":
    print("täidab rusika tuvastamisel funktsiooni 3")
elif funktsioonid[0]=="f4":
    print("täidab rusika tuvastamisel funktsiooni 4")
elif funktsioonid[0]=="f5":
    print("täidab rusika tuvastamisel funktsiooni 5")
    
if funktsioonid[1]=="f1":
    print("Kõik sõrmed püsti tuvastamisel paneb helitugevuse maksimumile")
    #if kõik sõrmed püsti:
        #volume.SetMasterVolumeLevel(-0.0, None) 
elif funktsioonid[1]=="f2":
    print("Kõik sõrmed püsti tuvastamisel paneb helitugevuse miinimumile")
    #if kõik sõrmed püsti:
        #volume.SetMasterVolumeLevel(-80.0, None)
elif funktsioonid[1]=="f3":
    print("täidab kõik sõrmed püsti tuvastamisel funktsiooni 3")
elif funktsioonid[1]=="f4":
    print("täidab kõik sõrmed püsti tuvastamisel funktsiooni 4")
elif funktsioonid[1]=="f5":
    print("täidab kõik sõrmed püsti tuvastamisel funktsiooni 5")

if funktsioonid[2]=="f1":
    print("Üks sõrm püsti tuvastamisel paneb helitugevuse maksimumile")
    #if üks sõrm püsti:
        #volume.SetMasterVolumeLevel(-0.0, None) 
elif funktsioonid[2]=="f2":
    print("Üks sõrm püsti tuvastamisel paneb helitugevuse miinimumile")
    #if üks sõrm püsti:
        #volume.SetMasterVolumeLevel(-80.0, None)
elif funktsioonid[2]=="f3":
    print("täidab üks sõrm püsti tuvastamisel funktsiooni 3")
elif funktsioonid[2]=="f4":
    print("täidab üks sõrm püsti tuvastamisel funktsiooni 4")
elif funktsioonid[2]=="f5":
    print("täidab üks sõrm püsti tuvastamisel funktsiooni 5")