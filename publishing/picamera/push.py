#! /usr/bin/python

import cv2
import os
import subprocess
import sys

from dotenv import load_dotenv
from picamera2 import Picamera2

if __name__ == '__main__':
  # Get host info
  load_dotenv()
  ENV_DEFAULT_PORT = os.getenv('ENV_DEFAULT_PORT', '1935')
  ENV_HOST_URL = os.getenv('ENV_HOST_URL')
  ENV_HOST_APP = os.getenv('ENV_HOST_APP', '/stream')
  
  sys.argv.pop(0)
  
  if len(sys.argv) == 0:
    sys.argv.append(ENV_DEFAULT_PORT)
  
  for arg in sys.argv:
      rtmp_url = ENV_HOST_URL + ":" + arg + ENV_HOST_APP
  
  fps = 30
  width = 768
  height = 540
  
  picam2 = Picamera2()
  picam2.configure(picam2.create_video_configuration({"format": 'RGB888', "size": (width, height)}, buffer_count=6, controls={"FrameDurationLimits": (33333, 33333)}))
  picam2.start()
  
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
    im = picam2.capture_array()
    cv2.resize(im, (width, height), interpolation = cv2.INTER_NEAREST)
    p.stdin.write(im.tobytes())