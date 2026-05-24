import requests
import json
import os
import subprocess
import time
import pymysql
from datetime import datetime
import Scanner
import traceback
from concurrent.futures import ThreadPoolExecutor


def storeBackup(data):
        try:
                conn = pymysql.connect(host='localhost',user='pyuser',password='123456',database='backup')

                cursor = conn.cursor()

                cursor.execute(f"insert into backups values('{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}','{data}')")

                conn.commit()
                conn.close()

        except Exception as e:
            print(f"Error: {e}")
            traceback.print_exc()

valid_ips = []
all_ips = []

def perform_network_scan():
    report = subprocess.getoutput("  | awk '{print $1}'").replace("WARNING: Cannot open MAC/Vendor file ieee-oui.txt: Permission denied", "").replace("WARNING: Cannot open MAC/Vendor file mac-vendor.txt: Permission denied","")

    ip = ""

    print(report)
    # Scanner.printf("\r\nScan complete \r\nFinding server")
    print("ip data retrieved | sorting everything out")

    for i in range(len(report)):
            if report[i] != "\n":
                    ip = f"{ip}{report[i]}"
            else:
                    all_ips.append(ip)
                    ip = ""
    all_ips.append(ip)

def check_ip(ip):
    global valid_ips, all_ips
    try:
        print(f"checking for {ip}")
        response = requests.post(f"http://{ip}/iot/main.php", timeout=10)

        if "oui, je suis le server" in response.text:
            valid_ips.append(ip)
    except:
        pass


def findServer(scan_times):
        global valid_ips, all_ips
        try:

                p = 0
                Scanner.printf("Checking ip\r\nvalidity")
                print("Checking old ip validity")

                try:
                        print("reading old ip")

                        with open("server_ip.txt","r") as f:
                                ip_old = f.read()

                        print("read old ip")

                        result = requests.post(f"http://{ip_old}/iot/main.php", timeout=10)

                        print(f"curling ip {ip_old}")
                        if "oui, je suis le server" in result.text:
                                print("ip is valid")
                                p = 1
                                return ip_old
                except Exception as e:
                        print(f"Error: {e}")
                        traceback.print_exc()

                if p == 0:

                        a = 0
                        while a == 0:
                                Scanner.printf("Scanning network")
                                perform_network_scan()
                                Scanner.printf("Scanning network\r\nFinding Server")

                                with ThreadPoolExecutor(max_workers=50) as executor:
                                   list(executor.map(check_ip,all_ips))

                                try:
                                        all_ips = []
                                        if len(valid_ips) != 1:

                                                if len(valid_ips) > 1:
                                                        Scanner.printf(f"{len(valid_ips)} servers\r\nfound, unsafe!")

                                                valid_ips = []
                                                Scanner.printf("1) Rescan\r\n2) Cancel")
                                                option = Scanner.get_selection()
                                                if option == 1:
                                                        pass
                                                elif option == 2:
                                                        a = 1
                                        elif len(valid_ips) == 1:

                                                ip = valid_ips[0]
                                                valid_ips = []
                                                with open("server_ip.txt","w") as f:
                                                        f.write(ip)
                                                return ip



                                except Exception as e:
                                        print(f"Error: {e}")

                                        Scanner.printf("1) Rescan\r\n2) Cancel")
                                        option = Scanner.get_selection()
                                        if option == 1:
                                                pass
                                        elif option == 2:
                                                a = 1
        except Exception as e:
            print(f"Error: {e}")
            traceback.print_exc()

def sendData():

        try:

                with open("server_ip.txt","r") as f:
                        ip = f.read()

                os.system('clear')
                print("taking in values")
                # data to b sent, if u want to change this then change database also
                # TO CHANGE DATA,...(in php file refer to the $table = (some stuff), that is also decorated with sm comments)
                # -----------------------------------------------

                with open("details.json","r") as f:
                    details = json.load(f)

                station_id = details["station_id"]
                machine_id = details["machine_id"]
                qty = Scanner.getInput("Quantity: ")

                if qty != "escape":
                        text = {
                                "machine_id": machine_id,
                                "station_id": station_id,
                                "quantity": qty
                        }
                        # -----------------------------------------------

                        print("done taking values | converting to json")

                        data = json.dumps(text)

                        print("converted to json | sending data")

                        try:
                                Scanner.printf("Data sent")
                                response = requests.post(f"http://{ip}/iot/main.php", data={"message": data}, timeout=1.5)
                                print("data sent")

                                if "success" in response.text:
                                        print("stored successfully | hit enter to proceed")
                                        Scanner.printf("Data sent,\r\nData Stored")
                                        time.sleep(0.25)
                                        Scanner.type("SUCCESS!")
                                else:
                                        Scanner.printf("Data sent,\r\nData NOT Stored\r\nby server")
                                        time.sleep(0.8)
                                        print("data sent but not stored in database, storing in local db")
                                        storeBackup(data)
                                        Scanner.printf("Stored in backup")
                        except Exception as e:
                                print(f"Error: {e}")

                                print("server couldn't recieve data, storing in local db")
                                storeBackup(data)
                                Scanner.printf("Server couldn't recieve\r\nStored in backup")
                                time.sleep(0.8)
                                Scanner.printf("Re-Finding server")
                                findServer(1)
                                print("stored in backup successfully")
                        time.sleep(0.4)

        except Exception as e:
            print(f"Error: {e}")
            traceback.print_exc()

def sendBackup():

        try:

                ip = findServer(2)

                conn = pymysql.connect(host='localhost',user='pyuser',password='123456',database='backup')
                cursor = conn.cursor()

                cursor.execute("select * from backups")

                data = cursor.fetchall()

                conn.commit()

                for i in range(len(data)):
                        print(data[i])

                status = "success"
                for i in range(len(data)):
                        response = requests.post(f"http://{ip}/iot/backup_script.php", data={"message": json.dumps(data[i])})
                        print("data sent")
                        Scanner.printf("Data sent")

                        if "success" not in response.text:
                                print(f"no valid response --> {response.text}  ")
                                Scanner.printf("Data sent\r\nUnsuccessful")
                                status = "unsuccessful"
                                break


                if status == "success":
                        cursor.execute("delete from backups")
                        conn.commit()
                
                conn.close()

        except Exception as e:
            print(f"Error: {e}")
            traceback.print_exc()


