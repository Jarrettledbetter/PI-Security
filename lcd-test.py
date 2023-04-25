from signal import signal, SIGTERM, SIGHUP, pause
from rpi_lcd import LCD
import time

lcd = LCD()

def safe_exit(signum, frame):
    exit(0)
    
signal(SIGTERM, safe_exit)
signal (SIGHUP, safe_exit)

try:
    lcd.text("Howdy Partner!", 1)
    lcd.text("Welcome Home!", 2)

    time.sleep(5)
    lcd.text("Input Password:/n", 1)
    pause()
    
except KeyboardInterrupt:
    pass

finally:
    lcd.clear()