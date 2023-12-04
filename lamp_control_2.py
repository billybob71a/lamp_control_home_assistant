from time import sleep
import json
import logging
import requests
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

button2 = 40

increment = 0

GPIO.setup(button2, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def call_api(onoff):
    if onoff == 'on':
        data = {
            'command': 'turn on lamp'
        }
    elif onoff == 'off':
        data = {
            'command': 'turn off lamp'
        }
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            print('POST request successful')
            print("Response:", response.json())
        else:
            print(f'Failed with status code : {response.status_code}')
    except requests.exceptions.RequestException as e:
            print('Request failed', e)

GPIO.add_event_detect(button2, GPIO.FALLING, callback=call_api, bouncetime=200)
url = "http://192.168.1.96:8123/api/services/google_assistant_sdk/send_text_command"

file_path = 'secret.txt'  # Replace with the path to your file

try:
    with open(file_path, 'r') as file:
        line = file.readline()  # Read one line from the file
        
        if line:
            token_secret = line.strip() #Stripping line of newline characters)
        else:
            print("File is empty or no lines to read.")
            
except FileNotFoundError:
    print(f"File '{file_path}' not found.")
except Exception as e:
    print("An error occurred:", e)
# reading secret token ends here
token = token_secret
headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json'
}

try: 
    while True:
        if GPIO.event_detected(button2):
            print("off button was pressed")
            increment+=1
            print("The value is " + str(increment))
            call_api('off')                
        sleep(.1)
except KeyboardInterrupt as e:
    GPIO.cleanup()