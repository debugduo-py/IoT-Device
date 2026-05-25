import requests
import os
import subprocess
import Scanner
import json
import sender
import time
import traceback

def editDetails():
    try:

        send = 0

        with open("station_id.txt","r") as f:
            station_id = int(f.read().replace("\n","").replace(" ",""))

        # print(station_id)

        option = 0

        while option != 2:

            Scanner.printf(f"Station id:{station_id}\r\n  \r\n1) Change\r\n2) Don't Change")

            while 1:
                option = Scanner.get_selection()
                if option == 1 or option == 2:
                    break

            if option == 1:
                time.sleep(0.4)
                station_id = Scanner.getInput("Station id: ")
                send = 1
            elif option == 2:
                pass

        with open("machine_id.txt","r") as f:
            machine_id = int(f.read().replace("\n","").replace(" ",""))

        Scanner.printf(f"Machine id:{machine_id}\r\n  \r\n1) Change\r\n2) Don't Change")

        while 1:
            option = Scanner.get_selection()
            if option == 1 or option == 2:
                break

        if option == 1:
            time.sleep(0.4)
            machine_id = Scanner.getInput("Machine id: ")
            send = 1

        elif option == 2:
            pass

        with open("machine_id.txt","r") as f:
            machine_id_old = f.read()

        with open("station_id.txt","r") as f:
            station_id_old = f.read()

        text = {

                    "machine_id": machine_id,
                    "station_id": station_id,
                    "machine_id_old": machine_id_old,
                    "station_id_old": station_id_old
        }

        data = json.dumps(text)

        with open("server_ip.txt","r") as f:
            ip = f.read().replace("\n","").replace(" ","")

        if ip != "":
            pass

        else:
            ip = sender.findServer()

        try:
            print("Sent data")
            response = requests.post(f"http://{ip}/iot/devices.php", data={"message": data}, timeout=5)

            Scanner.printf("Waiting for\r\n confirmation\r\n from server")

            if "success" in response.text:
                print("Server sent success")

                with open("station_id.txt","w") as f:
                    f.write(f"{station_id}")

                print("wrote data in station id")

                with open("machine_id.txt","w") as f:
                    f.write(f"{machine_id}")

                print("wrote data in machine id")

                Scanner.type("Success!")

            elif "exists" in response.text:
                Scanner.printf(f"Another device\r\nexists for:\r\nstation id: {station_id}\r\nmachine id: {machine_id}")

            elif "query failed" in response.text:
                Scanner.printf("Server side \r\nquery failed")

            print(f"response: {response.text}")
        except:
                Scanner.printf("server couldn't\r\nrecieve data")


        time.sleep(1.5)

    except Exception as e:
        print(f"Error: {e}")
        traceback.print_exc()


def deleteDetails():
    try:

        send = 0

        with open("station_id.txt","r") as f:
            station_id = int(f.read().replace("\n","").replace(" ",""))

        with open("station_id.txt","w") as f:
            f.write("0")

        with open("machine_id.txt","r") as f:
            machine_id = int(f.read().replace("\n","").replace(" ",""))

        with open("machine_id.txt","w") as f:
            f.write("0")


        text = {

                    "machine_id": machine_id,
                    "station_id": station_id
        }

        data = json.dumps(text)

        with open("server_ip.txt","r") as f:
            ip = f.read().replace("\n","").replace(" ","")

        if ip != "":
            pass

        else:
            ip = sender.findServer()

        try:
            print("Sent data")
            response = requests.post(f"http://{ip}/iot/devices.php", data={"removal": data}, timeout=5)
            print(response.text)
            if "success" in response.text:
                print("Server sent success")

                print("wrote data in machine id")

            elif "query failed" in response.text:
                Scanner.printf("Server side \r\nquery failed")

            print(f"response: {response.text}")
        except:
                Scanner.printf("server couldn't\r\nrecieve data")


        time.sleep(1.5)

    except Exception as e:
        print(f"Error: {e}")
        traceback.print_exc()
