from network import WLAN
import machine
import socket
import pycom
import time
import sys

# Sets up some variables we will use later
port = 12345

##############################################################################################################
# rcvSock Function
#   This function essentially blocks off time for the STA to send to it - roughly the time it takes
#   Note that we don't actually even receive the packet - just saves space on the AP side
#   Since we are using this to just monitor the traffic from USRP we dont need the individual packets
##############################################################################################################
def rcvSock():
    pycom.rgbled(0x12EB39)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    chrono = machine.Timer.Chrono()
    chrono.start()
    start = chrono.read()

    print("starttime:", start)
    while True:
        cur = chrono.read()
        if (cur - start) > 25.0:
            break
        #d = s.recvfrom(128)
        #print(d)

    end = chrono.read()
    print("finish time:", end)

    chrono.stop()
    s.close()
    return


#Set up our initial configurations for our AP
#   Main parts - use channel 1, put in AP mode, use external antenna, and set the bandwith to 20Mhz
wlan = WLAN()
wlan.init(mode=WLAN.AP, channel=1, antenna=WLAN.EXT_ANT, ssid='Pycom AP', bandwidth=WLAN.HT20)
wlan.ifconfig(id=1, config=('192.168.4.1', '255.255.255.0', '192.168.4.1', '0.0.0.0'))
settings = wlan.ifconfig(id=1)
wlan.wifi_protocol((1, 0, 0))

#print out the settings we are using
print("Gen Settings", wlan.ifconfig(id=1))
print("Channel", wlan.channel())
print("Bandwidth", wlan.bandwidth())
print("Wifi Proto", wlan.wifi_protocol())

pycom.heartbeat(False)
pycom.rgbled(0x12ADEB)


#Use the colors to display what is going on - blue means waiting for connection, turqouise means its receiving
#pycom.rgbled(0xFFD433)
#s = socket.socket()
while True:
    pycom.rgbled(0xFFD433)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
    print(settings[0], port)
    s.bind((settings[0], port))
    s.listen()

    #accept a connection from one of the STAs - then tell them to start transmitting
    print("waiting for connection")
    c, addr = s.accept()
    print('Got connection from', addr)
    message = b"start sending information"
    c.send(message)
    print("Start receiving")

    #after we notify them, close this initial socket, receive the packets, then reset the AP to conenct with new device
    c.close()
    s.close()
    rcvSock()
    #s.close()
    #sys.exit()
    machine.reset()


pycom.heartbeat(True)
