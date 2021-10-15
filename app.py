# -*- coding: UTF-8 -*-
from flask import Flask ,request,make_response
from flask import render_template
from picamera import PiCamera
from time import sleep
import requests
import os

app = Flask(__name__)

IMG_PATH=os.path.abspath(os.path.dirname(__file__))+"/image.jpg"
@app.route("/photo_page")#串流照片
def upload_photo():
    camera = PiCamera()
    sleep(2)
    camera.start_preview()
    camera.capture('./image.jpg')
    camera.stop_preview()
    camera.close()
    image_data = open(IMG_PATH,"rb").read()
    response = make_response(image_data)
    response.headers['Content-Type'] = 'image/jpg'
    return response
  
@app.route("/")
def photo():#控制樹梅派胎照
    if request.method=="GET":
        photo_enable = request.args.get(key='photo')
        print(str(photo_enable))
        if(str(photo_enable)=="ON"):
            try:
                camera = PiCamera()
                sleep(5)
                camera.start_preview()
                camera.capture('./image.jpg')
                camera.stop_preview()
                camera.close()
                return "Camera_success"
            except:
                return "Camera_fail"
        else:
            return "NO camera"
            pass
    else:
        pass
        return "Not get response"
if __name__ == '__main__':
    
    app.run(debug=True, host='0.0.0.0', port=2224)
