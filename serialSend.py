import serial
ser = serial.Serial(
    port='COM8',\
    baudrate=115200)


Start = 9
Start = Start.to_bytes(1, byteorder='big')

Mode =1
Mode = Mode.to_bytes(1, byteorder='big')

LRL = 60
LRL = LRL.to_bytes(1, byteorder='big')

ATR_PWIDTH = 10
ATR_PWIDTH = ATR_PWIDTH.to_bytes(2, byteorder='little')

VENT_PWIDTH = 10
VENT_PWIDTH = VENT_PWIDTH.to_bytes(2, byteorder='little')

URL = 120
URL = URL.to_bytes(1, byteorder='little')

VRP = 320
VRP = VRP.to_bytes(2, byteorder='little')

ARP = 250
ARP = ARP.to_bytes(2, byteorder='little')

ATRDUTY = 80
ATRDUTY = ATRDUTY.to_bytes(8, byteorder='little')

VENTDUTY = 80
VENTDUTY = VENTDUTY.to_bytes(8, byteorder='little')

AVDELAY = 150
AVDELAY = AVDELAY.to_bytes(2, byteorder='little')

send = (Start + Mode + LRL + ATR_PWIDTH + VENT_PWIDTH + URL + VRP + ARP + ATRDUTY + VENTDUTY + AVDELAY ) 

print("connected to: " + ser.portstr)
ser.write(send) 


