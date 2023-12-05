from time import sleep
import json
import logging
import requests
import RPi.GPIO as GPIO

logging.basicConfig(filename='lamp_control.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# GPIO.setWarnings(False)
GPIO.setmode(GPIO.BOARD)
button1 = 16
#button2 = 40

increment = 0
GPIO.setup(button1,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
#GPIO.setup(button2,GPIO.IN,pull_up_down=GPIO.PUD_DOWN) # set pin 16 to be an input pin and set initial value to be pulled low (off)
GPIO.add_event_detect(button1, GPIO.RISING, callback = lambda button1: call_api(button1), bouncetime=500)
#GPIO.add_event_detect(button2, GPIO.RISING)
url = "http://192.168.1.96:8123/api/services/google_assistant_sdk/send_text_command"
# the next lines are to read a the secret token from a file
file_path = 'secret.txt'  # Replace with the path to your file

try:
    with open(file_path, 'r') as file:
        line = file.readline()  # Read one line from the file
        
        if line:
            token_secret = line.strip() #Stripping line of newline characters)
        else:
            logging.info("File is empty or no lines to read.")
            
except FileNotFoundError:
    logging.info(f"File '{file_path}' not found.")
except Exception as e:
    logging.info("An error occurred:", e)
# reading secret token ends here
token = token_secret
headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json'
}

def call_api(pin):
    if pin == 16:
        data = {
            'command': 'turn off lamp'
        }
    elif pin == 'off':
        data = {
            'command': 'turn on lamp'
        }
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            logging.info('POST request successful')
            logging.info("Response:")
        else:
            logging.info(f'Failed with status code : {response.status_code}')
    except requests.exceptions.RequestException as e:
            logging.info('Request failed', e)

try: 
    while True:
        if GPIO.event_detected(button1):
            logging.info("off button was pressed")
            increment+=1
            logging.info("The value is " + str(increment))
            #call_api('on')                
        #elif GPIO.event_detected(button2):
        #    logging.info("off button pressed")
        #    increment+=1
        #    logging.info("The value is " + str(increment))
            #call_api('off')
        sleep(.1)
except KeyboardInterrupt as e:
    GPIO.cleanup()
    



