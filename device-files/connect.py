import os
import subprocess
import Scanner
import time
import traceback

def Networks():

    try:

        os.system("sudo nmcli device wifi rescan")
        raw_nets = subprocess.getoutput("nmcli -t -f SSID device wifi list | sort -u")
        raw_signals = subprocess.getoutput("nmcli -t -f SIGNAL device wifi list | sort -u")

        networks = []
        signals = []

        leave = 0
        network = ""

        for i in range(len(raw_nets)):

            if raw_nets[i] != "\n":
                network = f"{network}{raw_nets[i]}"
            else:
                networks.append(network)
                network = ""

        networks.append(network)

        print(networks)
        n = 0
        while n == 0:

            display_networks = ""

            for i in range(len(networks)):
                # os.system("clear")
                display_networks = f"{i+1}) {networks[i]}"

                try:
                    display_networks = f"{display_networks}\r\n{i+2}) {networks[i+1]}"
                except:
                    pass

                Scanner.printf(display_networks)

                if i == 0:
                    i = 1
                print(f"i = {i}")

                opt = Scanner.get_selection()

                if opt == 0:
                    pass
                elif opt == i:

                    Scanner.printf(f"Connecting to \r\n{networks[i-1]}")
                    status = subprocess.getoutput(f"sudo nmcli dev wifi connect \'{networks[i-1]}\'")
                    print(f"Command : sudo nmcli dev wifi connect \'{networks[i-1]}\'")
                    print(status)

                    if "successfully" not in status:
                        Scanner.clrscr()
                        status = subprocess.getoutput(f"sudo nmcli dev wifi connect \'{networks[i-1]}\' password \'{Scanner.getInput(f"Password:\r\n")}\' ")
                        print(status)
                     

                    
                    n = 1

                    break

                elif opt == i+1:

                    Scanner.printf(f"Connecting to \r\n{networks[i]}")

                    status = subprocess.getoutput(f"sudo nmcli dev wifi connect \'{networks[i]}\'")

                    if "successfully" not in status:
                        Scanner.clrscr()
                        os.system(f"sudo nmcli dev wifi connect \'{networks[i]}\' password \'{Scanner.getInput(f"Password:\r\n")}\' ")
                

                    n = 1

                    break
                    
    except Exception as e:
        print(f"Error: {e}")
        traceback.print_exc()

