# -*- coding: UTF-8 -*-
from flask import Flask ,request,make_response
from flask import render_template
from picamera import PiCamera
from time import sleep
import requests
import os

app = Flask(__name__)

IMG_PATH=os.path.abspath(os.path.dirname(__file__))+"/image.jpg"
@app.route("/photo_page")  #串流照片
def upload_photo():
    camera = PiCamera()
    sleep(2)
    camera.start_preview()  #開啟相機預覽
    #camera.rotation =180   #解決鏡頭上下顛倒
    camera.capture('./image.jpg')  #拍照並存檔
    camera.stop_preview()   #關閉預覽
    camera.close()
    image_data = open(IMG_PATH,"rb").read()   #只能讀檔(read only)
    response = make_response(image_data)      #設定 response
    response.headers['Content-Type'] = 'image/jpg'
    return response
  
@app.route("/")
def photo():   #控制樹梅派拍照
    if request.method=="GET":
        photo_enable = request.args.get(key='photo')   #設定key
        print(str(photo_enable))
        if(str(photo_enable)=="ON"):                   #檢查拍照權限
            try:
                camera = PiCamera()
                sleep(5)
                camera.start_preview()
                #camera.rotation =180   #解決鏡頭上下顛倒
                camera.capture('./image.jpg')
                camera.stop_preview()
                camera.close()
                return "Camera_success"
            except:
                return "Camera_fail"
        else:
            return "NO camera"
            pass
    else:                          #request.method=="POST"
        pass
        return "Not get response"
if __name__ == '__main__':
    
    app.run(debug=True, host='0.0.0.0', port=2224)
