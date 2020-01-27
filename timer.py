import sys
import os
import utilities as utils
import cv2
import numpy as np
import time

if not os.path.exists('./temp'):
  os.makedirs('temp')

time_start = time.time()
path = './images/lab2.jpg'
if len(sys.argv) > 1:
  path = sys.argv[1]

green_box = (421, 424)
red_box = (121, 421)
scaled = None
image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
new_size = (600, 600)
image = cv2.resize(image, new_size, interpolation=cv2.INTER_LINEAR)
ret, thresh = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)

kernel = np.ones((5, 5), np.uint8)
for i in range(30):
  thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
  thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

resized = cv2.resize(thresh, (12, 12), interpolation=cv2.INTER_LINEAR)
scaled = cv2.resize(resized, new_size, interpolation=cv2.INTER_NEAREST)
scaled = cv2.cvtColor(scaled, cv2.COLOR_GRAY2RGB)
scaled = utils.draw_rectangle(scaled, green_box, (0, 255, 0), 15)
scaled = utils.draw_rectangle(scaled, red_box, (0, 0, 255), 15)
to_process = cv2.resize(scaled, (50, 50), interpolation=cv2.INTER_LINEAR)
path = "./temp/to_process.jpg"
cv2.imwrite(path, to_process)
result = utils.parseMaze(path)
os.remove(path)
finished = utils.resize_gif(result)
os.remove(result)

time_end = time.time()
time_result = time_end - time_start
print("Time result", time_result)