import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

led = 5


GPIO.setup(led,GPIO.OUT)
try:

	for i in range(0,5):

		GPIO.output(led,1)
		sleep(0.5)
		GPIO.output(led,0)

	GPIO.output(led,0)
	GPIO.cleanup
	print ("El programa ha terminado de ejecutar")

except keyboardinterrupt:
	GPIO.output(led,0)
	GPIO.cleanup
	print("Se ha interrmpido la ejecucion")


