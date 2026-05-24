import Scanner
import time
import subprocess
import os
import edit_details
import sender
import connect
import traceback
import json

try:

    w = 0
    while w == 0:
        currently_connected = subprocess.getoutput("iwgetid -r")
        Scanner.printf(f"Network: \r\n{currently_connected}\r\n1[Yes] 2[Change]")
        opt = Scanner.get_selection()

        if opt == 2:
            Scanner.printf("Loading...")
            connect.Networks()
        elif opt == 1:
            w = 1


    sender.findServer(2)

    while 1:
        Scanner.clrscr()
        Scanner.printf("1. Connect\r\n2. Edit Details\r\n3. Send Backup\r\n4. Send Data")
        time.sleep(0.6)

        option = Scanner.get_selection()
        # except:
        #     os.system("sudo fuser -k /dev/gpiochip0")
        #     option = Scanner.get_selection()

        # print("exited")
        Scanner.clrscr()
        if option == 1:

            while 1:
                Scanner.printf("1.Change network\r\n2.Find Server\r\n3.Exit")
                option1 = Scanner.get_selection()

                if option1 == 1:
                    Scanner.printf("Loading...")
                    connect.Networks()
                elif option1 == 2:
                    sender.findServer(1)
                elif option1 == 3:
                    break

        elif option == 2:
            edit_details.editDetails()
        elif option == 3:
            sender.sendBackup()
        elif option == 4:
            with open("details.json","r") as f:
                details = json.load(f)

            station_id = details["station_id"]
            machine_id = details["machine_id"]


            if station_id != 0 and machine_id != 0:
                sender.sendData()
            else:
                Scanner.printf("Details not \r\nset!")
                time.sleep(0.75)

except Exception as e:
    print(f"Error: {e}")
    traceback.print_exc()
