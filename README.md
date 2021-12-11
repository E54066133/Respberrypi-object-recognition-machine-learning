# Respberrypi_object-recognition 
object recognition with machine learning on Respberry pi

![image](https://github.com/E54066133/Respberrypi-object-recognition-machine-learning/blob/62c83941ffd8614a041806652cd2eb6fa8f2a6b1/PI.png)

## line.py
建立一支與樹梅派連線的 linebot  
使用此 linebot 遠端控制樹梅派拍照

## config.ini
linebot 的 channel token & secret
raspberrypi 的連線位址

## app.py 
raspberrypi的主控制程式

## infrared.py
控制樹梅派的外接照相模組


## config_pi.ini
linbot 的連線位址


## recongnize.py
匯入訓練好的 tensorflow lite 物體辨識模型  
並根據樹梅派的照片資料做出物體辨識  
顯示照片中 辨識信心度最高的三樣物品 
 
