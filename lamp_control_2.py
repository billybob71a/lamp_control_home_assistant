from time import sleep
from datetime import datetime
import json
import logging
import requests
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

button2 = 40

logging.basicConfig(filename='lamp_control_2.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

increment = 0

GPIO.setup(button2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
url = "http://192.168.1.96:8123/api/services/google_assistant_sdk/send_text_command"
##this section is to get the token code from a file
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
##section ends here
#this section is a function to call the api
def call_api(onoff):
    logging.info(f"You pressed {onoff}")
    data = {}
    if onoff == 'on':
        data = {
            'command': 'turn on lamp'
        }
    elif onoff == 'off':
        data = {
            'command': 'turn off lamp'
        }
    elif onoff == 40:
        logging.info("you pressed off button which GPIO 40")
        data = {
            'command': 'turn off lamp'
        }
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            logging.info('POST request successful')
            logging.info("Response:", response.json())
        else:
            logging.info(f'the header info in url is {headers}, the json info is {data}')
            logging.info(f'Failed with status code : {response.status_code}')
    except requests.exceptions.RequestException as e:
            logging.info('Request failed', e)
#this section calls the api
GPIO.add_event_detect(button2, GPIO.FALLING, callback=lambda button2: call_api(button2), bouncetime=500)


try: 
    while True:
        if GPIO.event_detected(button2) == 1:
            current_datetime = datetime.now()
            date_string = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
            logging.info("date time is ", date_string)
            logging.info("off button was pressed")
            increment+=1
            logging.info("The value is " + str(increment))
            #call_api('off')
            logging.info("I called the api")                
except KeyboardInterrupt as e:
    GPIO.cleanup()
