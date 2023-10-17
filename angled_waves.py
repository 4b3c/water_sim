import numpy as np
import cv2
import pygame
import random

pygame.init()
seed = random.randint(1, 10000000)
print(seed)
random.seed(seed)

window = pygame.display.set_mode((1000, 800))
running = True
displacement = 0
images = []

# Assumes rotation around the origin
def rotate_point(point, angle_degrees):
	angle_radians = (angle_degrees * np.pi) / 180
	new_x = point[0] * np.cos(angle_radians) - point[1] * np.sin(angle_radians)
	new_y = point[0] * np.sin(angle_radians) + point[1] * np.cos(angle_radians)

	return (new_x, new_y)

# Assumes rotation around the center of a given rectangle
def rotate_rect(size, angle_degrees):
	quadrant = (angle_degrees // 90) + 1
	right = size[0] / 2
	top = size[1] / 2

	if quadrant == 1 or quadrant == 3:
		new_width = max(abs(rotate_point((-right, top), angle_degrees)[0] * 2), size[0])
		new_height = max(abs(rotate_point((right, top), angle_degrees)[1] * 2), size[1])
	else:
		new_width = max(abs(rotate_point((right, top), angle_degrees)[0] * 2), size[0])
		new_height = max(abs(rotate_point((right, -top), angle_degrees)[1] * 2), size[1])

	return (round(new_width / 10) * 10, round(new_height / 10) * 10)



class wave:
	def __init__(self, angle, output_size, height, count, color):
		self.angle = angle
		self.size = rotate_rect(output_size, angle)
		self.crop_x = abs(self.size[0] - output_size[0]) // 2
		self.crop_y = abs(self.size[1] - output_size[1]) // 2
		self.height = height
		self.freq = 0.01 * count
		self.rotation_matrix = cv2.getRotationMatrix2D((self.size[0] / 2, self.size[1] / 2), angle, 1)
		self.color = color

	def generate_wave(self, position):
		self.deriv_array = np.zeros((self.size[1], self.size[0], 3), dtype=np.uint8)
		for col in range(self.size[1]):
			col_input = (col * self.freq) + position
			grey_val = max(0, min(255, ((np.cos(col_input) * np.e**np.sin(col_input)) + 1.5) * self.height))
			self.deriv_array[col, 0:self.size[0]] = np.full((3), grey_val, dtype=np.uint8) * self.color

		# Rotate, crop then transpose from (h, w, d) to (w, h, d)
		self.deriv_array = cv2.warpAffine(self.deriv_array, self.rotation_matrix, self.size)
		self.deriv_array = self.deriv_array[self.crop_y:self.size[1] - self.crop_y, self.crop_x:self.size[0] - self.crop_x]
		self.deriv_array = self.deriv_array.transpose(1, 0, 2)

waves = [wave(random.randint(0, 360), (800, 600), random.randint(10, 150), random.randint(1, 10), np.random.rand((3))) for _ in range(5)]
# waves = [wave(12, (800, 600), 90, 3, c),
# 		 wave(89, (800, 600), 90, 5, np.array([0.3, 0.2, 0.1])),
# 		 wave(236, (800, 600), 90, 2, np.array([0.5, 0.1, 0.9])),
# 		 wave(32, (800, 600), 90, 7, np.array([0.7, 0.2, 1.0]))
# 		]

while running:
	window.fill((15, 45, 95));

	displacement += 0.07

	deriv_arrays = np.zeros((800, 600, 3), dtype=np.uint8)
	for wave in waves:
		wave.generate_wave(displacement)
		deriv_arrays += wave.deriv_array

	image = pygame.surfarray.make_surface(deriv_arrays)
	images.append(cv2.cvtColor(deriv_arrays, cv2.COLOR_BGR2RGB))
	window.blit(image, (100, 100))

	pygame.display.update()
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False


video_writer = cv2.VideoWriter('output.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 25, (images[0].shape[1], images[0].shape[0]))

for image in images:
	video_writer.write(image)

video_writer.release()