from flask import Flask, render_template, Response
from camera_pi import Camera
import cv2
from litelib import load_labels, detect_objects
import io
import time
import numpy as np
from tflite_runtime.interpreter import Interpreter
import heapq
app = Flask(__name__)

model_file = "model/detect.tflite"        #將 tensorflow lite訓練檔 設為 model_file
label_file = "model/coco_labels.txt"
threshold = 0.6

@app.route('/')
def index():                                #建立目錄
    return render_template('stream.html')



def gen(camera):
    while True:
        frame = camera.get_frame()
            
        #args = parser.parse_args()
        labels = load_labels(label_file)
        interpreter = Interpreter(model_file)
        interpreter.allocate_tensors()
        _, height, width, _ = interpreter.get_input_details()[0]['shape']
        #get image from camera
        image = cv2.resize(frame,(width, height))      # resize 相片大小
        #inference image
        result = detect_objects(interpreter, image, threshold)
        print(result)

        
        
        sp = image.shape
        sz1 = sp[0]                          #height(rows) of image
        sz2 = sp[1]                          #width(colums) of image

        ob_list = []                         #建立辨識物件清單
        if result:                           #將 inference 的 result 進行處理
            for i in range(0,len(result)):
                temp = result[i]['score']    #紀錄辨識物件及信心分數
                ob_list.append(temp)
            if len(ob_list) < 3 :            #若畫面中不足3個物件
                my_use = result[0]['bounding_box']
                cv2.rectangle(frame,(int(sz1*my_use[0]),int(sz2*my_use[1])),(int(sz1*my_use[2]),int(sz2*my_use[3])),(0, 255, 0),2)
            if len(ob_list) >= 3:            #若畫面中至少3個物件
                max_num_index_list = map(ob_list.index, heapq.nlargest(3, ob_list))
                max_num_index_list = list(max_num_index_list)
                my_use0 = result[max_num_index_list[0]]['bounding_box']    
                my_use1 = result[max_num_index_list[1]]['bounding_box']    
                my_use2 = result[max_num_index_list[2]]['bounding_box']    
                cv2.rectangle(frame,(int(sz1*my_use0[0]),int(sz2*my_use0[1])),(int(sz1*my_use0[2]),int(sz2*my_use0[3])),(0, 255, 0),2)   #繪製物件1的bounding_box
                cv2.rectangle(frame,(int(sz1*my_use1[0]),int(sz2*my_use1[1])),(int(sz1*my_use1[2]),int(sz2*my_use1[3])),(0, 255, 0),2)   #繪製物件2的bounding_box
                cv2.rectangle(frame,(int(sz1*my_use2[0]),int(sz2*my_use2[1])),(int(sz1*my_use2[2]),int(sz2*my_use2[3])),(0, 255, 0),2)   #繪製物件3的bounding_box
        
        frame = camera.to_jpeg(frame)    #儲存 frame
        yield (b'--frame\r\n'
           b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
