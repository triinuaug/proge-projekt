import os
import sys
import win32api         # package pywin32
import win32con
import win32gui_struct
try:
    import winxpgui as win32gui
except ImportError:
    import win32gui
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import Menubutton
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from statistics import *
import cv2
import imutils
import numpy as np
from math import ceil
from sklearn.metrics import pairwise
import itertools, glob
from multiprocessing import Process
import wmi


icons = itertools.cycle(glob.glob('*.ico'))
hover_text = "SysTrayIcon.py Demo"
funktsioonid=[]

bg = None
def dokumentatsioon():
    print("Hetkel puudub dokementatsioon.")

def heli_max():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volume.SetMasterVolumeLevel(-0.0, None) 
def heli_min():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volume.SetMasterVolumeLevel(-80.0, None) 


def run_avg(image, aWeight):
    global bg
    
    if bg is None:
        bg = image.copy().astype("float")
        return
    cv2.accumulateWeighted(image, bg, aWeight)
    
def segment(image, threshold=25):
    global bg
    diff = cv2.absdiff(bg.astype("uint8"), image)
    thresholded = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)[1]
    
    (cnts, _) = cv2.findContours(thresholded.copy(),
    cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE)
    
    if len(cnts) == 0:
        return
    else:
        segmented = max(cnts, key=cv2.contourArea)
        return (thresholded, segmented)

def camscan(a):
        
    if True:
        aWeight = 0.5
        camera = cv2.VideoCapture(0)
        top, right, bottom, left= 0, 450, 250, 700
        num_frames = 0
        fingerlist= []
        function_trigger = int()
        counter_f = 0
        
        while True:
            (grabbed, frame) = camera.read()
            frame = imutils.resize(frame, width=700)
            frame = cv2.flip(frame, 1)
            clone = frame.copy()
            (height, width) = frame.shape[:2]
            box = frame[top:bottom, right:left]
            grayscale = cv2.cvtColor(box, cv2.COLOR_BGR2GRAY)
            grayscale = cv2.GaussianBlur(grayscale, (7, 7), 0)
            
            if num_frames < 30:
                run_avg(grayscale, aWeight)
                
            else:
                hand = segment(grayscale)
                if hand is not None:
                    (thresholded, segmented) = hand


                    # count the number of fingers
                    fingers = count(thresholded, segmented)
                    fingerlist.append(fingers)
                    counter_f += 1
                    if counter_f == 15:
                        try:
                            function_trigger = mode(fingerlist)
                        except StatisticsError:
                            function_trigger = [count]
                        counter_f = 0
                        fingerlist.clear()



                    cv2.putText(clone, str(function_trigger), (70, 45), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
                    
                    cv2.drawContours(clone, [segmented + (right, top)], -1, (0, 0, 255))
                    #cv2.imshow("Thesholded", thresholded)
                    
               
            cv2.rectangle(clone, (left, top), (right, bottom), (0,255,0), 2)
            num_frames += 1


           
           
            cv2.imshow("Video Feed", clone)

            if function_trigger == 1:
                if len(a) is not 0:
                    if a[0] == "f1":
                        heledus_max()
                    elif a[0] == "f2":
                        heledus_miinus()
            elif function_trigger ==2:
                if a[1] == "f1":
                    heledus_max()
                elif a[1] == "f2":
                    heledus_miinus()

            keypress = cv2.waitKey(1) & 0xFF
            if keypress == ord("q"):
                break



    camera.release()
    cv2.destroyAllWindows()
        
    
def count(thresholded, segmented):
    chull = cv2.convexHull(segmented)
    extreme_top    = tuple(chull[chull[:, :, 1].argmin()][0])
    extreme_bottom = tuple(chull[chull[:, :, 1].argmax()][0])
    extreme_left   = tuple(chull[chull[:, :, 0].argmin()][0])
    extreme_right  = tuple(chull[chull[:, :, 0].argmax()][0])
    
    cX = int((extreme_left[0] + extreme_right[0]) / 2)
    cY = int((extreme_top[1] + extreme_bottom[1]) / 2)
    
    distance = pairwise.euclidean_distances([(cX, cY)], Y=[extreme_left, extreme_right, extreme_top, extreme_bottom])[0]
    maximum_distance = distance[distance.argmax()]
    
    radius = int(0.8 * maximum_distance)
    circumference = (2 * np.pi * radius)
    circular_roi = np.zeros(thresholded.shape[:2], dtype="uint8")
    cv2.circle(circular_roi, (cX, cY), radius, 255, 1)
    circular_roi = cv2.bitwise_and(thresholded, thresholded, mask=circular_roi)
    
    (cnts, _) = cv2.findContours(circular_roi.copy(),
    cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE)

    count = 0
    for c in cnts:
        (x, y, w, h) = cv2.boundingRect(c)
        if ((cY + (cY * 0.25)) > (y + h)) and ((circumference * 0.25) > c.shape[0]):
            count += 1
    return count


class SysTrayIcon(object):
    '''TODO'''
    QUIT = 'QUIT'
    SPECIAL_ACTIONS = [QUIT]

    FIRST_ID = 1023

    def __init__(self,
                 icon,
                 hover_text,
                 menu_options,
                 on_quit=None,
                 default_menu_index=None,
                 window_class_name=None,):

        self.icon = icon
        self.hover_text = hover_text
        self.on_quit = on_quit

        menu_options = menu_options + (('Välju', None, self.QUIT),)
        self._next_action_id = self.FIRST_ID
        self.menu_actions_by_id = set()
        self.menu_options = self._add_ids_to_menu_options(list(menu_options))
        self.menu_actions_by_id = dict(self.menu_actions_by_id)
        del self._next_action_id


        self.default_menu_index = (default_menu_index or 0)
        self.window_class_name = window_class_name or "SysTrayIconPy"

        message_map = {win32gui.RegisterWindowMessage("TaskbarCreated"): self.restart,
                       win32con.WM_DESTROY: self.destroy,
                       win32con.WM_COMMAND: self.command,
                       win32con.WM_USER+20 : self.notify,}
        # Register the Window class.
        window_class = win32gui.WNDCLASS()
        hinst = window_class.hInstance = win32gui.GetModuleHandle(None)
        window_class.lpszClassName = self.window_class_name
        window_class.style = win32con.CS_VREDRAW | win32con.CS_HREDRAW;
        window_class.hCursor = win32gui.LoadCursor(0, win32con.IDC_ARROW)
        window_class.hbrBackground = win32con.COLOR_WINDOW
        window_class.lpfnWndProc = message_map # could also specify a wndproc.
        classAtom = win32gui.RegisterClass(window_class)
        # Create the Window.
        style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU
        self.hwnd = win32gui.CreateWindow(classAtom,
                                          self.window_class_name,
                                          style,
                                          0,
                                          0,
                                          win32con.CW_USEDEFAULT,
                                          win32con.CW_USEDEFAULT,
                                          0,
                                          0,
                                          hinst,
                                          None)
        win32gui.UpdateWindow(self.hwnd)
        self.notify_id = None
        self.refresh_icon()

        win32gui.PumpMessages()

    def _add_ids_to_menu_options(self, menu_options):
        result = []
        for menu_option in menu_options:
            option_text, option_icon, option_action = menu_option
            if callable(option_action) or option_action in self.SPECIAL_ACTIONS:
                self.menu_actions_by_id.add((self._next_action_id, option_action))
                result.append(menu_option + (self._next_action_id,))
            elif non_string_iterable(option_action):
                result.append((option_text,
                               option_icon,
                               self._add_ids_to_menu_options(option_action),
                               self._next_action_id))
            else:
                print('Unknown item', option_text, option_icon, option_action)
            self._next_action_id += 1
        return result

    def refresh_icon(self):
        # Try and find a custom icon
        hinst = win32gui.GetModuleHandle(None)
        if os.path.isfile(self.icon):
            icon_flags = win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE
            hicon = win32gui.LoadImage(hinst,
                                       self.icon,
                                       win32con.IMAGE_ICON,
                                       0,
                                       0,
                                       icon_flags)
        else:
            print("Can't find icon file - using default.")
            hicon = win32gui.LoadIcon(0, win32con.IDI_APPLICATION)

        if self.notify_id: message = win32gui.NIM_MODIFY
        else: message = win32gui.NIM_ADD
        self.notify_id = (self.hwnd,
                          0,
                          win32gui.NIF_ICON | win32gui.NIF_MESSAGE | win32gui.NIF_TIP,
                          win32con.WM_USER+20,
                          hicon,
                          self.hover_text)
        win32gui.Shell_NotifyIcon(message, self.notify_id)

    def restart(self, hwnd, msg, wparam, lparam):
        self.refresh_icon()

    def destroy(self, hwnd, msg, wparam, lparam):
        if self.on_quit: self.on_quit(self)
        nid = (self.hwnd, 0)
        win32gui.Shell_NotifyIcon(win32gui.NIM_DELETE, nid)
        win32gui.PostQuitMessage(0) # Terminate the app.

    def notify(self, hwnd, msg, wparam, lparam):
        if lparam==win32con.WM_LBUTTONDBLCLK:
            self.execute_menu_option(self.default_menu_index + self.FIRST_ID)
        elif lparam==win32con.WM_RBUTTONUP:
            self.show_menu()
        elif lparam==win32con.WM_LBUTTONUP:
            pass
        return True

    def show_menu(self):
        menu = win32gui.CreatePopupMenu()
        self.create_menu(menu, self.menu_options)
        #win32gui.SetMenuDefaultItem(menu, 1000, 0)

        pos = win32gui.GetCursorPos()
        # See http://msdn.microsoft.com/library/default.asp?url=/library/en-us/winui/menus_0hdi.asp
        win32gui.SetForegroundWindow(self.hwnd)
        win32gui.TrackPopupMenu(menu,
                                win32con.TPM_LEFTALIGN,
                                pos[0],
                                pos[1],
                                0,
                                self.hwnd,
                                None)
        win32gui.PostMessage(self.hwnd, win32con.WM_NULL, 0, 0)

    def create_menu(self, menu, menu_options):
        for option_text, option_icon, option_action, option_id in menu_options[::-1]:
            if option_icon:
                option_icon = self.prep_menu_icon(option_icon)

            if option_id in self.menu_actions_by_id:                
                item, extras = win32gui_struct.PackMENUITEMINFO(text=option_text,
                                                                hbmpItem=option_icon,
                                                                wID=option_id)
                win32gui.InsertMenuItem(menu, 0, 1, item)
            else:
                submenu = win32gui.CreatePopupMenu()
                self.create_menu(submenu, option_action)
                item, extras = win32gui_struct.PackMENUITEMINFO(text=option_text,
                                                                hbmpItem=option_icon,
                                                                hSubMenu=submenu)
                win32gui.InsertMenuItem(menu, 0, 1, item)

    def prep_menu_icon(self, icon):
        # First load the icon.
        ico_x = win32api.GetSystemMetrics(win32con.SM_CXSMICON)
        ico_y = win32api.GetSystemMetrics(win32con.SM_CYSMICON)
        hicon = win32gui.LoadImage(0, icon, win32con.IMAGE_ICON, ico_x, ico_y, win32con.LR_LOADFROMFILE)

        hdcBitmap = win32gui.CreateCompatibleDC(0)
        hdcScreen = win32gui.GetDC(0)
        hbm = win32gui.CreateCompatibleBitmap(hdcScreen, ico_x, ico_y)
        hbmOld = win32gui.SelectObject(hdcBitmap, hbm)
        # Fill the background.
        brush = win32gui.GetSysColorBrush(win32con.COLOR_MENU)
        win32gui.FillRect(hdcBitmap, (0, 0, 16, 16), brush)
        # unclear if brush needs to be feed.  Best clue I can find is:
        # "GetSysColorBrush returns a cached brush instead of allocating a new
        # one." - implies no DeleteObject
        # draw the icon
        win32gui.DrawIconEx(hdcBitmap, 0, 0, hicon, ico_x, ico_y, 0, 0, win32con.DI_NORMAL)
        win32gui.SelectObject(hdcBitmap, hbmOld)
        win32gui.DeleteDC(hdcBitmap)

        return hbm

    def command(self, hwnd, msg, wparam, lparam):
        id = win32gui.LOWORD(wparam)
        self.execute_menu_option(id)

    def execute_menu_option(self, id):
        menu_action = self.menu_actions_by_id[id]      
        if menu_action == self.QUIT:
            win32gui.DestroyWindow(self.hwnd)
        else:
            menu_action(self)

##__import__("GUI")
def non_string_iterable(obj):
    try:
        iter(obj)
    except TypeError:
        return False
    else:
        return not isinstance(obj, str)

def activate_gui():
    def gui_main():
        funktsioonid=[]
        fun_label = '---Kasutuses---'
        def fun1():
            funktsioonid.append("f1")
            menüü.menu.entryconfig(1, label=fun_label)
            menüü2.menu.entryconfig(1, label=fun_label)
            menüü3.menu.entryconfig(1, label=fun_label)
            return funktsioonid
        def fun2():
            funktsioonid.append("f2")
            menüü.menu.entryconfig(2, label=fun_label)
            menüü2.menu.entryconfig(2, label=fun_label)
            menüü3.menu.entryconfig(2, label=fun_label)
            return funktsioonid
        def fun3():
            funktsioonid.append("f3")
            menüü.menu.entryconfig(3, label=fun_label)
            menüü2.menu.entryconfig(3, label=fun_label)
            menüü3.menu.entryconfig(3, label=fun_label)
        def fun4():
            funktsioonid.append("f4")
            menüü.menu.entryconfig(4, label=fun_label)
            menüü2.menu.entryconfig(4, label=fun_label)
            menüü3.menu.entryconfig(4, label=fun_label)
        def fun5():
            funktsioonid.append("f5")
            menüü.menu.entryconfig(5, label=fun_label)
            menüü2.menu.entryconfig(5, label=fun_label)
            menüü3.menu.entryconfig(5, label=fun_label)
            
        def menüülist(menüü):
            menüü.menu.add_command(label="Paneb heleduse maksimumile",command=fun1, activebackground="gray30", activeforeground="snow2")
            menüü.menu.add_command(label="Paneb heleduse miinimumile",command=fun2, activebackground="gray30", activeforeground="snow2")
        ##    menüü.menu.add_command(label="Funktsioon 3",command=fun3, activebackground="gray30", activeforeground="snow2")
        ##    menüü.menu.add_command(label="Funktsioon 4",command=fun4, activebackground="gray30", activeforeground="snow2")
        ##    menüü.menu.add_command(label="Funktsioon 5",command=fun5, activebackground="gray30", activeforeground="snow2")

        raam = Tk()
        raam.title("Kasutajaliides")

        pealkiri=ttk.Label(raam, text="Palun vali igale liigutusele vastav funktsioon (esimene valik loeb): ")
        pealkiri.grid(column=1, row=0, padx=10, pady=10, sticky=(N,S,W,E))

        silt1 = ttk.Label(raam, text="Üks sõrm püsti")
        silt1.grid(column=1, row=1, padx=10, pady=10, sticky=(E))
        silt2 = ttk.Label(raam, text="Kaks sõrme püsti")
        silt2.grid(column=1, row=2, padx=10, pady=10, sticky=(E))
        #silt3 = ttk.Label(raam, text="Kolm sõrme püsti")
        #silt3.grid(column=1, row=3, padx=10, pady=10, sticky=(E))

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
        #menüü3.grid(column=2, row=3, padx=10, pady=10, sticky=(W))

        def suleaken():
            
            raam.destroy()




        lõpeta=ttk.Button(raam, text="Salvesta", command=suleaken)
        lõpeta.grid(column=2, row=4, padx=10, pady=10, sticky=(N,S,W,E))

        raam.columnconfigure(2,weight=1)
        raam.rowconfigure(2,weight=1)

        raam.mainloop()
        return funktsioonid

    
    camscan(gui_main())

    


def heli_max():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volume.SetMasterVolumeLevel(-0.0, None) 

def heledus_miinus():
    brightness = 20
    c = wmi.WMI(namespace='wmi')

    methods = c.WmiMonitorBrightnessMethods()[0]
    methods.WmiSetBrightness(brightness, 0)
def heledus_max():
    brightness = 100 # percentage [0-100]
    c = wmi.WMI(namespace='wmi')

    methods = c.WmiMonitorBrightnessMethods()[0]
    methods.WmiSetBrightness(brightness, 0)
def heli_min():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volume.SetMasterVolumeLevel(-80.0, None) 

def menu(sysTrayIcon): activate_gui()
def heledus_plus(sysTrayIcon): heledus_max()
def heledus_min(sysTrayIcon): heledus_miinus()
def dokum(sysTrayIcon): dokumentatsioon()
menu_options = (('Menüü', None, menu),
            ('Dokumentatsioon', None, dokum),
            ('Lisa', next(icons), (('Heledus -', next(icons), heledus_min),
                                          ('Heledus +', next(icons), heledus_plus),
                                         ))
           )
def bye(sysTrayIcon): print('Katkestatud')


def systray_fun():
    SysTrayIcon(next(icons), hover_text, menu_options, on_quit=bye, default_menu_index=1)


systray_fun()