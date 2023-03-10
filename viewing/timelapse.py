#! /usr/bin/python3

import cv2
import os
import sys
import time

from datetime import datetime
from dotenv import load_dotenv

if __name__ == '__main__':
  # Get host info
  load_dotenv()
  ENV_DEFAULT_PORT = os.getenv('ENV_DEFAULT_PORT')
  ENV_HOST_URL = os.getenv('ENV_HOST_URL')
  ENV_HOST_APP = os.getenv('ENV_HOST_APP')
  ENV_FOURCC = os.getenv('ENV_FOURCC')
  ENV_OUTPUT_FORMAT = os.getenv('ENV_OUTPUT_FORMAT')
  ENV_TIME_INTERVAL = int(os.getenv('ENV_TIME_INTERVAL', 30))
  
  # Init VideoCaptures
  cam = []
  fps = 30.0
  sys.argv.pop(0)
  
  if len(sys.argv) == 0:
    sys.argv.append(ENV_DEFAULT_PORT)
  
  for arg in sys.argv:
    url = ENV_HOST_URL + ":" + arg + ENV_HOST_APP
    print(url)
    cam = cv2.VideoCapture(url)
    if cam.isOpened():
      fps = cam.get(cv2.CAP_PROP_FPS)
    break
  
  outputPath = f"timelapse_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
  output_dir = os.path.join(os.getcwd(), outputPath)
  print(output_dir)
  try:
    os.mkdir(output_dir)
  except:
    print('error creating output dir')
  
  frame_counter = 0
  last_timestamp = 0
  frame = []
  exit = False
  while cam.isOpened():
    ret, frame = cam.read()
    if not ret:
      continue
    
    elapsed_time = time.time() - last_timestamp
    if elapsed_time >= ENV_TIME_INTERVAL:
      filename = os.path.join(f"{output_dir}", f"frame_{frame_counter}.jpg")
      print(filename)
      cv2.imwrite(filename, frame)
      frame_counter += 1
      last_timestamp = time.time()
      
    cv2.imshow('cam', frame)
  
    if cv2.waitKey(1) & 0xFF == 0x1b:
      break
    
    
  
  
  # Clean up
  cam.release()
  cv2.destroyAllWindows()