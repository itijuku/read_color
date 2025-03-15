import cv2
import numpy as np
import picamera2
import time
from PIL import Image


# 変えるとこ #
del_range = 9000
trimming_range:list = [0, 360, 1919, 500]
file_name = "input.jpg"
lower = np.array([5,5,95])
upper = np.array([30,65,220])
#----------#









picam2 = picamera2.Picamera2()
picam2.start_preview()
config = picam2.create_preview_configuration(main={"size":(1919,600)})
picam2.configure(config)
picam2.start()

# time.sleep(2)
picam2.capture_file(file_name)

picam2.stop
file = file_name
im = Image.open(file_name)
im.crop((trimming_range[0], trimming_range[1], trimming_range[2], trimming_range[3])).save(file_name, quality=95)
image = cv2.imread(file_name)





color_data = []
len_block = []

image = image



hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
mask_ = cv2.inRange(hsv, lower, upper)

x_data = []
y_data = []
mask = cv2.bitwise_and(image,image, mask=mask_)
contours, hierarchy = cv2.findContours(
mask_, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contours = list(filter(lambda x: cv2.contourArea(x) > del_range, contours))#小さいの削除
cv2.drawContours(image, contours, -1, color=(0, 0, 255), thickness=2)
len_block.append(len(contours))
x, y, w, h = cv2.boundingRect(contours[0])

cv2.namedWindow("image", cv2.WINDOW_NORMAL)

cv2.imshow("image","input.jpg")
cv2.waitKey(0)
cv2.destroyAllWindows()
