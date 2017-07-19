from cv2.cv2 import *
from matplotlib import pyplot as plt
import numpy as np

marlboro_cascade = CascadeClassifier('cascade.xml')

img = imread('test_imgs/3.jpg', 1)
gray = cvtColor(img, COLOR_BGR2GRAY)

marlboros = marlboro_cascade.detectMultiScale(gray, 1.1, 3)
for (x,y,w,h) in marlboros:
    img = rectangle(img,(x,y),(x+w,y+h),(255,0,0),1)
    roi_gray = gray[y:y+h, x:x+w]
    roi_color = img[y:y+h, x:x+w]
    #plt.imshow(cvtColor(roi_color, COLOR_BGR2RGB)),plt.show()
    
result_img = cvtColor(img, COLOR_BGR2RGB)
plt.imshow(result_img),plt.show()
