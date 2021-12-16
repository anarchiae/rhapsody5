import time
import random
import RPi.GPIO as GPIO
import Adafruit_WS2801
import Adafruit_GPIO.SPI as SPI


class PixelsDriver:

    numpixels = 0
    myPixels = None
    pixel_groups = None

    def __init__(self, numpixels):
        self.numpixels = numpixels
        self.pixel_groups = dict()
        self.myPixels = Adafruit_WS2801.WS2801Pixels(numpixels, spi=SPI.SpiDev(0, 0), gpio=GPIO)

    # TOOLS METHODS
    # These methods are used by other functions of the class and cannot be used outside

    @staticmethod
    def __rgb_to_color(r, g, b):
        """Convert three 8-bit red, green, blue component values to a single 24-bit
        color value.
        """
        return ((r & 0xFF) << 16) | ((g & 0xFF) << 8) | (b & 0xFF)

    def __set_pixel(self, pixel, color):
        """Assign a color to the pixel given in params"""
        self.myPixels.set_pixel(pixel, self.__rgb_to_color(color[0], color[1], color[2]))

    def __set_all_pixels(self, color):
        """Assign one color to all the pixels"""
        for p in range(0, self.numpixels):
            self.myPixels.set_pixel(p, self.__rgb_to_color(color[0], color[1], color[2]))
        self.__show()

    def __show(self):
        """Apply the modifications made on the pixels"""
        self.myPixels.show()

    def __wheel(self, pos):
        if pos < 85:
            return_value = self.__rgb_to_color(pos * 3, 255 - pos * 3, 0)
        elif pos < 170:
            pos -= 85
            return_value = self.__rgb_to_color(255 - pos * 3, 0, pos * 3)
        else:
            pos -= 170
            return_value = self.__rgb_to_color(0, pos * 3, 255 - pos * 3)

        return return_value

    @staticmethod
    def __get_current_time_millis():
        return time.time() * 1000

    # DATA ORGANISATION METHODS
    def create_group(self, group_name):
        """Add a new group to the list of pixels"""
        self.pixel_groups[group_name] = None

    def add_pixels_to_group(self, pixels, group_name):
        """Add a pixel to a designated group"""
        try:
            if type(pixels) is list:
                self.pixel_groups[group_name] = pixels
            elif type(pixels) is int:
                self.pixel_groups[group_name] = [pixels]
        except KeyError:
            print("The specified group does not exist")

    @staticmethod
    def __create_disposable_group(start, end):
        """Create a disposable group that will be destroyed once the
        calling method as been executed. This method is private and
        should be used only if there is no alternative"""
        group = []
        for i in range(start, end):
            group.append(i)

        return group

    def print_groups(self):
        """Print a visual representation of the different
        groups created"""
        print(self.pixel_groups)

    # ANIMATIONS
    def brightness_decrease(self, pixels=None, interval=0.01, step=1):
        """Turn off all the selected pixels with a fade effect"""

        # Check the type of the pixels argument and works
        # to make it a list if it's not
        if pixels is not None:
            if type(pixels) is int:
                pixels = [pixels]
            elif type(pixels) is str:
                pixels = self.pixel_groups[pixels]
        else:
            pixels = self.__create_disposable_group(0, self.numpixels)

        for j in range(int(256 // step)):
            for i in range(len(pixels)):
                r, g, b = self.myPixels.get_pixel_rgb(pixels[i])
                r = int(max(0, r - step))
                g = int(max(0, g - step))
                b = int(max(0, b - step))
                self.__set_pixel(pixels[i], [r, g, b])
            self.__show()
            if interval > 0:
                time.sleep(interval)

    def off(self, pixels=None):
        """Turn off the pixels given in args"""

        # Check the type of the pixels argument and works
        # to make it a list if it's not
        if pixels is not None:
            if type(pixels) is int:
                pixels = [pixels]
            elif type(pixels) is str:
                pixels = self.pixel_groups[pixels]
        else:
            pixels = self.__create_disposable_group(0, self.numpixels)

        # Turning off the pixels
        for p in range(len(pixels)):
            color = [0, 0, 0]
            self.__set_pixel(p, color)
        self.__show()

    def static(self, colors, pixels=None, random_assign=False):
        """Apply a color to selected pixels"""

        # Check if there is one or multiple colors
        # If there is only one color, then the first item in
        # the list, must be an int and not a list
        if type(colors[0]) is int:
            colors = [colors]

        # Check the type of the pixels argument and works
        # to make it a list if it's not
        if pixels is not None:
            if type(pixels) is int:
                pixels = [pixels]
            elif type(pixels) is str:
                pixels = self.pixel_groups[pixels]
        else:
            pixels = self.__create_disposable_group(0, self.numpixels)

        # Apply the effect
        if random_assign:
            for p in range(len(pixels)):
                color = colors[random.randint(0, len(colors)-1)]
                self.__set_pixel(pixels[p], color)
            self.__show()
        else:
            color_index = 0
            for p in range(len(pixels)):
                color = colors[color_index]
                self.__set_pixel(pixels[p], color)

                color_index = color_index + 1
                if color_index > len(colors)-1:
                    color_index = 0
            self.__show()

    def sparkle(self, colors, interval, duration, pixels=None, number_of_flashes=3,
                random_assign=False, keep_old=False):
        """Sparkle effect on selected pixels"""

        # Time
        animation_end_time = self.__get_current_time_millis() + (duration * 1000)

        # Selected pixels. They will be set as flashes
        selected_pixels = []
        return_to_normal_colors = []

        # Check if there is one or multiple colors
        # If there is only one color, then the first item in
        # the list, must be an int and not a list
        if type(colors[0]) is int:
            colors = [colors]

        # Check the type of the pixels argument and works
        # to make it a list if it's not
        if pixels is not None:
            if type(pixels) is int:
                pixels = [pixels]
            elif type(pixels) is str:
                pixels = self.pixel_groups[pixels]
        else:
            pixels = self.__create_disposable_group(0, self.numpixels)

        # Animation start
        while self.__get_current_time_millis() < animation_end_time:

            # Select the pixels that will be used as flashes
            for i in range(number_of_flashes):
                selected_pixels.append(pixels[random.randint(0, len(pixels) - 1)])

            # Retrieves the color that will be applied once the selected pixels
            # will return to there "non-flash" status. If the argument keep_old is
            # False, then the pixel will be turned off (color values red : 0,
            # green : 0, blue : 0
            if keep_old:
                for i in range(number_of_flashes):
                    return_to_normal_colors.append(self.myPixels.get_pixel_rgb(selected_pixels[i]))
            else:
                for i in range(number_of_flashes):
                    return_to_normal_colors.append([0, 0, 0])

            # Apply the colors to the pixels
            if random_assign:
                for p in range(number_of_flashes):
                    color = colors[random.randint(0, len(colors) - 1)]
                    self.__set_pixel(selected_pixels[p], color)
                self.__show()
            else:
                color_index = 0
                for p in range(number_of_flashes):
                    color = colors[color_index]
                    self.__set_pixel(selected_pixels[p], color)

                    color_index = color_index + 1
                    if color_index > len(colors) - 1:
                        color_index = 0
                self.__show()

            # Waits for the time of the interval
            time.sleep(interval)

            # Reset all pixels to normal status
            for p in range(number_of_flashes):
                self.__set_pixel(selected_pixels[p], return_to_normal_colors[p])
            self.__show()

            # Empty lists
            selected_pixels = []
            return_to_normal_colors = []

    def altern(self, colors, interval, duration, pixels=None):

        # Time
        animation_end_time = self.__get_current_time_millis() + (duration * 1000)

        # Check if there is more than one color in the colors list
        # given in args. If there is only one color, then the other
        # color will be black [0, 0, 0] .If there is more than two
        # colors, then, only the first two colors will be used.
        if len(colors) < 1:
            colors = [colors, [0, 0, 0]]

        # Check the type of the pixels argument and works
        # to make it a list if it's not
        if pixels is not None:
            if type(pixels) is int:
                pixels = [pixels]
            elif type(pixels) is str:
                pixels = self.pixel_groups[pixels]
        else:
            pixels = self.__create_disposable_group(0, self.numpixels)

        while self.__get_current_time_millis() < animation_end_time:

            for p in range(len(pixels)):
                if p % 2 == 0:
                    self.__set_pixel(pixels[p], colors[0])
                else:
                    self.__set_pixel(pixels[p], colors[1])
            self.__show()

            time.sleep(interval)

            for p in range(len(pixels)):
                if p % 2 == 0:
                    self.__set_pixel(pixels[p], colors[1])
                else:
                    self.__set_pixel(pixels[p], colors[0])
            self.__show()

            time.sleep(interval)

    def wipe(self, colors, interval, pixels=None, direction="forward", random_assign=False):
        """Apply a color to LEDS one after another"""

        # Check if there is one or multiple colors
        # If there is only one color, then the first item in
        # the list, must be an int and not a list
        if type(colors[0]) is int:
            colors = [colors]

        # Check the type of the pixels argument and works
        # to make it a list if it's not
        if pixels is not None:
            if type(pixels) is int:
                pixels = [pixels]
            elif type(pixels) is str:
                pixels = self.pixel_groups[pixels]
        else:
            pixels = self.__create_disposable_group(0, self.numpixels)

        # Apply the effect
        if random_assign:
            if direction == "forward":
                for p in range(len(pixels)):
                    color = colors[random.randint(0, len(colors) - 1)]
                    self.__set_pixel(pixels[p], color)
                    self.__show()
                    time.sleep(interval)
            else:
                for p in range((len(pixels)-1), 0, -1):
                    color = colors[random.randint(0, len(colors) - 1)]
                    self.__set_pixel(pixels[p], color)
                    self.__show()
                    time.sleep(interval)
        else:
            if direction == "forward":
                color_index = 0
                for p in range(len(pixels)):
                    color = colors[color_index]
                    self.__set_pixel(pixels[p], color)

                    color_index = color_index + 1
                    if color_index > len(colors) - 1:
                        color_index = 0
                    self.__show()
            else:
                color_index = 0
                for p in range((len(pixels)-1), 0, -1):
                    color = colors[color_index]
                    self.__set_pixel(pixels[p], color)

                    color_index = color_index + 1
                    if color_index > len(colors) - 1:
                        color_index = 0
                    self.__show()

    def group_by_group(self, colors, interval, direction="up", random_assign=False, assign_type="group",
                       keep_old=False, remain=False, groups=None):
        """Turn on the pixels group by group"""

        back_to_normal_values = []

        # Checks if group names are specified in
        # str
        if groups is not None:
            for group in groups:
                if type(group) is not str:
                    raise TypeError("Groups names must be of type 'str'")

        # Check if there is one or multiple colors
        # If there is only one color, then the first item in
        # the list, must be an int and not a list
        if type(colors[0]) is int:
            colors = [colors]

        if random_assign:
            if direction == "up":
                for group in groups:
                    color = colors[random.randint(0, len(colors) - 1)]
                    for p in range(0, len(self.pixel_groups[group])):
                        # Retrieve the current values of the pixel
                        back_to_normal_values.append(self.myPixels.get_pixel_rgb(self.pixel_groups[group][p]))

                        # If the assign_type is set to "pixel" in the parameters
                        # then, each pixel will have a different color. Else, the
                        # color applied will be the one selected at the beginning
                        # of the groups loop.
                        if assign_type == "pixel":
                            color = colors[random.randint(0, len(colors) - 1)]

                        # Apply the new color
                        self.__set_pixel(self.pixel_groups[group][p], color)

                    self.__show()
                    time.sleep(interval)

                    # Return to normal
                    if keep_old:
                        for p in range(0, len(self.pixel_groups[group])):
                            color = back_to_normal_values[p]
                            self.__set_pixel(self.pixel_groups[group][p], color)
                    elif not remain:
                        for p in range(0, len(self.pixel_groups[group])):
                            self.__set_pixel(self.pixel_groups[group][p], [0, 0, 0])

                    self.__show()

                    back_to_normal_values = list()

            else:  # Direction = down
                for g in range(len(self.pixel_groups) - 1, -1, -1):
                    color = colors[random.randint(0, len(colors) - 1)]
                    for p in range(0, len(self.pixel_groups[groups[g]])):
                        # Retrieve the current values of the pixel
                        back_to_normal_values.append(self.myPixels.get_pixel_rgb(self.pixel_groups[groups[g]][p]))

                        # If the assign_type is set to "pixel" in the parameters
                        # then, each pixel will have a different color. Else, the
                        # color applied will be the one selected at the beginning
                        # of the groups loop.
                        if assign_type == "pixel":
                            color = colors[random.randint(0, len(colors) - 1)]

                        # Apply the new color
                        self.__set_pixel(self.pixel_groups[groups[g]][p], color)

                    self.__show()
                    time.sleep(interval)

                    # Return to normal
                    if keep_old:
                        for p in range(0, len(self.pixel_groups[groups[g]])):
                            color = back_to_normal_values[p]
                            self.__set_pixel(self.pixel_groups[groups[g]][p], color)
                        self.__show()
                    elif not remain:
                        for p in range(0, len(self.pixel_groups[groups[g]])):
                            self.__set_pixel(self.pixel_groups[groups[g]][p], [0, 0, 0])
                        self.__show()

        else:  # Not random_assign
            if direction == "up":
                color_index = 0
                for group in groups:
                    for p in range(len(self.pixel_groups[group])):
                        back_to_normal_values.append(self.myPixels.get_pixel_rgb(self.pixel_groups[group][p]))

                        # If the assign_type is set to "pixel" in the parameters
                        # then, each pixel will have a different color. Else, the
                        # color applied will be the one selected at the beginning
                        # of the groups loop.
                        if assign_type == "pixel":
                            color_index = color_index + 1
                            if color_index > len(colors) - 1:
                                color_index = 0

                        self.__set_pixel(self.pixel_groups[group][p], colors[color_index])

                    self.__show()
                    time.sleep(interval)

                    # Return to normal
                    if keep_old:
                        for p in range(0, len(self.pixel_groups[group])):
                            color = back_to_normal_values[p]
                            self.__set_pixel(self.pixel_groups[group][p], color)
                    elif not remain:
                        for p in range(0, len(self.pixel_groups[group])):
                            self.__set_pixel(self.pixel_groups[group][p], [0, 0, 0])
                        self.__show()

                    # Increment color_index
                    color_index = color_index + 1
                    if color_index > len(colors) - 1:
                        color_index = 0

                    back_to_normal_values = list()

            else:  # direction = down
                color_index = 0
                for g in range(len(self.pixel_groups)-1, -1, -1):
                    for p in range(len(self.pixel_groups[groups[g]])):
                        back_to_normal_values.append(self.myPixels.get_pixel_rgb(self.pixel_groups[groups[g]][p]))

                        # If the assign_type is set to "pixel" in the parameters
                        # then, each pixel will have a different color. Else, the
                        # color applied will be the one selected at the beginning
                        # of the groups loop.
                        if assign_type == "pixel":
                            color_index = color_index + 1
                            if color_index > len(colors) - 1:
                                color_index = 0

                        color = colors[color_index]
                        self.__set_pixel(self.pixel_groups[groups[g]][p], color)

                    self.__show()
                    time.sleep(interval)

                    # Return to normal
                    if keep_old:
                        for p in range(0, len(self.pixel_groups[groups[g]])):
                            color = back_to_normal_values[p]
                            self.__set_pixel(self.pixel_groups[groups[g]][p], color)
                        self.__show()
                    elif not remain:
                        for p in range(0, len(self.pixel_groups[groups[g]])):
                            self.__set_pixel(self.pixel_groups[groups[g]][p], [0, 0, 0])
                        self.__show()

                    # Increment color_index
                    color_index = color_index + 1
                    if color_index > len(colors) - 1:
                        color_index = 0

                    back_to_normal_values = list()

    def rainbow(self, interval, duration, pixels=None):
        """Rainbow animation"""

        animation_end_time = self.__get_current_time_millis() + (duration * 1000)

        # Check the type of the pixels argument and works
        # to make it a list if it's not
        if pixels is not None:
            if type(pixels) is int:
                pixels = [pixels]
            elif type(pixels) is str:
                pixels = self.pixel_groups[pixels]
        else:
            pixels = self.__create_disposable_group(0, self.numpixels)

        while self.__get_current_time_millis() < animation_end_time:
            for j in range(256):  # one cycle of all 256 colors in the wheel
                for p in range(len(pixels) - 1):
                    self.myPixels.set_pixel(pixels[p], self.__wheel(((p * 256 // self.myPixels.count()) + j) % 256))
                self.__show()
                time.sleep(interval)

    @staticmethod
    def delay(duration):
        """Stop the script for a time equal to duration"""
        if type(duration) is not int:
            try:
                int(duration)
            except ValueError:
                duration = 0
                print("Delay error : The specified duration must be a valid numeric value")

        time.sleep(duration)
        