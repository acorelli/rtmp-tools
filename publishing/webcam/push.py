#! /usr/bin/python

import cv2
import os
import subprocess
import sys

from dotenv import load_dotenv

if __name__ == '__main__':
  # Get host info
  load_dotenv()
  CAM_NUMBER = int(os.getenv('CAM_NUMBER', 0))
  ENV_DEFAULT_PORT = os.getenv('ENV_DEFAULT_PORT', '1935')
  ENV_HOST_URL = os.getenv('ENV_HOST_URL')
  ENV_HOST_APP = os.getenv('ENV_HOST_APP', '/stream')
  
  sys.argv.pop(0)
  
  if len(sys.argv) == 0:
    sys.argv.append(ENV_DEFAULT_PORT)
  
  for arg in sys.argv:
      rtmp_url = ENV_HOST_URL + ":" + arg + ENV_HOST_APP
  
  fps = 30
  width = 640
  height = 480
  
  cap = cv2.VideoCapture(CAM_NUMBER)
  
  command = ['ffmpeg',
             '-y',
             '-f', 'rawvideo',
             '-vcodec', 'rawvideo',
             '-pix_fmt', 'bgr24',
             '-s', "{}x{}".format(width, height),
             '-r', str(fps),
             '-i', '-',
             '-c:v', 'libx264',
             '-pix_fmt', 'yuv420p',
             '-preset', 'ultrafast',
             '-f', 'flv',
             '-segment_time', '2',
             '-g', '120',
             '-b:v', '1500k',
             '-bufsize', '3000k',
             '-minrate', '500k',
             '-maxrate', '1500k',
             '-r', str(fps),
             rtmp_url]
  
  p = subprocess.Popen(command, stdin=subprocess.PIPE)
  
  while True:
    ret, im = cap.read()
    if not ret:
      continue
      
    cv2.resize(im, (width, height), interpolation = cv2.INTER_NEAREST)
    p.stdin.write(im.tobytes())
    
    if cv2.waitKey(1) & 0xFF == 0x1b:
      break
  
  cap.release()