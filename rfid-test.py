import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

try:
    text = input("Data: ")
    print("Now place your tag to write")
    reader.write(text)
    print("Written")
    
finally:
    GPIO.cleanup()
