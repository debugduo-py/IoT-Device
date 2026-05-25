# IoT Data Collection Device

A lightweight IoT data collection device built on the Raspberry Pi Zero W, featuring a custom hardware abstraction layer, smart server discovery, local backup, and a web-based monitoring dashboard.

---

## Project Structure

```
├── main.py            # Entry point
├── Scanner.py         # Hardware abstraction layer (LCD + keypad)
├── sender.py          # Network, server discovery, data transmission
├── connect.py         # WiFi management
├── edit_details.py    # Device configuration
├── station_id.txt     # Stores station ID and machine ID in JSON format
├── machine_id.txt     # Stores machine id
└── server_ip.txt      # Stores last known server IP
```

---

## Function Reference

### `Scanner.py`

Hardware abstraction layer for the LCD display and GPIO keypad. All user interaction on the physical device goes through this file.

---

#### `displayOff()`

Turns off the LCD backlight and clears the display.

```python
Scanner.displayOff()
```

---

#### `printf(text)`

Clears the LCD display and prints new content. This is the primary way to show information to the user on the device.

| Parameter | Type | Description |
|---|---|---|
| `text` | `str` | The text to display on the LCD |

```python
Scanner.printf("Hello World")
Scanner.printf("Station ID: 3\r\nMachine ID: 7")
```

> Use `\r\n` to move to the next line on the LCD.

---

#### `clrscr()`

Clears all content currently shown on the LCD display without printing anything new.

```python
Scanner.clrscr()
```

---

#### `type(text)`

Same as `printf()` but writes each character one by one, creating a typewriter animation effect on the LCD.

| Parameter | Type | Description |
|---|---|---|
| `text` | `str` | The text to animate onto the LCD |

```python
Scanner.type("SUCCESS!")
```

---

#### `getInput(text)`

A hardware equivalent of Python's built-in `input()` function, tailored specifically for this IoT device. Displays a prompt on the LCD and waits for the user to type a number using the physical keypad. Supports backspace and enter.

| Parameter | Type | Description |
|---|---|---|
| `text` | `str` | The prompt shown on the LCD before the user types |

**Returns:** `int` — the number entered by the user.

```python
qty = Scanner.getInput("Quantity: ")

if qty != "escape":
    # proceed with qty
```

> This function only works on this specific device. It is not a general-purpose input function.

---

#### `get_selection()`

Waits for the user to press a button on the keypad and returns which button was pressed. Used throughout the program for menu navigation and option selection.

**Returns:** `int` — the number corresponding to the button pressed.

```python
Scanner.printf("1) Yes\r\n2) No")
option = Scanner.get_selection()

if option == 1:
    print("u seected Yes")
elif option == 2:
    print("u selected no")
```

> Buttons 7 and 8 on the keypad are reserved for shutdown and restart confirmation menus respectively and are handled internally by this function.

---

### `connect.py`

Handles WiFi network management on the device.

---

#### `Networks()`

Rescans for available WiFi networks, displays them on the LCD, and lets the user select which network to connect to. If the selected network requires a password, the user is prompted to enter it via the keypad.

```python
connect.Networks()
```

**What it does step by step:**
1. Triggers a fresh WiFi rescan via `nmcli`
2. Retrieves and displays the list of available networks on the LCD
3. User selects a network using the keypad
4. Attempts to connect without a password first
5. If connection fails, prompts the user to enter the password

---

### `sender.py`

Handles all data transmission, server discovery, and local backup management.

---

#### `storeBackup(data)`

Stores data locally in the device's MariaDB database when the server is unreachable. The data is saved alongside a timestamp so it can be sent to the server later when connectivity is restored.


#### `perform_network_scan()`

Scans the local network using `arp-scan` and returns a list of IP addresses of all devices currently connected to the same network. Significantly faster than traditional `nmap` scanning.

```python
perform_network_scan()
# populates the global all_ips list
```

> Uses `arp-scan --localnet --plain` which completes a full subnet scan in approximately 2 seconds compared to 10–30 seconds with nmap.

---

#### `check_ip(ip)`

Checks whether a given IP address belongs to the server by sending a request and verifying the server's response string.

| Parameter | Type | Description |
|---|---|---|
| `ip` | `str` | IP address to check |

```python
check_ip("192.168.1.105")
# adds to valid_ips if confirmed as server
```

> This function is designed to be called in parallel via `ThreadPoolExecutor`. Do not call it sequentially for multiple IPs.

---

#### `findServer(scan_times)`

The main server discovery function. First checks if the previously known server IP is still valid. If not, performs a full parallel network scan to locate the server.

| Parameter | Type | Description |
|---|---|---|
| `scan_times` | `int` | Number of scan attempts before prompting user to retry or cancel |

**Returns:** `str` — the IP address of the confirmed server.

**Discovery flow:**
```
Check cached IP (server_ip.txt)
        │
        ├── still valid → return immediately
        │
        └── not valid → run arp-scan
                              │
                              └── check all IPs in parallel (50 workers)
                                        │
                                        ├── 1 server found → save and return
                                        ├── 0 found → prompt retry
                                        └── 2+ found → warn unsafe, prompt retry
```

```python
ip = sender.findServer(2)
```

---

#### `sendData()`

Prompts the user to enter a quantity via the keypad, then sends the collected data (machine ID, station ID, quantity) to the server in JSON format. If the server is unreachable, the data is automatically saved to the local backup database.

```python
sender.sendData()
```

**Payload format:**
```json
{
    "machine_id": "3",
    "station_id": "7",
    "quantity": 150
}
```

**Failure handling:**
- Server unreachable → stored in local `backup` database
- After storing backup → attempts to rediscover server via `findServer()`

---

#### `sendBackup()`

Retrieves all locally stored backup records from the device's MariaDB database and sends them to the server one by one in JSON format. If all records are sent successfully, the local backup table is cleared.

```python
sender.sendBackup()
```

**Behaviour:**
- Calls `findServer()` first to confirm server is reachable
- Sends each backup record individually
- On first failed transmission — stops and preserves remaining records
- On full success — deletes all records from local database

---

### `edit_details.py`

Handles device identity configuration.

---

#### `editDetails()`

Allows the user to view and update the device's machine ID and station ID via the LCD and keypad. After the user confirms changes, the new values are sent to the server. The server checks whether the combination of machine ID and station ID is already taken by another device — if it is, the update is rejected and the user is notified.

```python
edit_details.editDetails()
```

**Validation:**
- Duplicate machine ID + station ID combination → server rejects, device notifies user
- Unique combination → server accepts, local config files updated

---

#### `deleteDetails()`

Resets the device's machine ID and station ID to `0` on both the device and the server's database, effectively deregistering the device.

```python
edit_details.deleteDetails()
```

---

## Hardware

| Component | Details |
|---|---|
| Main board | Raspberry Pi Zero W |
| Display | 16×4 I2C LCD (PCF8574 backpack) |
| Input | 13-button GPIO keypad |
| PCB | Hand-soldered dotted perfboard |
| OS | sand OS |

---

## Notes

- This device is designed for local network operation only
- All data transmission is over HTTP on the local LAN
- Backup data is stored locally in MariaDB when server is unreachable
- Server discovery uses ARP scanning and is limited to the local subnet
