import numpy as np
import cv2
import pygame
import random

pygame.init()

window = pygame.display.set_mode((1000, 800))
running = True
displacement = 0

# Assumes rotation around the origin
def rotate_point(point, angle_degrees):
	angle_radians = (angle_degrees * np.pi) / 180
	new_x = point[0] * np.cos(angle_radians) - point[1] * np.sin(angle_radians)
	new_y = point[0] * np.sin(angle_radians) + point[1] * np.cos(angle_radians)

	return (new_x, new_y)

# Assumes rotation around the center of a given rectangle
def rotate_rect(size, angle_degrees):
	right = size[0] / 2
	top = size[1] / 2

	new_width = -rotate_point((-right, top), angle_degrees)[0] * 2
	new_height = rotate_point((right, top), angle_degrees)[1] * 2

	return (round(new_width / 10) * 10, round(new_height / 10) * 10)



class wave:
	def __init__(self, angle, output_size, height, count):
		self.angle = angle
		self.size = rotate_rect(output_size, angle)
		self.crop_x = (self.size[0] - output_size[0]) // 2
		self.crop_y = (self.size[1] - output_size[1]) // 2
		self.height = height
		self.freq = 0.01 * count
		self.rotation_matrix = cv2.getRotationMatrix2D((self.size[0] / 2, self.size[1] / 2), angle, 1)

	def generate_wave(self, position):
		self.deriv_array = np.zeros((self.size[1], self.size[0], 3), dtype=np.uint8)
		for col in range(self.size[1]):
			col_input = (col * self.freq) + position
			grey_val = ((np.cos(col_input) * np.e**np.sin(col_input)) + 1.5) * self.height
			self.deriv_array[col, 0:self.size[0]] = (grey_val*(35/255), grey_val*(139/255), grey_val*(209/255))

		# Rotate, crop then transpose from (h, w, d) to (w, h, d)
		self.deriv_array = cv2.warpAffine(self.deriv_array, self.rotation_matrix, self.size)
		self.deriv_array = self.deriv_array[self.crop_y:self.size[1] - self.crop_y, self.crop_x:self.size[0] - self.crop_x]
		self.deriv_array = self.deriv_array.transpose(1, 0, 2)
		

waves = [wave(random.randint(10, 50), (800, 600), 100, random.randint(5, 10)) for _ in range(5)]

# wave = wave(66, (800, 600), 100, 15)

while running:
	window.fill((15, 45, 95));

	displacement += 0.07

	deriv_arrays = np.zeros((800, 600, 3), dtype=np.uint8)
	for wave in waves:
		wave.generate_wave(displacement)
		deriv_arrays += wave.deriv_array

	# wave.generate_wave(displacement)
	image = pygame.surfarray.make_surface(deriv_arrays)
	window.blit(image, (100, 100))

	pygame.display.update()
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			quit()