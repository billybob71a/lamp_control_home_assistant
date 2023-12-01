from time import sleep
import RPi.GPIO as GPIO

# GPIO.setWarnings(False)
GPIO.setmode(GPIO.BOARD)
button1=16
button2=12
GPIO.setup(button1,GPIO.IN,pull_up_down=GPIO.PUD_UP) # set pin 16 to be an input pin and set initial value to be pulled low (off)
GPIO.setup(button2, GPIO.IN,pull_up_down=GPIO.PUD_UP) 
while True:
    if GPIO.input(button1) == False:
        print("Button 1 was pressed")
        sleep(.1)
    if GPIO.input(button2) == False:
        print("Button 2 was pressed")



