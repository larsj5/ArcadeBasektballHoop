import RPi.GPIO as GPIO
import time
from rpi_ws281x import *
import argparse

#distance sensor setup
# GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# set GPIO Pins
GPIO_TRIGGER = 23
GPIO_ECHO = 24

# set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

GPIO.output(GPIO_TRIGGER, False)
time.sleep(2)

# LED strip configuration:
LED_COUNT      = 120      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)

    # set Trigger after 5ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    StartTime = time.time()
    StopTime = time.time()

    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()

    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()

    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34578) / 2

    return distance

#Quickly run green across display a pixel at a time.
def colorGreen(strip, color = Color(0, 200, 0), wait_ms=5):
    for i in range(30, strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000)

#flash strip red
def flashRed(strip, color = Color(200, 0, 0)):
    for i in range(30, strip.numPixels()):
        strip.setPixelColor(i, color)
    strip.show()
    time.sleep(.5)
    clearLED(strip)
    time.sleep(.5)

#flash strip green
def flashGreen(strip, color = Color(0, 200, 0)):
    for i in range(30, strip.numPixels()):
        strip.setPixelColor(i, color)
    strip.show()
    time.sleep(.5)
    clearLED(strip)

def clearLED(strip, color = Color(0, 0, 0)):
    #Clear LED
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
    strip.show()

if __name__ == '__main__':
    try:
        # Process arguments
        parser = argparse.ArgumentParser()
        parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
        args = parser.parse_args()

        # Create NeoPixel object with appropriate configuration.
        strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
        # Intialize the library (must be called once before other functions).
        strip.begin()

        gameStatus = True
        while gameStatus:
            gameTime = 60
            score = 0
            dist = 0
            print("Welcome! Game Starting in 3 Seconds")
            for i in range(3):
                flashRed(strip)
            flashGreen(strip)
            print("Game Started! Bombs Away")
            start = time.time()
            while time.time() - start < gameTime:
                dist = distance()
                print dist
                if dist < 25  and dist > 1:
                    score += 1
                    colorGreen(strip)
                    print("You scored! Score = " + str(score))
                    time.sleep(1)
                    clearLED(strip)
                    t = 60 - int(time.time() - start)
                    print(str(t) + " Seconds Remaining")
            for i in range(3):
                flashRed(strip)
            print("Time's Up!")
            print("Score: " + str(score))
            gameStatus = False
    except KeyboardInterrupt:
        print("Game stopped by User")
        clearLED(strip)
        GPIO.cleanup()














