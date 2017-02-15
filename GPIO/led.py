import RPi.GPIO as GPIO
from time import sleep
GPIO.setmode(GPIO.BCM)

led = 5

cd
GPIO.setup(led,GPIO.OUT)
try:

	for i in range(0,5):

		GPIO.output(led,1)
		sleep(0.25)
		GPIO.output(led,0)
		sleep(0.25)


	GPIO.output(led,0)
	GPIO.cleanup
	print ("El programa ha terminado de ejecutar")

except KeyboardInterrupt:
	GPIO.output(led,0)
	GPIO.cleanup
	print("Se ha interrmpido la ejecucion")


