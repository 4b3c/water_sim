import numpy as np
import angled_waves as aw
import cv2
import pygame
import random

pygame.init()
clock = pygame.time.Clock()

seed = [random.randint(1, 10000000)]
curr_seed_index = 0
print(curr_seed_index, ":", seed[curr_seed_index])
random.seed(seed[curr_seed_index])

window = pygame.display.set_mode((1000, 800))
wave_window = (800, 600)
running = True
unclicked = True
displacement = 0
images = []
x = 0

def fill_waves_list():
	return [aw.wave(random.randint(0, 360), (800, 600), random.randint(10, 150), random.uniform(0.05, 3.05), np.random.rand((3))) for _ in range(5)]

waves = fill_waves_list()

# waves = [aw.wave(12, wave_window, 90, 3, np.array([0.4, 0.9, 0.1])),
# 		 aw.wave(89, wave_window, 90, 5, np.array([0.3, 0.2, 0.1])),
# 		 aw.wave(236, wave_window, 90, 2, np.array([0.5, 0.1, 0.9])),
# 		 aw.wave(32, wave_window, 90, 7, np.array([0.7, 0.2, 1.0]))
# 		]

while running:
	window.fill((15, 45, 95));

	displacement += 0.02

	deriv_arrays = np.zeros((wave_window[0], wave_window[1], 3), dtype=np.uint8)
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

	keys_pressed = pygame.key.get_pressed()

	# x += 1
	if (keys_pressed[pygame.K_RIGHT] and unclicked) or x == 5:
		x = 0
		unclicked = False
		# images = []
		curr_seed_index += 1
		if curr_seed_index > len(seed) - 1:
			seed.append(random.randint(1, 10000000))
		print(curr_seed_index, ":", seed[curr_seed_index])
		random.seed(seed[curr_seed_index])
		waves = fill_waves_list()

	elif keys_pressed[pygame.K_LEFT] and unclicked:
		unclicked = False
		# images = []
		curr_seed_index -= 1
		print(curr_seed_index, ":", seed[curr_seed_index])
		random.seed(seed[curr_seed_index])
		waves = fill_waves_list()

	else:
		unclicked = True

	# clock.tick()
	# print("FPS:", int(clock.get_fps()))


video_writer = cv2.VideoWriter('output.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 25, (images[0].shape[1], images[0].shape[0]))

for image in images:
	video_writer.write(image)

video_writer.release()