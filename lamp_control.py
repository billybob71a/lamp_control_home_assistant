from time import sleep
import RPi.GPIO as GPIO

# GPIO.setWarnings(False)
GPIO.setmode(GPIO.BOARD)
button1 = 10

def button_callback(channel):
    print("Callback function called Button 1 was pushed!")

button2 = 12
increment = 0
GPIO.setup(button1,GPIO.IN,pull_up_down=GPIO.PUD_DOWN) # set pin 16 to be an input pin and set initial value to be pulled low (off)
GPIO.add_event_detect(button1, GPIO.RISING)
GPIO.add_event_detect(button2, GPIO.RISING)
while True:
    if GPIO.event_detected(button1):
        print("button 1 pressed")
        increment+=1
        print("The value is " + str(increment))
    elif GPIO.event_detected(button2):
        print("button 2 was pressed")
        increment+=1
        print("The value is " + str(increment))
#    if GPIO.input(10) == GPIO.HIGH:
#        print("Button 1 was pushed")
#        increment+=1
#        print("The value is " + str(increment))

#GPIO.setup(button2, GPIO.IN,pull_up_down=GPIO.PUD_UP) 
#while True:
#    if GPIO.input(button1) == False:
#        print("Button 1 was pressed")
#        sleep(1)
#    if GPIO.input(button2) == False:
#        print("Button 2 was pressed")
#        sleep(1)
#    increment+=1
    #print("The value is " + str(increment))
    



