# startup:
# python wifiauto.py <interfejs>

from re import findall
from sys import argv, stdout, stdin
from time import sleep
from subprocess import call, check_output

INTERFACE = argv[1]
maxtxpower = 22

def info_txpower():
    info = str(check_output(['iwconfig', INTERFACE]))
    txinfo = findall('\d+',info)
    return(txinfo[13])

def info_quality():
    info = str(check_output(['iwconfig', INTERFACE]))
    quality = findall('\d+',info)
    return(quality[15])

def change_power(power):
    #call(['ifconfig', INTERFACE, 'down'])
    call(['iwconfig', INTERFACE, 'txpower', power])
    #call(['ifconfig', INTERFACE, 'up'])
    sleep(1)

def start():
    maxtxpower = info_txpower()
    quality = info_quality()
    print("Starting with TX-Power: " + str(maxtxpower) + " dBm and quality: " + str(quality) + "/70")
    
    while(1):
        if int(quality) <= 10 :
            change_power(str(maxtxpower))
        if int(quality) > 10 and int(quality) <= 25 : #80%
            power = 0.8 * float(maxtxpower)
            change_power(str(int(power)))
        if int(quality) > 25 and int(quality) <= 40 : #60%
            power = 0.6 * float(maxtxpower)
            change_power(str(int(power)))
        if int(quality) > 40 and int(quality) <= 55 : #40%
            power = 0.4 * float(maxtxpower)
            change_power(str(int(power)))
        if int(quality) > 55 :                        #20%
            power = 0.2 * float(maxtxpower)
            change_power(str(int(power)))
        
        txpower = info_txpower()
        quality = info_quality()
        sleep(5)
        print("Current TX-Power: " + str(txpower) + " dBm and quality: " + str(quality) + "/70")
        
try:
 start()
 except KeyboardInterrupt:
    change_power(str(maxtxpower)) #back to default value
    print("\nAuto Wifi power switcher shutting down...\n")

exit()
