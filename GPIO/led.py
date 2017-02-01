import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

led = 5


GPIO.setup(led,GPIO.OUT)

for i in range(0,5):

	GPIO.output(led,1)

GPIO.cleanup


