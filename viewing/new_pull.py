import cv2
import os
import sys

from datetime import datetime
from dotenv import load_dotenv

def pull_video():
  # Get host info
  load_dotenv()
  ENV_DEFAULT_PORT = os.getenv('ENV_DEFAULT_PORT', '1935')
  ENV_HOST_URL = os.getenv('ENV_HOST_URL')
  ENV_HOST_APP = os.getenv('ENV_HOST_APP', '/stream')
  ENV_FOURCC = os.getenv('ENV_FOURCC', 'mp4v')
  ENV_OUTPUT_FORMAT = os.getenv('ENV_OUTPUT_FORMAT', '.mp4')
  
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
      case 0x70: # 'p'
        outputPath = "frames"
        output_dir = os.path.join(os.getcwd(), outputPath)
        try:
          os.mkdir(output_dir)
        except:
          pass
        fname = output_dir + '/output_{0}'.format(datetime.now().strftime('%Y%m%d_%H%M%S')) + '.png'
        print('Writing to {}'.format(fname))
        cv2.imwrite(fname, frame)
      case 0x72: # 'r'
        record = not record
        if record:
          outputPath = "clips"
          output_dir = os.path.join(os.getcwd(), outputPath)
          try:
            os.mkdir(output_dir)
          except:
            pass
          print(output_dir)
          fname = output_dir + '/output_{0}'.format(datetime.now().strftime('%Y%m%d_%H%M%S')) + ENV_OUTPUT_FORMAT
          print('Writing to {}'.format(fname))
          writer = cv2.VideoWriter(filename=fname,
                                   fourcc=cv2.VideoWriter_fourcc(*ENV_FOURCC),
                                   fps=fps,
                                   frameSize=(frame.shape[1], frame.shape[0]))
        else:
          writer.release()
  
  
  # Clean up
  cam.release()
  if writer.isOpened():
    writer.release()
  cv2.destroyAllWindows()

if __name__ == '__main__':
  try:
    pull_video()
  except Exception as e:
    print(f'Error: {e}')
    pass
