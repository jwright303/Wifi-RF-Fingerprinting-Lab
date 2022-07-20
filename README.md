# Wifi-RF-Fingerprinting-Lab

## Description
This repository contains code I developed for the WiFi fingerprinting lab I have been working in as an undergraduate. The repository is broken into two main parts: code for the access point (AP) and code for the station nodes (STA's). The code works by having one of the Pycom devices act as the access point to which the other pycom devices can connect to. The other pycom devices with the STA code then connect to the AP and take turns creating a TCP connection with the AP. Once the TCP conneciton is made the STA starts transmitting a randomized message to the AP. These transmission signals were then collected by a USRP which are then being used as a part of a larger dataset. 

## Use
To use this code it is necessary first to obtain Pycom devices. In this lab, Lopy and Fipy Pycom devices are the two variants that are used. To get the devices to start running the code one must upload one of the folders (Pycom_Auto_AP or Pycom_Auto_STA) to the Pycom device. This can be done with software such as [Atom](https://atom.io).

## Purpose
In our lab, this code is used to get the Pycom devices to transmit wifi packets to the AP so that we can observe and collect the transmissions. These transmissions are then used to create a dataset to facilitate the training of machine learning algorithms to identify the devices based on the wifi signals they transmit. So far I have collected data for two scenarios: indoor and outdoor. In each scenario the transmitters are placed three meters from the USRP and transmit a random message via the UDP protocol for 2 seconds. We collected 5 transmissions for all 50 devices each day for 5 non-consecutive days.
