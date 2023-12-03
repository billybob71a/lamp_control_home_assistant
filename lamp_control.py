from time import sleep
import json
import requests
import RPi.GPIO as GPIO

# GPIO.setWarnings(False)
GPIO.setmode(GPIO.BOARD)
button1 = 40
button2 = 12

increment = 0
GPIO.setup(button1,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(button2,GPIO.IN,pull_up_down=GPIO.PUD_DOWN) # set pin 16 to be an input pin and set initial value to be pulled low (off)
GPIO.add_event_detect(button1, GPIO.RISING)
GPIO.add_event_detect(button2, GPIO.RISING)
url = "http://192.168.1.96:8123/api/services/google_assistant_sdk/send_text_command"
# the next lines are to read a the secret token from a file
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

try: 
    while True:
        if GPIO.event_detected(button1):
            print("button 1 pressed")
            increment+=1
            print("The value is " + str(increment))
            #call_api('on')                
        elif GPIO.event_detected(button2):
            print("button 2 was pressed")
            increment+=1
            print("The value is " + str(increment))
            #call_api('off')
except KeyboardInterrupt as e:
    GPIO.cleanup()
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
    



