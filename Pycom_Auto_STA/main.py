from network import WLAN
import machine
import socket
import pycom
import time
import uos
import sys

#Important Variables - who we are sending to and who we are
dIP = "192.168.4.1"
sIP = "192.168.4.3"
port = 12345

#########################################################################################################
# sendSocket function
#   This function handles the sending of informaiton to the AP
#       Starts by creating a socket between the two devices
#       Goes on to send a random assortment of messages to the AP
#       In our case enough was sent that the device runs out of memory and stops but sending continues
##########################################################################################################
def sendSocket():
    #Working with UDP sockets
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    running = True
    pycom.heartbeat(False)
    pycom.rgbled(0x007f00)

    print("sending messages")

    #Randomish message is sent each time
    messages = [b"hello", b"beach", b"crown", b"field", b"whole"]
    chrono = machine.Timer.Chrono()
    chrono.start()
    start = chrono.read()
    while running:
        cur = chrono.read()
        if (cur - start) > 25.0:
            running = False
        time.sleep(0.01)
        ind = int((uos.urandom(1)[0] / 256) * 5)
        s.sendto(messages[ind] * 610, (dIP, 12345))

    s.close()
    return

#####################################################################################
# connectToAp function
#   Takes in the WLAN object that we created earlier - has all of our configurations
#       Function works by trying to connect to the AP, wont stop until it does
#####################################################################################
def connectToAp(wlan):
    nets = wlan.scan()
    print("UDP")

    while not wlan.isconnected():
        print("Finding the network..")
        nets = wlan.scan()

        for net in nets:
            print(net)
            pycom.heartbeat(False)
            pycom.rgbled(0x7f7f00)

            #Preset network to connect to
            if net.ssid == 'Pycom AP':
                print('Network found!')

                #Attempt a connection
                wlan.connect(net.ssid, auth=None, timeout=1000)
                print("connecting...")
                pycom.rgbled(0x12A1DA)

                #Wait while its not connected until it succeeds
                while not wlan.isconnected():
                    machine.idle() # save power while waiting
                print('WLAN connection succeeded!')

                return

#############################################################
# Main part of program -
#   1. sets up the device
#   2. connects to AP
#   3. connects to socket and sends
##############################################################

#Set into station mode and set the antenna
wlan = WLAN()

wlan.init(mode=WLAN.STA, bandwidth=WLAN.HT20, antenna=WLAN.EXT_ANT, channel=1)
wlan.ifconfig(id=0, config=('192.168.4.3', '255.255.255.0', '192.168.4.1', '0.0.0.0'))
# mac = bytearray([0xAE, 0x77, 0x88, 0x99, 0x22, 0x44])
# wlan.mac(mac, WLAN.STA)
wlan.wifi_protocol((1, 0, 0))
settings = wlan.ifconfig(id=0)
print("Gen Settings", wlan.ifconfig(id=0))
print("Channel", wlan.channel())
print("Bandwidth", wlan.bandwidth())
print("Wifi proto", wlan.wifi_protocol())
print(wlan.mac())

#Start scanning through the networks
connectToAp(wlan)
print(wlan.ifconfig())

#Start setting up a socket to AP if successfully connected
#This is the automated version - after we are connected to the AP we will attempt transmission
if wlan.isconnected():
    while True:
        print(wlan.ifconfig())
        #s = socket.socket()
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)

        #Tries to connect to the socket - if the AP is busy this will not work - hence the loop
        try:
            s.connect((dIP, port))

            break
        #If AP is busy then wait for a little and try again
        except:
            s.close()
            time.sleep(2)
            #s.close()

    #Once we get access to the AP wait for it to give us the go message to transmit
    print("waiting for message from AP")
    inp = s.recv(1024)
    print(inp)

    print("got mess and moving on")
    #Close the socket and start the UDP transmission
    print("about to send")
    s.close()
    print("sending")
    sendSocket()

    wlan.disconnect()           # Disconnect from the wifi
    pycom.heartbeat(True)
