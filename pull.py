import cv2
import os
import sys

from datetime import datetime
from dotenv import load_dotenv

if __name__ == '__main__':
  # Get host info
  load_dotenv()
  ENV_DEFAULT_PORT = os.getenv('ENV_DEFAULT_PORT')
  ENV_HOST_URL = os.getenv('ENV_HOST_URL')
  ENV_HOST_APP = os.getenv('ENV_HOST_APP')
  
  # Init VideoCaptures
  cam = []
  writer = []
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
  
  frame = []
  exit = False
  record = False
  while not exit:
    # Display Frames
    if cam.isOpened():
      ret, frame = cam.read()
      if not ret:
        continue
      if record:
        writer.write(frame)
        cv2.circle(frame, (frame.shape[1]-25, 25), 10, (0, 0, 255), -1)
      cv2.imshow('cam', frame)
  
    key = cv2.waitKey(1) & 0xFF
    match key:
      case 0x1b: # 'ESC'
        exit = True
      case 0x72: # 'r'
        record = not record
        if record:
          writer = cv2.VideoWriter(filename='output_{}.avi'.format(datetime.now().strftime('%Y%m%d_%H%M%S')),
                                   fourcc=cv2.VideoWriter_fourcc(*'XVID'),
                                   fps=fps,
                                   frameSize=(frame.shape[1], frame.shape[0]))
        else:
          writer.release()
  
  
  # Clean up
  cam.release()
  if writer.isOpened():
    writer.release()
  cv2.destroyAllWindows()