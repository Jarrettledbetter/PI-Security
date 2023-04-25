from signal import signal, SIGTERM, SIGHUP
from rpi_lcd import LCD
import time
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

lcd = LCD()
reader = SimpleMFRC522()
GPIO.cleanup()

def LCD_conf():
    #defines a safe_exit function that would enact termination procedure
    def safe_exit(signum, frame):
        exit(0)

    #if a SIGHTERM or SIGHUP signal is present, the safe_exit function would run
    signal(SIGTERM, safe_exit)
    signal(SIGHUP, safe_exit)
    
def Keypad_conf():
    global readKeypad
    L1 = 17
    L2 = 18
    L3 = 27
    L4 = 22

    C1 = 23
    C2 = 24
    C3 = 25
    C4 = 4

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(L1, GPIO.OUT)
    GPIO.setup(L2, GPIO.OUT)
    GPIO.setup(L3, GPIO.OUT)
    GPIO.setup(L4, GPIO.OUT)

    GPIO.setup(C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(C4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def readLine(line, characters):
        GPIO.output(line, GPIO.HIGH)
        if(GPIO.input(C1) == 1):
            return characters[0]
        if(GPIO.input(C2) == 1):
            return characters[1]
        if(GPIO.input(C3) == 1):
            return characters[2]
        if(GPIO.input(C4) == 1):
            return characters[3]
        GPIO.output(line, GPIO.LOW)

    def readKeypad():
        while True:
            key = readLine(L1, ["1","2","3","A"])
            if key:
                return key
            key = readLine(L2, ["4","5","6","B"])
            if key:
                return key
            key = readLine(L3, ["7","8","9","C"])
            if key:
                return key
            key = readLine(L4, ["*","0","#","D"])
            if key:
                return key
            time.sleep(0.1)
    return readKeypad


def start_up():
    LCD_conf()
    lcd.text("Howdy Partner!", 1)
    lcd.text("Welcome Home!", 2)
    time.sleep(5)
    lcd.text("Input Pin: #", 1)
    lcd.text("Scan Card: *", 2)
    readKeypad = Keypad_conf()
    authentication(readKeypad)
    time.sleep(5)
    lcd.clear()
    time.sleep(25)
    start_up()

def authentication(readKeypad):
    code = ""
    pin = "1010"
    attempts = 3
    accessible = False
    try:
        while True:
            k = readKeypad()
            if k == "#":
                while attempts != 0:
                    if attempts != 0:
                        lcd.clear()
                        lcd.text("Please type Pin:", 1)
            
                        for i in range(4):
                            key = None
                            while key is None:
                                key = readKeypad()
                                time.sleep(0.1)
                            code += key
                            lcd.text(code, 2)

                        if code == pin:
                            lcd.clear()
                            lcd.text("Correct Pin", 1)
                            lcd.text("Please Wait :)", 2)
                            time.sleep(5)
                            lcd.clear()
                            lcd.text("Welcome in", 1)
                            return True
                        else:
                            lcd.clear()
                            attempts -= 1
                            lcd.text("Incorrect Pin", 1)
                            lcd.text("You have " + str(attempts) + " left", 2)
                            time.sleep(2)
                            code = ""
                    else:
                        lcd.clear()
                        lcd.text("Too Many Tries",1)
                        lcd.text("Try in 5 minutes", 2)
                        time.sleep(300)
                        attempts = 3
            elif k == "*":
                while attempts != 0:
                    lcd.clear()
                    lcd.text(" Please Present ", 1)
                    lcd.text("  Your Keycard  ", 2)
                    try:
                        text = str(reader.read()[1])
                        keypass = text[:4]
                        if keypass == pin:
                            lcd.clear()
                            lcd.text("Welcome In", 1)
                            return True
                        else:
                            print(keypass)
                            lcd.clear()
                            lcd.text("Scan Fail", 1)
                            lcd.text("Invalid Keypass", 2)
                            time.sleep(5)
                            lcd.clear()
                            attempts -= 1
                            lcd.text("You have " + str(attempts) + " left", 1)
                            time.sleep(2)
                    finally:
                        GPIO.cleanup()
                    if attempts == 0:
                        lcd.clear()
                        lcd.text("Too Many Tries",1)
                        lcd.text("Try in 5 minutes", 2)
                        time.sleep(300)
                        attempts = 3
                        authentication()
            else:
                lcd.clear()
                lcd.text("Invalid Reply", 1)
                lcd.clear()
                start_up()
            
    except Exception as e:
        print("Error Occurred{}".format(str(e)))
        time.sleep(1)
    finally:
        GPIO.cleanup()
        
        
start_up()
