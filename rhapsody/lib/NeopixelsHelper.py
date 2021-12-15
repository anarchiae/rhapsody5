import time
import random
import RPi.GPIO as GPIO
import Adafruit_WS2801
import Adafruit_GPIO.SPI as SPI


class NeopixelsHelper():
    NUMPIXELS = 88
    SPI_PORT = 0
    SPI_DEVICE = 0
    pixels = None

    # Listes
    sapin = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31,32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60,61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87)
    ligne_1 = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23)
    ligne_2 = (24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43)
    ligne_3 = (44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59)
    ligne_4 = (60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71)
    ligne_5 = (72, 73, 74, 75, 76, 77, 78, 79)
    ligne_6 = (80, 81, 82, 83)
    ligne_7 = (84, 85, 86, 87)
    altern_1 = (1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 34, 37, 39, 41, 43, 45, 47, 49, 51, 53, 55, 57, 59, 60, 61, 63, 65, 67, 69, 71, 73, 75, 77, 79, 81, 83, 85, 87)
    altern_2 = (0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 42, 44, 46, 48, 50, 52, 54, 56, 58, 60, 62, 64, 66, 68, 70, 72, 74, 76, 78, 80, 82, 84, 86)

    def __init__(self):
        self.pixels = Adafruit_WS2801.WS2801Pixels(self.NUMPIXELS, spi=SPI.SpiDev(self.SPI_PORT, self.SPI_DEVICE),
                                                   gpio=GPIO)

    # TOOLS #
    def RGB_to_color(self, r, g, b):
        """Convert three 8-bit red, green, blue component values to a single 24-bit
        color value.
        """
        return ((r & 0xFF) << 16) | ((g & 0xFF) << 8) | (b & 0xFF)

    def set_pixel(self, pixel, red, green, blue):
        self.pixels.set_pixel(pixel, self.RGB_to_color(red, green, blue))

    def set_all_pixels(self, red, green, blue):
        for p in range(0, self.NUMPIXELS):
            self.pixels.set_pixel(p, self.RGB_to_color(red, green, blue))
        self.pixels.show()

    def off_all_pixels(self):
        for p in range(0, self.NUMPIXELS):
            self.pixels.set_pixel(p, self.RGB_to_color(0, 0, 0))
        self.pixels.show()

    def show(self):
        self.pixels.show()

    # EFFECTS #
    def smooth_altern(self, step, loop):
        for l in range(0, loop):
            for i in range(0, 255, step):
                for p in range(0, len(self.altern_1)):
                    self.set_pixel(self.altern_1[p], i, i, i)
                self.show()
            for i in range(255, 0, -step):
                for p in range(0, len(self.altern_1)):
                    self.set_pixel(self.altern_1[p], i, i, i)
                self.show()
            for i in range(0, 255, step):
                for p in range(0, len(self.altern_2)):
                    self.set_pixel(self.altern_2[p], i, i, i)
                self.show()
            for i in range(255, 0, -step):
                for p in range(0, len(self.altern_2)):
                    self.set_pixel(self.altern_2[p], i, i, i)
                self.show()

    def smooth_altern_blue(self, step, loop):
        for l in range(0, loop):
            for i in range(0, 255, step):
                for p in range(0, len(self.altern_1)):
                    self.set_pixel(self.altern_1[p], 0, 0, i)
                self.show()
            for i in range(255, 0, -step):
                for p in range(0, len(self.altern_1)):
                    self.set_pixel(self.altern_1[p], 0, 0, i)
                self.show()
            for i in range(0, 255, step):
                for p in range(0, len(self.altern_2)):
                    self.set_pixel(self.altern_2[p], 0, 0, i)
                self.show()
            for i in range(255, 0, -step):
                for p in range(0, len(self.altern_2)):
                    self.set_pixel(self.altern_2[p], 0, 0, i)
                self.show()

    ##########

    def altern(self, asked_time, sleep_time, colors):
        passed_time = 0
        while(passed_time < asked_time):
            for p in range(0, len(self.altern_1)):
                self.set_pixel(self.altern_1[p], colors[0][0], colors[0][1], colors[0][2])
            for p in range(0, len(self.altern_2)):
                self.set_pixel(self.altern_2[p], colors[1][0], colors[1][1], colors[1][2])
            self.show()
            time.sleep(sleep_time)
            for p in range(0, len(self.altern_2)):
                self.set_pixel(self.altern_2[p], colors[0][0], colors[0][1], colors[0][2])
            for p in range(0, len(self.altern_1)):
                self.set_pixel(self.altern_1[p], colors[1][0], colors[1][1], colors[1][2])
            self.show()
            time.sleep(sleep_time)
            passed_time = passed_time + sleep_time + sleep_time

    ##########

    def sparkle(self, r, g, b, t):
        time_passed = 0
        while (time_passed < t):
            self.set_all_pixels(0, 0, 0)
            for p in range(0, 10):
                self.set_pixel(random.randint(0, 87), r, g, b)
            self.show()
            time.sleep(0.05)
            time_passed = time_passed + 0.05
        self.set_all_pixels(0, 0, 0)

    ##########

    def random_sparkle(self, sleep_time, asked_time, colors):
        passed_time = 0
        while(passed_time < asked_time):
            self.off_all_pixels()
            for i in range(0, 3):
                color = random.randint(0, len(colors)-1)
                self.set_pixel(random.randint(0,self.NUMPIXELS-1), colors[color][0], colors[color][1], colors[color][2])
            self.show()
            time.sleep(sleep_time)
            passed_time = passed_time + sleep_time

    ##########

    def sparkle_with_background(self, r, g, b, bR, bG, bB, t):
        time_passed = 0
        while(time_passed < t):
            self.set_all_pixels(bR, bG, bB)
            for p in range(0, 10):
                self.set_pixel(random.randint(0, 87), r, g, b)
            self.show()
            time.sleep(0.05)
            time_passed = time_passed + 0.05

    ##########

    def spiral_altern_bottom_to_top(self, sleep_time, colors):
        for p in range(0, 87):
            if(p%2 == 0):
                color = 0
            else:
                color = 1
            
            self.set_pixel(p, colors[color][0], colors[color][1], colors[color][2])
            self.show()
            time.sleep(sleep_time)

    ##########

    def spiral_bottom_to_top(self, sleep_time=0.008, red=255, green=255, blue=255):
        """Spirale qui va de base en haut
        """
        for p in self.ligne_1:
            self.set_pixel(p, red, green, blue)
            time.sleep(sleep_time)
            self.show()

        for p in self.ligne_2:
            self.set_pixel(p, red, green, blue)
            time.sleep(sleep_time)
            self.show()

        for p in self.ligne_3:
            self.set_pixel(p, red, green, blue)
            time.sleep(sleep_time)
            self.show()

        for p in self.ligne_4:
            self.set_pixel(p, red, green, blue)
            time.sleep(sleep_time)
            self.show()

        for p in self.ligne_5:
            self.set_pixel(p, red, green, blue)
            time.sleep(sleep_time)
            self.show()

        for p in self.ligne_6:
            self.set_pixel(p, red, green, blue)
            time.sleep(sleep_time)
            self.show()

        for p in self.ligne_7:
            self.set_pixel(p, red, green, blue)
            time.sleep(sleep_time)
            self.show()

    ##########

    def random_spiral_bottom_to_top(self, delay, colors):
        for p in range(0, 87):
            color = random.randint(0, len(colors)-1)
            self.set_pixel(p, 255, 255, 255)
            if(p != 0):
                self.set_pixel(p-1, colors[color][0], colors[color][1], colors[color][2])
            time.sleep(delay)
            self.show()

    ##########
    
    def spiral_top_to_bottom(self, sleep_time=0.008, red=255, green=255, blue=255):
        """Spirale qui va de base en haut
        """
        for p in self.ligne_7:
            self.pixels.set_pixel(p, self.RGB_to_color(red, green, blue))
            time.sleep(sleep_time)
            self.pixels.show()
    
        for p in self.ligne_6:
            self.pixels.set_pixel(p, self.RGB_to_color(red, green, blue))
            time.sleep(sleep_time)
            self.pixels.show()
    
        for p in self.ligne_5:
            self.pixels.set_pixel(p, self.RGB_to_color(red, green, blue))
            time.sleep(sleep_time)
            self.pixels.show()
    
        for p in self.ligne_4:
            self.pixels.set_pixel(p, self.RGB_to_color(red, green, blue))
            time.sleep(sleep_time)
            self.pixels.show()
    
        for p in self.ligne_3:
            self.pixels.set_pixel(p, self.RGB_to_color(red, green, blue))
            time.sleep(sleep_time)
            self.pixels.show()
    
        for p in self.ligne_2:
            self.pixels.set_pixel(p, self.RGB_to_color(red, green, blue))
            time.sleep(sleep_time)
            self.pixels.show()
    
        for p in self.ligne_1:
            self.pixels.set_pixel(p, self.RGB_to_color(red, green, blue))
            time.sleep(sleep_time)
            self.pixels.show()

    ##########

    def blink_with_color_background(self, asked_time, red, green, blue, b_red, b_green, b_blue):
        time_passed = 0
        while (time_passed < asked_time):
            ledsA = self.sapin[random.randint(0, len(self.sapin) - 1)]
            ledsB = self.sapin[random.randint(0, len(self.sapin) - 1)]
            ledsC = self.sapin[random.randint(0, len(self.sapin) - 1)]

            for p in self.sapin:
                self.pixels.set_pixel(p, self.RGB_to_color(b_red, b_green, b_blue))
            self.pixels.show()

            self.pixels.set_pixel(ledsA, self.RGB_to_color(red, green, blue))
            self.pixels.set_pixel(ledsB, self.RGB_to_color(red, green, blue))
            self.pixels.set_pixel(ledsC, self.RGB_to_color(red, green, blue))
            self.pixels.show()

            time.sleep(0.05)

            time_passed = time_passed + 0.05

    ##########

    def brightness_decrease(self, wait=0.01, step=1):
        for j in range(int(256 // step)):
            for i in range(self.pixels.count()):
                r, g, b = self.pixels.get_pixel_rgb(i)
                r = int(max(0, r - step))
                g = int(max(0, g - step))
                b = int(max(0, b - step))
                self.pixels.set_pixel(i, Adafruit_WS2801.RGB_to_color(r, g, b))
            self.pixels.show()
            if wait > 0:
                time.sleep(wait)

    ##########

    def multicolor_blink(self, asked_time, sleep_time):
        passed_time = 0
        colors = [[255, 0, 0], [0, 0, 255], [0, 255, 0]]
        while (passed_time < asked_time):
            for p in self.sapin:
                self.set_pixel(p, 0, 0, 0)
            self.show()

            ledsA = self.sapin[random.randint(0, len(self.sapin) - 1)]
            ledsB = self.sapin[random.randint(0, len(self.sapin) - 1)]
            ledsC = self.sapin[random.randint(0, len(self.sapin) - 1)]

            colorA = colors[random.randint(0, len(colors) - 1)]
            colorB = colors[random.randint(0, len(colors) - 1)]
            colorC = colors[random.randint(0, len(colors) - 1)]

            self.set_pixel(ledsA, colorA[0], colorA[1], colorA[2])
            self.set_pixel(ledsB, colorB[0], colorB[1], colorB[2])
            self.set_pixel(ledsC, colorC[0], colorC[1], colorC[2])

            self.show()

            passed_time = passed_time + sleep_time
            time.sleep(sleep_time)


    ##########

    def multicolor(self, asked_time, sleep_time, colors):
        passed_time = 0
        while(passed_time < asked_time):
            ledsA = self.sapin[random.randint(0, len(self.sapin)-1)]
            ledsB = self.sapin[random.randint(0, len(self.sapin)-1)]
            ledsC = self.sapin[random.randint(0, len(self.sapin)-1)]

            colorA = colors[random.randint(0, len(colors)-1)]
            colorB = colors[random.randint(0, len(colors)-1)]
            colorC = colors[random.randint(0, len(colors)-1)]

            self.set_pixel(ledsA, colorA[0], colorA[1], colorA[2])
            self.set_pixel(ledsB, colorB[0], colorB[1], colorB[2])
            self.set_pixel(ledsC, colorC[0], colorC[1], colorC[2])

            self.show()

            time.sleep(sleep_time)

            passed_time = passed_time + sleep_time

    ##########

    def from_top_to_bottom(self, sleep_time=0.008, red=255, green=255, blue=255):
        for p in range(0, len(self.ligne_7)):
            self.set_pixel(self.ligne_7[p], red, green, blue)
        self.show()
        time.sleep(sleep_time)

        for p in range(0, len(self.ligne_6)):
            self.set_pixel(self.ligne_6[p], red, green, blue)
        self.show()
        time.sleep(sleep_time)

        for p in range(0, len(self.ligne_5)):
            self.set_pixel(self.ligne_5[p], red, green, blue)
        self.show()
        time.sleep(sleep_time)

        for p in range(0, len(self.ligne_4)):
            self.set_pixel(self.ligne_4[p], red, green, blue)
        self.show()
        time.sleep(sleep_time)

        for p in range(0, len(self.ligne_3)):
            self.set_pixel(self.ligne_3[p], red, green, blue)
        self.show()
        time.sleep(sleep_time)

        for p in range(0, len(self.ligne_2)):
            self.set_pixel(self.ligne_2[p], red, green, blue)
        self.show()
        time.sleep(sleep_time)

        for p in range(0, len(self.ligne_1)):
            self.set_pixel(self.ligne_1[p], red, green, blue)
        self.show()
        time.sleep(sleep_time)

    ##########

    def from_bottom_to_top(self, sleep_time=0.008, red=255, green=255, blue=255):
        for p in range(0, len(self.ligne_1)):
            self.set_pixel(self.ligne_1[p], red, green, blue)
        self.show()
        time.sleep(sleep_time)

        for p in range(0, len(self.ligne_2)):
            self.set_pixel(self.ligne_2[p], red, green, blue)
        self.show()
        time.sleep(sleep_time)

        for p in range(0, len(self.ligne_3)):
            self.set_pixel(self.ligne_3[p], red, green, blue)
        self.show()
        time.sleep(sleep_time)

        for p in range(0, len(self.ligne_4)):
            self.set_pixel(self.ligne_4[p], red, green, blue)
        self.show()
        time.sleep(sleep_time)

        for p in range(0, len(self.ligne_5)):
            self.set_pixel(self.ligne_5[p], red, green, blue)
        self.show()
        time.sleep(sleep_time)

        for p in range(0, len(self.ligne_6)):
            self.set_pixel(self.ligne_6[p], red, green, blue)
        self.show()
        time.sleep(sleep_time)

        for p in range(0, len(self.ligne_7)):
            self.set_pixel(self.ligne_7[p], red, green, blue)
        self.show()
        time.sleep(sleep_time)

    ##########

    def wheel(self, pos):
        if pos < 85:
            return Adafruit_WS2801.RGB_to_color(pos * 3, 255 - pos * 3, 0)
        elif pos < 170:
            pos -= 85
            return Adafruit_WS2801.RGB_to_color(255 - pos * 3, 0, pos * 3)
        else:
            pos -= 170
            return Adafruit_WS2801.RGB_to_color(0, pos * 3, 255 - pos * 3)


    ##########

    def rainbow_cycle_successive(self, wait=0.1):
        for i in range(self.pixels.count()):
            # tricky math! we use each pixel as a fraction of the full 96-color wheel
            # (thats the i / strip.numPixels() part)
            # Then add in j which makes the colors go around per pixel
            # the % 96 is to make the wheel cycle around
            self.pixels.set_pixel(i, self.wheel(((i * 256 // self.pixels.count())) % 256))
            self.show()
            if wait > 0:
                time.sleep(wait)

    ##########

    def rainbow_cycle(self, asked_time, wait=0.005):
        passed_time = 0
        while (passed_time < asked_time):
            for j in range(256):  # one cycle of all 256 colors in the wheel
                for i in range(self.pixels.count()):
                    self.pixels.set_pixel(i, self.wheel(((i * 256 // self.pixels.count()) + j) % 256))
                self.show()
                time.sleep(wait)
                passed_time = passed_time + wait

    ##########

    def random_from_bottom_to_top(self, colors, delay):
        for p in range(0, len(self.ligne_1)):
            color = random.randint(0, len(colors)-1)
            self.set_pixel(self.ligne_1[p], colors[color][0], colors[color][1], colors[color][2])
        self.show()

        time.sleep(delay)

        for p in range(0, len(self.ligne_2)):
            color = random.randint(0, len(colors)-1)
            self.set_pixel(self.ligne_2[p], colors[color][0], colors[color][1], colors[color][2])
        self.show()

        time.sleep(delay)

        for p in range(0, len(self.ligne_3)):
            color = random.randint(0, len(colors)-1)
            self.set_pixel(self.ligne_3[p], colors[color][0], colors[color][1], colors[color][2])
        self.show()

        time.sleep(delay)

        for p in range(0, len(self.ligne_4)):
            color = random.randint(0, len(colors)-1)
            self.set_pixel(self.ligne_4[p], colors[color][0], colors[color][1], colors[color][2])
        self.show()

        time.sleep(delay)

        for p in range(0, len(self.ligne_5)):
            color = random.randint(0, len(colors)-1)
            self.set_pixel(self.ligne_5[p], colors[color][0], colors[color][1], colors[color][2])
        self.show()

        time.sleep(delay)

        for p in range(0, len(self.ligne_6)):
            color = random.randint(0, len(colors)-1)
            self.set_pixel(self.ligne_6[p], colors[color][0], colors[color][1], colors[color][2])
        self.show()

        time.sleep(delay)

        for p in range(0, len(self.ligne_7)):
            color = random.randint(0, len(colors)-1)
            self.set_pixel(self.ligne_7[p], colors[color][0], colors[color][1], colors[color][2])
        self.show()


    ##########

    def flash_and_keep_old(self, asked_time, delay, red, green, blue):
        time_passed = 0
        while(time_passed < asked_time):
            ledA = random.randint(0, 87)
            ledB = random.randint(0, 87)
            ledC = random.randint(0, 87)

            oldValueA = self.pixels.get_pixel_rgb(ledA)
            oldValueB = self.pixels.get_pixel_rgb(ledB)
            oldValueC = self.pixels.get_pixel_rgb(ledC)

            self.set_pixel(ledA, red, green, blue)
            self.set_pixel(ledB, red, green, blue)
            self.set_pixel(ledC, red, green, blue)
            self.show()

            time.sleep(delay)
            time_passed = time_passed + delay

            self.set_pixel(ledA, oldValueA[0], oldValueA[1], oldValueA[2])
            self.set_pixel(ledB, oldValueB[0], oldValueB[1], oldValueB[2])
            self.set_pixel(ledC, oldValueC[0], oldValueC[1], oldValueC[2])
            self.show()


    ##########

    def random_static(self, colors):
        for p in range(0, 87):
            color = random.randint(0, len(colors)-1)
            self.set_pixel(p, colors[color][0], colors[color][1], colors[color][2])
        self.show()

    ##########

    def travelling_line_bottom_to_top(self, delay, tR, tG, tB, lR, lG, lB):
        self.set_all_pixels(tR, tG, tB)
        for p in self.ligne_1:
            self.set_pixel(p, lR, lG, lB)
        self.show()
        time.sleep(delay)
        self.set_all_pixels(tR, tG, tB)
        for p in self.ligne_2:
            self.set_pixel(p, lR, lG, lB)
        self.show()
        time.sleep(delay)
        for p in self.ligne_3:
            self.set_pixel(p, lR, lG, lB)
        self.show()
        time.sleep(delay)
        for p in self.ligne_4:
            self.set_pixel(p, lR, lG, lB)
        self.show()
        time.sleep(delay)
        for p in self.ligne_5:
            self.set_pixel(p, lR, lG, lB)
        self.show()
        time.sleep(delay)
        for p in self.ligne_6:
            self.set_pixel(p, lR, lG, lB)
        self.show()
        time.sleep(delay)
        for p in self.ligne_7:
            self.set_pixel(p, lR, lG, lB)
        self.show()
        time.sleep(delay)
        self.set_all_pixels(tR, tG, tB)

    ##########

    def travelling_line_top_to_bottom(self, delay, tR, tG, tB, lR, lG, lB):
        self.set_all_pixels(tR, tG, tB)
        for p in self.ligne_7:
            self.set_pixel(p, lR, lG, lB)
        self.show()
        time.sleep(delay)
        self.set_all_pixels(tR, tG, tB)
        for p in self.ligne_6:
            self.set_pixel(p, lR, lG, lB)
        self.show()
        time.sleep(delay)
        for p in self.ligne_5:
            self.set_pixel(p, lR, lG, lB)
        self.show()
        time.sleep(delay)
        for p in self.ligne_4:
            self.set_pixel(p, lR, lG, lB)
        self.show()
        time.sleep(delay)
        for p in self.ligne_3:
            self.set_pixel(p, lR, lG, lB)
        self.show()
        time.sleep(delay)
        for p in self.ligne_2:
            self.set_pixel(p, lR, lG, lB)
        self.show()
        time.sleep(delay)
        for p in self.ligne_1:
            self.set_pixel(p, lR, lG, lB)
        self.show()
        time.sleep(delay)
        self.set_all_pixels(tR, tG, tB)


