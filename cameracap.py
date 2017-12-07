import picamera
import time, datetime
import ConfigParser

config = ConfigParser.ConfigParser()
config.read('config')

class CaptureImage:
  def __init__(self):
    self.camera = picamera.PiCamera()
    w, h = config.get('Camera', 'Resolution').split('x')
    self.camera.resolution = (int(w), int(h))
    self.camera.brightness = int(config.get('Camera', 'Brightness'))

  def capture_image(self):
    cam = self.camera
    cam.start_preview()
    time.sleep(2)
    filename = '/tmp/' + datetime.datetime.now().strftime('%s') + '.jpg'
    cam.capture(filename)
    cam.stop_preview()
    print "Captured at " + filename
    cam.close()
    return filename
