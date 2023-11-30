import RPi.GPIO as GPIO

# GPIO.setWarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(10,GPIO.IN) # set pin 10 to be an input pin and set initial value to be pulled low (off)

while True:
    input_value = GPIO.input(10)
    if input_value == True:
        print("Who pressed my Button")

