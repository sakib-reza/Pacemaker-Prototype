import tkinter as tk
import serial
import time
import struct
from tkinter import ttk

ser = serial.Serial(
    port='COM8',
    baudrate=115200)

LARGE_FONT = ("Arial", 12)
SMALL_FONT = ("Arial", 8)

mode=1
Lower_Rate_Limit=60
Upper_Rate_Limit=120
Maximum_Sensor_Rate=120
Fixed_AV_Delay=150
#Dynamic_AV_Delay=0
#Sensed_AV_Delay_Offset=0
#Atrial_Amplitude=0
#Ventricular_Amplitude=0
Atrial_Pulse_Width=10
Ventricular_Pulse_Width=10
#Atrial_Sensitivity=0
#Ventricular_Sensitivity=0
VRP=320
ARP=320

Reaction_Time=30
Response_Factor=8
Recover_Time=5
A_Duty_Cycle=80
V_Duty_Cycle=80

def send_data(mode, LRL, ATR_PWIDTH, VENT_PWIDTH, URL, VRP, ARP, ATRDUTY, VENTDUTY, AVDELAY):
    Start = 9
    Start = Start.to_bytes(1, byteorder='big')
    if (mode == "AOO"):
        Mode = 1
        Mode = Mode.to_bytes(1, byteorder='big')
    elif (mode == "VOO"):
        Mode = 2
        Mode = Mode.to_bytes(1, byteorder='big')
    elif (mode == "AAI"):
        Mode = 3
        Mode = Mode.to_bytes(1, byteorder='big')
    elif (mode == "VVI"):
        Mode = 4
        Mode = Mode.to_bytes(1, byteorder='big')
    elif (mode == "DOO"):
        Mode = 5
        Mode = Mode.to_bytes(1, byteorder='big')
    elif (mode == "AOOR"):
        Mode = 6
        Mode = Mode.to_bytes(1, byteorder='big')
    elif (mode == "VOOR"):
        Mode = 7
        Mode = Mode.to_bytes(1, byteorder='big')
    elif (mode == "AAIR"):
        Mode = 8
        Mode = Mode.to_bytes(1, byteorder='big')
    elif (mode == "VVIR"):
        Mode = 9
        Mode = Mode.to_bytes(1, byteorder='big')
    elif (mode == "DOOR"):
        Mode = 10
        Mode = Mode.to_bytes(1, byteorder='big')

    #LRL = 60
    LRL = LRL.to_bytes(1, byteorder='big')
    #ATR_PWIDTH = 10
    ATR_PWIDTH = ATR_PWIDTH.to_bytes(2, byteorder='little')
    #VENT_PWIDTH = 10
    VENT_PWIDTH = VENT_PWIDTH.to_bytes(2, byteorder='little')
    #URL = 120
    URL = URL.to_bytes(1, byteorder='little')
    #VRP = 320
    VRP = VRP.to_bytes(2, byteorder='little')
    #ARP = 250
    ARP = ARP.to_bytes(2, byteorder='little')
    #ATRDUTY = 80
    ATRDUTY = ATRDUTY.to_bytes(8, byteorder='little')
    #VENTDUTY = 80
    VENTDUTY = VENTDUTY.to_bytes(8, byteorder='little')
    #AVDELAY = 150
    AVDELAY = AVDELAY.to_bytes(2, byteorder='little')

    send = (Start + Mode + LRL + ATR_PWIDTH + VENT_PWIDTH + URL + VRP + ARP + ATRDUTY + VENTDUTY + AVDELAY) 
    ser.write(send) 



class PacemakerApp(tk.Tk):
    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "Pacemaker Application")

        self.resizable(width=False, height=False)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (WelcomeScreen, HomeScreen, AOO, VOO, AAI, VVI, DOO, AOOR, AAIR, VVIR, DOOR):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(WelcomeScreen)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

class WelcomeScreen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        welcome = tk.Label(self, text="Welcome to the Pacemaker App", font=LARGE_FONT)
        welcome.grid(row=0, columnspan=2)

        user = tk.Label(self, text="Username: ", font=SMALL_FONT)
        userbox = tk.Entry(self, bd="5")
        passw = tk.Label(self, text="Password: ", font=SMALL_FONT)
        passbox = tk.Entry(self, bd="5", show="*")
        user.grid(row=1, column=0)
        passw.grid(row=1, column=1)
        userbox.grid(row=2, column=0)
        passbox.grid(row=2, column=1)

        enter = ttk.Button(self, text="Login", command=lambda: self.login(userbox, passbox, msg, hostmsg, parent, controller))
        enter.grid(row=3, columnspan=2)

        register = ttk.Button(self, text="Sign Up", command=lambda: self.register(userbox, passbox, msg, hostmsg))
        register.grid(row=4, columnspan=2)

        hostmsg = ""
        msg = tk.Label(self, text=hostmsg, font=SMALL_FONT)
        msg.grid(row=5, columnspan=2)

    def login(self, userbox, passbox, msg, hostmsg, parent, controller):

        login_get = open("login_info.txt","r")
        login_info = login_get.readlines()
        login_get.close()
        for i in range(len(login_info)):
            login_info[i] = login_info[i].rstrip()

        username = userbox.get()
        password = passbox.get()

        verified = False

        for i in range(len(login_info)):
            if username==login_info[i].split(":")[0] and password==login_info[i].split(":")[1]:
                verified = True
                break

        if verified:
            controller.show_frame(HomeScreen)
            hostmsg = "Logout Successful."
            msg.config(text=hostmsg)
            userbox.delete(0, 'end')
            passbox.delete(0, 'end')
        else:
            hostmsg = "Login Information is incorrect. Please try again."
            msg.config(text=hostmsg)

    def register(self, userbox, passbox, msg, hostmsg):

        login_get = open("login_info.txt","r")
        login_info = login_get.readlines()
        login_get.close()
        for i in range(len(login_info)):
            login_info[i] = login_info[i].rstrip()

        username = userbox.get()
        password = passbox.get()

        if len(login_info) < 10:
            create_user = True

            for i in range(len(login_info)):
                if username==login_info[i].split(":")[0]:
                    create_user = False

            if create_user:
                if len(username) > 2 and len(password) > 2:
                    login_write = open("login_info.txt","a")
                    login_write.write(username + ":" + password + "\n")
                    login_write.close()
                    hostmsg = "Registration complete"
                    msg.config(text=hostmsg)
                else:
                    hostmsg = "Username or password is too short."
                    msg.config(text=hostmsg)
            else:
                hostmsg = "Username already registered. Pick a new username."
                msg.config(text=hostmsg)

            userbox.delete(0, 'end')
            passbox.delete(0, 'end')

        else:
            hostmsg = "Too many users have registered."
            msg.config(text=hostmsg)

class HomeScreen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        header = tk.Label(self, text="Select a pacing mode:", font=LARGE_FONT)
        header.grid(row=0, columnspan=2)

        aoo = ttk.Button(self, text="AOO", command=lambda: controller.show_frame(AOO))
        aoo.grid(row=1, columnspan=2)
        voo = ttk.Button(self, text="VOO", command=lambda: controller.show_frame(VOO))
        voo.grid(row=2, columnspan=2)
        aai = ttk.Button(self, text="AAI", command=lambda: controller.show_frame(AAI))
        aai.grid(row=3, columnspan=2)
        vvi = ttk.Button(self, text="VVI", command=lambda: controller.show_frame(VVI))
        vvi.grid(row=4, columnspan=2)
        doo = ttk.Button(self, text="DOO", command=lambda: controller.show_frame(DOO))
        doo.grid(row=5, columnspan=2)
        aoor = ttk.Button(self, text="AOOR", command=lambda: controller.show_frame(AOOR))
        aoor.grid(row=6, columnspan=2)
        voor = ttk.Button(self, text="VOOR", command=lambda: controller.show_frame(VOOR))
        voor.grid(row=7, columnspan=2)
        aair = ttk.Button(self, text="AAIR", command=lambda: controller.show_frame(AAIR))
        aair.grid(row=8, columnspan=2)
        vvir = ttk.Button(self, text="VVIR", command=lambda: controller.show_frame(VVIR))
        vvir.grid(row=9, columnspan=2)
        door = ttk.Button(self, text="DOOR", command=lambda: controller.show_frame(DOOR))
        door.grid(row=10, columnspan=2)

        back = ttk.Button(self, text="Log Out", command=lambda: controller.show_frame(WelcomeScreen))
        back.grid(row=11, columnspan=2)

        deviceid = "Device Connected" if (ser.port == "COM8") else "Device disconnected"
        devid = tk.Label(self, text=deviceid, font=SMALL_FONT)
        devid.grid(row=12, columnspan=2)

# operation modes
class AOO(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        tk.Label(self, text="LRL", font=SMALL_FONT).grid(row=0, column=1)
        LRL_input = tk.Entry(self, bd="5")
        LRL_input.grid(row=0, column=2)

        tk.Label(self, text="ATR_PWIDTH", font=SMALL_FONT).grid(row=1, column=1)
        ATR_PWIDTH_input = tk.Entry(self, bd="5")
        ATR_PWIDTH_input.grid(row=1, column=2)

        tk.Label(self, text="VENT_PWIDTH", font=SMALL_FONT).grid(row=2, column=1)
        VENT_PWIDTH_input = tk.Entry(self, bd="5")
        VENT_PWIDTH_input.grid(row=2, column=2)

        tk.Label(self, text="URL", font=SMALL_FONT).grid(row=3, column=1)
        URL_input = tk.Entry(self, bd="5")
        URL_input.grid(row=3, column=2)

        tk.Label(self, text="VRP", font=SMALL_FONT).grid(row=4, column=1)
        VRP_input = tk.Entry(self, bd="5")
        VRP_input.grid(row=4, column=2)

        tk.Label(self, text="ARP", font=SMALL_FONT).grid(row=5, column=1)
        ARP_input = tk.Entry(self, bd="5")
        ARP_input.grid(row=5, column=2)

        tk.Label(self, text="ATRDUTY", font=SMALL_FONT).grid(row=6, column=1)
        ATRDUTY_input = tk.Entry(self, bd="5")
        ATRDUTY_input.grid(row=6, column=2)

        tk.Label(self, text="VENTDUTY", font=SMALL_FONT).grid(row=7, column=1)
        VENTDUTY_input = tk.Entry(self, bd="5")
        VENTDUTY_input.grid(row=7, column=2)

        tk.Label(self, text="AVDELAY", font=SMALL_FONT).grid(row=8, column=1)
        AVDELAY_input = tk.Entry(self, bd="5")
        AVDELAY_input.grid(row=8, column=2)

        hostmsg = ""
        msg = tk.Label(self, text=hostmsg, font=SMALL_FONT)
        msg.grid(row=9, columnspan=3)

        change_param = ttk.Button(self, text="Change Parameters", command=lambda: [send_data("AOO", int(LRL_input.get()),\
                                        int(ATR_PWIDTH_input.get()), int(VENT_PWIDTH_input.get()), int(URL_input.get()),\
                                        int(VRP_input.get()), int(ARP_input.get()), int(ATRDUTY_input.get()), \
                                        int(VENTDUTY_input.get()), int(AVDELAY_input.get())), msg.config(text="Data Sent")])
        change_param.grid(row=0, column=0)
        back = ttk.Button(self, text="Return", command=lambda: controller.show_frame(HomeScreen))
        back.grid(row=1, column=0)

class VOO(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        tk.Label(self, text="LRL", font=SMALL_FONT).grid(row=0, column=1)
        LRL_input = tk.Entry(self, bd="5")
        LRL_input.grid(row=0, column=2)

        tk.Label(self, text="ATR_PWIDTH", font=SMALL_FONT).grid(row=1, column=1)
        ATR_PWIDTH_input = tk.Entry(self, bd="5")
        ATR_PWIDTH_input.grid(row=1, column=2)

        tk.Label(self, text="VENT_PWIDTH", font=SMALL_FONT).grid(row=2, column=1)
        VENT_PWIDTH_input = tk.Entry(self, bd="5")
        VENT_PWIDTH_input.grid(row=2, column=2)

        tk.Label(self, text="URL", font=SMALL_FONT).grid(row=3, column=1)
        URL_input = tk.Entry(self, bd="5")
        URL_input.grid(row=3, column=2)

        tk.Label(self, text="VRP", font=SMALL_FONT).grid(row=4, column=1)
        VRP_input = tk.Entry(self, bd="5")
        VRP_input.grid(row=4, column=2)

        tk.Label(self, text="ARP", font=SMALL_FONT).grid(row=5, column=1)
        ARP_input = tk.Entry(self, bd="5")
        ARP_input.grid(row=5, column=2)

        tk.Label(self, text="ATRDUTY", font=SMALL_FONT).grid(row=6, column=1)
        ATRDUTY_input = tk.Entry(self, bd="5")
        ATRDUTY_input.grid(row=6, column=2)

        tk.Label(self, text="VENTDUTY", font=SMALL_FONT).grid(row=7, column=1)
        VENTDUTY_input = tk.Entry(self, bd="5")
        VENTDUTY_input.grid(row=7, column=2)

        tk.Label(self, text="AVDELAY", font=SMALL_FONT).grid(row=8, column=1)
        AVDELAY_input = tk.Entry(self, bd="5")
        AVDELAY_input.grid(row=8, column=2)

        hostmsg = ""
        msg = tk.Label(self, text=hostmsg, font=SMALL_FONT)
        msg.grid(row=9, columnspan=3)

        change_param = ttk.Button(self, text="Change Parameters", command=lambda: [send_data("VOO", int(LRL_input.get()),\
                                        int(ATR_PWIDTH_input.get()), int(VENT_PWIDTH_input.get()), int(URL_input.get()),\
                                        int(VRP_input.get()), int(ARP_input.get()), int(ATRDUTY_input.get()), \
                                        int(VENTDUTY_input.get()), int(AVDELAY_input.get())), msg.config("Data Sent")])
        change_param.grid(row=0, column=0)
        back = ttk.Button(self, text="Return", command=lambda: controller.show_frame(HomeScreen))
        back.grid(row=1, column=0)

class AAI(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        tk.Label(self, text="LRL", font=SMALL_FONT).grid(row=0, column=1)
        LRL_input = tk.Entry(self, bd="5")
        LRL_input.grid(row=0, column=2)

        tk.Label(self, text="ATR_PWIDTH", font=SMALL_FONT).grid(row=1, column=1)
        ATR_PWIDTH_input = tk.Entry(self, bd="5")
        ATR_PWIDTH_input.grid(row=1, column=2)

        tk.Label(self, text="VENT_PWIDTH", font=SMALL_FONT).grid(row=2, column=1)
        VENT_PWIDTH_input = tk.Entry(self, bd="5")
        VENT_PWIDTH_input.grid(row=2, column=2)

        tk.Label(self, text="URL", font=SMALL_FONT).grid(row=3, column=1)
        URL_input = tk.Entry(self, bd="5")
        URL_input.grid(row=3, column=2)

        tk.Label(self, text="VRP", font=SMALL_FONT).grid(row=4, column=1)
        VRP_input = tk.Entry(self, bd="5")
        VRP_input.grid(row=4, column=2)

        tk.Label(self, text="ARP", font=SMALL_FONT).grid(row=5, column=1)
        ARP_input = tk.Entry(self, bd="5")
        ARP_input.grid(row=5, column=2)

        tk.Label(self, text="ATRDUTY", font=SMALL_FONT).grid(row=6, column=1)
        ATRDUTY_input = tk.Entry(self, bd="5")
        ATRDUTY_input.grid(row=6, column=2)

        tk.Label(self, text="VENTDUTY", font=SMALL_FONT).grid(row=7, column=1)
        VENTDUTY_input = tk.Entry(self, bd="5")
        VENTDUTY_input.grid(row=7, column=2)

        tk.Label(self, text="AVDELAY", font=SMALL_FONT).grid(row=8, column=1)
        AVDELAY_input = tk.Entry(self, bd="5")
        AVDELAY_input.grid(row=8, column=2)

        hostmsg = ""
        msg = tk.Label(self, text=hostmsg, font=SMALL_FONT)
        msg.grid(row=9, columnspan=3)

        change_param = ttk.Button(self, text="Change Parameters", command=lambda: [send_data("AAI", int(LRL_input.get()),\
                                        int(ATR_PWIDTH_input.get()), int(VENT_PWIDTH_input.get()), int(URL_input.get()),\
                                        int(VRP_input.get()), int(ARP_input.get()), int(ATRDUTY_input.get()), \
                                        int(VENTDUTY_input.get()), int(AVDELAY_input.get())), msg.config("Data Sent")])
        change_param.grid(row=0, column=0)
        back = ttk.Button(self, text="Return", command=lambda: controller.show_frame(HomeScreen))
        back.grid(row=1, column=0)

class VVI(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        tk.Label(self, text="LRL", font=SMALL_FONT).grid(row=0, column=1)
        LRL_input = tk.Entry(self, bd="5")
        LRL_input.grid(row=0, column=2)

        tk.Label(self, text="ATR_PWIDTH", font=SMALL_FONT).grid(row=1, column=1)
        ATR_PWIDTH_input = tk.Entry(self, bd="5")
        ATR_PWIDTH_input.grid(row=1, column=2)

        tk.Label(self, text="VENT_PWIDTH", font=SMALL_FONT).grid(row=2, column=1)
        VENT_PWIDTH_input = tk.Entry(self, bd="5")
        VENT_PWIDTH_input.grid(row=2, column=2)

        tk.Label(self, text="URL", font=SMALL_FONT).grid(row=3, column=1)
        URL_input = tk.Entry(self, bd="5")
        URL_input.grid(row=3, column=2)

        tk.Label(self, text="VRP", font=SMALL_FONT).grid(row=4, column=1)
        VRP_input = tk.Entry(self, bd="5")
        VRP_input.grid(row=4, column=2)

        tk.Label(self, text="ARP", font=SMALL_FONT).grid(row=5, column=1)
        ARP_input = tk.Entry(self, bd="5")
        ARP_input.grid(row=5, column=2)

        tk.Label(self, text="ATRDUTY", font=SMALL_FONT).grid(row=6, column=1)
        ATRDUTY_input = tk.Entry(self, bd="5")
        ATRDUTY_input.grid(row=6, column=2)

        tk.Label(self, text="VENTDUTY", font=SMALL_FONT).grid(row=7, column=1)
        VENTDUTY_input = tk.Entry(self, bd="5")
        VENTDUTY_input.grid(row=7, column=2)

        tk.Label(self, text="AVDELAY", font=SMALL_FONT).grid(row=8, column=1)
        AVDELAY_input = tk.Entry(self, bd="5")
        AVDELAY_input.grid(row=8, column=2)

        hostmsg = ""
        msg = tk.Label(self, text=hostmsg, font=SMALL_FONT)
        msg.grid(row=9, columnspan=3)

        change_param = ttk.Button(self, text="Change Parameters", command=lambda: [send_data("VVI", int(LRL_input.get()),\
                                        int(ATR_PWIDTH_input.get()), int(VENT_PWIDTH_input.get()), int(URL_input.get()),\
                                        int(VRP_input.get()), int(ARP_input.get()), int(ATRDUTY_input.get()), \
                                        int(VENTDUTY_input.get()), int(AVDELAY_input.get())), msg.config("Data Sent")])
        change_param.grid(row=0, column=0)
        back = ttk.Button(self, text="Return", command=lambda: controller.show_frame(HomeScreen))
        back.grid(row=1, column=0)

class DOO(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        tk.Label(self, text="LRL", font=SMALL_FONT).grid(row=0, column=1)
        LRL_input = tk.Entry(self, bd="5")
        LRL_input.grid(row=0, column=2)

        tk.Label(self, text="ATR_PWIDTH", font=SMALL_FONT).grid(row=1, column=1)
        ATR_PWIDTH_input = tk.Entry(self, bd="5")
        ATR_PWIDTH_input.grid(row=1, column=2)

        tk.Label(self, text="VENT_PWIDTH", font=SMALL_FONT).grid(row=2, column=1)
        VENT_PWIDTH_input = tk.Entry(self, bd="5")
        VENT_PWIDTH_input.grid(row=2, column=2)

        tk.Label(self, text="URL", font=SMALL_FONT).grid(row=3, column=1)
        URL_input = tk.Entry(self, bd="5")
        URL_input.grid(row=3, column=2)

        tk.Label(self, text="VRP", font=SMALL_FONT).grid(row=4, column=1)
        VRP_input = tk.Entry(self, bd="5")
        VRP_input.grid(row=4, column=2)

        tk.Label(self, text="ARP", font=SMALL_FONT).grid(row=5, column=1)
        ARP_input = tk.Entry(self, bd="5")
        ARP_input.grid(row=5, column=2)

        tk.Label(self, text="ATRDUTY", font=SMALL_FONT).grid(row=6, column=1)
        ATRDUTY_input = tk.Entry(self, bd="5")
        ATRDUTY_input.grid(row=6, column=2)

        tk.Label(self, text="VENTDUTY", font=SMALL_FONT).grid(row=7, column=1)
        VENTDUTY_input = tk.Entry(self, bd="5")
        VENTDUTY_input.grid(row=7, column=2)

        tk.Label(self, text="AVDELAY", font=SMALL_FONT).grid(row=8, column=1)
        AVDELAY_input = tk.Entry(self, bd="5")
        AVDELAY_input.grid(row=8, column=2)

        hostmsg = ""
        msg = tk.Label(self, text=hostmsg, font=SMALL_FONT)
        msg.grid(row=9, columnspan=3)

        change_param = ttk.Button(self, text="Change Parameters", command=lambda: [send_data("DOO", int(LRL_input.get()),\
                                        int(ATR_PWIDTH_input.get()), int(VENT_PWIDTH_input.get()), int(URL_input.get()),\
                                        int(VRP_input.get()), int(ARP_input.get()), int(ATRDUTY_input.get()), \
                                        int(VENTDUTY_input.get()), int(AVDELAY_input.get())), msg.config("Data Sent")])
        change_param.grid(row=0, column=0)
        back = ttk.Button(self, text="Return", command=lambda: controller.show_frame(HomeScreen))
        back.grid(row=1, column=0)

class AOOR(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        tk.Label(self, text="LRL", font=SMALL_FONT).grid(row=0, column=1)
        LRL_input = tk.Entry(self, bd="5")
        LRL_input.grid(row=0, column=2)

        tk.Label(self, text="ATR_PWIDTH", font=SMALL_FONT).grid(row=1, column=1)
        ATR_PWIDTH_input = tk.Entry(self, bd="5")
        ATR_PWIDTH_input.grid(row=1, column=2)

        tk.Label(self, text="VENT_PWIDTH", font=SMALL_FONT).grid(row=2, column=1)
        VENT_PWIDTH_input = tk.Entry(self, bd="5")
        VENT_PWIDTH_input.grid(row=2, column=2)

        tk.Label(self, text="URL", font=SMALL_FONT).grid(row=3, column=1)
        URL_input = tk.Entry(self, bd="5")
        URL_input.grid(row=3, column=2)

        tk.Label(self, text="VRP", font=SMALL_FONT).grid(row=4, column=1)
        VRP_input = tk.Entry(self, bd="5")
        VRP_input.grid(row=4, column=2)

        tk.Label(self, text="ARP", font=SMALL_FONT).grid(row=5, column=1)
        ARP_input = tk.Entry(self, bd="5")
        ARP_input.grid(row=5, column=2)

        tk.Label(self, text="ATRDUTY", font=SMALL_FONT).grid(row=6, column=1)
        ATRDUTY_input = tk.Entry(self, bd="5")
        ATRDUTY_input.grid(row=6, column=2)

        tk.Label(self, text="VENTDUTY", font=SMALL_FONT).grid(row=7, column=1)
        VENTDUTY_input = tk.Entry(self, bd="5")
        VENTDUTY_input.grid(row=7, column=2)

        tk.Label(self, text="AVDELAY", font=SMALL_FONT).grid(row=8, column=1)
        AVDELAY_input = tk.Entry(self, bd="5")
        AVDELAY_input.grid(row=8, column=2)

        hostmsg = ""
        msg = tk.Label(self, text=hostmsg, font=SMALL_FONT)
        msg.grid(row=9, columnspan=3)
        
        change_param = ttk.Button(self, text="Change Parameters", command=lambda: [send_data("AOOR", int(LRL_input.get()),\
                                        int(ATR_PWIDTH_input.get()), int(VENT_PWIDTH_input.get()), int(URL_input.get()),\
                                        int(VRP_input.get()), int(ARP_input.get()), int(ATRDUTY_input.get()), \
                                        int(VENTDUTY_input.get()), int(AVDELAY_input.get())), msg.config("Data Sent")])
        change_param.grid(row=0, column=0)
        back = ttk.Button(self, text="Return", command=lambda: controller.show_frame(HomeScreen))
        back.grid(row=1, column=0)

class VOOR(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        tk.Label(self, text="LRL", font=SMALL_FONT).grid(row=0, column=1)
        LRL_input = tk.Entry(self, bd="5")
        LRL_input.grid(row=0, column=2)

        tk.Label(self, text="ATR_PWIDTH", font=SMALL_FONT).grid(row=1, column=1)
        ATR_PWIDTH_input = tk.Entry(self, bd="5")
        ATR_PWIDTH_input.grid(row=1, column=2)

        tk.Label(self, text="VENT_PWIDTH", font=SMALL_FONT).grid(row=2, column=1)
        VENT_PWIDTH_input = tk.Entry(self, bd="5")
        VENT_PWIDTH_input.grid(row=2, column=2)

        tk.Label(self, text="URL", font=SMALL_FONT).grid(row=3, column=1)
        URL_input = tk.Entry(self, bd="5")
        URL_input.grid(row=3, column=2)

        tk.Label(self, text="VRP", font=SMALL_FONT).grid(row=4, column=1)
        VRP_input = tk.Entry(self, bd="5")
        VRP_input.grid(row=4, column=2)

        tk.Label(self, text="ARP", font=SMALL_FONT).grid(row=5, column=1)
        ARP_input = tk.Entry(self, bd="5")
        ARP_input.grid(row=5, column=2)

        tk.Label(self, text="ATRDUTY", font=SMALL_FONT).grid(row=6, column=1)
        ATRDUTY_input = tk.Entry(self, bd="5")
        ATRDUTY_input.grid(row=6, column=2)

        tk.Label(self, text="VENTDUTY", font=SMALL_FONT).grid(row=7, column=1)
        VENTDUTY_input = tk.Entry(self, bd="5")
        VENTDUTY_input.grid(row=7, column=2)

        tk.Label(self, text="AVDELAY", font=SMALL_FONT).grid(row=8, column=1)
        AVDELAY_input = tk.Entry(self, bd="5")
        AVDELAY_input.grid(row=8, column=2)

        hostmsg = ""
        msg = tk.Label(self, text=hostmsg, font=SMALL_FONT)
        msg.grid(row=9, columnspan=3)
        

        change_param = ttk.Button(self, text="Change Parameters", command=lambda: [send_data("VOOR", int(LRL_input.get()),\
                                        int(ATR_PWIDTH_input.get()), int(VENT_PWIDTH_input.get()), int(URL_input.get()),\
                                        int(VRP_input.get()), int(ARP_input.get()), int(ATRDUTY_input.get()), \
                                        int(VENTDUTY_input.get()), int(AVDELAY_input.get())), msg.config("Data Sent")])
        change_param.grid(row=0, column=0)
        back = ttk.Button(self, text="Return", command=lambda: controller.show_frame(HomeScreen))
        back.grid(row=1, column=0)

class AAIR(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        tk.Label(self, text="LRL", font=SMALL_FONT).grid(row=0, column=1)
        LRL_input = tk.Entry(self, bd="5")
        LRL_input.grid(row=0, column=2)

        tk.Label(self, text="ATR_PWIDTH", font=SMALL_FONT).grid(row=1, column=1)
        ATR_PWIDTH_input = tk.Entry(self, bd="5")
        ATR_PWIDTH_input.grid(row=1, column=2)

        tk.Label(self, text="VENT_PWIDTH", font=SMALL_FONT).grid(row=2, column=1)
        VENT_PWIDTH_input = tk.Entry(self, bd="5")
        VENT_PWIDTH_input.grid(row=2, column=2)

        tk.Label(self, text="URL", font=SMALL_FONT).grid(row=3, column=1)
        URL_input = tk.Entry(self, bd="5")
        URL_input.grid(row=3, column=2)

        tk.Label(self, text="VRP", font=SMALL_FONT).grid(row=4, column=1)
        VRP_input = tk.Entry(self, bd="5")
        VRP_input.grid(row=4, column=2)

        tk.Label(self, text="ARP", font=SMALL_FONT).grid(row=5, column=1)
        ARP_input = tk.Entry(self, bd="5")
        ARP_input.grid(row=5, column=2)

        tk.Label(self, text="ATRDUTY", font=SMALL_FONT).grid(row=6, column=1)
        ATRDUTY_input = tk.Entry(self, bd="5")
        ATRDUTY_input.grid(row=6, column=2)

        tk.Label(self, text="VENTDUTY", font=SMALL_FONT).grid(row=7, column=1)
        VENTDUTY_input = tk.Entry(self, bd="5")
        VENTDUTY_input.grid(row=7, column=2)

        tk.Label(self, text="AVDELAY", font=SMALL_FONT).grid(row=8, column=1)
        AVDELAY_input = tk.Entry(self, bd="5")
        AVDELAY_input.grid(row=8, column=2)

        hostmsg = ""
        msg = tk.Label(self, text=hostmsg, font=SMALL_FONT)
        msg.grid(row=9, columnspan=3)

        change_param = ttk.Button(self, text="Change Parameters", command=lambda: [send_data("AAIR", int(LRL_input.get()),\
                                        int(ATR_PWIDTH_input.get()), int(VENT_PWIDTH_input.get()), int(URL_input.get()),\
                                        int(VRP_input.get()), int(ARP_input.get()), int(ATRDUTY_input.get()), \
                                        int(VENTDUTY_input.get()), int(AVDELAY_input.get())), msg.config("Data Sent")])
        change_param.grid(row=0, column=0)
        back = ttk.Button(self, text="Return", command=lambda: controller.show_frame(HomeScreen))
        back.grid(row=1, column=0)

class VVIR(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        tk.Label(self, text="LRL", font=SMALL_FONT).grid(row=0, column=1)
        LRL_input = tk.Entry(self, bd="5")
        LRL_input.grid(row=0, column=2)

        tk.Label(self, text="ATR_PWIDTH", font=SMALL_FONT).grid(row=1, column=1)
        ATR_PWIDTH_input = tk.Entry(self, bd="5")
        ATR_PWIDTH_input.grid(row=1, column=2)

        tk.Label(self, text="VENT_PWIDTH", font=SMALL_FONT).grid(row=2, column=1)
        VENT_PWIDTH_input = tk.Entry(self, bd="5")
        VENT_PWIDTH_input.grid(row=2, column=2)

        tk.Label(self, text="URL", font=SMALL_FONT).grid(row=3, column=1)
        URL_input = tk.Entry(self, bd="5")
        URL_input.grid(row=3, column=2)

        tk.Label(self, text="VRP", font=SMALL_FONT).grid(row=4, column=1)
        VRP_input = tk.Entry(self, bd="5")
        VRP_input.grid(row=4, column=2)

        tk.Label(self, text="ARP", font=SMALL_FONT).grid(row=5, column=1)
        ARP_input = tk.Entry(self, bd="5")
        ARP_input.grid(row=5, column=2)

        tk.Label(self, text="ATRDUTY", font=SMALL_FONT).grid(row=6, column=1)
        ATRDUTY_input = tk.Entry(self, bd="5")
        ATRDUTY_input.grid(row=6, column=2)

        tk.Label(self, text="VENTDUTY", font=SMALL_FONT).grid(row=7, column=1)
        VENTDUTY_input = tk.Entry(self, bd="5")
        VENTDUTY_input.grid(row=7, column=2)

        tk.Label(self, text="AVDELAY", font=SMALL_FONT).grid(row=8, column=1)
        AVDELAY_input = tk.Entry(self, bd="5")
        AVDELAY_input.grid(row=8, column=2)

        hostmsg = ""
        msg = tk.Label(self, text=hostmsg, font=SMALL_FONT)
        msg.grid(row=9, columnspan=3)
        
        change_param = ttk.Button(self, text="Change Parameters", command=lambda: [send_data("VVIR", int(LRL_input.get()),\
                                        int(ATR_PWIDTH_input.get()), int(VENT_PWIDTH_input.get()), int(URL_input.get()),\
                                        int(VRP_input.get()), int(ARP_input.get()), int(ATRDUTY_input.get()), \
                                        int(VENTDUTY_input.get()), int(AVDELAY_input.get())), msg.config("Data Sent")])
        change_param.grid(row=0, column=0)
        back = ttk.Button(self, text="Return", command=lambda: controller.show_frame(HomeScreen))
        back.grid(row=1, column=0)

class DOOR(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        tk.Label(self, text="LRL", font=SMALL_FONT).grid(row=0, column=1)
        LRL_input = tk.Entry(self, bd="5")
        LRL_input.grid(row=0, column=2)

        tk.Label(self, text="ATR_PWIDTH", font=SMALL_FONT).grid(row=1, column=1)
        ATR_PWIDTH_input = tk.Entry(self, bd="5")
        ATR_PWIDTH_input.grid(row=1, column=2)

        tk.Label(self, text="VENT_PWIDTH", font=SMALL_FONT).grid(row=2, column=1)
        VENT_PWIDTH_input = tk.Entry(self, bd="5")
        VENT_PWIDTH_input.grid(row=2, column=2)

        tk.Label(self, text="URL", font=SMALL_FONT).grid(row=3, column=1)
        URL_input = tk.Entry(self, bd="5")
        URL_input.grid(row=3, column=2)

        tk.Label(self, text="VRP", font=SMALL_FONT).grid(row=4, column=1)
        VRP_input = tk.Entry(self, bd="5")
        VRP_input.grid(row=4, column=2)

        tk.Label(self, text="ARP", font=SMALL_FONT).grid(row=5, column=1)
        ARP_input = tk.Entry(self, bd="5")
        ARP_input.grid(row=5, column=2)

        tk.Label(self, text="ATRDUTY", font=SMALL_FONT).grid(row=6, column=1)
        ATRDUTY_input = tk.Entry(self, bd="5")
        ATRDUTY_input.grid(row=6, column=2)

        tk.Label(self, text="VENTDUTY", font=SMALL_FONT).grid(row=7, column=1)
        VENTDUTY_input = tk.Entry(self, bd="5")
        VENTDUTY_input.grid(row=7, column=2)

        tk.Label(self, text="AVDELAY", font=SMALL_FONT).grid(row=8, column=1)
        AVDELAY_input = tk.Entry(self, bd="5")
        AVDELAY_input.grid(row=8, column=2)

        hostmsg = ""
        msg = tk.Label(self, text=hostmsg, font=SMALL_FONT)
        msg.grid(row=9, columnspan=3)
        
        change_param = ttk.Button(self, text="Change Parameters", command=lambda: [send_data("DOOR", int(LRL_input.get()),\
                                        int(ATR_PWIDTH_input.get()), int(VENT_PWIDTH_input.get()), int(URL_input.get()),\
                                        int(VRP_input.get()), int(ARP_input.get()), int(ATRDUTY_input.get()), \
                                        int(VENTDUTY_input.get()), int(AVDELAY_input.get())), msg.config("Data Sent")])
        change_param.grid(row=0, column=0)
        back = ttk.Button(self, text="Return", command=lambda: controller.show_frame(HomeScreen))
        back.grid(row=1, column=0)

app = PacemakerApp()
app.mainloop()