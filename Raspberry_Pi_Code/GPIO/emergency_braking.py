import RPi.GPIO as GPIO

channel = 2;

def brake(channel):
    print('Objeto detectado en el camino')
    print('Activando protocolo de frenado de emergencia)

if __name__ == '__main__':
    GPIO.add_event_detect(channel, GPIO.RISING, callback=brake)
