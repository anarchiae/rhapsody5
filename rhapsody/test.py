import lib.RhapsodyPixels as rhapsodypixels
import lib.NeopixelsHelper as neopixelshelper
import time

neopixels = neopixelshelper.NeopixelsHelper()
pixels = rhapsodypixels.RhapsodyPixels(88)


pixels.create_group("ligne_1")
pixels.add_pixels_to_group([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23], "ligne_1")
pixels.create_group("ligne_2")
pixels.add_pixels_to_group([24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43], "ligne_2")
pixels.create_group("ligne_3")
pixels.add_pixels_to_group([44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59], "ligne_3")
pixels.create_group("ligne_4")
pixels.add_pixels_to_group([60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71], "ligne_4")
pixels.create_group("ligne_5")
pixels.add_pixels_to_group([72, 73, 74, 75, 76, 77, 78, 79], "ligne_5")
pixels.create_group("ligne_6")
pixels.add_pixels_to_group([80, 81, 82, 83], "ligne_6")
pixels.create_group("ligne_7")
pixels.add_pixels_to_group([84, 85, 86, 87], "ligne_7")

#pixels.print_groups()

colors = [[255, 0, 0], [0, 255, 0], [0, 0, 255], [255, 255, 255]]
pixels.static(colors, random_assign = True)
#time.sleep(5)
#print("sparkle now")
#pixels.sparkle([[255, 255, 255], [0, 0, 255], [255, 100, 0]], 0.05, 10, pixels = None, number_of_flashes = 10, random_assign = True, keep_old = False)
#print("altern now")
#pixels.altern(colors, 0.5, 10)
#pixels.off()
#pixels.wipe(colors, 0.5, pixels = None, direction = "forward", random_assign = False)
#pixels.sparkle([255, 255, 255], 0.05, 10, pixels = None, number_of_flashes = 10, random_assign = False, keep_old = True)
#neopixels.travelling_line_bottom_to_top(1, 255, 0, 0, 0, 255, 0)
pixels.group_by_group(colors = [255, 255, 255], interval = 1, direction = "up", random_assign = False, assign_type = "pixel", keep_old = True, remain = True, groups = ['ligne_1', 'ligne_2', 'ligne_3', 'ligne_4', 'ligne_5', 'ligne_6', 'ligne_7' ])

pixels.rainbow(0.001, 180, "ligne_1")
#pixels.off()

print("michel bougenat")