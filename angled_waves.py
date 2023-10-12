import pygame, math
import numpy as np

# pygame.init()

# window = pygame.display.set_mode((1000, 800))
# running = True
# displacement = 0

def direction_amount(x):
	if x % 3 == 0:
		return -1
	else:
		return x % 2

def more_waves_with_derivative(position):
	pixel_array = np.zeros((800, 400, 3))
	for x in range(800):
		h = 0
		dh = 0
		for y in range(1, 8):
			position_mod = position * direction_amount(y) * (30 / (y + 1))
			x_mod = x * 1.2
			y_mod = 33 / (y + 0.1)

			c = math.e**math.sin((x_mod + position_mod) * (y / 300)) * y_mod
			h -= c
			dh -= c * y * y * math.cos((x_mod + position_mod) * (y / 300)) * y_mod

		derivative_clamp = min(max(dh / 60, -125), 100) + 155
		pixel_array[x, 250 + int(h / 5):650 + int(h / 5)] = [derivative_clamp*(35/255), derivative_clamp*(137/255), derivative_clamp*(218/255)]


def rotate_point(x, y, angle_degrees):
	angle_radians = (angle_degrees * math.pi) / 180
	new_x = x * math.cos(angle_radians) - y * math.sin(angle_radians)
	new_y = x * math.sin(angle_radians) + y * math.cos(angle_radians)

	return (new_x, new_y)

def new_dimensions(width, height, angle_degrees):
	right = width / 2
	left = -width / 2
	top = height / 2

	_, new_top = rotate_point(right, top, angle_degrees)
	new_left, _ = rotate_point(left, top, angle_degrees)

	print(new_top, new_left)

	new_height = new_top * 2
	new_width = abs(new_left) * 2

	return (new_width, new_height)



class wave:
	def __init__(self, angle, end_size, height):
		self.angle = angle
		self.size = 1

# while running:
# 	window.fill((15, 45, 95));

# 	displacement += 0.3
# 	more_waves_with_derivative(displacement)

# 	pygame.display.update()
# 	for event in pygame.event.get():
# 		if event.type == pygame.QUIT:
# 			quit()


print(new_dimensions(13, 6, 24))