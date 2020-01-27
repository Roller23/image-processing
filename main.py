import sys
import os
import utilities as utils
from utilities import show_image
import cv2
import numpy as np
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk

def on_click(event, x, y, flags, param):
  global green_box
  global red_box
  global scaled
  global new_size
  global output_name
  global windowName
  if event == cv2.EVENT_LBUTTONUP:
    if green_box == None:
      green_box = (x, y)
      scaled = utils.draw_rectangle(scaled, green_box, (0, 255, 0), 15)
      cv2.imshow(windowName, scaled)
    else:
      red_box = (x, y)
      scaled = utils.draw_rectangle(scaled, red_box, (0, 0, 255), 15)
      cv2.imshow(windowName, scaled)
      to_process = cv2.resize(scaled, (50, 50), interpolation=cv2.INTER_LINEAR)
      path = "./temp/to_process.jpg"
      cv2.imwrite(path, to_process)
      result = utils.parseMaze(path)
      os.remove(path)
      print("Resizing...")
      finished = utils.resize_gif(result)
      print("Done!")
      os.remove(result)
      cv2.waitKey(0)
      cv2.destroyAllWindows()
      print("Output path:", finished)
      os.system(("start " if os.name == 'nt' else "open ") + finished)
      exit(0)

if not os.path.exists('./temp'):
  os.makedirs('temp')

Tk().withdraw()
filename = askopenfilename()
path = filename
green_box = None
red_box = None
scaled = None
image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
new_size = (700, 700)
image = cv2.resize(image, new_size, interpolation=cv2.INTER_LINEAR)
ret, thresh = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)
show_image(image)
show_image(thresh)

kernel = np.ones((5, 5), np.uint8)

for i in range(30):
  thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
  thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

show_image(thresh)
resized = cv2.resize(thresh, (12, 12), interpolation=cv2.INTER_LINEAR)
scaled = cv2.resize(resized, new_size, interpolation=cv2.INTER_NEAREST)
scaled = cv2.cvtColor(scaled, cv2.COLOR_GRAY2RGB)
windowName = "Click to choose starting and ending point"
cv2.namedWindow(windowName)
cv2.setMouseCallback(windowName, on_click)
cv2.imshow(windowName, scaled)
while not (cv2.waitKey(0) & 0xFF == ord('q')):
  continue