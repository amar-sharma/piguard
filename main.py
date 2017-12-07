#!/usr/bin/env python

import ConfigParser
import datetime, time
import RPi.GPIO as GPIO
config = ConfigParser.ConfigParser()
config.read('config')
from cameracap import CaptureImage
from sendalert import Alertall
isAnyOneHome = False

class PiguardScheduler:
  def __init__(self):
    self.weekno = datetime.datetime.today().weekday()
    self.OnWeekdays = str(config.get('Schedule', 'OnWeekdays'))
    self.OnWeekends = str(config.get('Schedule', 'OnWeekends'))
    self.startTime = datetime.datetime.strptime(str(config.get('Schedule', 'StartTime')), '%H:%M')
    self.endTime = datetime.datetime.strptime(str(config.get('Schedule', 'EndTime')), '%H:%M')

  def shouldMonitor(self, isAnyOneHome):
    if isAnyOneHome:
      return False
    result = True
    currentTime = datetime.datetime.now().strftime('%H:%M')
    currentTime = datetime.datetime.strptime(currentTime, '%H:%M')
    if self.weekno < 5:
      if self.OnWeekdays == 'False':
        return False
    else:
      if self.OnWeekends == 'False':
        return False
    if self.startTime <= currentTime <= self.endTime:
      return True
    else:
      return False

  def sleepTillNextCycle(self):
    cTime = datetime.datetime.now().strftime('%H:%M')
    cTime = datetime.datetime.strptime(cTime, '%H:%M')
    sleepSec = (self.startTime + datetime.timedelta(days=1) - cTime).seconds
    print "Sleeping for " + str(sleepSec/3600) + "hrs"
    time.sleep(abs(sleepSec))
    print "Sleep Ended"

def detectMotion(channel):
  global isAnyOneHome
  print "Motion Detected"
  isAnyOneHome = True
  cap = CaptureImage()
  image_file = cap.capture_image()
  alertme = Alertall()
  alertme.sendEmail(image_file)

def main():
  global isAnyOneHome
  sched = PiguardScheduler()
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(4, GPIO.IN)
  while(True):
    print sched.shouldMonitor(isAnyOneHome)
    if (sched.shouldMonitor(isAnyOneHome)):
      print "Starting Sensors"
      GPIO.add_event_detect(4, GPIO.RISING, callback=detectMotion,
              bouncetime=int(config.get('PIR', 'BounceTime'))*1000)
    while(sched.shouldMonitor(isAnyOneHome)):
      try:
        time.sleep(1)
      except KeyboardInterrupt:
        GPIO.cleanup()
        sys.exit(0)
    GPIO.remove_event_detect(4)
    sched.sleepTillNextCycle()
    isAnyOneHome = False

try:
  main()
except Exception,e:
  print "Got some Error " + str(e)

GPIO.cleanup()
