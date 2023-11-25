import numpy as np
import angled_waves as aw
import cv2
import pygame
import random

pygame.init()
clock = pygame.time.Clock()

window = pygame.display.set_mode((1000, 800))
wave_window = (800, 600)
running = True
displacement = 1
images = []


waves = [
		 aw.wave(12, wave_window, 32, 3, np.ones(3)),
		 aw.wave(95, wave_window, 24, 4, np.ones(3)),
		 aw.wave(126, wave_window, 41, 2, np.ones(3)),
		 aw.wave(49, wave_window, 29, 5, np.ones(3)),
		 aw.wave(172, wave_window, 36, 1, np.ones(3))
		]


while running:
	window.fill((15, 45, 95));

	displacement += 0.07

	deriv_arrays = np.zeros((wave_window[0], wave_window[1], 3), dtype=np.uint8)
	for wave in waves:
		wave.generate_wave(displacement)
		deriv_arrays += wave.deriv_array
	
	image = pygame.surfarray.make_surface(deriv_arrays)
	# images.append(cv2.cvtColor(deriv_arrays, cv2.COLOR_BGR2RGB))
	window.blit(image, (100, 100))

	pygame.display.update()
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False


# video_writer = cv2.VideoWriter('output.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 25, (images[0].shape[1], images[0].shape[0]))

# for image in images:
# 	video_writer.write(image)

# video_writer.release()