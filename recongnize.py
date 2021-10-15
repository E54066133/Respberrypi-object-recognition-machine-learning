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

model_file = "model/detect.tflite"
label_file = "model/coco_labels.txt"
threshold = 0.6

@app.route('/')
def index():
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
        image = cv2.resize(frame,(width, height))
        #inference image
        result = detect_objects(interpreter, image, threshold)
        print(result)

        #在這裡將 inference 的 result 進行處理，
        #並且在 frame 上畫出作業要求的 bounding box
        #cv2.line(影像, 開始座標, 結束座標, 顏色, 線條寬度)
        #cv2.rectangle(影像, 頂點座標, 對向頂點座標, 顏色, 線條寬度)
        #cv2.rectangle(img, (20, 60), (120, 160), (0, 255, 0), 2)
        ### result 資料樣子 ###
        #[{'bounding_box': array([0.3174595 , 0.01692551, 0.9899411 , 0.60023886], 
        # dtype=float32), 'class_id': 16.0, 'score': 0.65625}]

        sp = image.shape
        sz1 = sp[0]#height(rows) of image
        sz2 = sp[1]#width(colums) of image

        ob_list = []
        if result:
            for i in range(0,len(result)):
                temp = result[i]['score']
                ob_list.append(temp)
            if len(ob_list) < 3 :
                my_use = result[0]['bounding_box']
                cv2.rectangle(frame,(int(sz1*my_use[0]),int(sz2*my_use[1])),(int(sz1*my_use[2]),int(sz2*my_use[3])),(0, 255, 0),2)
            if len(ob_list) >= 3:
                max_num_index_list = map(ob_list.index, heapq.nlargest(3, ob_list))
                max_num_index_list = list(max_num_index_list)
                my_use0 = result[max_num_index_list[0]]['bounding_box']
                my_use1 = result[max_num_index_list[1]]['bounding_box']
                my_use2 = result[max_num_index_list[2]]['bounding_box']
                cv2.rectangle(frame,(int(sz1*my_use0[0]),int(sz2*my_use0[1])),(int(sz1*my_use0[2]),int(sz2*my_use0[3])),(0, 255, 0),2)
                cv2.rectangle(frame,(int(sz1*my_use1[0]),int(sz2*my_use1[1])),(int(sz1*my_use1[2]),int(sz2*my_use1[3])),(0, 255, 0),2)
                cv2.rectangle(frame,(int(sz1*my_use2[0]),int(sz2*my_use2[1])),(int(sz1*my_use2[2]),int(sz2*my_use2[3])),(0, 255, 0),2)
        
        frame = camera.to_jpeg(frame)
        yield (b'--frame\r\n'
           b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
