import RPi.GPIO as pins
import time
import os
from RPLCD.i2c import CharLCD
import traceback
import edit_details

try:

    lcd = CharLCD('PCF8574', 0x27, cols=16, rows=4)
    pins.cleanup()
    pins.setmode(pins.BCM)
    pins.setup(21,pins.IN,pull_up_down = pins.PUD_UP)
    pins.setup(20,pins.IN,pull_up_down = pins.PUD_UP)
    pins.setup(7,pins.IN,pull_up_down = pins.PUD_UP)
    pins.setup(1,pins.IN,pull_up_down = pins.PUD_UP)
    pins.setup(16,pins.IN,pull_up_down = pins.PUD_UP)
    pins.setup(12,pins.IN,pull_up_down = pins.PUD_UP)
    pins.setup(8,pins.IN,pull_up_down = pins.PUD_UP)
    pins.setup(25,pins.IN,pull_up_down = pins.PUD_UP)
    pins.setup(24,pins.IN,pull_up_down = pins.PUD_UP)
    pins.setup(23,pins.IN,pull_up_down = pins.PUD_UP)
    pins.setup(18,pins.IN,pull_up_down = pins.PUD_UP)
    pins.setup(15,pins.IN,pull_up_down = pins.PUD_UP)
    pins.setup(14,pins.IN,pull_up_down = pins.PUD_UP)
    pins.setup(27,pins.IN,pull_up_down = pins.PUD_UP)

except Exception as e:
    print(f"Error: {e}")
    traceback.print_exc()

def displayOff():
    try:
        lcd.backlight_enabled = False
        lcd.clear()
    except Exception as e:
        print(f"Error: {e}")
        traceback.print_exc()

def printf(text):
    try:
        lcd.clear()
        lcd.write_string(text)

    except Exception as e:
        print(f"Error: {e}")
        traceback.print_exc()

def showOS_branding():
    lcd.cursor_mode = 'blink'  # Blinking block cursor

    lcd.cursor_pos = (0,2)
    text = "Saeed"

    for i in range(len(text)):
            lcd.write_string(text[i])
            time.sleep(0.1)




def clrscr():
    try:

        lcd.clear()

    except Exception as e:
        print(f"Error: {e}")
        traceback.print_exc()

def type(text):
    try:

        lcd.clear()
        for i in range(len(text)):

            lcd.write_string(text[i])
            time.sleep(0.1)

    except Exception as e:
        print(f"Error: {e}")
        traceback.print_exc()


def getInput(text):

    try:

        numpad = [27,18,15,14,8,25,24,7,1,16,12,23,21,20]

        last_states = [pins.HIGH]*14

        current_states = [pins.HIGH]*14
        word = ""
        try:
            m = 0
            while m == 0:


                lcd.cursor_pos = (0, 0)
                lcd.write_string(f"{text}{word}")

                for i in range(14):
                    current_states[i] = pins.input(numpad[i])

                    if last_states[i] == pins.HIGH and current_states[i] == pins.LOW:
                        if i == 12:
                            word = word[:-1]
                            lcd.clear()
                            lcd.write_string(f"{text}{word}")
                        elif i == 10:
                            m = 1
                            break
                        elif i == 13:
                            m = 1
                            return("escape")
                            break

                        else:
                            word = f"{word}{i}"


                for i in range(14):
                    last_states[i] = current_states[i]

                time.sleep(0.001)

        except KeyboardInterrupt:
            print("terminating")


        return int(word)

    except Exception as e:
        print(f"Error: {e}")
        traceback.print_exc()

def get_selection():

    try:

        numpad = [27,18,15,14,8,25,21,20]

        last_states = [pins.HIGH]*8

        current_states = [pins.HIGH]*8

        m = 0
        print("Waiting for button press")

        while m == 0:

            for i in range(8):

                current_states[i] = pins.input(numpad[i])

                if last_states[i] == pins.HIGH and current_states[i] == pins.LOW:
                    if i != 6 and i != 7:

                            print("reached")
                            m = 1
                            return i
                            break

                    elif i == 6:

                        printf("Shutdown ?\r\n  \r\n1. YES\r\n2. NO")

                        opt = get_selection()

                        if opt == 1:
                            displayOff()
                            edit_details.deleteDetails()
                            pins.cleanup()

                            os.system("sudo shutdown now")

                        elif opt == 2:
                            m = 1
                            break

                    elif i == 7:
                        print("supposed to restart")
                        printf("Restart ?\r\n  \r\n1. YES\r\n2. NO")

                        opt = get_selection()

                        if opt == 1:
                            printf("RESTARTING...")
                            pins.cleanup()
                            os.system("sudo reboot")

                        elif opt == 2:
                            m = 1
                            break

            # print("reached1")
            for i in range(5):
                last_states[i] = current_states[i]

            time.sleep(0.001)
        print(f"Displaying {i+1}")

    except Exception as e:
        print(f"Error: {e}")
        traceback.print_exc()
