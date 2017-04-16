import picamera
import time

class CaptureAndEmail:
  def __init__(self):
    self.camera = picamera.PiCamera()

  def capture_image():
    cam = self.camera
    cam.start_preview()
    time.sleep(5)
    cam.capture('/tmp/' + datetime.datetime.now().strftime('%s') + '.jpg')
    cam.stop_preview()

x = CaptureAndEmail()

x.capture_image()
