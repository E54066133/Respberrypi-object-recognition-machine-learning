import time
import requests
import RPi.GPIO as GPIO
import configparser
config = configparser.ConfigParser()
config.read('config_pi.ini')
lineserver_host =config.get('line-bot', 'lineserver_host') 
SEN_PIN = 36  #IR sensor腳位
data = {
    "name": "Jason",
    "SENSOR": "ON"
}
GPIO.setmode(GPIO.BOARD)
GPIO.setup(SEN_PIN,GPIO.IN)
try:
    while True:
        #print(GPIO.input(SEN_PIN))
        if GPIO.input(SEN_PIN) == GPIO.HIGH:    #有人接進時觸發反應
            r = requests.get(lineserver_host+"/callback", params=data)  #抓 linebot sever callback
        time.sleep(1)
except Exception as e:
    print(e)
