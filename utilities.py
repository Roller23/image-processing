from PIL import Image, ImageDraw, ImageSequence
import cv2

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

def normalize_rgb(rgb):
  r, g, b = rgb
  max_color = max(rgb)
  if r > 200 and g > 200 and b > 200:
    return WHITE
  if r < 100 and g < 100 and b < 100:
    return BLACK
  if r == max_color and r > 140:
    return RED
  if g == max_color and g > 140:
    return GREEN
  if b == max_color and b > 140:
    return BLUE
  return BLACK

def resize_gif(path):
  size = 500, 500
  image = Image.open(path)
  frames = []
  for frame in ImageSequence.Iterator(image):
    frames.append(frame.copy().resize(size))
  new_path = './temp/finished.gif'
  frames.reverse()
  make_gif(frames, new_path)
  return new_path

def normalize_image(image):
  imageWidth, imageHeight = image.size
  for j in range(imageHeight):
    for i in range(imageWidth):
      image.putpixel((i, j), 
        normalize_rgb(
          image.getpixel((i, j))
        )
      )
  return image

def find_start_and_end(image):
  imageWidth, imageHeight = image.size
  start, end = None, None
  for j in range(imageHeight):
    for i in range(imageWidth):
      color = normalize_rgb(image.getpixel((i, j)))
      if color == GREEN:
        start = (i, j)
      if color == RED:
        end = (i, j)
  return (start, end)

def check_offset(x, y, end):
  mainly_up = y > end[1]
  mainly_right = x < end[0]
  direct = ['up' if mainly_up else 'down', 'right' if mainly_right else 'left']
  direct = (direct[0], direct[1], 'up' if direct[0] == 'down' else 'down', 'right' if direct[1] == 'left' else 'left')
  return direct

def solve_maze(image, x, y, end, frames):
  color = normalize_rgb(image.getpixel((x, y)))
  if color == RED:
    frames.append(image)
    return True
  if color == BLACK:
    return False
  if color == BLUE:
    return False
  newImage = image.copy()
  newImage.putpixel((x, y), BLUE)
  directions = check_offset(x, y, end)
  for direction in directions:
    if direction == 'up':
      if solve_maze(newImage, x, y - 1, end, frames):
        frames.append(newImage)
        return True
    if direction == 'down':
      if solve_maze(newImage, x, y + 1, end, frames):
        frames.append(newImage)
        return True
    if direction == 'right':
      if solve_maze(newImage, x + 1, y, end, frames):
        frames.append(newImage)
        return True
    if direction == 'left':
      if solve_maze(newImage, x - 1, y, end, frames):
        frames.append(newImage)
        return True
  newImage.putpixel((x, y), WHITE)
  return False

def draw_rectangle(image, point, color, size):
  return cv2.rectangle(image, (point[0] - size, point[1] - size), (point[0] + size, point[1] + size), color, size * 2)

def show_image(image, name='Image'):
  cv2.imshow(name, image)
  cv2.waitKey(0)
  cv2.destroyAllWindows()

def make_gif(frames, name='solved.gif'):
  frames[0].save(name, format='gif', append_images=frames[1:], save_all=True, duration=50, loop=0)

def parseMaze(path):
  print("Parsing", path)
  inputImage = Image.open(path).convert('RGB')
  inputImage = normalize_image(inputImage)
  start, end = find_start_and_end(inputImage)
  if start == None:
    raise ValueError('Couldn\'t find a start')
    exit(0)
  if end == None:
    raise ValueError('Coun\'t find an end')
    exit(0)
  print('Found start and end, solving the maze...')
  frames = []
  solve_maze(inputImage, start[0], start[1], end, frames)
  print('Maze solved, creating a gif...')
  if len(frames) < 2:
    raise ValueError("Not enough frames: {}".format(len(frames)))
    exit(0)
  output_name = './temp/temp_solved.gif'
  make_gif(frames, output_name)
  print('Done!')
  return output_name